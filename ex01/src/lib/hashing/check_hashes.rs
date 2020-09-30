use std::error::Error;
use std::ffi::OsString;
use std::collections::{HashMap,HashSet};
use std::iter::FromIterator;

use super::{hash_files::HashWalker,DIR_STR};

// Obtain the changes in a given path relative to a HashMap mapping paths to hash values.
// The paths of changed files, new files, new directories, deleted files and deleted directories
// are all returned in a seperate vector of strings.
// 
// # Arguments
// * `dir_path` - string describing a relative or absolute path to a directory to check for changes
// * `old_mapping` - the 'path->hash value' mapping that describes the old state. Notice that, if
//                   this contains *relative* paths and `dir_path` was given as an *absolute* path
//                   (or vice versa), this funciton is not smart enough to check if the same files/
//                   directories were specified and it will treat these paths as if they would
//                   describe different folders
// * `exceptions` - an Option wrapping an optional string describing an absolut or a relative
//                  path to a file with exceptions (i.e. files or directories not to check)
pub fn check_directory(
    dir_path: &str,
    old_mapping: &HashMap<String, String>,
    exceptions: Option<HashSet<String>>
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

    let walker = HashWalker::new(OsString::from(dir_path), exceptions);
    let new_mapping: HashMap<String, String> = HashMap::from_iter(walker?);

    // Check every entry in the new mapping against the old mapping to find
    // new entries and changed hash values
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

    // Check every entry in the old mapping against the new mapping to see if
    // a file was deleted
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
