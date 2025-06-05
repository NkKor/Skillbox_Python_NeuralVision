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

# Путь к лучшей модели (S:\code\vscode\Skillbox_Python_NeuralVision\PythonForInginiers\Module3\M3_hw7\CatVideoDetection\models) 
model_path = Path(r"S:\code\vscode\Skillbox_Python_NeuralVision\PythonForInginiers\Module3\M3_hw7\MyCatDetection\models\best.pt")

UPLOAD_FOLDER = r"S:\code\vscode\Skillbox_Python_NeuralVision\PythonForInginiers\Module3\M3_hw7\CatVideoDetection\uploads"
RESULT_FOLDER = r"S:\code\vscode\Skillbox_Python_NeuralVision\PythonForInginiers\Module3\M3_hw7\CatVideoDetection\results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Загрузка модели YOLOv8
model = YOLO(model_path)

UPLOAD_FOLDER = '/results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/detect", methods=["POST"])
def detect():
    if "video" not in request.files:
        return "No file part"

    file = request.files["video"]
    if file.filename == "":
        return "No selected file"

    input_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4().hex}_input.mp4")
    output_path = input_path.replace("_input.mp4", "_output.mp4")
    file.save(input_path)

    process_video(input_path, output_path)

    filename = os.path.basename(output_path)
    return render_template("index.html", video_result=filename)

def process_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)[0]
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls = int(box.cls[0])
            label = model.names[cls]
            if "cat" in label.lower():
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        out.write(frame)

    cap.release()
    out.release()

@app.route("/videos/<path:filename>")
def video(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    from waitress import serve
    print("Сервер запущен на http://localhost:8000")
    serve(app, host="0.0.0.0", port=8000)