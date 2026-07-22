# barcode_python.py — генератор штрих-кодов (EAN/QR) на Python

import argparse
import os
import sys
from barcode import EAN13, EAN8, Code128, Code39
from barcode.writer import ImageWriter, SVGWriter
import qrcode
from PIL import Image
import csv
import time

class BarcodeGenerator:
    def __init__(self, barcode_type, data, output, format='png', 
                 width=300, height=150, fg='black', bg='white', text=True):
        self.barcode_type = barcode_type
        self.data = data
        self.output = output
        self.format = format  # png или svg
        self.width = width
        self.height = height
        self.fg = fg
        self.bg = bg
        self.text = text

    def generate(self):
        if self.barcode_type in ['ean13', 'ean8', 'code128', 'code39']:
            return self._generate_linear()
        elif self.barcode_type == 'qr':
            return self._generate_qr()
        else:
            raise ValueError(f"Неподдерживаемый тип: {self.barcode_type}")

    def _generate_linear(self):
        # Выбор класса
        classes = {
            'ean13': EAN13,
            'ean8': EAN8,
            'code128': Code128,
            'code39': Code39
        }
        cls = classes[self.barcode_type]
        # Настройка писателя
        if self.format == 'svg':
            writer = SVGWriter()
            ext = '.svg'
        else:
            writer = ImageWriter()
            ext = '.png'
        # Генерация
        try:
            barcode = cls(self.data, writer=writer)
            # Настройки
            options = {
                'module_width': 0.2 if self.format == 'svg' else 0.3,
                'module_height': 15.0,
                'font_size': 10,
                'text_distance': 5.0,
                'background': self.bg,
                'foreground': self.fg,
                'write_text': self.text
            }
            # Сохранение
            filename = self.output if self.output.endswith(ext) else self.output + ext
            barcode.save(filename, options=options)
            return filename
        except Exception as e:
            raise RuntimeError(f"Ошибка генерации: {e}")

    def _generate_qr(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(self.data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=self.fg, back_color=self.bg)
        # Изменение размера
        if self.width and self.height:
            img = img.resize((self.width, self.height), Image.Resampling.LANCZOS)
        ext = '.png'
        filename = self.output if self.output.endswith(ext) else self.output + ext
        img.save(filename)
        return filename

def batch_generate(csv_file, output_dir, barcode_type, format='png', **kwargs):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        total = 0
        for row in reader:
            if not row:
                continue
            data = row[0].strip()
            if not data:
                continue
            output = os.path.join(output_dir, f"{data}.{format}")
            generator = BarcodeGenerator(barcode_type, data, output, format, **kwargs)
            try:
                generator.generate()
                total += 1
                sys.stdout.write(f"\rОбработано: {total}")
                sys.stdout.flush()
            except Exception as e:
                print(f"\nОшибка для {data}: {e}")
        print(f"\n✅ Сгенерировано {total} штрих-кодов в {output_dir}")

def main():
    parser = argparse.ArgumentParser(description="Генератор штрих-кодов")
    parser.add_argument('--type', required=True, 
                       choices=['ean13', 'ean8', 'code128', 'code39', 'qr'],
                       help="Тип штрих-кода")
    parser.add_argument('--data', help="Данные для кодирования")
    parser.add_argument('--output', help="Выходной файл (без расширения)")
    parser.add_argument('--format', default='png', choices=['png', 'svg'],
                       help="Формат (png или svg)")
    parser.add_argument('--width', type=int, default=300, help="Ширина (для QR)")
    parser.add_argument('--height', type=int, default=150, help="Высота (для QR)")
    parser.add_argument('--fg', default='black', help="Цвет переднего плана")
    parser.add_argument('--bg', default='white', help="Цвет заднего плана")
    parser.add_argument('--no-text', action='store_true', help="Убрать текст под кодом")
    parser.add_argument('--batch', help="CSV-файл для пакетной генерации")
    parser.add_argument('--output-dir', help="Папка для пакетной генерации")
    args = parser.parse_args()

    if args.batch:
        if not args.output_dir:
            print("Для пакетной генерации укажите --output-dir")
            sys.exit(1)
        batch_generate(args.batch, args.output_dir, args.type, args.format,
                      width=args.width, height=args.height,
                      fg=args.fg, bg=args.bg, text=not args.no_text)
        return

    if not args.data or not args.output:
        print("Укажите --data и --output")
        sys.exit(1)

    generator = BarcodeGenerator(args.type, args.data, args.output, args.format,
                                 args.width, args.height, args.fg, args.bg,
                                 not args.no_text)
    try:
        filename = generator.generate()
        print(f"✅ Штрих-код сохранён в {filename}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
