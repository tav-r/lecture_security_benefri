from .base import Command
from . import NEW_PEOPLE_ATTRIBUTES, DN, OBJECT_CLASS


class AddCommand(Command):
    def __init__(self, client):

        def add_entry():
            conn = client.connection

            # read cn from stdin
            cn = input("> cn=")
            entry_dict = {"cn": cn}

            # read the the other attributes according to NEW_PEOPLE_ATTRIBUTES
            for attr in NEW_PEOPLE_ATTRIBUTES:
                entry_dict.update({attr: input(f"> {attr}=")})

            res = conn.add(f"cn={cn},{DN}", OBJECT_CLASS, entry_dict)
            if res:
                print("Successfully added person!")

        super().__init__("add", "adds a new person to the LDAP.", add_entry)
