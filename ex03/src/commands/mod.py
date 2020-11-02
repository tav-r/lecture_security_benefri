import crypt

from ldap3 import Connection as ldap_Connection, ObjectDef, Writer

from . import DN, OBJECT_CLASS, search_entries
from .base import Command

class Modifycommand(Command):
    def __init__(self, client):

        def modify_entry(cn=None):
            conn: ldap_Connection = client.connection

            if not cn:
                cn = input("> cn=")

            entries = search_entries(conn, f"(cn={cn})")
            if not entries:
                print("entry not found")
                return

            assert len(entries) == 1

            writer = entries.pop().entry_writable()
            for key, val in writer.entry_attributes_as_dict.items():
                if key == "objectClass":
                    continue

                msg = f"> ({val.pop()}, leave empty for unchanged) {key}="
                ans = input(msg)

                if ans:
                    setattr(writer, key, crypt.crypt(ans, crypt.METHOD_SHA512)
                            if key == "userPassword" else ans)

            writer.entry_commit_changes()

            print("Successfully modified person!")

        super().__init__("modify", "modifies an existing user.",
                         modify_entry)
