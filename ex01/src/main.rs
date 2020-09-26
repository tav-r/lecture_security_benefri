mod lib;


use std::env::{args,Args,var};
use std::error::Error;
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
    changed: &Vec<String>,
    new_files: &Vec<String>,
    deleted_files: &Vec<String>,
    new_dirs: &Vec<String>,
    deleted_dirs: &Vec<String>
) -> Result<(), Box<dyn Error>> {
    for (n, v) in vec![
        ("Changed files", changed), ("New files", new_files), ("Deleted files", deleted_files),
        ("New directories", new_dirs), ("Deleted directories", deleted_dirs)
    ] {
        term.write_line(&format!("{}:", n))?;
        if v.len() > 0 {
            for e in v {
                term.write_line(&format!("\t{}", e))?;
            }
        } else {
            term.write_line("\t(None)")?;
        }
    }

    term.write_str("\n")?;

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

fn check_mode(mut arguments: Args) -> Result<(), Box<dyn Error>> {
    let mut sw = stopwatch::Stopwatch::new();
    let term = Term::stdout();
    let hash_file_path = arguments.next().expect("No hash file specified!");
    let dir_path = arguments.next().expect("No directory specified");

    sw.start();

    term.write_line("Running...")?;
    term.write_line("\tParsing json")?;

    let mapping = file_handling::parse_json_file(&hash_file_path)?;

    term.write_str(&format!("\tLooking for changes in {}", dir_path))?;

    let (changed, new_files, deleted_files, new_dirs, deleted_dirs) = check_hashes::check_directory(&dir_path, &mapping)?;

    term.clear_line()?;

    term.move_cursor_up(1)?;
    term.clear_line()?;
    term.move_cursor_up(1)?;
    term.clear_line()?;
    term.write_line("Done!")?;

    if let Ok(_) = var("LIST_CHANGES") {
        print_changes(&term, &changed, &new_files, &deleted_files, &new_dirs, &deleted_dirs)?;
    }

    sw.stop();

    term.write_line(
        &format!("\t{} files changed, {} new files, {} files deleted, {} new directories, \
                  {} deleted directories\n\t(checked {} files and directories in {} seconds)",
            changed.len(), new_files.len(), deleted_files.len(), new_dirs.len(), deleted_dirs.len(),
            mapping.len() + new_dirs.len() + new_files.len(), sw.elapsed().as_secs()))?;

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
