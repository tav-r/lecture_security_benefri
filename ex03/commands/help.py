from typing import Dict

import commands.base


class HelpCommand(commands.base.Command):
    def __init__(self, command_description: Dict["str", "str"]):

        def print_help():
            for key, val in command_description.items():
                print(f"{key} : {val}")

            print(f"{self.cmd_name} : {self.description}")

        super().__init__("help", "print this help message", print_help)
