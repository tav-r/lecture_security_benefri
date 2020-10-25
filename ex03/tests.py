from ldap3 import Server, Connection, ALL

server = Server('ldap.secuis.fun:8443', use_ssl=True, get_info=ALL)
conn = Connection(server, 'cn=admin,dc=ldap,dc=secuis,dc=fun', 'ta643upKzcANJU2c!6aj', auto_bind=True)
print(conn)
conn.search('ou=people,dc=ldap,dc=secuis,dc=fun', '(objectclass=UniPerson)')
conn.entries

