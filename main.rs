// Tomb - file compressing
// (c) aichingert

use std::fs;

fn compress_directory(args: &Vec<String>) -> Result<(), ()> {

    Ok(())
}

fn main() {
    let args = std::env::args().collect::<Vec<String>>();

    if args.len() > 2 {

    }

    let filename = fs::canonicalize(&args[0]).expect(&format!("File: {} not found!", &args[0]));
    

    println!("{:?}", args);
}
