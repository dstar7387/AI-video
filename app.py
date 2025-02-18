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
    # Ensure directories exist
    auto_upload_files()

    # Check for existing images
    image_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER_img']) 
                  if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not image_files:
        return render_template('index.html', message='No images found in myimg folder')

    # Check for existing audio
    audio_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER_speech']) 
                  if f.lower().endswith('.mp3')]
    
    if not audio_files:
        print("No audio file found in myspeech folder")

    # Log files being used
    for img in image_files:
        print(f"Using image: {img}")
    
    if audio_files:
        print(f"Using audio: {audio_files[0]}")

    # Generate the video
    try:
        output_path = generatex()
        return render_template('result.html', output_path=output_path)
    except Exception as e:
        print(f"Error generating video: {str(e)}")
        return render_template('index.html', message='Error generating video')

    


if __name__ == '__main__':
    app.run(debug=True, port=5000)
