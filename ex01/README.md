# Exercise 1
**This program was only tested on Linux and I do not know if it also works on MacOS or Windows (although I think it should)**.
## Build
To build the project, [cargo](https://github.com/rust-lang/cargo) (and all its dependencies like `rustc`) must be installed. An easy way to get the rust-toolchain is described at [rustup.rs](https://rustup.rs/). When you have `cargo`, run:
```bash 
cd ex01 && cargo build --release
``` 
The compiled binary will be at `ex01/target/release/ex01`

## Using the program
An example usage might be the following: The file `/tmp/exceptions` contains the following lines:
```
/home/user/hugedirectory
/home/user/somedirectory/irrelevantfile
```
To index `/home/user` ignoring the paths in the `exceptions`-file and to store the hash file at `/tmp/hashes.json` run
```
$ target/release/ex01 -e /tmp/exceptions -f /tmp/hashes.json index /home/user
```
This may take a while, depending on the size of the folder to index. When the program has finished its work, you can run
```
$ target/release/ex01 -e /tmp/exceptions -f /tmp/hashes.json analyze /home/user
```
You will get an output like
```
Done!
	0 files changed, 8 new files, 2994 files deleted, 1 new directories, 585 deleted directories
	(checked 27756 files and directories in 1 seconds)
```

Run `ex01 help` or `ex01 -h` or `ex01 --help` to get a more detailed overview:
```bash
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
