"""A simple interactive LDAP client for the command line."""

import getpass
from typing import Union, Tuple, List
from sys import stderr, exit as sys_exit

from ldap3 import Server, Connection, SAFE_SYNC, ALL as ldap_ALL, ObjectDef

from .commands import base, exit as _exit, help as _help, all as _all,\
                      see, add, remove, log, mod


class LDAPClient():
    """An interactive LDAP client."""

    def __init__(self, hostname: str, user: str, password: str):
        self.__conn = None
        self.__hostname = hostname
        self.__user = user
        self.__password = password
        self.__cmds: List[base.Command] =\
            [_exit.ExitCommand(self), _help.HelpCommand(self),
             _all.ListAllCommand(self), see.SeeCommand(self),
             add.AddCommand(self), remove.RemoveCommand(self),
             log.LogCommand(self), mod.Modifycommand(self)]

        self.__prompt = "> "

        # no two commands can have the same name
        assert len(self.__cmds) == len({cmd.cmd_name for cmd in self.__cmds})

    def run(self):
        """Start interactive mode."""

        assert self.__conn

        print(f"[*] successfully logged in as {self.__conn.user}")
        cmd = None
        while self.running:
            try:
                cmd, cmd_args = self.__get_matching(input(self.__prompt))
                if cmd:
                    cmd.run(*cmd_args)
            except (EOFError, KeyboardInterrupt):
                print("Exiting...")
                self.disconnect()

    @property
    def running(self):
        """Check if the client is running."""
        return self.__conn is not None

    @property
    def connection(self):
        """The connection the client is using."""
        return self.__conn

    @property
    def commands(self):
        """A list of the commands the client supports."""
        return self.__cmds

    def __get_matching(self, cmd_str: str)\
            -> Union[Tuple[None, None], Tuple[base.Command, List[str]]]:

        cmd_name, *cmd_args = cmd_str.split(" ", 1)
        cmds = [cmd for cmd in self.__cmds
                if cmd.cmd_name.startswith(cmd_name)]

        if len(cmds) == 0:
            print("unknown command")
            return None, None

        if len(cmds) > 1:
            print("ambiguous command")
            return None, None

        return cmds.pop(), cmd_args

    def disconnect(self):
        """Disconnect the client from the server."""
        if self.__conn:
            self.__conn.unbind()

        self.__conn = None

    def connect(self):
        """Connect the client to the server."""
        srv = Server(self.__hostname, use_ssl=True, get_info=ldap_ALL)
        self.__conn = Connection(srv, self.__user, self.__password,
                                 auto_bind=True,
                                 return_empty_attributes=True)

    def __enter__(self):
        self.connect()

        return self

    def __exit__(self, _, __, ___):
        if self.__conn:
            self.__conn.unbind()
