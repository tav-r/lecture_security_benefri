#an ez ldaps client, assignment 03 security lecture, mka 2020-11-04

import crypt, hmac
from ldap3 import Server, Connection, ALL, ObjectDef, Reader, Writer, AttrDef

###connect to server ("server" needed as global) securely, but dont check the certifcate (because the cert is not valid on the server)
server = Server('ldap.secuis.fun:8443', use_ssl=True, get_info=ALL)

### global variables allowed / meant to be hard coded ######
oc = 'UniPerson'
dn = 'cn=admin,dc=ldap,dc=secuis,dc=fun'
pw = 'ta643upKzcANJU2c!6aj'
c = Connection(server, dn, pw, auto_bind=True, return_empty_attributes=True)
o = ObjectDef(oc, c)
d = 'ou=people,dc=ldap,dc=secuis,dc=fun'

### function to find the difference between two lists ####
def Diff(li1, li2):
    return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))


###### function to display possible user choices #########
def Help():
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


############# function to create a dn entry ################
def	Create():
    print()
    print('c : create an object of objectClass '+ oc +' in', d)
    print()

    #use cursor from ldap3's abstraction layer in order to get information which attributes are mandatory or optional
    r = Reader(c, o, d)
    r.search()
    list_of_attributes = r[0].entry_attributes
    list_of_mandatory_attributes = r[0].entry_mandatory_attributes
    list_of_optional_attributes = Diff(list_of_attributes,list_of_mandatory_attributes)
    w = Writer.from_cursor(r)

    # create new object using the writer created from the reader r
    # input loop for cn
    userinput = ''
    while userinput == '':
        userinput = input('input Common Name (cn) value of Destinguished Name (dn) (cannot be empty): ')
        if userinput != '':
            commonname = userinput

            #hotfix to avoid a crash when the cn already exists
            try:
                e = w.new('cn='+commonname+',' + d)
            except:
                print()
                print("invalid username, please try another one")
                print()
                userinput=''

    # input loop for mandatory attribs
    userinput = ''
    while userinput == '':
        for mandatoryattrib in list_of_mandatory_attributes:

            # skip attribute "ObjectClass" because it comes from Reader r and cannot be edited (in the assigment only "email" is a normal unhandled mandatory attribute)
            if mandatoryattrib != 'objectClass':
                # cn in dn cannot/should not be different from attribute cn and is mandatory I guess
                if mandatoryattrib == 'cn':
                    userinput = commonname
                else:
                    userinput = ''
                    while userinput == '':
                        userinput=input('input value for mandatory attribute '+ mandatoryattrib + ' (cannot be empty): ')

                        # if the input is a userPassword, crypt it before pushing to the writer
                        if mandatoryattrib == 'userPassword':
                            if userinput != '':
                                userinput = '{CRYPT}' + crypt.crypt(userinput, crypt.METHOD_SHA512)
                    e[mandatoryattrib] = userinput
        e[mandatoryattrib] = userinput

    # input loop for optional attribs and handle them differently (optional input)
    for optionalattrib in list_of_optional_attributes:
        userinput = input('input value for optional attribute ' + optionalattrib + ' (can be empty, just press enter): ')
        if not userinput:
            userinput = ' '
        # if the input is a userPassword, crypt it before pushing to the writer
        if optionalattrib == 'userPassword':
            if userinput != '':
                userinput = '{CRYPT}' + crypt.crypt(userinput, crypt.METHOD_SHA512)
    e[optionalattrib] = userinput
    print(e[optionalattrib])

    e.entry_commit_changes()


############# function to read a dn entry ################
def Read():
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


