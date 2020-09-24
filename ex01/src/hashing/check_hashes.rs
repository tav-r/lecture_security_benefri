use std::error::Error;
use std::ffi::OsString;
use std::collections::HashMap;
use std::iter::FromIterator;

use super::hash_files::HashWalker;

pub fn check_directory(dir_path: &str, old_mapping: &HashMap<&str, &str>) -> Result<(Vec<String>, Vec<String>, Vec<String>), Box<dyn Error>> {
    let mut changed = Vec::new();
    let mut new = Vec::new();

    let walker = HashWalker::new(OsString::from(dir_path));
    let new_mapping: HashMap<String, String> = HashMap::from_iter(walker?);

    for (file_path, hash) in &new_mapping {
        if let Some(entry) = old_mapping.get(&file_path[..]) {
            if hash != *entry {
                changed.push(String::from(file_path))
            }
        } else {
            new.push(String::from(file_path))
        }
    }

    let deleted = old_mapping.iter().filter(|(file_path, _)| {
        new_mapping.get(**file_path).is_none()
    }).map(|(file_path, _)| {
        String::from(*file_path)
    }).collect();

    Ok((changed, new, deleted))
}