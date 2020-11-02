"""Definition of the 'modify' command"""

import crypt

from ldap3 import Connection as ldap_Connection, ObjectDef, Writer

from . import DN, OBJECT_CLASS, search_entries
from .base import Command


def modify_interactive(entry):
    """Interactively modify attributes of an LDAP entry."""
    for key, val in entry.entry_attributes_as_dict.items():
        if key == "objectClass":
            continue

        msg = f"> ({val.pop()}, leave empty for unchanged) {key}="
        ans = input(msg)

        if ans:
            setattr(entry, key, crypt.crypt(ans, crypt.METHOD_SHA512)
                    if key == "userPassword" else ans)

        entry.entry_commit_changes()


class Modifycommand(Command):
    """Command to modify entries in the LDAP."""
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

            modify_interactive(entries.pop().entry_writable())

            print("Successfully modified person!")

        super().__init__("modify", "modifies an existing user.",
                         modify_entry)
