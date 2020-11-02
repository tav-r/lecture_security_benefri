"""Definition of the 'remove' command."""

from ldap3 import Connection as ldap_Connection

from .base import Command
from . import DN


class RemoveCommand(Command):
    """Command to remove an LDAP entry."""
    def __init__(self, client):
        
        def remove_entry(cn=None):
            conn: ldap_Connection = client.connection
            
            if not cn:
                cn = input("> cn=")

            full_dn = f"cn={cn},{DN}"
            if conn.delete(full_dn):
                print(f"Successfully deleted person {cn}!")
            else:
                print(f"Error deleting {full_dn}, did you maybe misspell "
                      f"something?")

        super().__init__("remove", "removes an existing user from the LDAP",
                         remove_entry)
