from ldap3 import Server, Connection, ALL, MODIFY_REPLACE, ObjectDef, Reader, Writer

#connect to server
server = Server('ldap.secuis.fun:8443', use_ssl=True, get_info=ALL)

oc = 'UniPerson'
dn = 'cn=admin,dc=ldap,dc=secuis,dc=fun'
pw = 'ta643upKzcANJU2c!6aj'
c = Connection(server, dn, pw, auto_bind=True, return_empty_attributes=True)
o = ObjectDef(oc, c)
d = 'ou=people,dc=ldap,dc=secuis,dc=fun'

userinput = ""
while userinput != "q":

    print()
    print("press h vor help")
    userinput = input("what do you want to do? : ")
    print()

    if userinput == "h" :
        print()
        print("actual directory is: ", d)
        print()
        print("type one of the following letters and press enter")
        print("\"c\" to create an entry")
        print("\"r\" to read")
        print("\"u\" to update an entry")
        print("\"d\" to delete an entry")
        print("\"l\" to list all objects")
        print("\"s\" to search attributes")
        print("\"v\" to verify password")
        print()

    if userinput == "c":
        print()
        print('c : create an entry in', d)
        print()
        print('please enter the Common Name CN of entry you want to create in', d)
        print()

    if userinput == "r":
        print()
        print('r : read an entry in', d)
        print()
        cninput=input('please enter the Common Name CN of entry you want to show : ')
        print()
        r = Reader(c, o, 'cn=' + cninput + ',ou=people,dc=ldap,dc=secuis,dc=fun')
        r.search()
        print(r.entries)

    if userinput == "u":
        print()
        print('u : update an entry in', d)
        print()
        print('please enter the Common Name CN of entry you want to update')
        print()
        r = Reader(c, o, d)
        w = Writer.from_cursor(r)

    if userinput == "d":
        print()
        print('d : delete an entry', d)
        print()

    if userinput == "l" :
        print()
        print('l : lists all entries in', d)
        print()
        r = Reader(c, o, d)
        output=r.search()
        print(output)
        print()

    if userinput == "s":
        print()
        print('s : search attributes of UniPerson-entries in ',d )
        print()
        r = Reader(c, o, d)
        r.search()
        print('the attributes are ',r[0].entry_attributes)
        print()
        attribute = input('please specify which attribute to search : ')
        value = input('please specify which value the attribute has : ')
        for iter in r:
            print(r[iter].entry_attributes)
            #for attrib in r[entry]:
             #   print(r[entry].entry_attributes)

    if userinput == "v":
        print()
        print('v : verify password', d)
        print()
        userinputvalue = input("type a string you are looking for in" + d)
        print(r.search(userinputvalue))
#close connection to server
c.unbind()

