# Exercise 1
**This program was only tested on Linux and I do not know if it also works on MacOS or Windows (although I think it should)**.
## Build
To build the project, [cargo](https://github.com/rust-lang/cargo) (and all its dependencies like `rustc`) must be installed. An easy way to get the rust-toolchain is described at [rustup.rs](https://rustup.rs/). When you have `carg`, run:
```bash 
cd ex01 && cargo build --release
``` 
The compiled binary will be in `ex01/target/release/ex01`

## Using the program
Run `ex01 help` or `ex01 -h` or `ex01 --help` to get an overview:
```
$ ./ex01 -h
ex01

USAGE:
    ex01 [OPTIONS] --file <HASH_FILE> [SUBCOMMAND]

FLAGS:
    -h, --help       Prints help information
    -V, --version    Prints version information

OPTIONS:
    -e, --exception-file <EXCEPTION_FILE>    Path to file with a list of files to skip
    -f, --file <HASH_FILE>                   Path to file with hashes

SUBCOMMANDS:
    analyze    Check hash file for given path
    help       Prints this message or the help of the given subcommand(s)
    index      Create hash file for given path
```
Notice, that you *have* to specify `HASH_FILE` with the `-f/--file` flag while the `-e/--exception-file` flag is optional. Use the `-h/--help` flags to get an overview of how to use the subcommands:
```bash
$ ./ex01 -f /tmp/hashes.json index -h
ex01-index
Create hash file for given path

USAGE:
    ex01 index <PATH>

FLAGS:
    -h, --help       Prints help information
    -V, --version    Prints version information

ARGS:
    <PATH>
```
and
```bash
$ ./ex01 -f /tmp/hashes.json analyze -h
ex01-analyze
Check hash file for given path

USAGE:
    ex01 analyze [FLAGS] <PATH>

FLAGS:
    -h, --help       Prints help information
    -l, --list       List changed files and directories
    -V, --version    Prints version information

ARGS:
    <PATH>
```
