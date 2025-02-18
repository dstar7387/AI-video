from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from generate import generatex
import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER_img'] = 'myimg'
app.config['UPLOAD_FOLDER_speech'] = 'myspeech'
app.config['UPLOAD_FOLDER_background'] = 'mybackground'

@app.route('/')
def index():
    return render_template('index.html')

def auto_upload_files():
    # Auto upload images from myimg folder
    if not os.path.exists(app.config['UPLOAD_FOLDER_img']):
        os.makedirs(app.config['UPLOAD_FOLDER_img'])
    
    # Auto upload speech if exists
    if not os.path.exists(app.config['UPLOAD_FOLDER_speech']):
        os.makedirs(app.config['UPLOAD_FOLDER_speech'])
        
    # Auto upload background if exists
    if not os.path.exists(app.config['UPLOAD_FOLDER_background']):
        os.makedirs(app.config['UPLOAD_FOLDER_background'])

@app.route('/generate', methods=['POST'])
def generate():
    auto_upload_files()
    
    # Check if we have images in myimg folder
    images = [f for f in os.listdir(app.config['UPLOAD_FOLDER_img']) 
             if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not images:
        return render_template('index.html', message='No images found in myimg folder')
    
    # Generate the video
    output_path = generatex()
    return render_template('result.html', output_path=output_path)

if __name__ == '__main__':
    app.run(debug=True,port=5000)
