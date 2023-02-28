// Tomb - file compressing
// (c) aichingert

use tomb::{File,Replace};
use std::path::Path;

fn is_file(args: &Vec<String>) {
    let file: tomb::File = tomb::File::new(args[1].as_str());

    match args[1].as_str() {
        "encode" => {
            let res = file.encode(&args);
        },
        "decode" => {
        },
        _ => {
            println!("Invalid option {:?}", args[1]);
            std::process::exit(1);
        }
    };


}

fn main() {
    let args = std::env::args().collect::<Vec<String>>();

    if args.len() <= 1 {
        println!("Not enough parameter [expected: file/folder name]");
        std::process::exit(1);
    }

    let path = Path::new(args[1].as_str());
    
    match path.is_dir() {
        true => (),
        false => is_file(&args),
    };

    println!("{:?}", args);
}
