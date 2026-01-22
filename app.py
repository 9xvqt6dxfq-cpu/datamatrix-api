import os
import io
from flask import Flask, request, jsonify
from pdf2image import convert_from_bytes
from PIL import Image
import zxingcpp

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "DataMatrix API is running"})

@app.route('/decode', methods=['POST'])
def decode():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "Only PDF files allowed"}), 400

    try:
        # Читаем PDF как байты
        pdf_bytes = file.read()

        # Конвертируем в изображения (dpi=200 достаточно для DataMatrix)
        images = convert_from_bytes(pdf_bytes, dpi=200)

        codes = []
        for img in images:
            results = zxingcpp.read_barcodes(img)
            for res in results:
                if res.format == zxingcpp.BarcodeFormat.DataMatrix:
                    code = res.text
                    if code not in codes:
                        codes.append(code)

        return jsonify({"codes": codes})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port)