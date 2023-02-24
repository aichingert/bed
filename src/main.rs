// Tomb - file compressing
// (c) aichingert

use std::fs;

fn encode(args: &Vec<String>) -> Result<(), ()> {
    let filename = fs::canonicalize(&args[0]).expect(&format!("File: {} not found!", &args[0]));


    Ok(())
}

fn decode(args: &Vec<String>) -> Result<(), ()> {

    Ok(())
}

fn main() {
    let args = std::env::args().collect::<Vec<String>>();

    match args[1].as_str() {
        "encode" => {
            let res = encode(&args);
        },
        "decode" => {
            let res = decode(&args);
        },
        _ => panic!("Invalid option {:?}", args[1]),
    };

    println!("{:?}", args);
}
