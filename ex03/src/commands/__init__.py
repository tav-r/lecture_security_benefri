"""This module holds the definitions for the commands."""
from typing import List, Optional

from ldap3 import Reader, ObjectDef, Connection as ldap_Connection, Entry

DN = "ou=people,dc=ldap,dc=secuis,dc=fun"
OBJECT_CLASS = "UniPerson"


def search_entries(conn: ldap_Connection, _filter: Optional[str] = None)\
     -> List[Entry]:
    """
    Search entries under the specified DN matching a given filter, using the
    given connection.

    Args:
        conn (ldap_Connection): an established ldap3 connection.
        filter (Optional[str]): a filter to use in the search (can be None).

    Returns:
        List[Entry]: a list of matching entries.
    """
    obj_uniperson = ObjectDef(OBJECT_CLASS, conn)
    reader = Reader(conn, obj_uniperson, DN, _filter)
    reader.search()

    return reader.entries
