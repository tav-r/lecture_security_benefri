use std::collections::{HashMap,HashSet};
use std::fs::File;
use std::io::{BufReader,prelude::*};
use std::error::Error;
use std::iter::FromIterator;


pub fn parse_exception_file(exceptions_file_path: &str) -> Result<HashSet<String>, Box<dyn Error>> {
    Ok(BufReader::new(File::open(exceptions_file_path)?).lines().map(|r| r.unwrap()).collect())
}

// Parse a json file of the form
// `[{path: "PATH1", hash: "HASH_VALUE1"}, {path: "PATH2", hash: "HASH_VALUE2"}...]`
// and return a HashMap: "PATHn" -> "HASHn"
// 
// # Arguments
// * `hash_file_path` - a string describing an absolute or a relative path to a hash file of the form
//                      described above
pub fn parse_json_file(hash_file_path: &str) -> Result<HashMap<String, String>, Box<dyn Error>> {
    let reader = BufReader::new(File::open(hash_file_path)?);
    let parsed: Vec<serde_json::Value> = serde_json::from_reader(reader)?;

    // parse json file into path->hash HashMap
    let mapping :HashMap<String, String> = HashMap::from_iter(parsed.iter().map(|member| {
        if let serde_json::Value::Object(obj) = member {
            (obj["path"].as_str().unwrap().to_owned(), obj["hash"].as_str().unwrap().to_owned())
        } else {
            panic!()
        }
    }));

    Ok(mapping)
}

// Write a json file of the form
// `[{path: "PATH1", hash: "HASH_VALUE1"}, {path: "PATH2", hash: "HASH_VALUE2"}...]`
// from a Vec of the form: [("PATH1", "HASH1"), ("PATH2", "HASH2"), ...]
// 
// # Arguments
// * `out_file` - a string describing an absolute or a relative path to the hash file to write to 
// * `contents` - a vector containning the paths and the hashes in the form described above
pub fn save_contents(out_file: &str, contents: Vec<(String, String)>) -> Result<(), Box<dyn Error>> {
    let json_vec: serde_json::Value = contents.iter().map(|(key, val)| {
        serde_json::json!({
            "path": key,
            "hash": val
        })
    }).collect();

    let mut out_file = File::create(out_file)?;
    out_file.write_all(serde_json::ser::to_string(&json_vec).unwrap().as_bytes())?;

    Ok(())
}
