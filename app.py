# app.py
from flask import Flask, request, render_template, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

# Ensure the upload and result directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the image with YOLOv5 model
        # Note: Replace this with the actual function you use to process the image
        result_filepath = process_image(filepath)
        
        return send_from_directory(app.config['RESULT_FOLDER'], os.path.basename(result_filepath))

def process_image(filepath):
    # Call your existing YOLOv5 script here to process the image
    # Example: !python detect.py --source {filepath} --weights path_to_your_weights --save-conf
    # For this example, we're just returning the uploaded file as the result
    result_filepath = os.path.join(app.config['RESULT_FOLDER'], os.path.basename(filepath))
    os.rename(filepath, result_filepath)  # Simulate processing
    return result_filepath

if __name__ == '__main__':
    app.run(debug=True)
