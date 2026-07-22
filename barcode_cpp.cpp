// barcode_cpp.cpp — генератор штрих-кодов (EAN/QR) на C++ (Zint)

#include <iostream>
#include <string>
#include <vector>
#include <cstring>
#include <zint.h>
#include <zint/backend_gtk.h> // для PNG
#include <fstream>
#include <filesystem>

using namespace std;

class BarcodeGenerator {
private:
    string type;
    string data;
    string output;
    int width, height;
    string fg, bg;

public:
    BarcodeGenerator(const string& type, const string& data, const string& output,
                     int width=300, int height=150, const string& fg="black", const string& bg="white")
        : type(type), data(data), output(output), width(width), height(height), fg(fg), bg(bg) {}

    bool generate() {
        struct zint_symbol *symbol = ZBarcode_Create();
        if (!symbol) return false;

        // Настройка
        symbol->output_options = BARCODE_STDOUT;
        symbol->scale = 2;
        symbol->height = 80;
        symbol->whitespace_width = 10;
        // Цвета
        strcpy(symbol->fgcolour, fg.c_str());
        strcpy(symbol->bgcolour, bg.c_str());

        // Тип
        int symbology;
        if (type == "ean13") symbology = BARCODE_EANX;
        else if (type == "ean8") symbology = BARCODE_EANX;
        else if (type == "code128") symbology = BARCODE_CODE128;
        else if (type == "code39") symbology = BARCODE_CODE39;
        else if (type == "qr") symbology = BARCODE_QRCODE;
        else return false;

        // Кодирование
        int ret = ZBarcode_Encode(symbol, (unsigned char*)data.c_str(), data.length());
        if (ret < 0) {
            ZBarcode_Delete(symbol);
            return false;
        }

        // Экспорт в PNG (требуется GTK)
        string ext = output.find(".png") != string::npos ? "" : ".png";
        string full_output = output + ext;
        ret = ZBarcode_Print(symbol, (char*)full_output.c_str(), 0);
        ZBarcode_Delete(symbol);
        return ret == 0;
    }
};

int main(int argc, char* argv[]) {
    if (argc < 5) {
        cout << "Использование: barcode_cpp --type <type> --data <data> --output <file> [--width W] [--height H]" << endl;
        return 1;
    }
    string type, data, output;
    int width = 300, height = 150;
    for (int i = 1; i < argc; i++) {
        string arg = argv[i];
        if (arg == "--type" && i+1 < argc) type = argv[++i];
        else if (arg == "--data" && i+1 < argc) data = argv[++i];
        else if (arg == "--output" && i+1 < argc) output = argv[++i];
        else if (arg == "--width" && i+1 < argc) width = stoi(argv[++i]);
        else if (arg == "--height" && i+1 < argc) height = stoi(argv[++i]);
    }
    BarcodeGenerator gen(type, data, output, width, height);
    if (gen.generate()) {
        cout << "✅ Штрих-код сохранён в " << output << endl;
    } else {
        cout << "❌ Ошибка генерации" << endl;
    }
    return 0;
}
