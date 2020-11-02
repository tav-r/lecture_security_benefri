from ldap3 import Connection as ldap_Connection, ObjectDef, Reader

from .base import Command
from . import DN, OBJECT_CLASS, search_entries


class SeeCommand(Command):
    def __init__(self, client):
        
        def see_entry(cn=None):
            conn: ldap_Connection = client.connection

            if not cn:
                cn = input("> cn=")

            for entry in search_entries(conn, f"(cn={cn})"):
                print(entry)

        super().__init__("see", "display the information of one person.",
                         see_entry)
