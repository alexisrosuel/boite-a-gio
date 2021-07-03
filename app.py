import os
import sys
from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename
from sqlalchemy import asc, desc

#from forms import MusicSearchForm

import database
import commands
from model import AudioFile, SearchForm, SortForm
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


@app.route("/", methods=['GET', 'POST'])
def main_page():
    if not os.path.exists(app.config['UPLOAD_PATH']):
        init()

    column_sort = asc(AudioFile.id)
    sort = SortForm(request.form)
    if request.method == 'POST' and sort.data['select'] is not None:
        sort_string = sort.data['select']
        map_string_to_column = {'Date d\'ajout': desc(AudioFile.date_added),
                                'Nombre de lectures': desc(AudioFile.nb_lecture),
                                'Utilisateur': asc(AudioFile.user),
                                'Nom': asc(AudioFile.title)}
        column_sort = map_string_to_column[sort_string]

    items = AudioFile.query.order_by(column_sort).all()

    search = SearchForm(request.form)
    if request.method == 'POST' and search.data['search'] is not None:
        search_string = search.data['search'].lower()
        if search.data['search'] != '':
            items = [item for item in items if search_string in item.title.lower() or search_string in item.user.lower() or search_string in item.filename.lower()]


    return render_template('index.html', items=items, search_form=search, sort_form=sort)



@app.route("/upload/")
def upload():
    return render_template('upload.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        user = request.form.get('user')
        title = request.form.get('title')
        filename = request.files['file'].filename
        filename = filename.replace(' ','_')
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




@app.route('/count', methods = ['POST'])
def add_lecture_count():
    if request.method == 'POST':

        file_id = request.json['id']

        item = AudioFile.query.filter_by(id=file_id).first()
        item.nb_lecture = item.nb_lecture +1
        database.db.session.commit()

    return 'ok'





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
