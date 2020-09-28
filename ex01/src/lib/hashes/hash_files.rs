use std::fs::{read_dir,File,DirEntry,ReadDir};
use std::io::{prelude::*};
use std::ffi::{OsString};
use std::error::Error;
use std::iter::Iterator;
use std::collections::HashSet;

use super::DIR_STR;

fn get_file_hash(entry: &DirEntry) -> Result<String, Box<dyn Error>> {
    let mut contents = String::new();
    let _ = File::open(entry.path())?.read_to_string(&mut contents);

    let hash = crypto_hash::hex_digest(crypto_hash::Algorithm::SHA256, contents.as_ref());
    Ok(hash)
}

pub struct HashWalker {
    dir_stack: Vec<OsString>,
    iterator: ReadDir,
    exceptions: Option<HashSet<String>>
}

impl HashWalker {
    pub fn new(path_str: OsString, exceptions: Option<HashSet<String>>) -> Result<Self, Box<dyn Error>> {
        let stack = Vec::new();
        Ok(Self{dir_stack: stack, iterator: read_dir(path_str).unwrap(), exceptions: exceptions})
    }
}

impl Iterator for HashWalker {
     type Item = (String, String);

     fn next(&mut self) -> Option<(String, String)> {
        if let Some(entry_res) = self.iterator.next() {
            let entry = entry_res.unwrap();
            let pathtype = entry.metadata().unwrap().file_type();
            let mut path_str = String::from(entry.path().as_os_str().to_str().unwrap());
            let hash;

            // skip symlinks (to avoid having to deal with infinite loops)
            if pathtype.is_symlink() {
                return self.next()
            }
 
            // skip files on exception list
            if let Some(exceptions_list) = &self.exceptions {
                if exceptions_list.contains(&path_str) {
                    return self.next()
                }
            }

            // push entry on stack and set 'special' hash val if it is a directory
            if pathtype.is_dir() {
                self.dir_stack.push(OsString::from(entry.path().as_os_str()));
                hash = String::from(DIR_STR);
                path_str = format!("{}/", path_str);
            } else {
                hash = get_file_hash(&entry).unwrap();
            }

            Some((path_str, hash))
        } else {
            if let Some(dir) = self.dir_stack.pop() {
                self.iterator = read_dir(dir).unwrap();
                return self.next()
            }

            None
        }
    }
}
