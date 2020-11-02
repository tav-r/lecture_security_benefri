#an ez ldaps client, assignment 03 security lecture, mka 2020-11-02

from ldap3 import Server, Connection, ALL, ObjectDef, Reader, Writer, AttrDef

#connect to server
server = Server('ldap.secuis.fun:8443', use_ssl=True, get_info=ALL)

#allowed / meant to be hard coded but could easily be put in by the user
oc = 'UniPerson'
dn = 'cn=admin,dc=ldap,dc=secuis,dc=fun'
pw = 'ta643upKzcANJU2c!6aj'
c = Connection(server, dn, pw, auto_bind=True, return_empty_attributes=True)
o = ObjectDef(oc, c)
d = 'ou=people,dc=ldap,dc=secuis,dc=fun'

#function used to find the difference between two lists
def Diff(li1, li2):
    return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))

#main program, sorry no nice pattern, I learned Python 3 months ago
userinput = ""
while userinput != "q":

    print()
    print("press h vor help")
    userinput = input("what do you want to do? : ")
    print()

    #h displays what the user can choose from
    if userinput == "h" :
        print()
        print("actual directory is: ", d)
        print()
        print("type one of the following letters and press enter")
        print("\"c\" to create an entry")
        print("\"r\" to read an entry")
        print("\"u\" to update an entry")
        print("\"d\" to delete an entry")
        print("\"l\" to list all objects")
        print("\"s\" to search attributes")
        print("\"v\" to verify password")
        print("\"q\" to quit")
        print()

    #c starts the creation of a new entry
    if userinput == "c":
        print()
        print('c : create an object of objectClass '+ oc +' in', d)
        print()
        r = Reader(c, o, d)
        r.search()
        list_of_attributes = r[0].entry_attributes
        list_of_mandatory_attributes = r[0].entry_mandatory_attributes
        list_of_optional_attributes = Diff(list_of_attributes,list_of_mandatory_attributes)
        w = Writer.from_cursor(r)

        # create new object using the writer created from the reader r
        userinput = ''
        while userinput == '':
            userinput = input('input Common Name (cn) value of Destinguished Name (dn) (cannot be empty): ')
        e = w.new('cn='+userinput+',' + d)

        # input loop for mandatory attribs
        for mandatoryattrib in list_of_mandatory_attributes:
            if mandatoryattrib != 'objectClass':  # skip attribute "ObjectClass" because it comes from Reader r and cannot be edited
                userinput=''
                while userinput == '' :
                    # cn in dn can be different from attribute cn
                    if mandatoryattrib == 'cn':
                        userinput=input('input value for mandatory attribute '+ mandatoryattrib + ' (cannot be empty, same cn as in dn is recommended): ')
                    else:
                        userinput=input('input value for mandatory attribute '+ mandatoryattrib + ' (cannot be empty): ')
                        e[mandatoryattrib] = userinput #uses MODIFY_REPLACE

        # input loop for optional attribs
        for optionalattrib in list_of_optional_attributes:
            userinput = input('input value for optional attribute ' + optionalattrib + ' (can be empty, just press enter): ')
            e[optionalattrib] = userinput  # uses MODIFY_REPLACE

        e.entry_commit_changes()

    #r reads an entry when the user knows the dn of the object he wants to query
    if userinput == "r":
        print()
        print('r : read an entry from', d)
        print()
        userinput=input('please enter the Common Name of the dn-entry you want to read : ')
        print()
        query = ('cn: '+userinput)
        r = Reader(c, o, d, query)
        r.search()
        print(r.entries)
        print()

    #u updates the entry the user knows the dn of
    if userinput == "u":
        print()
        print('u : update an entry in', d)
        print()
        print('please enter the Common Name CN of entry you want to update')
        print()

       # ask user for cn of dn he wants to update
        userinput = ''
        while userinput == '':
            userinput = input('input Common Name (cn) value of Destinguished Name (dn) (cannot be empty): ')
        entrydn = ('cn=' + userinput + ',' + d)

        #read object from directory and create a writer cursor from/for this entry
        r = Reader(c, o, entrydn)
        r.search()
        list_of_attributes = r[0].entry_attributes
        list_of_mandatory_attributes = r[0].entry_mandatory_attributes
        list_of_optional_attributes = Diff(list_of_attributes, list_of_mandatory_attributes)
        w = Writer.from_cursor(r)
        e = w[0] #dn can never be double, so the first element is also the only one
        print(e)
        # input loop for mandatory attribs
        for mandatoryattrib in list_of_mandatory_attributes:
            if mandatoryattrib != 'objectClass':  # skip attribute "ObjectClass" because it comes from Reader r and cannot be edited
                userinput = ''
                while userinput == '':
                    # cn in dn can be different from attribute cn
                    if mandatoryattrib == 'cn':
                        userinput = input(
                            'input value for mandatory attribute ' + mandatoryattrib + ' (cannot be empty, same cn as in dn is recommended): ')
                    else:
                        userinput = input(
                            'input value for mandatory attribute ' + mandatoryattrib + ' (cannot be empty): ')
                        e[mandatoryattrib] = userinput  # uses MODIFY_REPLACE

        # input loop for optional attribs
        for optionalattrib in list_of_optional_attributes:
            userinput = input(
                'input value for optional attribute ' + optionalattrib + ' (can be empty, just press enter): ')
            e[optionalattrib] = userinput  # uses MODIFY_REPLACE

        # commit changes to w[0]
        e.entry_commit_changes()

    #d deletes the entry the user knows the dn of
    if userinput == "d":
        print()
        print('d : delete an entry from', d)
        print()
        userinput = input('please enter the Common Name of the dn-entry you want to delete : ')
        print()
        # perform the Delete operation
        c.delete('cn='+userinput+','+d)

    #l lists all dn-entries
    if userinput == "l" :
        print()
        print('l : lists all entries in', d)
        print()
        r = Reader(c, o, d)
        output=r.search()
        print(output)
        print()

    #s starts the search of all attributes for the given ObjectClass in the given path (hardcoded for the moment, as allowed by the assignment)
    if userinput == "s":
        print()
        print('s : search attributes of '+ oc + '-entries in ',d )
        print()
        r = Reader(c, o, d)
        r.search()
        print('the attributes are ',r[0].entry_attributes)
        print()
        attribute = input('please specify which attribute to search : ')
        value = input('please specify which value to find (you can use wildcards with *): ')
        query = (attribute + ' : ' + value)
        r = Reader(c, o, d, query)
        output=r.search()
        print(output)
        print()

    #v to verify password
    if userinput == "v":
        print()
        print('v : verify password', d)
        print()
        userinputvalue = input("type a string you are looking for in" + d)
        print(r.search(userinputvalue))

    #q to quit program
    if userinput == "q":
        print()
        print('arrivederci')
        print()
        #close connection to server
        c.unbind()