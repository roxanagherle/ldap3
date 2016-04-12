import re
from ..strategy.sync import SyncStrategy
from .. import RESPONSE_COMPLETE


# for rapid prototyping
USER_TREE_DN = 'cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org'
GROUP_TREE_DN = 'cn=groups,cn=accounts,dc=demo1,dc=freeipa,dc=org'

mock_users = {
    'admin': {'dn': 'uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org',
              'attributes': {
                  'cn': ['Administrator'],
                  'nsAccountLock': ['FALSE'],
                  'uid': ['admin']}
              },
    'manager': {'dn': 'uid=manager,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org',
                'attributes': {
                    'cn': ['Test Manager'],
                    'uid': ['manager']}
                },
    'employee': {'dn': 'uid=employee,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org',
                 'attributes': {'cn': ['Test Employee'],
                                'uid': ['employee']}
                 },
    'helpdesk': {'dn': 'uid=helpdesk,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org',
                 'attributes': {'cn': ['Test Helpdesk'],
                                'uid': ['helpdesk']}
                 },
    'blabla': {'dn': 'uid=blabla,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org',
               'attributes': {'cn': ['Bla Blala'],
                              'uid': ['blabla']}
               },
    'arti': {'dn': 'uid=arti,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org',
             'attributes': {'cn': ['Roma Neco'],
                            'uid': ['arti']}
             },
}

mock_groups = {
    'admins': {'dn': 'cn=admins,cn=groups,cn=accounts,dc=demo1,dc=freeipa,dc=org',
               'attributes': {'member': ['uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org'],
                              'cn': ['admins']},
               },
    'ipausers': {'dn': 'cn=ipausers,cn=groups,cn=accounts,dc=demo1,dc=freeipa,dc=org',
                 'attributes':
                     {'member': ['uid=manager,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org',
                                  'uid=employee,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org',
                                  'uid=helpdesk,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org',
                                  'uid=blabla,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org',
                                  'uid=arti,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org',],
                      'cn': ['ipausers']
                      }
                 },
    'editors': {'dn': 'cn=editors,cn=groups,cn=accounts,dc=demo1,dc=freeipa,dc=org',
                'attributes': {'cn': ['editors']}
                },
    'trust admins': {'dn': 'cn=trust admins,cn=groups,cn=accounts,dc=demo1,dc=freeipa,dc=org',
                     'attributes': {
                         'member': ['uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org'],
                         'cn': ['trust admins']}
                     },
    'employees': {'dn': 'cn=employees,cn=groups,cn=accounts,dc=demo1,dc=freeipa,dc=org',
                  'attributes': {
                      'member': [
                          'uid=employee,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org',
                          'uid=manager,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org'],
                      'cn': ['employees']}
                  },
    'managers': {'dn': 'cn=managers,cn=groups,cn=accounts,dc=demo1,dc=freeipa,dc=org',
                 'attributes': {'member': ['uid=manager,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org'],
                                'cn': ['managers']}
                 },
}


class MockSyncStrategy(SyncStrategy):
    """
    This strategy create a mock LDAP server, with synchronous access
    It can be useful to test LDAP without a real Server
    """
    def __init__(self, ldap_connection):
        SyncStrategy.__init__(self, ldap_connection)
        self.sync = True
        self.no_real_dsa = True
        self.pooled = False
        self.can_stream = False
        self.receiving_mock = None

    def sending(self, ldap_message):
        pass

    def _mock_search_response(self, request):
        import pdb; pdb.set_trace()

        # discover if it's a user or group query
        search_base = request['baseObject']
        search_base = re.sub(r'\s+', '', str(search_base))

        request_filter = request['filter']
        search_eq = request_filter['equalityMatch']

        if search_eq is not None:
            search_attr = search_eq['attributeDesc']
            search_value = search_eq['assertionValue']

        receiving_mock = []
        if search_base == USER_TREE_DN:
            if search_eq is not None and search_attr == 'uid':
                receiving_mock.append(self._build_user_response(search_value))
            elif search_eq is None:
                receiving_mock.extend([self._build_user_response(user) for user in mock_users.iterkeys()])
            else:
                # FIXME: raise an exception
                pass
        elif search_base == GROUP_TREE_DN:
            if search_eq is not None and search_attr == 'cn':
                receiving_mock.append(self._build_group_response(search_value))
            elif search_eq is None:
                receiving_mock.extend([self._build_group_response(group) for group in mock_groups.iterkeys()])
            else:
                # FIXME: raise an exception
                pass
        elif USER_TREE_DN in search_base and search_base.startswith('uid='):
            user_search = search_base.split(',')[0].split('=')[1]
            if user_search in mock_users.keys():
                receiving_mock.append(self._build_user_response(user_search))
        receiving_mock.append(self._build_searchResDone_dict())
        return receiving_mock

    def _build_user_response(self, user):
        user_dict_resp = mock_users[user]
        #user_dict_resp['attributes'] = {str(k): str(v) for k, v in user_dict_resp['attributes']}
        user_dict_resp['raw_attributes'] = user_dict_resp['attributes']
        user_dict_resp['type'] = 'searchResEntry'
        return user_dict_resp

    def _build_group_response(self, group):
        group_dict_resp = mock_groups[group]
        #group_dict_resp['attributes'] = {str(k): str(v) for k, v in group_dict_resp['attributes']}
        group_dict_resp['raw_attributes'] = group_dict_resp['attributes']
        group_dict_resp['type'] = 'searchResEntry'
        return group_dict_resp

    def _build_searchResDone_dict(self):
        searchResDone_dict = {}
        searchResDone_dict['dn'] = u''
        searchResDone_dict['referrals'] = None
        searchResDone_dict['description'] = 'success'
        searchResDone_dict['result'] = 0
        searchResDone_dict['message'] = u''
        searchResDone_dict['type'] = 'searchResDone'
        return searchResDone_dict

    def _mock_bind_response(self):
        bind_dict_resp = {}
        bind_dict_resp['dn'] = u''
        bind_dict_resp['saslCreds'] = None
        bind_dict_resp['description'] = 'success'
        bind_dict_resp['result'] = 0
        bind_dict_resp['message'] = u''
        bind_dict_resp['type'] = 'bindResponse'
        return [bind_dict_resp]

    def send(self, message_type, request, controls=None):
        self.connection.listening = True

        if message_type == 'searchRequest':
            self.receiving_mock = self._mock_search_response(request)
        elif message_type == 'bindRequest':
            self.receiving_mock = self._mock_bind_response()
        self.receiving_mock.append(RESPONSE_COMPLETE)

        return super(MockSyncStrategy, self).send(message_type,
                                                  request,
                                                  controls)

    def receiving(self):
        pass

    def _get_response(self, message_id):
        return self.receiving_mock

    def _open_socket(self, address, use_ssl=False, unix_socket=False):
        self.connection.closed = False

    def _close_socket(self):
        self.connection.closed = True

