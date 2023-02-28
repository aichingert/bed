// lexer
//

#[derive(Debug)]
pub enum Token {
    Word(String),
    Special(char),
}

#[derive(Debug)]
pub struct Lexer<'a> {
    chars: std::iter::Peekable<std::str::Chars<'a>>,
    pub tokens: Vec<Token>
}

impl<'a> Lexer<'a> {
    pub fn new(source: &'a str) -> Self {
        Lexer {
            chars: source.chars().peekable(),
            tokens: Vec::new()
        }
    }

    pub fn get_tokens_from(source: &'a str) -> Vec<Token> {
        let mut lexer = Lexer::new(source);
        lexer.lex();
        lexer.tokens
    }

    fn peek(&mut self) -> Option<&char> {
        self.chars.peek()
    }

    fn next(&mut self) -> Option<char> {
        self.chars.next()
    }

    pub fn lex(&mut self) {
        while let Some(ch) = self.next() {
            match ch.is_alphanumeric() {
                true => {
                    let mut word = String::from(ch); 

                    while self.peek().is_some() && self.peek().unwrap().is_alphanumeric() {
                        word.push(self.next().unwrap());
                    }

                    self.tokens.push(Token::Word(word));
                },
                false => self.tokens.push(Token::Special(ch)),
            }
        }
    }
}
