from typing import List

from ldap3 import Reader, ObjectDef, Connection as ldap_Connection, Entry

DN = "ou=people,dc=ldap,dc=secuis,dc=fun"
OBJECT_CLASS = "UniPerson"


def search_entries(conn: ldap_Connection, _filter=None) -> List[Entry]:
    obj_uniperson = ObjectDef(OBJECT_CLASS, conn)
    reader = Reader(conn, obj_uniperson, DN, _filter)
    reader.search()

    return reader.entries
