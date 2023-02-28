pub mod lex;
pub use lex::{Token, Lexer};

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

    let conmpressed = compress(&content);
    //println!("{:?}", word_frequenzy);

    Ok(())
}

pub fn decode(args: &Vec<String>) -> Result<(), ()> {

    Ok(())
}

fn compress<'a>(content: &'a String) -> HashMap<String, usize> {
    let mut words = HashMap::new();
    let mut tokens = Lexer::get_tokens_from(content.as_str());

    for i in 0..tokens.len() {
        match &tokens[i]{
            Token::Word(word) => match words.contains_key(word.as_str()) {
                true =>  { *words.get_mut(word).unwrap() += 1; },
                false => { words.insert(word.clone(), 1); },
            },
            Token::Special(ch) => (),
        };
    }

    let mut sorted_by_len: Vec<(&String, usize)> = words.iter().map(|(s,n)| (s,*n)).collect();
    sorted_by_len.sort_by(|a,b| (b.0.len()*b.1).partial_cmp(&(a.0.len() * a.1)).unwrap());
    println!("{:?}", sorted_by_len);

    words
}
