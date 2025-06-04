from flask import Flask, request, jsonify, send_from_directory, render_template
import os
from pathlib import Path
from waitress import serve
from ultralytics import YOLO
import uuid
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Путь к лучшей модели (S:\code\vscode\Skillbox_Python_NeuralVision\PythonForInginiers\Module3\M3_hw7\MyCatDetection\models) 
model_path = Path(r"S:\code\vscode\Skillbox_Python_NeuralVision\PythonForInginiers\Module3\M3_hw7\MyCatDetection\models\best.pt")

UPLOAD_FOLDER = r"S:\code\vscode\Skillbox_Python_NeuralVision\PythonForInginiers\Module3\M3_hw7\MyCatDetection\uploads"
RESULT_FOLDER = r"S:\code\vscode\Skillbox_Python_NeuralVision\PythonForInginiers\Module3\M3_hw7\MyCatDetection\results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Загрузка модели YOLOv8
model = YOLO(model_path)

UPLOAD_FOLDER = '/results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html', result_filename=None)

@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return 'No file part', 400
    file = request.files['image']
    if file.filename == '':
        return 'No selected file', 400

    filename = f"{uuid.uuid4().hex}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    image = Image.open(file.stream)
    results = model(image)
    result_image = results[0].plot()
    result_image = Image.fromarray(result_image)
    result_image.save(filepath)

    return render_template('index.html', result_filename=filename)

@app.route('/static/results/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    from waitress import serve
    print("Сервер запущен на http://localhost:8000")
    serve(app, host='0.0.0.0', port=8000)