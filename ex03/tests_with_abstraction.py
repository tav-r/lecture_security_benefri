from ldap3 import Server, Connection, ALL, MODIFY_REPLACE, ObjectDef, Reader, Writer

name = 'Arnold Schwarzenegger'
email = 'arnold.schwarzenegger@gmail.com'

#connect to server
server = Server('ldap.secuis.fun:8443', use_ssl=True, get_info=ALL)

oc = 'UniPerson'
dn = 'cn=admin,dc=ldap,dc=secuis,dc=fun'
pw = 'ta643upKzcANJU2c!6aj'
c = Connection(server, dn, pw, auto_bind=True, return_empty_attributes=True)
o = ObjectDef(oc, c)
d = 'ou=people,dc=ldap,dc=secuis,dc=fun'
r = Reader(c,o,d)
w = Writer.from_cursor(r)

userinput = ""
while userinput != "q":

    print()
    print ("press h vor help")
    userinput = input ("what do you want to do? : ")
    print()

    if userinput == "h" :
        print()
        print("actual directory is: ",d)
        print()
        print("type one of the following letters and press enter")
        print("\"c\" to create an entry")
        print("\"r\" to read")
        print("\"u\" to update an entry")
        print("\"d\" to delete an entry")
        print("\"l\" to list all objects")
        print("\"v\" to verify password")
        print()
    if userinput == "c":
        print()
        print('c : create an entry', d)
        print()
    if userinput == "r":
        print()
        print('r : read', d)
        print()
    if userinput == "u":
        print()
        print('u : update an entry', d)
        print()
    if userinput == "d":
        print()
        print('d : delete an entry', d)
        print()
    if userinput == "l" :
        print()
        print('l : lists all entries in', d)
        print()
        entries = r.search()
        print(entries)
        print()
    if userinput == "v":
        print()
        print('v : verify password', d)
        print()

        userinputvalue = input("type a string you are looking for in" + d)
        print(r.search(userinputvalue))
#close connection to server
c.unbind()

