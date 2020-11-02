from ldap3 import Server, Connection, ALL, MODIFY_REPLACE, ObjectDef, Reader, Writer

name = 'Arnold Schwarzenegger'
email = 'arnold.schwarzenegger@gmail.com'

#connect to server and print connection
server = Server('ldap.secuis.fun:8443', use_ssl=True, get_info=ALL)
conn = Connection(server, 'cn=admin,dc=ldap,dc=secuis,dc=fun', 'ta643upKzcANJU2c!6aj', auto_bind=True, return_empty_attributes=True)
print(conn)

#Print server's schema
#print (server.schema)

#look for all Uniperson and print them before adding
conn.search('ou=people,dc=ldap,dc=secuis,dc=fun', '(objectClass=UniPerson)')
#print(conn.entries)

#look for all attributes of Uniperson from schema, save it in an iterable "ObjectDef"

#print(person)
#for test in person:
#    if test['mandatory': True]: print('mandatory')

#add a UniPerson user with attributes mail and userPassword
conn.add('cn='+ name +',ou=people,dc=ldap,dc=secuis,dc=fun','UniPerson',{'mail': email, 'userPassword': '123456' })
#print(conn.result)
#print()

#modify a UniPerson's attributes mail and userPassword
conn.modify('cn='+ name +',ou=people,dc=ldap,dc=secuis,dc=fun',{'mail': [(MODIFY_REPLACE, [email])], 'userPassword': [(MODIFY_REPLACE, ['111111'])]})
#print(conn.result)
#print()

#compare Uniperson's attributes userPassword
pwd = '123456'
check = conn.compare('cn='+ name +',ou=people,dc=ldap,dc=secuis,dc=fun','userPassword', pwd)
#print ('compare with ', pwd)
#print(check)
#print()
pwd = '111111'
check = conn.compare('cn='+ name +',ou=people,dc=ldap,dc=secuis,dc=fun','userPassword', pwd)
#print ('compare with ', pwd)
#print(check)
#print()

#look for all Uniperson and print them before deleting
conn.search('ou=people,dc=ldap,dc=secuis,dc=fun', '(objectClass=UniPerson)',attributes=['*'])
#print(conn.entries)

#remove new Uniperson
conn.delete('cn='+ name +',ou=people,dc=ldap,dc=secuis,dc=fun')
#print(conn.result)
#print()

#look for all Uniperson and print after deletion
conn.search('ou=people,dc=ldap,dc=secuis,dc=fun', '(objectClass=UniPerson)')
#print(conn.entries)

#close connection to server
conn.unbind()

