from ldap3 import Connection as ldap_Connection

from .base import Command
from . import PEOPLE_ATTRIBUTES, DN, OBJECT_CLASS


class ListAllCommand(Command):
    def __init__(self, client):

        def list_persons():
            conn: ldap_Connection = client.connection
            res = conn.search(DN, f"(objectclass={OBJECT_CLASS})",
                              attributes=PEOPLE_ATTRIBUTES)

            if res:
                for entry in conn.entries:
                    print(entry)

        super().__init__("all",
                         "display a list of all the persons in the LDAP",
                         list_persons)
