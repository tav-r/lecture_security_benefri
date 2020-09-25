mod lib;


use std::env::{args,Args,var};
use std::error::Error;
use std::collections::HashMap;
use std::ffi::OsString;

use console::Term;

use lib::{check_hashes,file_handling,hash_files::HashWalker};

fn print_usage(prog_name: &str) {
    println!("Usage: 
    to hash files:
        {} hash OUT_FILE PATH1 [PATH2 [...[PATHn]]]
    and to check files against hashes in HASH_FILE:
        {} check HASH_FILE [PATH1 [...[PATHn]]]",
    prog_name, prog_name)
}

fn hash_mode(mut arguments: Args) -> Result<(), Box<dyn Error>> {
    let term = Term::stdout();
    let out_file = arguments.next().expect("No out file specified!");

    term.write_line("Running...")?;

    let contents = get_contents(arguments, &term)?;
    file_handling::save_contents(&out_file, contents)?;

    term.move_cursor_up(1)?;
    term.clear_line()?;
    term.write_line("Done!")?;

    Ok(())
}

pub fn print_changes(
    term: &console::Term,
    new: &Vec<String>,
    changed: &Vec<String>,
    deleted: &Vec<String>)
-> Result<(), Box<dyn Error>> {
        term.write_line("Changed:")?;
        for c in changed {
            term.write_line(&format!("\t{}", c))?;
        }

        term.write_line("new:")?;
        for n in new {
            term.write_line(&format!("\t{}", n))?;
        }

        term.write_line("Deleted:")?;
        for d in deleted {
            term.write_line(&format!("\t{}", d))?;
        }

        Ok(())
}

pub fn get_contents(paths: Args, term: &console::Term) -> Result<Vec<(String, String)>, Box<dyn Error>> {
    let mut tot = vec![];

    for (n, path) in paths.enumerate() {
        term.write_str(&format!("\t{}. hashing files in {}", n + 1, path))?;
        let walker = HashWalker::new(OsString::from(path)).unwrap();

        for (path_str, hash) in walker {
            tot.push((path_str, hash))
        }

        term.clear_line()?;
    }

    Ok(tot)
}

fn check_changes(
    mapping: &HashMap<String, String>,
    arguments: Args,
    term: &console::Term
) -> Result<(Vec<String>, Vec<String>, Vec<String>), Box<dyn Error>> {

    let mut changed = Vec::new();
    let mut new = Vec::new();
    let mut deleted = Vec::new();

    for dir_path in arguments {
        term.write_str(&format!("\tLooking for changes in {}", dir_path))?;
        let (mut c, mut n, mut d) = check_hashes::check_directory(&dir_path, mapping)?;
        changed.append(&mut c);
        new.append(&mut n);
        deleted.append(&mut d);

        term.clear_line()?;
   }

   Ok((changed, new, deleted))
}

fn check_mode(mut arguments: Args) -> Result<(), Box<dyn Error>> {
    let term = Term::stdout();
    let hash_file_path = arguments.next().expect("No hash file specified!");

    term.write_line("Running...")?;
    term.write_str("\tParsing json")?;

    let mapping = file_handling::parse_json_file(&hash_file_path)?;

    term.clear_line()?;
    term.move_cursor_up(1)?;
    term.clear_line()?;
    term.write_line("Done!")?;

    let (changed, new, deleted) = check_changes(&mapping, arguments, &term)?;

    if let Ok(_) = var("LIST_CHANGES") {
        print_changes(&term, &changed, &new, &deleted)?;
    }

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
