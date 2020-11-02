NEW_PEOPLE_ATTRIBUTES = ["description", "mail"]

PEOPLE_ATTRIBUTES = NEW_PEOPLE_ATTRIBUTES + \
                    ["cn", "objectClass", "userPassword"]
DN = "ou=people,dc=ldap,dc=secuis,dc=fun"
OBJECT_CLASS = "UniPerson"
