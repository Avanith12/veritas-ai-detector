import os
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify, render_template, send_from_directory
from PIL import Image

# V2 Refactor: Import Brain
try:
    from model_handler import load_model_safe, predict_image
except ImportError:
    # Handle possible path issues
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from model_handler import load_model_safe, predict_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load Brain on Startup
load_model_safe()

@app.route('/')
def home():
    # List example images dynamically
    examples_dir = os.path.join(os.getcwd(), 'test_examples')
    examples = []
    if os.path.exists(examples_dir):
        examples = os.listdir(examples_dir)
    return render_template('index.html', examples=examples)

@app.route('/test_examples/<filename>')
def serve_example(filename):
    return send_from_directory('test_examples', filename)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Get Prediction from Brain
        result = predict_image(filepath)
        
        if 'error' in result:
             return jsonify({'error': result['error']})
        
        # Save Debug Image (Neural View)
        # We process the debug image here to keep UI logic separate from core AI logic
        # 'processed_array' is uint8 [0-255] (32, 32, 3)
        if 'processed_array' in result:
             debug_img = Image.fromarray(result['processed_array'].astype('uint8'))
             debug_path = os.path.join(app.config['UPLOAD_FOLDER'], 'debug.png')
             debug_img.save(debug_path)
        
        return jsonify({
            'label': result['label'],
            'confidence': f"{result['confidence']:.2f}",
            'image_url': filepath,
            'neural_view': f"/{app.config['UPLOAD_FOLDER']}/debug.png?t={np.random.random()}" 
        })

if __name__ == '__main__':
    app.run(debug=True)
