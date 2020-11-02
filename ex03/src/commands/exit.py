"""Definition of the 'exit' command."""

import src.commands.base


class ExitCommand(src.commands.base.Command):
    """Command to exit the client."""
    def __init__(self, client):

        def _exit():
            client.disconnect()

        super().__init__("exit", "exit client", _exit)
