import src.commands.base


class ExitCommand(src.commands.base.Command):
    def __init__(self, client):

        def exit():
            client.disconnect()

        super().__init__("exit", "exit client", exit)
