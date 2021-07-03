import os
import sys
from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename
#from forms import MusicSearchForm

import database
import commands
from model import AudioFile
# init flask app instance
app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

# setup with the configuration provided by the user / environment
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['UPLOAD_EXTENSIONS'] = ['.mp3', '.ogg', '.wav', '.aiff', '.flac', '.alac', '.aac']
app.config['UPLOAD_PATH'] = 'static/audio_files/'

# setup all our dependencies, for now only database using application factory pattern
database.init_app(app)
commands.init_app(app)


@app.route("/")
def main_page():
    if not os.path.exists(app.config['UPLOAD_PATH']):
        init()

    items = AudioFile.query.all()
    return render_template('index.html', items=items)



@app.route("/upload/")
def upload():
    return render_template('upload.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        user = request.form.get('user')
        title = request.form.get('title')
        filename = request.files['file'].filename
        uploaded_file = request.files['file']
        byte_array = request.files['file'].read()
        request.files['file'].seek(0)

        if not os.path.exists(app.config['UPLOAD_PATH']):
            os.makedirs(app.config['UPLOAD_PATH'])

        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400)
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))

        model = AudioFile(title=title, user=user, filename=filename, file=byte_array)
        database.db.session.add(model)
        database.db.session.commit()

        return 'file uploaded successfully'





@app.route("/init")
def init():
    if not os.path.exists(app.config['UPLOAD_PATH']):
        os.makedirs(app.config['UPLOAD_PATH'])

    items = AudioFile.query.all()
    for item in items:
        file = open(app.config['UPLOAD_PATH']+item.filename, "wb")
        file.write(item.file)
        file.close()

    return 'init successfull'


if __name__ == "__main__":
    app.run()
