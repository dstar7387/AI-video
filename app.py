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

    # Clear existing files in myimg and myspeech folders
    # for folder in [app.config['UPLOAD_FOLDER_img'], app.config['UPLOAD_FOLDER_speech']]:
    #     for filename in os.listdir(folder):
    #         file_path = os.path.join(folder, filename)
    #         if os.path.isfile(file_path) and not filename.endswith('.txt'):
    #             os.remove(file_path)

    # Handle image uploads
    images = request.files.getlist('images')
    if not images:
        return render_template('index.html', message='No images uploaded')

    # Save uploaded images to myimg folder
    for image in images:
        if image and image.filename:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER_img'], filename))

    # Handle audio upload to myspeech folder
    audio = request.files.get('audio')
    if audio and audio.filename:
        filename = secure_filename(audio.filename)
        audio.save(os.path.join(app.config['UPLOAD_FOLDER_speech'], filename))

    # Generate the video
    output_path = generatex()
    return render_template('result.html', output_path=output_path)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
