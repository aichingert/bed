// Tomb - file compressing
// (c) aichingert

use tomb::File;
use std::path::Path;

fn is_file(args: &Vec<String>) {
    let filename = std::fs::canonicalize(&args[2]).expect(&format!("File: {} not found!", &args[2]));
    let mut file: File = tomb::File::new(&filename.display().to_string());

    match args[1].as_str() {
        "encode" => {
            let _res = file.encode();
        },
        "decode" => {
            let _res = file.decode();
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
