from ..strategy.sync import SyncStrategy

MOCK_MESAGE_ID = 2

# for rapid prototyping
USER_TREE_DN = 'cn=users, cn=accounts, dc=demo1, dc=freeipa, dc=org'
GROUP_TREE_DN = 'cn=groups, cn=accounts, dc=demo1, dc=freeipa, dc=org'

receiving_users = {
    'admin': '0\x81\x83\x02\x01\x02d~\x049uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org0A0\x15\x04\x02cn1\x0f\x04\rAdministrator0\x18\x04\rnsAccountLock1\x07\x04\x05FALSE0\x0e\x04\x03uid1\x07\x04\x05admin',
    'manager': '0l\x02\x01\x02dg\x04;uid=manager,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org0(0\x14\x04\x02cn1\x0e\x04\x0cTest Manager0\x10\x04\x03uid1\t\x04\x07manager',
    'employee': '0o\x02\x01\x02dj\x04<uid=employee,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org0*0\x15\x04\x02cn1\x0f\x04\rTest Employee0\x11\x04\x03uid1\n\x04\x08employee',
    'helpdesk': '0o\x02\x01\x02dj\x04<uid=helpdesk,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org0*0\x15\x04\x02cn1\x0f\x04\rTest Helpdesk0\x11\x04\x03uid1\n\x04\x08helpdesk',
    'jim': '0a\x02\x01\x02d\\\x047uid=jim,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org0!0\x11\x04\x02cn1\x0b\x04\tJim Smith0\x0c\x04\x03uid1\x05\x04\x03jim',
    'jimmy': '0f\x02\x01\x02da\x049uid=jimmy,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org0$0\x12\x04\x02cn1\x0c\x04\nJim Corbet0\x0e\x04\x03uid1\x07\x04\x05jimmy',
    'darthvader': '0k\x02\x01\x02df\x04>uid=darthvader,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org0$0\r\x04\x02cn1\x07\x04\x05darth0\x13\x04\x03uid1\x0c\x04\ndarthvader',
    'testtest': "0l\x02\x01\x02dg\x04<uid=testtest,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org0'0\x12\x04\x02cn1\x0c\x04\nja testuju0\x11\x04\x03uid1\n\x04\x08testtest",
    'test': "0h\x02\x01\x02dc\x048uid=test,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org0'0\x16\x04\x02cn1\x10\x04\x0etest netestovy0\r\x04\x03uid1\x06\x04\x04test",
}

