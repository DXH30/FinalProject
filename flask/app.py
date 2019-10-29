from flask import Flask, render_template, flash, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from time import sleep
from werkzeug.utils import secure_filename
import json
import os

UPLOAD_FOLDER = './file'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_PCAP = {'pcap'}
ALLOWED_H5 = {'h5', 'hs5'}
ALLOWED_JSON = {'json'}

app = Flask(__name__)
app.config['UPLOAD_FOlDER'] = UPLOAD_FOLDER
nav = Nav(app)
Bootstrap(app)

@nav.navigation()
def mynavbar():
    return Navbar(
            'FINPROJ',
            View('Home', 'index'),
            View('Upload', 'uploadFile'),
            View('Setting', 'Setting'),
            View('Log', 'Stream')
            )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def uploadFile():
    return render_template('upload.html')

@app.route('/setting', methods=['GET', 'POST'])
def Setting():
    data = json.load(open('setting.json'))
    if request.method == 'POST':
        if 'file' not in request.modelFile:
            flash('Tidak ada model File')
            return redirect(request.url)
        fileModel = request.files['fileModel']
        fileBobot = request.files['fileBobot']
        if fileModel.filename == '':
            flash('No selected Model file')
            return redirect(request.url)
        if fileBobot.filename == '':
            flash('No selected Bobot File')
            return redirect(request.url)

        if fileModel and allowed_model(fileModel.filename):
            filename = secure_filename('model.json')
            fileModel.save(os.path.join('model/', filename))
        if fileBobot and allowed_bobot(fileBobot.filename):
            filename = secure_filename('bobot.h5')
            fileBobot.save(os.path.join('bobot/', filename))

        with open('setting.json', 'w') as f:
            json.dump(request.form, f)
        return redirect(url_for('setting'))
    return render_template('setting.html', data=data)

@app.route('/stream')
def Stream():
    with open('sjd_alert.full') as f:
        data = f.read().replace('\n', '\r')
    return render_template('stream.html', data=data)


# Upload file
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_model(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_JSON

def allowed_bobot(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_H5

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('upload_file', filename=filename))
    return render_template('uploading.html')


if __name__ == '__main__':
    app.run()
    nav.init_app(app)
