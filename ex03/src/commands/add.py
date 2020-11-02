import crypt
from typing import Tuple, Optional

from .base import Command
from . import DN, OBJECT_CLASS

from ldap3 import Writer, ObjectDef, Entry


class AddCommand(Command):
    def __init__(self, client):

        def add_entry(cn: Optional[str] = None):
            conn = client.connection

            cn = cn if cn else input("> cn=")

            obj_def = ObjectDef(OBJECT_CLASS, conn)
            writer = Writer(conn, obj_def)
            entry = writer.new(f"cn={cn},{DN}")

            for attr in writer.attributes:
                if attr == "userPassword":
                    val = crypt.crypt(input(f"> {attr}="), crypt.METHOD_SHA512)
                elif attr == "cn":
                    val = cn
                elif attr == "objectClass":
                    val = OBJECT_CLASS
                else:
                    val = input(f"> {attr}=")
                setattr(entry, attr, val)

            writer.commit()

            print("Successfully added person!")

        super().__init__("add", "adds a new person to the LDAP.", add_entry)
