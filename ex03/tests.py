from ldap3 import Server, Connection, ALL

server = Server('ldap.secuis.fun:8443', use_ssl=True, get_info=ALL)
conn = Connection(server, 'cn=admin,dc=ldap,dc=secuis,dc=fun', 'ta643upKzcANJU2c!6aj', auto_bind=True)
print(conn)

conn.search('ou=people,dc=ldap,dc=secuis,dc=fun', '(objectClass=UniPerson)')
print(conn.entries)

conn.add('cn=Marc Kaeser,ou=people,dc=ldap,dc=secuis,dc=fun','UniPerson',{'mail': 'marc.kaeser@gmail.com', 'userPassword': '123456'})
print(conn.result)

conn.search('ou=people,dc=ldap,dc=secuis,dc=fun', '(objectClass=UniPerson)')
print(conn.entries)

conn.unbind()

