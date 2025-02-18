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

    # Handle image uploads
    uploaded_images = request.files.getlist('images')
    if not uploaded_images:
        return render_template('index.html', message='No images uploaded')

    # # Clear existing images
    # for file in os.listdir(app.config['UPLOAD_FOLDER_img']):
    #     if file.lower().endswith(('.png', '.jpg', '.jpeg')):
    #         os.remove(os.path.join(app.config['UPLOAD_FOLDER_img'], file))

    # # Save new images
    # for image in uploaded_images:
    #     if image and image.filename:
    #         filename = secure_filename(image.filename)
    #         image.save(os.path.join(app.config['UPLOAD_FOLDER_img'], filename))

    # # Handle audio upload
    # audio = request.files.get('audio')
    # if audio and audio.filename:
    #     filename = secure_filename(audio.filename)
    #     audio.save(os.path.join(app.config['UPLOAD_FOLDER_speech'], filename))

    # Generate the video
    try:
        output_path = generatex()
        return render_template('result.html', output_path=output_path)
    except Exception as e:
        print(f"Error generating video: {str(e)}")
        return render_template('index.html', message='Error generating video')

    


if __name__ == '__main__':
    app.run(debug=True, port=5000)
