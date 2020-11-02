import crypt
import hmac

from ldap3 import Connection as ldap_Connection

from .base import Command
from . import DN


class LogCommand(Command):
    def __init__(self, client):

        def login(cn_pw=None):
            conn: ldap_Connection = client.connection

            if not cn_pw:
                cn = input("> cn=")
                pw = input("> pw=")

            else:
                try:
                    cn, pw = cn_pw.split(":")
                except ValueError:
                    print("invalid arguments. use this subcommand like this:"
                          f"{self.cmd_name} [cn:userPassword]")

            res = conn.search(DN, f"(cn={cn})", attributes="userPassword")

            assert len(conn.entries) == 1

            if res:
                crypt_hash = conn.entries.pop()\
                             .entry_attributes_as_dict["userPassword"]\
                             .pop().decode()\
                             .strip("{CRYPT}")

                if hmac.compare_digest(crypt.crypt(pw, crypt_hash),
                                       crypt_hash):
                    print("Successfully logged in!")
                else:
                    print("Passwords did not match!")

        super().__init__("login", "test login credentials.", login)
