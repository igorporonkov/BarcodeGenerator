// barcode_java.java — генератор штрих-кодов (EAN/QR) на Java (Barcode4J)

import org.krysalis.barcode4j.impl.code128.Code128Bean;
import org.krysalis.barcode4j.impl.ean.EAN13Bean;
import org.krysalis.barcode4j.impl.ean.EAN8Bean;
import org.krysalis.barcode4j.impl.code39.Code39Bean;
import org.krysalis.barcode4j.impl.qr.QRCodeBean;
import org.krysalis.barcode4j.output.bitmap.BitmapCanvasProvider;
import org.krysalis.barcode4j.output.svg.SVGCanvasProvider;
import org.krysalis.barcode4j.tools.UnitConv;

import java.awt.image.BufferedImage;
import java.io.*;
import java.nio.file.*;

public class BarcodeGenerator {
    public static void main(String[] args) throws Exception {
        if (args.length < 4) {
            System.out.println("Использование: java BarcodeGenerator --type <type> --data <data> --output <file>");
            return;
        }
        String type = "", data = "", output = "";
        for (int i = 0; i < args.length; i++) {
            if (args[i].equals("--type") && i+1 < args.length) type = args[++i];
            else if (args[i].equals("--data") && i+1 < args.length) data = args[++i];
            else if (args[i].equals("--output") && i+1 < args.length) output = args[++i];
        }
        if (type.isEmpty() || data.isEmpty() || output.isEmpty()) {
            System.out.println("Не все параметры указаны.");
            return;
        }
        // Генерация
        if (type.equals("ean13")) {
            EAN13Bean bean = new EAN13Bean();
            bean.setHeight(2.0);
            bean.setModuleWidth(UnitConv.in2mm(0.33));
            generate(bean, data, output);
        } else if (type.equals("ean8")) {
            EAN8Bean bean = new EAN8Bean();
            bean.setHeight(2.0);
            generate(bean, data, output);
        } else if (type.equals("code128")) {
            Code128Bean bean = new Code128Bean();
            bean.setHeight(2.0);
            generate(bean, data, output);
        } else if (type.equals("code39")) {
            Code39Bean bean = new Code39Bean();
            bean.setHeight(2.0);
            generate(bean, data, output);
        } else if (type.equals("qr")) {
            QRCodeBean bean = new QRCodeBean();
            bean.setHeight(2.0);
            generate(bean, data, output);
        } else {
            System.out.println("Неверный тип");
        }
    }

    private static void generate(Object bean, String data, String output) throws Exception {
        OutputStream out = new FileOutputStream(output);
        try {
            if (output.endsWith(".svg")) {
                SVGCanvasProvider provider = new SVGCanvasProvider(false, 0);
                if (bean instanceof EAN13Bean) ((EAN13Bean)bean).generateBarcode(provider, data);
                else if (bean instanceof EAN8Bean) ((EAN8Bean)bean).generateBarcode(provider, data);
                else if (bean instanceof Code128Bean) ((Code128Bean)bean).generateBarcode(provider, data);
                else if (bean instanceof Code39Bean) ((Code39Bean)bean).generateBarcode(provider, data);
                else if (bean instanceof QRCodeBean) ((QRCodeBean)bean).generateBarcode(provider, data);
                String svg = provider.getDOM().getDocumentElement().toString();
                out.write(svg.getBytes());
            } else {
                BitmapCanvasProvider provider = new BitmapCanvasProvider(out, "image/png", 300, BufferedImage.TYPE_BYTE_GRAY, true, 0);
                if (bean instanceof EAN13Bean) ((EAN13Bean)bean).generateBarcode(provider, data);
                else if (bean instanceof EAN8Bean) ((EAN8Bean)bean).generateBarcode(provider, data);
                else if (bean instanceof Code128Bean) ((Code128Bean)bean).generateBarcode(provider, data);
                else if (bean instanceof Code39Bean) ((Code39Bean)bean).generateBarcode(provider, data);
                else if (bean instanceof QRCodeBean) ((QRCodeBean)bean).generateBarcode(provider, data);
                provider.finish();
            }
        } finally {
            out.close();
        }
        System.out.println("✅ Штрих-код сохранён в " + output);
    }
}
