// Lib 
// (c) aichingert

pub mod lex;
pub use lex::{Token, Lexer};

use std::fs;
use std::collections::HashMap;

pub struct File {
    header: HashMap<String, String>,
    
}

pub struct Replace {
    pub cur: Vec<u8>,
}

impl Replace {
    pub fn new() -> Self {
        Self { cur: vec![47] }
    }

    pub fn next(&mut self) -> &str {
        for i in (0..self.cur.len()).rev() {
            match self.cur[i] {
                57 => self.cur[i] = 65,
                90 => self.cur[i] = 97,
                122 => {
                    if i == 0 {
                        self.cur[i] = 48;
                        self.cur.insert(0, 48);
                    } else {
                        self.cur[i] = 48;
                        continue;
                    }
                },
                _ => self.cur[i] += 1,
            }

            break
        }

        match std::str::from_utf8(&self.cur) {
            Ok(s) => s,
            Err(e) => panic!("I failed to implement this..."),
        }
    }
}

impl File {
    pub fn encode(&self, args: &Vec<String>) -> Result<(), ()> {
        let filename = fs::canonicalize(&args[2]).expect(&format!("File: {} not found!", &args[2]));

        let content = match fs::read_to_string(&filename) {
            Ok(con) => con,
            Err(e) => {
                println!("Cannot open file {filename:?} because {:?}", e);
                std::process::exit(1);
            }
        };

        let conmpressed = File::compress(&content);
        //println!("{:?}", word_frequenzy);

        Ok(())
    }

    pub fn decode(args: &Vec<String>) -> Result<(), ()> {

        Ok(())
    }

    fn create_header(&mut self, words: &mut Vec<(String, usize)>) {
        words.sort_by(|a,b| (b.0.len()*b.1).partial_cmp(&(a.0.len() * a.1)).unwrap());

        for _i in 0..words.len() {
            //self.header.insert
        }
    }

    fn compress(content: &String) -> Vec<(String, usize)> {
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

        words.iter().map(|(s,n)| (s.clone(),*n)).collect::<Vec<(String, usize)>>()
    }
}
