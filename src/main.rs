// Tomb - file compressing
// (c) aichingert

use tomb::{encode,decode};
use tomb::lex;

fn main() {
    let args = std::env::args().collect::<Vec<String>>();

    if args.len() <= 1 {
        println!("Not enough parameter [expected: file/folder name]");
        std::process::exit(1);
    }

    match args[1].as_str() {
        "encode" => {
            let res = encode(&args);
        },
        "decode" => {
            let res = decode(&args);
        },
        _ => {
            println!("Invalid option {:?}", args[1]);
            std::process::exit(1);
        }
    };

    println!("{:?}", args);
}