####### function to update a dn entry's attributes #########
def Update():
    print()
    print('u : update an entry in', d)
    print()
    print('please enter the Common Name CN of entry you want to update')
    print()

    # ask user for cn of dn he wants to update
    userinput = ''
    while userinput == '':
        userinput = input('input Common Name (cn) value of Destinguished Name (dn) (cannot be empty): ')
        commonname = userinput

        entrydn = ('cn=' + userinput + ',' + d)

        #read object from directory and create a writer cursor from/for this entry
        r = Reader(c, o, entrydn)
        r.search()
        # hotfix to avoid a crash when the cn already exists
        try:
            list_of_attributes = r[0].entry_attributes
            list_of_mandatory_attributes = r[0].entry_mandatory_attributes
            list_of_optional_attributes = Diff(list_of_attributes, list_of_mandatory_attributes)
            w = Writer.from_cursor(r)

            # dn cannot be double, so the first element is also the only one
            e = w[0]

        except:
            print()
            print("invalid username, please try another one")
            print()
            userinput=''

    #continue if it worked to get the object
    print()
    print('you are editing the following entry')
    print()
    print(e)
    print()

    # input loop for mandatory attribs
    userinput = ''
    while userinput == '':
        for mandatoryattrib in list_of_mandatory_attributes:

            # skip attribute "ObjectClass" because it comes from Reader r and cannot be edited (in the assigment only "email" is a normal unhandled mandatory attribute)
            if mandatoryattrib != 'objectClass':
                # cn in dn cannot/should not be different from attribute cn and is mandatory I guess
                if mandatoryattrib == 'cn':
                    userinput = commonname
                else:
                    userinput = ''
                    while userinput == '':
                        userinput = input(
                            'input value for mandatory attribute ' + mandatoryattrib + ' (cannot be empty): ')

                        # if the input is a userPassword, crypt it before pushing to the writer
                        if mandatoryattrib == 'userPassword':
                            if userinput != '':
                                userinput = '{CRYPT}' + crypt.crypt(userinput, crypt.METHOD_SHA512)
                    e[mandatoryattrib] = userinput
        e[mandatoryattrib] = userinput

    # input loop for optional attribs and handle them differently (optional input)
    for optionalattrib in list_of_optional_attributes:
        userinput = input('input value for optional attribute ' + optionalattrib + ' (can be empty, just press enter): ')
        if not userinput:
            userinput = ' '
        # if the input is a userPassword, crypt it before pushing to the writer
        if optionalattrib == 'userPassword':
            if userinput != '':
                userinput = '{CRYPT}' + crypt.crypt(userinput, crypt.METHOD_SHA512)
    e[optionalattrib] = userinput
    print(e[optionalattrib])

    e.entry_commit_changes()


############# function to delete a dn entry ################
def Delete():
    print()
    print('d : delete an entry from', d)
    print()
    userinput = input('please enter the Common Name of the dn-entry you want to delete : ')
    print()
    # perform the Delete operation
    c.delete('cn='+userinput+','+d)


############ function to list all dn-entries ##############
def List():
    print()
    print('l : lists all entries in', d)
    print()
    r = Reader(c, o, d)
    output=r.search()
    print(output)
    print()


############ function to search for attributes ############
def Search():
    print()
    print('s : search attributes of '+ oc + '-entries in ',d )
    print()
    r = Reader(c, o, d)
    r.search()
    print('the attributes are ',r[0].entry_attributes)
    print()
    attribute = input('please specify which attribute to search : ')
    value = input('please specify which value to find (you can use wildcards with *): ')
    print()
    query = (attribute + ' : ' + value)
    try:
        r = Reader(c, o, d, query)
        output=r.search()
        print(output)
        print()
    except:
        print()
        print("invalid query, please try another one")
        print()
################ function to verify password ##############
def Verify():
    print()
    print('v : verify password', d)
    print()
    userinput_cn = input('please enter the Common Name of the dn-entry you want to check the password : ')
    print()
    userinput_pwd = input('please enter the password stored in attribute \'userPassword\' : ')
    print()
    entrydn = ('cn=' + userinput_cn + ',' + d)
    r = Reader(c, o, entrydn)
    r.search()

    # dn is unique so we take the first list of attributes and extract userPassword
    hash_from_DIT=(r[0].userPassword.value.decode().strip("{CRYPT}"))

    if hmac.compare_digest(crypt.crypt(userinput_pwd, hash_from_DIT),hash_from_DIT):
        print()
        print("SUCCESS, the password matches")
        print()
    else:
        print()
        print("FAILED, the password doesn't match")
        print()


################# function to quit program ################
def Quit():
    print()
    print('arrivederci')
    print()
    #close connection to server
    c.unbind()


###########################################################
## MAIN PROGRAM - sorry no time left for a nicer pattern ##
###########################################################

#ask the user what he/she wants to do
userinput = ""
while userinput != "q":

    print()
    print("press h vor help")
    userinput = input("what do you want to do? : ")
    print()

    #h displays what the user can choose from
    if userinput == "h" :
        Help()

    #c starts the creation of a new entry
    if userinput == "c":
        Create()

    #r reads an entry when the user knows the dn of the object he wants to query
    if userinput == "r":
        Read()

    #u updates the entry the user knows the dn of
    if userinput == "u":
        Update()

     #d deletes the entry the user knows the dn of
    if userinput == "d":
        Delete()

    #l lists all dn-entries
    if userinput == "l" :
        List()

    #s starts the search of all attributes for the given ObjectClass in the given path (hardcoded for the moment, as allowed by the assignment)
    if userinput == "s":
       Search()

    #v to verify password
    if userinput == "v":
        Verify()

    #q to quit program
    if userinput == "q":
        Quit()