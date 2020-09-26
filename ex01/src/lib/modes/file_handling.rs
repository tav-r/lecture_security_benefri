use std::collections::HashMap;
use std::fs::File;
use std::io::BufReader;
use std::error::Error;
use std::iter::FromIterator;
use std::io::prelude::*;


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
