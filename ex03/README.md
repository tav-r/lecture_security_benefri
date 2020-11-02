# A simple interactive LDAP client
## Installation
The only requirement is the Python module [ldap3](https://github.com/cannatag/ldap3).

## Usage
The `-h` flag gives a quick overview of the usage of the client:
```
$ python main.py -h
usage: main.py [-h] [-u USERNAME] [-p PASSWORD] HOSTNAME[:PORT]

positional arguments:
  HOSTNAME[:PORT]       hostname of ldap server

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        username for login
  -p PASSWORD, --password PASSWORD
                        password for login
```

When connected to the server, you can use `help` to get an overview of the available commands:
```
> help
exit : exit client
help : print this help message
all : display a list of all the persons in the LDAP
see : display the information of one person.
add : adds a new person to the LDAP.
remove : removes an existing user from the LDAP
login : test login credentials.
modify : modifies an existing user.
>
```
You can run a command by typing only the beginning as long as it is unambiguous. You can for example just type `log` to run the `login` command.

For the `login` command you have two options: you can either specify the `cn` and the password directly like this: `login David Herrmann:test` or you can just type `login` and you will be prompted for the `cn` and the password. Similiarly, you can use `see` like `see David Herrmann` or you can just run `see` and you will be prompted for the `cn`. The same is true for `add`, `remove` and `modify`.
