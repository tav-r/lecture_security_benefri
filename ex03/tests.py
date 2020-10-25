from ldap3 import Server, Connection, ALL, MODIFY_REPLACE

server = Server('ldap.secuis.fun:8443', use_ssl=True, get_info=ALL)
conn = Connection(server, 'cn=admin,dc=ldap,dc=secuis,dc=fun', 'ta643upKzcANJU2c!6aj', auto_bind=True)
print(conn)

conn.search('ou=people,dc=ldap,dc=secuis,dc=fun', '(objectClass=UniPerson)')
print(conn.entries)

conn.add('cn=Marc Kaeser,ou=people,dc=ldap,dc=secuis,dc=fun','UniPerson',{'mail': 'marc.kaeser@gmail.com', 'userPassword': '123456'})
print(conn.result)
print()

conn.modify('cn=Marc Kaeser,ou=people,dc=ldap,dc=secuis,dc=fun',{'mail': [(MODIFY_REPLACE, ['marc.kaeser@unifr.ch'])], 'userPassword': [(MODIFY_REPLACE, ['123456'])]})
print(conn.result)
print()

conn.delete('cn=Marc Kaeser,ou=people,dc=ldap,dc=secuis,dc=fun')
print(conn.result)
print()

#conn.search('ou=people,dc=ldap,dc=secuis,dc=fun', '(objectClass=UniPerson)')
#print(conn.entries)

conn.unbind()

