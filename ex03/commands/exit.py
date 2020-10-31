import commands.base

class ExitCommand(commands.base.Command):
    def __init__(self):
        super().__init__(name="exit")

    def end(self):
        return True
