use std::error::Error;
use std::ffi::OsString;
use std::collections::HashMap;
use std::iter::FromIterator;

use super::{hash_files::HashWalker,DIR_STR};

pub fn check_directory(
    dir_path: &str, old_mapping: &HashMap<String, String>
) -> Result<(
    Vec<String>,
    Vec<String>,
    Vec<String>,
    Vec<String>,
    Vec<String>
), Box<dyn Error>> {
    let mut changed = Vec::new();
    let mut newf = Vec::new();
    let mut newd = Vec::new();
    let mut deletedf = Vec::new();
    let mut deletedd = Vec::new();

    let walker = HashWalker::new(OsString::from(dir_path));
    let new_mapping: HashMap<String, String> = HashMap::from_iter(walker?);

    for (file_path, hash) in &new_mapping {
        if let Some(entry) = old_mapping.get(&file_path[..]) {
            if hash != entry {
                changed.push(String::from(file_path))
            }
        } else {
            if hash == DIR_STR {
                newd.push(String::from(file_path))
            } else {
                newf.push(String::from(file_path))
            }
        }
    }

    for (file_path, hash) in old_mapping {
        if new_mapping.get(file_path).is_none() {
            if hash == DIR_STR {
                deletedd.push(String::from(file_path));
            } else {
                deletedf.push(String::from(file_path));
            }
        }
    }

    Ok((changed, newf, deletedf, newd, deletedd))
}