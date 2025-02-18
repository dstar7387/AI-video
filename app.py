
from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import os
from generate import generatex
import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER_img'] = 'myimg'
app.config['UPLOAD_FOLDER_speech'] = 'myspeech'
app.config['UPLOAD_FOLDER_background'] = 'mybackground'

@app.route('/images')
def get_images():
    images = os.listdir(app.config['UPLOAD_FOLDER_img'])
    return jsonify(images)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    files = request.files.getlist('file')
    uploaded_files = []
    
    for file in files:
        if file.filename == '':
            continue

        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{timestamp}_{secure_filename(file.filename)}"
        
        file.save(os.path.join(app.config['UPLOAD_FOLDER_img'], filename))
        uploaded_files.append(filename)
    
    return jsonify({'message': 'Files uploaded successfully', 'files': uploaded_files})

@app.route('/myimg/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER_img'], filename)

@app.route('/delete/<image>')
def delete(image):
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER_img'], image))
        return jsonify({'message': 'File deleted successfully'})
    except:
        return jsonify({'error': 'Error deleting file'}), 400

@app.route('/generate', methods=['POST'])
def generate():
    if request.method == 'POST':
        speech_file = request.files.get('speech')
        background_file = request.files.get('background')

        if speech_file and speech_file.filename.endswith('.mp3') and background_file and background_file.filename.endswith('.mp3'):
            speech_file.save(f"{app.config['UPLOAD_FOLDER_speech']}/{speech_file.filename}")
            background_file.save(f"{app.config['UPLOAD_FOLDER_background']}/{background_file.filename}")
            
            output_path = generatex()
            return jsonify({'output_path': output_path})
        else:
            return jsonify({'error': 'Please upload both MP3 files'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
