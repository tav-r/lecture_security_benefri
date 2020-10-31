"""A simple interactive LDAP client for the command line."""

import getpass
from typing import Union
from sys import stderr, exit as sys_exit

import ldap

from commands.base import Command
from commands.exit import ExitCommand


class LDAPClient():
    """An interactive LDAP client."""

    def __init__(self, hostname, user, password):
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT,
                        ldap.OPT_X_TLS_NEVER)
        self.__conn = None
        self.__hostname = hostname
        self.__user = user
        self.__password = password
        self.__cmds = [ExitCommand()]

        self.__prompt = "> "

        # no two commands can have the same name
        assert len(self.__cmds) == len({cmd.cmd_name for cmd in self.__cmds})

    def run(self):
        """Start interactive mode."""

        assert self.__conn

        print(f"[*] successfully logged in as {self.__conn.whoami_s()}")
        cmd = None
        while not cmd or not cmd.end():
            cmd = self.__get_matching(input(self.__prompt))
            if cmd:
                cmd.run()

    def __get_matching(self, cmd_str) -> Union[None, Command]:
        cmd_name, *cmd_args = cmd_str.split(" ", 1)
        cmds = [cmd for cmd in self.__cmds
                if cmd.cmd_name.startswith(cmd_name)]

        if len(cmds) == 0:
            print("unknown command")
            return None

        if len(cmds) > 1:
            print("ambiguous command")
            return None

        return cmds.pop()

    def __enter__(self):
        self.__conn = ldap.initialize(self.__hostname)
        self.__conn.set_option(ldap.OPT_REFERRALS, 0)
        self.__conn.simple_bind(self.__user, self.__password)

        return self

    def __exit__(self, _, __, ___):
        if self.__conn:
            self.__conn.unbind_ext()


def main():
    """Create a client instance and run it."""

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-H", "--hostname", dest="hostname",
                            help="hostname of ldap server")
    arg_parser.add_argument("-u", "--username", dest="username",
                            help="username for login")
    arg_parser.add_argument("-p", "--password", dest="password",
                            help="password for login", default=None)
    args = arg_parser.parse_args()

    if not args.username:
        print("Please specify a username with the '-u' flag", file=stderr)
        sys_exit(1)

    if not args.hostname:
        print("Please specify a hostname with the '-H' flag", file=stderr)
        sys_exit(1)

    passwd = args.password if args.password else getpass.getpass()

    with LDAPClient(args.hostname, args.username, passwd) as client:
        client.run()


if __name__ == "__main__":
    import argparse
    main()
