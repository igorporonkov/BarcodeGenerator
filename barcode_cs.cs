// barcode_cs.cs — генератор штрих-кодов (EAN/QR) на C# (ZXing.Net)

using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using ZXing;
using ZXing.QrCode;
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.PixelFormats;
using SixLabors.ImageSharp.Processing;

class BarcodeGenerator
{
    static void Main(string[] args)
    {
        var parser = new CommandLine.Parser();
        // Упрощённый парсинг
        string type = "", data = "", output = "";
        for (int i=0; i<args.Length; i++) {
            if (args[i] == "--type" && i+1 < args.Length) type = args[++i];
            else if (args[i] == "--data" && i+1 < args.Length) data = args[++i];
            else if (args[i] == "--output" && i+1 < args.Length) output = args[++i];
        }
        if (string.IsNullOrEmpty(type) || string.IsNullOrEmpty(data) || string.IsNullOrEmpty(output)) {
            Console.WriteLine("Использование: barcode_cs --type <type> --data <data> --output <file>");
            return;
        }
        Generate(type, data, output);
    }

    static void Generate(string type, string data, string output)
    {
        var writer = new BarcodeWriterPixelData
        {
            Format = type == "qr" ? BarcodeFormat.QR_CODE : BarcodeFormat.EAN_13,
            Options = new ZXing.Common.EncodingOptions
            {
                Width = 300,
                Height = 150,
                Margin = 10
            }
        };
        if (type == "ean13") writer.Format = BarcodeFormat.EAN_13;
        else if (type == "ean8") writer.Format = BarcodeFormat.EAN_8;
        else if (type == "code128") writer.Format = BarcodeFormat.CODE_128;
        else if (type == "code39") writer.Format = BarcodeFormat.CODE_39;
        else if (type == "qr") writer.Format = BarcodeFormat.QR_CODE;
        else { Console.WriteLine("Неверный тип"); return; }

        var pixelData = writer.Write(data);
        using (var img = SixLabors.ImageSharp.Image.LoadPixelData<Rgba32>(pixelData.Pixels, pixelData.Width, pixelData.Height))
        {
            img.Save(output);
        }
        Console.WriteLine($"✅ Штрих-код сохранён в {output}");
    }
}
