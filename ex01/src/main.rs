mod lib;


use std::error::Error;
use clap::{App,Arg,SubCommand};

use lib::modes::{hash,check};

fn main() -> Result<(), Box<dyn Error>> {
    let matches = App::new("ex01")
        .arg(Arg::with_name("file").long("file").short("f").takes_value(true).help("Path to file with hashes").required(true))
        .subcommand(SubCommand::with_name("check").about("Check hash file for given path")
            .arg(Arg::with_name("list").long("list").short("l").help("List changed files and directories"))
            .arg(Arg::with_name("path").value_name("PATH").takes_value(true).required(true))
        )
        .subcommand(SubCommand::with_name("hash").about("Create hash file for given path")
            .arg(Arg::with_name("path").value_name("PATH").takes_value(true).required(true))
        )
        .get_matches();

    let hash_file_path = matches.value_of("file").unwrap();

    match matches.subcommand() {
        ("hash", Some(subcomm)) => hash::hash_mode(subcomm.value_of("path").unwrap(), hash_file_path),
        ("check", Some(subcomm)) => check::check_mode(subcomm.value_of("path").unwrap(), hash_file_path, subcomm.is_present("list")),
        _ => {
            println!("{}", matches.usage());
            Ok(())
        }
    }
}
