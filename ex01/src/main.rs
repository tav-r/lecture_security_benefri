mod lib;


use std::env::{args};
use std::error::Error;

use lib::modes::{hash,check};

fn print_usage(prog_name: &str) {
    println!("Usage: 
    to hash files:
        {} hash OUT_FILE PATH1 [PATH2 [...[PATHn]]]
    and to check files against hashes in HASH_FILE:
        {} check HASH_FILE [PATH1 [...[PATHn]]]",
    prog_name, prog_name)
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut arguments = args();
    let prog_name = arguments.next().unwrap();
    let mode = arguments.next().unwrap_or(String::from("help"));

    match &mode[..] {
        "hash" => hash::hash_mode(arguments),
        "check" => check::check_mode(arguments),
        _ => {
            print_usage(&prog_name);
            Ok(())
        }
    }
}
