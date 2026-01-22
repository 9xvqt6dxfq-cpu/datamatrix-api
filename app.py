import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/decode', methods=['POST'])
def decode():
    return jsonify({"error": "No file provided"}), 400

# Добавляем корневой маршрут для проверки
@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "OK"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))