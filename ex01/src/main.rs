mod hashing;

#[macro_use]
extern crate json;

use std::env::{args,Args};
use std::ffi::OsString;
use std::error::Error;
use std::fs::File;
use std::iter::FromIterator;
use std::collections::HashMap;
use std::io::prelude::*;
use hashing::{hash_files::HashWalker,check_hashes};
use console::Term;

fn print_usage(prog_name: &str) {
    println!("Usage: 
    to hash files:
        {} hash OUT_FILE PATH1 [PATH2 [...[PATHn]]]
    and to check hashes in HASH_FILE:
        {} check HASH_FILE [PATH2 [...[PATHn]]]",
    prog_name, prog_name)
}

fn hash_mode(mut arguments: Args) -> Result<(), Box<dyn Error>> {
    let term = Term::stdout();
    let out_file = arguments.next().expect("No out file specified!");
    let mut tot = vec![];

    term.write_line("Running...")?;

    for (n, path) in arguments.enumerate() {
        term.write_str(&format!("\t{}. hashing files in {}", n + 1, path))?;
        let walker = HashWalker::new(OsString::from(path)).unwrap();

        for (path_str, hash) in walker {
            tot.push((path_str, hash))
        }

        term.clear_line()?;
    }

    let contents = json::JsonValue::Array(tot.iter().map(|(key, val)| {object!{
        "path" => key[..],
        "hash" => val[..]
    }}).collect());

    // println!("{}", contents.pretty(4));
    let mut out_file = File::create(out_file)?;
    out_file.write_all(contents.pretty(4).as_bytes())?;

    term.move_cursor_up(1)?;
    term.clear_line()?;
    term.write_line("Done!")?;

    Ok(())
}

fn check_mode(mut arguments: Args) -> Result<(), Box<dyn Error>> {
    let term = Term::stdout();
    let hash_file = arguments.next().expect("No hash file specified!");
    let mut changed = Vec::new();
    let mut new = Vec::new();
    let mut deleted = Vec::new();

    term.write_line("Running...")?;
    term.write_str("\tParsing json")?;

    let mut contents = String::new();
    let _ = File::open(hash_file)?.read_to_string(&mut contents)?;
    let parsed = json::parse(&contents)?;

    let mapping :HashMap<&str, &str> = HashMap::from_iter(parsed.members().map(|member| {
        if let json::JsonValue::Object(obj) = member {
            (obj["path"].as_str().unwrap(), obj["hash"].as_str().unwrap())
        } else {
            panic!()
        }
    }));

    term.clear_line()?;

    for dir_path in arguments {
        term.write_str(&format!("\tLooking for changes in {}", dir_path))?;
        let (mut c, mut n, mut d) = check_hashes::check_directory(&dir_path, &mapping)?;
        changed.append(&mut c);
        new.append(&mut n);
        deleted.append(&mut d);

        term.clear_line()?;
   }

    term.move_cursor_up(1)?;
    term.clear_line()?;
    term.write_line("Done!")?;

    term.write_line(
        &format!("\t{} files changed, {} new files, {} files deleted, {} files unchanged",
            changed.len(), new.len(), deleted.len(), mapping.len() - changed.len()))?;

    Ok(())
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut arguments = args();
    let prog_name = arguments.next().unwrap();
    let mode = arguments.next().unwrap_or(String::from("help"));

    match &mode[..] {
        "hash" => hash_mode(arguments),
        "check" => check_mode(arguments),
        _ => {
            print_usage(&prog_name);
            Ok(())
        }
    }
}
