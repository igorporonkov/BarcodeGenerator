// barcode_go.go — генератор штрих-кодов (EAN/QR) на Go

package main

import (
	"flag"
	"fmt"
	"image/png"
	"os"
	"strconv"
	"github.com/boombuler/barcode"
	"github.com/boombuler/barcode/ean"
	"github.com/boombuler/barcode/qr"
)

func main() {
	typ := flag.String("type", "ean13", "Тип (ean13, ean8, code128, code39, qr)")
	data := flag.String("data", "", "Данные")
	output := flag.String("output", "barcode.png", "Выходной файл")
	width := flag.Int("width", 300, "Ширина")
	height := flag.Int("height", 150, "Высота")
	flag.Parse()

	if *data == "" {
		fmt.Println("Укажите --data")
		return
	}

	var code barcode.Barcode
	var err error
	switch *typ {
	case "ean13":
		code, err = ean.Encode(*data)
	case "ean8":
		code, err = ean.Encode8(*data)
	case "qr":
		code, err = qr.Encode(*data, qr.H, qr.Auto)
	default:
		fmt.Println("Неверный тип")
		return
	}
	if err != nil {
		fmt.Println("Ошибка:", err)
		return
	}
	// Масштабирование
	code, err = barcode.Scale(code, *width, *height)
	if err != nil {
		fmt.Println("Ошибка масштабирования:", err)
		return
	}
	file, err := os.Create(*output)
	if err != nil {
		fmt.Println("Ошибка создания файла:", err)
		return
	}
	defer file.Close()
	err = png.Encode(file, code)
	if err != nil {
		fmt.Println("Ошибка сохранения:", err)
		return
	}
	fmt.Printf("✅ Штрих-код сохранён в %s\n", *output)
}
