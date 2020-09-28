mod lib;


use std::error::Error;
use clap::{App,Arg,SubCommand};

use lib::modes::{index,analyze};

fn main() -> Result<(), Box<dyn Error>> {
    let matches = App::new("ex01")
        .arg(Arg::with_name("file")
            .long("file")
            .short("f")
            .value_name("HASH_FILE")
            .takes_value(true)
            .help("Path to file with hashes")
            .required(true)
        )
        .arg(Arg::with_name("exceptions")
            .long("exception-file")
            .short("e")
            .value_name("EXCEPTION_FILE")
            .takes_value(true)
            .help("Path to file with a list of files to skip")
            .required(false)
        )
        .subcommand(SubCommand::with_name("analyze")
            .about("Check hash file for given path")
            .arg(Arg::with_name("list")
                .long("list")
                .short("l")
                .help("List changed files and directories")
            )
            .arg(Arg::with_name("path")
                .value_name("PATH")
                .takes_value(true)
                .required(true)
            )
        )
        .subcommand(SubCommand::with_name("index")
            .about("Create hash file for given path")
            .arg(Arg::with_name("path")
                .value_name("PATH")
                .takes_value(true)
                .required(true)
            )
        )
        .get_matches();

    let hash_file_path = matches.value_of("file").unwrap();
    let exception_file_path = matches.value_of("exceptions");

    match matches.subcommand() {
        ("index", Some(subcomm)) => index::index_mode(subcomm.value_of("path").unwrap(), hash_file_path, exception_file_path),
        ("analyze", Some(subcomm)) => analyze::analyze_mode(subcomm.value_of("path").unwrap(), hash_file_path, exception_file_path, subcomm.is_present("list")),
        _ => {
            println!("{}", matches.usage());
            Ok(())
        }
    }
}