receiving_groups = {
    'admins': '0\x82\x03s\x02\x01\x06d\x82\x03l\x04:cn=admins,cn=groups,cn=accounts,dc=demo1,dc=freeipa,dc=org0\x82\x03,0\x0e\x04\x02cn1\x08\x04\x06admins0\x82\x03\x18\x04\x06member1\x82\x03\x0c\x049uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org\x04;uid=mmuster,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org\x04:uid=freddy,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org\x048uid=ozub,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org\x047uid=jim,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org\x047uid=ook,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org\x04;uid=toharek,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org\x04@uid=reggaedancer,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org\x04<uid=helpdesk,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org\x04<uid=employee,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org\x04;uid=manager,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org\x04:uid=lloool,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org\x046uid=42,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org',
    'ipausers': '0\x82\x03<\x02\x01\x06d\x82\x035\x04<cn=ipausers,cn=groups,cn=accounts,dc=demo1,dc=freeipa,dc=org0\x82\x02\xf30\x10\x04\x02cn1\n\x04\x08ipausers0\x82\x02\xdd\x04\x06member1\x82\x02\xd1\x04;uid=manager,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org\x04<uid=employee,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org\x04<uid=helpdesk,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org\x04;uid=mmuster,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org\x04:uid=freddy,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org\x048uid=ozub,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org\x047uid=jim,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org\x047uid=ook,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org\x04;uid=toharek,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org\x04@uid=reggaedancer,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org\x04:uid=lloool,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org\x046uid=42,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org',
    'editors': '0U\x02\x01\x06dP\x04;cn=editors,cn=groups,cn=accounts,dc=demo1,dc=freeipa,dc=org0\x110\x0f\x04\x02cn1\t\x04\x07editors',
    'trust admins': '0\x81\xa7\x02\x01\x06d\x81\xa1\x04@cn=trust admins,cn=groups,cn=accounts,dc=demo1,dc=freeipa,dc=org0]0\x14\x04\x02cn1\x0e\x04\x0ctrust admins0E\x04\x06member1;\x049uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org',
    'employees': '0\x81\xe3\x02\x01\x06d\x81\xdd\x04=cn=employees,cn=groups,cn=accounts,dc=demo1,dc=freeipa,dc=org0\x81\x9b0\x11\x04\x02cn1\x0b\x04\temployees0\x81\x85\x04\x06member1{\x04<uid=employee,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org\x04;uid=manager,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org',
    'managers': '0\x81\xa1\x02\x01\x06d\x81\x9b\x04<cn=managers,cn=groups,cn=accounts,dc=demo1,dc=freeipa,dc=org0[0\x10\x04\x02cn1\n\x04\x08managers0G\x04\x06member1=\x04;uid=manager,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org',
    'under_under': '0]\x02\x01\x06dX\x04?cn=under_under,cn=groups,cn=accounts,dc=demo1,dc=freeipa,dc=org0\x150\x13\x04\x02cn1\r\x04\x0bunder_under',
    'under_verifier': '0c\x02\x01\x06d^\x04Bcn=under_verifier,cn=groups,cn=accounts,dc=demo1,dc=freeipa,dc=org0\x180\x16\x04\x02cn1\x10\x04\x0eunder_verifier',
}

END_RESPONSE = '0\x0c\x02\x01\x02e\x07\n\x01\x00\x04\x00\x04\x00'

receiving_bind = ['0\x0c\x02\x01\x02a\x07\n\x01\x00\x04\x00\x04\x00']


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
        # TODO: message_id validation is failing, find a way to generate it
        message_id = ldap_message['messageID']

    def _mock_search_request(self, request):
        # discover if it's a user or group query
        search_base = request['baseObject']

        # we'll assume it's a search query since our queries are all read only
        request_filter = request['filter']
        search_eq = request_filter['equalityMatch']

        if search_eq is not None:
            search_attr = search_eq['attributeDesc']
            search_value = search_eq['assertionValue']

        receiving_mock = []
        if search_base == USER_TREE_DN:
            if search_eq is not None and search_attr == 'uid':
                receiving_mock = list(receiving_users[search_value])
            elif search_eq is None:
                receiving_mock = list(receiving_users.values())
            else:
                # FIXME: raise an exception
                pass
        elif search_base == GROUP_TREE_DN:
            if search_eq is not None and search_attr == 'cn':
                receiving_mock = list(receiving_groups[search_value])
            elif search_eq is None:
                receiving_mock = list(receiving_groups.values())
            else:
                # FIXME: raise an exception
                pass
        receiving_mock.append(END_RESPONSE)
        return receiving_mock

    def send(self, message_type, request, controls=None):
        self.connection.listening = True

        if message_type == 'searchRequest':
            self.receiving_mock = self._mock_search_request(request)
        elif message_type == 'bindRequest':
            self.receiving_mock = receiving_bind
        message_id = super(MockSyncStrategy, self).send(message_type,
                                                        request,
                                                        controls)
        self._outstanding.pop(message_id)
        self._outstanding[MOCK_MESAGE_ID] = self.connection.request
        return MOCK_MESAGE_ID

    def receiving(self):
        import pdb; pdb.set_trace()
        return self.receiving_mock

    def _open_socket(self):
        self.connection.closed = False

    def _close_socket(self):
        self.connection.closed = True

