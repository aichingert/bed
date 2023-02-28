// Lib 
// (c) aichingert

pub mod lex;
pub use lex::{Token, Lexer};

use std::fs;
use std::io::Write;
use std::collections::HashMap;

pub struct Replace {
    cur: Vec<u8>,
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
            Err(_e) => panic!("I failed to implement this..."),
        }
    }
}

pub struct File {
    name: String,
    header: String,
    content: String,
}

impl File {
    pub fn new(name: &str) -> Self {
        Self {
            name: name.to_string(),
            header: String::new(),
            content: String::new(),
        }
    }

    pub fn encode(&self, args: &Vec<String>) -> Result<(), ()> {
        let filename = fs::canonicalize(&args[2]).expect(&format!("File: {} not found!", &args[2]));

        let content = match fs::read_to_string(&filename) {
            Ok(con) => con,
            Err(e) => {
                println!("Cannot open file {filename:?} because {:?}", e);
                std::process::exit(1);
            }
        };

        let mut file = File::new(filename.display().to_string().as_str());
        let (words, tokens) = File::filter_words(&content);
        let value_to_token = file.create_header(&words);
        file.create_content(&value_to_token, &tokens);

        let mut compressed_file = std::fs::File::create(&format!("{}.tb",file.name)).unwrap();
        compressed_file.write_all(file.content.as_bytes().try_into().unwrap()).unwrap();

        Ok(())
    }

    pub fn decode(args: &Vec<String>) -> Result<(), ()> {

        Ok(())
    }

    fn create_header(&mut self, words: &HashMap<String, usize>) -> HashMap<String, String> {
        let mut token = Replace::new();
        let mut strs = words.iter().map(|(s,n)| (s.clone(),*n)).collect::<Vec<(String, usize)>>();
        let mut maped = HashMap::new();
        strs.sort_by(|a,b| (b.0.len() * b.1).partial_cmp(&(a.0.len() * a.1)).unwrap());

        for i in 0..strs.len() {
            let mut cur = token.next();

            while words.contains_key(cur) {
                cur = token.next();
                continue; 
            }

            self.header.push_str(&format!("{} {};", strs[i].0, cur));
            maped.insert(strs[i].0.clone(), cur.to_string());
        }

        self.header.pop();
        maped
    }

    fn filter_words(content: &String) -> (HashMap<String, usize>, Vec<Token>) {
        let mut words = HashMap::new();
        let tokens = Lexer::get_tokens_from(content.as_str());

        for i in 0..tokens.len() {
            match &tokens[i] {
                Token::Word(word) => match words.contains_key(word.as_str()) {
                    true =>  { *words.get_mut(word).unwrap() += 1; },
                    false => { words.insert(word.clone(), 1); },
                },
                Token::Special(_ch) => (),
            };
        }

        (words, tokens)
    }

    fn create_content(&mut self, value_to_tokens: &HashMap<String, String>, tokens: &Vec<Token>) {
        self.content.push_str(&format!("{}\n", self.header));

        for i in 0..tokens.len() {
            match &tokens[i] {
                Token::Word(word) => self.content.push_str(value_to_tokens[word].as_str()),
                Token::Special(ch) => self.content.push(*ch),
            }
        }
    }
}
