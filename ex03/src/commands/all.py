"""Definition of the 'all' command."""

from ldap3 import Connection as ldap_Connection

from .base import Command
from . import search_entries


class ListAllCommand(Command):
    """Command to list all entries undert the configured LDAP branch."""
    def __init__(self, client):

        def list_persons():
            conn: ldap_Connection = client.connection
            for entry in search_entries(conn):
                print(entry)

        super().__init__("all",
                         "display a list of all the persons in the LDAP",
                         list_persons)
