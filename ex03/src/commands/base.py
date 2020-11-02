"""Defintion of the interface for commands."""

from abc import ABCMeta


class Command(metaclass=ABCMeta):
    """Interface for commands."""
    def __init__(self, name="base command",
                 description="", callback=None):
        self.__cmd_name = name
        self.__description = description
        self.__callback = callback

    @property
    def cmd_name(self):
        return self.__cmd_name

    @property
    def description(self):
        return self.__description

    def run(self, *args, **kwargs):
        if self.__callback:
            return self.__callback(*args, **kwargs)

    def end(self):
        return False
