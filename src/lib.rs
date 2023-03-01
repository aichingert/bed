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

    pub fn encode(&mut self) -> Result<(), ()> {
        let content = match fs::read_to_string(&self.name) {
            Ok(con) => con,
            Err(e) => {
                println!("Cannot open file {} because {:?}",self.name, e);
                std::process::exit(1);
            }
        };

        let (words, tokens) = File::filter_words(&content);
        let value_to_token = self.create_header(&words);
        self.create_content(&value_to_token, &tokens);

        let mut compressed_file = std::fs::File::create(&format!("{}.tb",self.name)).unwrap();
        compressed_file.write_all(self.content.as_bytes().try_into().unwrap()).unwrap();

        Ok(())
    }

    pub fn decode(&mut self) -> Result<(), ()> {
        let (mapings, content) = self.read_header();
        self.reproduce_content(&content,&mapings);
        self.name = self.name[..self.name.len()-3].to_string();

        let mut decoded = std::fs::File::create(&format!("{}",self.name)).unwrap();
        decoded.write_all(self.content.as_bytes().try_into().unwrap()).unwrap();

        Ok(())
    }

    fn read_header(&self) -> (HashMap<String, String>, String) {
        let mut mapings = HashMap::new();
        let content = fs::read_to_string(&self.name).unwrap();

        let (head, rest) = content.split_once("\n").unwrap();

        for token in head.split(';') {
            let (value, map) = token.split_once(' ').unwrap();
            mapings.insert(map.to_string(), value.to_string());
        }

        (mapings, rest.to_string())
    }

    fn reproduce_content(&mut self, content: &String, mapings: &HashMap<String, String>) {
        let tokens = Lexer::get_tokens_from(content);

        for i in 0..tokens.len() {
            match &tokens[i] {
                Token::Word(tok) => self.content.push_str(&mapings[tok]),
                Token::Special(ch) => self.content.push(*ch),
            }
        }
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
