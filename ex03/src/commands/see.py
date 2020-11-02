from ldap3 import Connection as ldap_Connection

from .base import Command
from . import PEOPLE_ATTRIBUTES


class SeeCommand(Command):
    def __init__(self, client):
        
        def see_entry(cn=None):
            conn: ldap_Connection = client.connection

            if not cn:
                cn = input("> cn=")

            res = conn.search("ou=people,dc=ldap,dc=secuis,dc=fun",
                              f"(cn={cn})", attributes=PEOPLE_ATTRIBUTES)

            if res:
                for entry in conn.entries:
                    print(entry)
            else:
                print("no matching entry found")
    
        super().__init__("see", "display the information of one person.",
                         see_entry)
