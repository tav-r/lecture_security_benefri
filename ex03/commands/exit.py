import commands.base

class ExitCommand(commands.base.Command):
    def __init__(self):
        super().__init__("exit", "exit client")

    def end(self):
        return True
