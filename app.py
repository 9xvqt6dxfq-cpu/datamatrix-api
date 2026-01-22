import os
import tempfile
from flask import Flask, request, jsonify
import fitz  # PyMuPDF
from PIL import Image
import zxingcpp
import io

app = Flask(__name__)

@app.route('/decode-datamatrix', methods=['POST'])
def decode_datamatrix():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "Only PDF allowed"}), 400

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_path = os.path.join(tmpdir, "input.pdf")
            file.save(pdf_path)

            pdf_document = fitz.open(pdf_path)
            codes = []

            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                mat = fitz.Matrix(3.0, 3.0)  # ~216 DPI
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))

                results = zxingcpp.read_barcodes(img)
                for res in results:
                    if res.format == zxingcpp.BarcodeFormat.DataMatrix:
                        code = res.text
                        if code not in codes:
                            codes.append(code)

            pdf_document.close()
            return jsonify({"codes": codes})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))