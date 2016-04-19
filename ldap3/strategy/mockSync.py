from copy import deepcopy
import re
from ..strategy.sync import SyncStrategy
from .. import RESPONSE_COMPLETE
from ..core.exceptions import LDAPNoSuchObjectResult
from ..utils import dn as dn_utils
from ..operation.search import filter_to_string
from filter import parse, UnsupportedOp


MOCK_BIND_RESPONSE = {'dn': u'', 'saslCreds': None, 'description': 'success',
                      'result': 0, 'message': u'', 'type': 'bindResponse'}
MOCK_SEARCH_RES_DONE = {'dn': u'', 'referrals': None, 'description': 'success',
                        'result': 0, 'message': u'', 'type': 'searchResDone'}


class MockSyncStrategy(SyncStrategy):
    """
    This strategy create a mock LDAP server, with synchronous access
    It can be useful to test LDAP without a real Server
    """
    def __init__(self, ldap_connection, directory=None):
        SyncStrategy.__init__(self, ldap_connection)
        self.sync = True
        self.no_real_dsa = True
        self.pooled = False
        self.can_stream = False
        self.mock_response = None
        #if directory is not None:
        #    self.directory = deepcopy(directory)

        # for rapid prototyping
        top = ('dc=com', {'dc': ['com']})
        example = ('dc=example,dc=com', {'dc': ['example']})
        other = ('dc=other,dc=com', {'dc': ['other']})
        users = ('cn=users,dc=example,dc=com', {'cn': ['users']})
        groups = ('cn=groups,dc=example,dc=com', {'cn': ['groups']})
        admin = ('uid=admin,cn=users,dc=example,dc=com',
                 {'uid': ['admin'],
                  'nsAccountLock': ['FALSE'],
                  'objectClass': 'person'})
        manager = ('uid=manager,cn=users,dc=example,dc=com',
                   {'uid': ['manager'],
                    'userPassword': ['ldaptest'],
                    'objectClass': 'person'})
        employee = ('uid=employee,cn=users,dc=example,dc=com',
                    {'uid': ['employee'],
                     'objectClass': 'person'})
        admins = ('cn=admins,cn=groups,dc=example,dc=com',
                  {'cn': ['admins'],
                   'member': ['uid=admin,cn=users,dc=example,dc=com'],
                   'objectClass': 'groupOfNames'})
        employees = ('cn=employees,cn=groups,dc=example,dc=com',
                     {'cn': ['employees'],
                      'member': ['uid=employee,cn=users,dc=example,dc=com',
                                 'uid=manager,cn=users,dc=example,dc=com'],
                      'objectClass': 'groupOfNames'})
        editors = ('cn=editors,cn=groups,dc=example,dc=com',
                   {'cn': ['editors'],
                    'objectClass': 'groupOfNames'})

        # This is the content of our mock LDAP directory. It takes the form
        # {dn: {attr: [value, ...], ...}, ...}.
        directory = dict([top, example, other, users, groups, admin, manager,
                          employee, admins, employees, editors])
        self.directory = deepcopy(directory)

    def _build_search_response(self, dn_entry, attrs):
        """
        :param dn: dn entry in the directory
        :return: a dict search result of the form
        { 'dn': ...,
          'attributes': ...,
          'raw_attributes': ....
        }
        """
        search_resp = {'dn': dn_entry,
                       'attributes': attrs,
                       'raw_attributes': attrs,
                       'type': 'searchResEntry'
                       }
        return search_resp

    def _mock_search(self, request):
        base = request['baseObject']
        base = re.sub(r'\s+', '', str(base))

        if base not in self.directory:
            raise LDAPNoSuchObjectResult

        # find the dns in the directory
        base_parts = dn_utils.parse_dn(base)
        base_len = len(base_parts)
        dn_parts = dict((dn, dn_utils.parse_dn(dn.lower()))
                        for dn in self.directory.keys())

        scope = request['scope']
        if scope == 0:
            dns = (dn for dn, parts in dn_parts.items() if parts == base_parts)
        elif scope == 1:
            dns = (dn for dn, parts in dn_parts.items()
                   if parts[1:] == base_parts)
        elif scope == 2:
            dns = (dn for dn, parts in dn_parts.items() if
                   parts[-base_len:] == base_parts)
        else:
            raise ValueError(u"Unrecognized scope: {0}".format(scope))

        request_filter = request['filter']
        filterstr = filter_to_string(request_filter)

        # Apply the filter expression
        try:
            filter_expr = parse(filterstr)
        except UnsupportedOp as e:
            raise ValueError(e)

        results = ((dn, self.directory[dn]) for dn in dns
                   if filter_expr.matches(dn, self.directory[dn]))

        # Apply attribute filtering, if any
        filter_attr = request['attributes']
        if filter_attr is not None:
            results = ((dn, dict((attr, values)
                                 for attr, values in attrs.items()
                                 if attr in filter_attr))
                       for dn, attrs in results)

        mock_response = [self._build_search_response(dn, attrs)
                         for dn, attrs in results]

        mock_response.append(MOCK_SEARCH_RES_DONE)
        return mock_response

    def _mock_bind(self):
        return [MOCK_BIND_RESPONSE]

    def send(self, message_type, request, controls=None):
        self.connection.listening = True

        if message_type == 'searchRequest':
            self.mock_response = self._mock_search(request)
        elif message_type == 'bindRequest':
            self.mock_response = self._mock_bind()
        # TODO: implement other operations mocks

        self.mock_response.append(RESPONSE_COMPLETE)

        return super(MockSyncStrategy, self).send(message_type,
                                                  request,
                                                  controls)

    def sending(self, ldap_message):
        pass

    def receiving(self):
        pass

    def _get_response(self, message_id):
        return self.mock_response

    def _open_socket(self, address, use_ssl=False, unix_socket=False):
        self.connection.closed = False

    def _close_socket(self):
        self.connection.closed = True

