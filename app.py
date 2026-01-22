import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Корневой маршрут — для проверки
@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "DataMatrix API is running"})

# Основной маршрут — для распознавания
@app.route('/decode', methods=['POST'])
def decode():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    return jsonify({"error": "File received but not processed yet"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port)