// barcode_rs.rs — генератор штрих-кодов (EAN/QR) на Rust

use std::env;
use std::fs::File;
use std::io::Write;
use barcode::{Barcode, ean::EAN13, ean::EAN8, code128::Code128, code39::Code39};
use qrcode::QrCode;
use qrcode::types::QrErrorCorrectionLevel;
use image::{ImageBuffer, Luma};

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut typ = "ean13".to_string();
    let mut data = String::new();
    let mut output = "barcode.png".to_string();
    let mut width = 300;
    let mut height = 150;

    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--type" => { i+=1; typ = args[i].clone(); }
            "--data" => { i+=1; data = args[i].clone(); }
            "--output" => { i+=1; output = args[i].clone(); }
            "--width" => { i+=1; width = args[i].parse().unwrap_or(300); }
            "--height" => { i+=1; height = args[i].parse().unwrap_or(150); }
            _ => {}
        }
        i+=1;
    }
    if data.is_empty() {
        println!("Укажите --data");
        return;
    }

    let result = match typ.as_str() {
        "ean13" => generate_ean13(&data, width, height),
        "ean8" => generate_ean8(&data, width, height),
        "qr" => generate_qr(&data, width, height),
        _ => { println!("Неверный тип"); return; }
    };
    match result {
        Ok(img) => {
            let _ = img.save(&output);
            println!("✅ Штрих-код сохранён в {}", output);
        }
        Err(e) => println!("❌ Ошибка: {}", e),
    }
}

fn generate_ean13(data: &str, w: u32, h: u32) -> Result<image::GrayImage, Box<dyn std::error::Error>> {
    let barcode = EAN13::new(data)?;
    let img = barcode.render().resize(w, h, image::imageops::FilterType::Nearest);
    Ok(img)
}

fn generate_ean8(data: &str, w: u32, h: u32) -> Result<image::GrayImage, Box<dyn std::error::Error>> {
    let barcode = EAN8::new(data)?;
    let img = barcode.render().resize(w, h, image::imageops::FilterType::Nearest);
    Ok(img)
}

fn generate_qr(data: &str, w: u32, h: u32) -> Result<image::GrayImage, Box<dyn std::error::Error>> {
    let code = QrCode::with_error_correction_level(data, QrErrorCorrectionLevel::H)?;
    let img = code.render::<Luma<u8>>().build();
    Ok(img.resize(w, h, image::imageops::FilterType::Nearest))
}
