from flask import Flask, request, render_template, jsonify, send_file
from waitress import serve
from ultralytics import YOLO
import cv2
import os
import shutil
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

# Путь к лучшей модели (локальный путь на Windows)
MODEL_PATH = "S:\code\vscode\Skillbox_Python_NeuralVision\PythonForInginiers\Module3\M3_hw7\MyCatDetection\models\best.pt"
model = YOLO(MODEL_PATH)

# Папки для загрузки и результатов
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

# Уровень уверенности для детекции
CONFIDENCE_THRESHOLD = 0.75

# Главная страница
@app.route('/')
def index():
    # Очистка папок uploads и results при загрузке страницы
    for folder in [UPLOAD_FOLDER, RESULT_FOLDER]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder, exist_ok=True)
    return render_template('index.html')

# Обработка загрузки изображения и детекции (JSON-ответ для фронтенда)
@app.route('/detect', methods=['POST'])
def detect_objects():
    try:
        if 'image_file' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        file = request.files['image_file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Сохранение загруженного файла
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Выполнение детекции
        results = model.predict(source=file_path, conf=CONFIDENCE_THRESHOLD, save=False)

        # Форматирование результатов в bounding box'ы
        boxes = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = box.conf[0].item()
                class_id = int(box.cls[0].item()) if box.cls.numel() > 0 else 0
                boxes.append([x1, y1, x2, y2, confidence, class_id])

        # Рисование bounding box'ов на изображении для скачивания
        img = cv2.imread(file_path)
        for box in boxes:
            x1, y1, x2, y2, confidence, class_id = box
            label = f"Cat: {confidence:.2f}"
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Сохранение результата
        result_path = os.path.join(app.config['RESULT_FOLDER'], f"result_{file.filename}")
        cv2.imwrite(result_path, img)

        return jsonify(boxes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Возвращение обработанного изображения
@app.route('/get_result/<filename>')
def get_result(filename):
    result_path = os.path.join(app.config['RESULT_FOLDER'], f"result_{filename}")
    if os.path.exists(result_path):
        return send_file(result_path, mimetype='image/jpeg')
    return "Результат не найден", 404

if __name__ == '__main__':
    print("Запуск сервера на порту 8000...")
    serve(app, host='127.0.0.1', port=8000)