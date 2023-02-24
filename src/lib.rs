use std::fs;
use std::collections::HashMap;

pub fn encode(args: &Vec<String>) -> Result<(), ()> {
    let filename = fs::canonicalize(&args[2]).expect(&format!("File: {} not found!", &args[2]));

    let content = match fs::read_to_string(&filename) {
        Ok(con) => con,
        Err(e) => {
            println!("Cannot open file {filename:?} because {:?}", e);
            std::process::exit(1);
        }
    };

    let word_frequenzy = frequenzy(&content);
    println!("{:?}", word_frequenzy);

    Ok(())
}

pub fn decode(args: &Vec<String>) -> Result<(), ()> {

    Ok(())
}

fn frequenzy<'a>(content: &'a String) -> HashMap<&'a str, u32> {
    let mut words = HashMap::new();

    for line in content.lines() {
        for word in line.split(' ') {
            println!("{:?}", word);

            if words.contains_key(word) {
                *words.get_mut(word).unwrap() += 1;
            } else {
                words.insert(word, 1);
            }
        }
    }

    words
}
