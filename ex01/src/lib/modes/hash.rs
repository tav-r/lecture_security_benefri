use std::error::Error;
use std::ffi::OsString;

use console::Term;

use super::file_handling;
use super::hash_files;

fn get_contents(path_str: &str, term: &console::Term) -> Result<Vec<(String, String)>, Box<dyn Error>> {
    let mut tot = vec![];

    term.write_str(&format!("\thashing files in {}", path_str))?;
    let walker = hash_files::HashWalker::new(OsString::from(path_str)).unwrap();

    for (path_str, hash) in walker {
        tot.push((path_str, hash))
    }

    term.clear_line()?;

    Ok(tot)
}

pub fn hash_mode(path_str: &str, out_file: &str) -> Result<(), Box<dyn Error>> {
    let term = Term::stdout();

    term.write_line("Running...")?;

    let contents = get_contents(&path_str, &term)?;
    file_handling::save_contents(&out_file, contents)?;

    term.move_cursor_up(1)?;
    term.clear_line()?;
    term.write_line("Done!")?;

    Ok(())
}