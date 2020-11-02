NEW_PEOPLE_ATTRIBUTES = ["description", "mail", "userPassword"]

PEOPLE_ATTRIBUTES = NEW_PEOPLE_ATTRIBUTES + ["cn", "objectClass"]
DN = "ou=people,dc=ldap,dc=secuis,dc=fun"
OBJECT_CLASS = "UniPerson"
