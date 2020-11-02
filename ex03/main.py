"""A simple interactive LDAP client for the command line."""

import getpass
from sys import stderr, exit as sys_exit

import src.client


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

    with src.client.LDAPClient(args.hostname, args.username, passwd) as client:
        client.run()


if __name__ == "__main__":
    import argparse
    main()
