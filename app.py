import os
import io
from flask import Flask, request, jsonify
from flask_cors import CORS  # ← добавлено
from pdf2image import convert_from_bytes
from PIL import Image
import zxingcpp

app = Flask(__name__)
CORS(app)  # ← разрешает все CORS-запросы

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
        pdf_bytes = file.read()
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