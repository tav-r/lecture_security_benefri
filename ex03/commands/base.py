from abc import ABCMeta


class Command(metaclass=ABCMeta):
    def __init__(self, name="base command", callback=None):
        self.__cmd_name = name
        self.__callback = callback

    @property
    def cmd_name(self):
        return self.__cmd_name

    def run(self, *args, **kwargs):
        if self.__callback:
            return self.__callback(*args, **kwargs)

    def end(self):
        return False
