// barcode_js.js — генератор штрих-кодов (EAN/QR) на JavaScript (Node.js)

const bwipjs = require('bwip-js');
const QRCode = require('qrcode');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
let type = 'ean13', data = '', output = 'barcode.png';
let width = 300, height = 150;

for (let i=0; i<args.length; i++) {
    if (args[i] === '--type' && i+1 < args.length) type = args[++i];
    else if (args[i] === '--data' && i+1 < args.length) data = args[++i];
    else if (args[i] === '--output' && i+1 < args.length) output = args[++i];
    else if (args[i] === '--width' && i+1 < args.length) width = parseInt(args[++i]);
    else if (args[i] === '--height' && i+1 < args.length) height = parseInt(args[++i]);
}

if (!data) {
    console.log('Укажите --data');
    process.exit(1);
}

async function generate() {
    if (type === 'qr') {
        await QRCode.toFile(output, data, {
            width: width,
            height: height,
            color: { dark: '#000000', light: '#ffffff' }
        });
        console.log(`✅ QR-код сохранён в ${output}`);
    } else {
        bwipjs.toBuffer({
            bcid: type.toUpperCase(),
            text: data,
            scale: 3,
            height: 10,
            width: 5,
            includetext: true,
            textxalign: 'center',
            backgroundcolor: 'FFFFFF',
            foregroundcolor: '000000'
        }, (err, png) => {
            if (err) {
                console.log('❌ Ошибка:', err);
                return;
            }
            fs.writeFileSync(output, png);
            console.log(`✅ Штрих-код сохранён в ${output}`);
        });
    }
}
generate();
