use std::error::Error;

use console::Term;

use super::file_handling;
use super::check_hashes;

// Write the changes (according to the given vectors) to the given console::Term
fn print_changes(
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

/// The entry function that gets called when the analyze-subcommand is executed
///
/// # Arguments
/// * `dir_path` - a string describing an absolute or a relative path to the directory to analyze
/// * `hash_file` - a string describing an absolute or a relative path to the file to store the hashes
/// * `exception_file_path` - an Option wrapping an optional string describing an absolut or a relative
///                           path to a file with exceptions (i.e. files or directories not to check)
/// * `full_list` - a boolean value, if set true, a list with changed, deleted and new files and
///                 directories will be printed
pub fn analyze_mode(dir_path: &str, hash_file_path: &str, exception_file_path: Option<&str>, full_list: bool) -> Result<(), Box<dyn Error>> {
    let mut sw = stopwatch::Stopwatch::new();
    let term = Term::stdout();

    sw.start();

    term.write_line("Running...")?;

    let exceptions = match exception_file_path {
        Some(path) => Some(file_handling::parse_exception_file(path)?),
        None => None
    };

    term.write_line("\tParsing hash file")?;

    let mapping = file_handling::parse_json_file(&hash_file_path)?;

    term.write_line(&format!("\tLooking for changes in {}", dir_path))?;

    let (changed, new_files, deleted_files, new_dirs, deleted_dirs) = check_hashes::check_directory(&dir_path, &mapping, exceptions)?;

    for _ in 0..3 {
        term.move_cursor_up(1)?;
        term.clear_line()?;
    }

    term.write_line("Done!")?;

    sw.stop();

    if full_list {
        print_changes(&term, &changed, &new_files, &deleted_files, &new_dirs, &deleted_dirs)?;
    }

    term.write_line(
        &format!("\t{} files changed, {} new files, {} files deleted, {} new directories, \
                  {} deleted directories\n\t(checked {} files and directories in {} seconds)",
            changed.len(), new_files.len(), deleted_files.len(), new_dirs.len(), deleted_dirs.len(),
            mapping.len() + new_dirs.len() + new_files.len(), sw.elapsed().as_secs()))?;

    Ok(())
}
