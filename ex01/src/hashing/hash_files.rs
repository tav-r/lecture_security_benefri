use std::fs::{read_dir,File,DirEntry,canonicalize,ReadDir};
use std::io::{prelude::*};
use std::ffi::{OsString};
use std::error::Error;
use std::iter::Iterator;

fn get_file_hash(entry: DirEntry) -> Result<(String, String), Box<dyn Error>> {
    let mut contents = String::new();
    let _ = File::open(entry.path())?.read_to_string(&mut contents);

    let hash = crypto_hash::hex_digest(crypto_hash::Algorithm::SHA256, contents.as_ref());
    Ok((String::from(entry.path().as_os_str().to_str().unwrap()), hash))
}

pub struct HashWalker {
    dir_stack: Vec<OsString>,
    iterator: ReadDir
}

impl HashWalker {
    pub fn new(path_str: OsString) -> Result<Self, Box<dyn Error>> {
        let stack = Vec::new();
        Ok(Self{dir_stack: stack, iterator: read_dir(path_str).unwrap()})
    }
}

impl Iterator for HashWalker {
     type Item = (String, String);

     fn next(&mut self) -> Option<(String, String)> {
        if let Some(entry_res) = self.iterator.next() {
            let entry = entry_res.unwrap();
            let path = canonicalize(entry.path()).unwrap();
            let pathtype = entry.metadata().unwrap().file_type();

            // Ignore symlinks for now
            if pathtype.is_symlink() {
                return self.next()
            }
 
            // push directory to stack for later traversal an go on to next entry
            if pathtype.is_dir() {
                self.dir_stack.push(OsString::from(path.as_os_str()));
                return self.next()
            };

            let (path_str, hash) = get_file_hash(entry).unwrap();
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