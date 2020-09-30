use std::error::Error;
use std::ffi::OsString;

use console::Term;

use super::file_handling;
use super::hash_files;

/// The entry function that gets called when the index-subcommand is executed
///
/// # Arguments
/// * `path_str` - a string describing an absolute or a relative path to the directory to analyze
/// * `out_file` - a string describing an absolute or a relative path to the file to store the hashes
/// * `exception_file_path` - an Option wrapping an optional string describing an absolut or a relative
///                           path to a file with exceptions (i.e. files or directories not to check)
pub fn index_mode(path_str: &str, out_file: &str, exception_file_path: Option<&str>) -> Result<(), Box<dyn Error>> {
    let term = Term::stdout();

    term.write_line("Running...")?;

    let exceptions = match exception_file_path {
        Some(path) => Some(file_handling::parse_exception_file(path)?),
        None => None
    };

    term.write_str(&format!("\thashing files in {}", path_str))?;

    let contents = hash_files::HashWalker::new(OsString::from(path_str), exceptions).unwrap().collect();

    term.clear_line()?;

    file_handling::save_contents(&out_file, contents)?;

    term.move_cursor_up(1)?;
    term.clear_line()?;
    term.write_line("Done!")?;

    Ok(())
}
