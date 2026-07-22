📦 BarcodeGenerator — генератор штрих-кодов (EAN/QR)
Универсальный генератор штрих-кодов с поддержкой EAN-13, EAN-8, QR-кодов и множества других форматов.
Позволяет создавать штрих-коды в PNG, SVG, с настройкой размера, цвета, текста и пакетной генерацией из CSV.
Реализован на 7 языках программирования для демонстрации алгоритмов кодирования и работы с графикой.

https://img.shields.io/github/repo-size/yourname/barcodegenerator
https://img.shields.io/github/stars/yourname/barcodegenerator?style=social
https://img.shields.io/badge/License-MIT-blue.svg

🧠 Концепция
BarcodeGenerator — это инструмент для создания профессиональных штрих-кодов. Он позволяет:

✅ Генерировать EAN-13 и EAN-8 (стандарт для товаров) с проверкой контрольной суммы.

✅ Создавать QR-коды из любого текста или URL.

✅ Экспортировать в PNG и SVG (векторный формат для масштабирования).

✅ Настраивать размер (ширина, высота, масштаб).

✅ Изменять цвета (передний и задний план).

✅ Добавлять текст под кодом (опционально).

✅ Пакетная генерация из CSV-файла.

✅ Простой интерфейс — всё через командную строку или интерактивный режим.

🚀 Как запустить
Каждая версия использует соответствующие библиотеки. Инструкции по установке и запуску:

Python
bash
pip install python-barcode qrcode[pil] pillow
python barcode_python.py --type ean13 --data 5901234123457 --output code.png
python barcode_python.py --type qr --data "https://github.com" --output qr.png
C++
bash
# Требуется Zint (sudo apt install libzint-dev)
g++ -std=c++17 barcode_cpp.cpp -o barcode -lzint
./barcode --type ean13 --data 5901234123457 --output code.png
Java
bash
# Требуется Barcode4J (скачать barcode4j.jar)
javac -cp .:barcode4j.jar barcode_java.java
java -cp .:barcode4j.jar barcode_java --type ean13 --data 5901234123457 --output code.png
C# (.NET Core)
bash
dotnet add package ZXing.Net
dotnet add package SixLabors.ImageSharp
dotnet run -- --type ean13 --data 5901234123457 --output code.png
Go
bash
go get github.com/boombuler/barcode
go get github.com/skip2/go-qrcode
go run barcode_go.go --type ean13 --data 5901234123457 --output code.png
Rust
bash
cargo add barcode
cargo add qrcode
cargo add image
cargo run -- --type ean13 --data 5901234123457 --output code.png
JavaScript (Node.js)
bash
npm install bwip-js qrcode canvas
node barcode_js.js --type ean13 --data 5901234123457 --output code.png
🧩 Пример использования
bash
# Генерация EAN-13
$ python barcode_python.py --type ean13 --data 5901234123457 --output ean.png
✅ Штрих-код сохранён в ean.png (текст: 5901234123457)

# Генерация QR-кода
$ python barcode_python.py --type qr --data "https://github.com" --output qr.png
✅ QR-код сохранён в qr.png

# Пакетная генерация из CSV
$ python barcode_python.py --batch codes.csv --output-dir ./barcodes
✅ Сгенерировано 50 штрих-кодов в ./barcodes
📦 Содержимое репозитория
Файл	Язык	Особенности
barcode_python.py	Python	python-barcode + qrcode, пакетная обработка, цвет
barcode_cpp.cpp	C++	Zint, поддержка всех форматов, высокое качество
barcode_java.java	Java	Barcode4J, генерация PNG/SVG, настройка размера
barcode_cs.cs	C#	ZXing.Net, поддержка EAN/QR, ImageSharp для экспорта
barcode_go.go	Go	boombuler/barcode + qrcode, быстрая генерация
barcode_rs.rs	Rust	barcode + qrcode, цветной вывод, прогресс-бар
barcode_js.js	JavaScript	bwip-js + qrcode, веб-интерфейс (опционально)
🔮 Расширенные функции
Поддержка всех основных форматов: EAN-13, EAN-8, UPC-A, Code128, Code39, QR-код.

Векторный SVG для печати высокого качества.

Пакетная генерация из CSV с прогресс-баром.

Интерактивный режим (в консольных версиях).

📜 Лицензия
MIT — свободно используйте, модифицируйте и распространяйте.

🤝 Вклад
Приветствуются пул-реквесты с улучшениями, поддержкой новых форматов и расширением функциональности.

⭐ Если проект помогает вам генерировать штрих-коды — поставьте звёздочку!
