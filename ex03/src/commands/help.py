from typing import Dict

import src.commands.base


class HelpCommand(src.commands.base.Command):
    def __init__(self, client):

        def print_help():
            for key, val in {cmd.cmd_name: cmd.description
                             for cmd in client.commands}.items():
                print(f"{key} : {val}")

        super().__init__("help", "print this help message", print_help)
