use std::error::Error;

use console::Term;

use super::file_handling;
use super::check_hashes;

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

pub fn analyze_mode(dir_path: &str, hash_file_path: &str, exception_file_path: Option<&str>, full_list: bool) -> Result<(), Box<dyn Error>> {
    let mut sw = stopwatch::Stopwatch::new();
    let term = Term::stdout();

    sw.start();

    term.write_line("Running...")?;
    term.write_line("\tParsing exception file")?;

    let exceptions = match exception_file_path {
        Some(path) => Some(file_handling::parse_exception_file(path)?),
        None => None
    };

    term.write_line("\tParsing json")?;

    let mapping = file_handling::parse_json_file(&hash_file_path)?;

    term.write_line(&format!("\tLooking for changes in {}", dir_path))?;

    let (changed, new_files, deleted_files, new_dirs, deleted_dirs) = check_hashes::check_directory(&dir_path, &mapping, exceptions)?;

    for _ in 0..4 {
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
