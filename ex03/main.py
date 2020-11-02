"""A simple interactive LDAP client for the command line."""

import getpass
from sys import stderr, exit as sys_exit

import src.client


def main():
    """Create a client instance and run it."""

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("hostname", metavar="HOSTNAME[:PORT]",
                            help="hostname of ldap server")
    arg_parser.add_argument("-u", "--username", dest="username",
                            help="username for login")
    arg_parser.add_argument("-p", "--password", dest="password",
                            help="password for login", default=None)
    args = arg_parser.parse_args()

    username = args.username if args.username else input("username:")
    passwd = args.password if args.password else getpass.getpass()

    with src.client.LDAPClient(args.hostname, username, passwd) as client:
        client.run()


if __name__ == "__main__":
    import argparse
    main()
