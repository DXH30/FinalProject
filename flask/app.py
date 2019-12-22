from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from time import sleep
from werkzeug.utils import secure_filename
from scapy.all import *
from scipy.interpolate import interp1d
import json
import os
import struct
import socket
import numpy as np
import matplotlib.pyplot as plt
import time
import shutil
owd = os.getcwd()
def cekbobotLSTM():
    weight_path = os.path.join(os.getcwd(),'bobot/bobotLSTM.h5')
    return os.path.exists(weight_path)

def cekmodelLSTM():
    model_path = os.path.join(os.getcwd(),'model/modelLSTM.json')
    return os.path.exists(model_path)

def cekbobotCNN():
    weight_path = os.path.join(os.getcwd(),'bobot/bobotCNN.h5')
    return os.path.exists(weight_path)

def cekmodelCNN():
    model_path = os.path.join(os.getcwd(),'model/modelCNN.json')
    return os.path.exists(model_path)

UPLOAD_FOLDER = './dataset'
ALLOWED_EXTENSIONS = {'pcap'}
ALLOWED_PCAP = {'pcap'}
ALLOWED_H5 = {'h5', 'hs5'}
ALLOWED_JSON = {'json'}


# Disini kita definisika fungsi untuk mengambil
app = Flask(__name__)
app.secret_key = 'secretkey123'
app.config['UPLOAD_FOlDER'] = UPLOAD_FOLDER
nav = Nav(app)
Bootstrap(app)

@nav.navigation()
def mynavbar():
    return Navbar(
            'FINPROJ : DIDIK HADUMI SETIAJI',
            View('Home', 'index'),
            View('Upload', 'uploadFile'),
            View('Setting', 'Setting'),
            View('Log', 'Stream'),
            View('Live', 'Live'),
            )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def uploadFile():
    if cekmodelLSTM() and cekbobotLSTM():
        messages = "Model LSTM sudah ada, silahkan upload file virus"
    else:
        messages = "Model LSTM belum ada, silahkan upload model terlebih dahulu"
    
    if cekmodelCNN() and cekbobotCNN():
        messages += " Model CNN sudah ada, silahkan upload file virus"
    else:
        messages += " Model CNN belum ada, silahkan upload model terlebih dahulu"
    if request.method == 'POST':
        filePcap = request.files['filePcap']
        filename = filePcap.filename
        filePcap.save(os.path.join('./dataset/', filename))
        return redirect(url_for('uploadFile'))

    return render_template('upload.html', messages=messages)

@app.route('/setting', methods=['GET', 'POST'])
def Setting():
    data = json.load(open('setting.json'))
    # Definisikan untuk LSTM
    if os.path.exists('./static/modelLSTM.png'):
        lstm_model_exists = 1
    else:
        lstm_model_exists = 0
        message = 'Data Model LSTM gagal dimuat model tidak ada'
    if os.path.exists('./bobot/bobotLSTM.h5'):
        lstm_bobot_exists = 1
    else:
        lstm_bobot_exists = 0
        message = 'Data Bobot LSTM gagal dimuat bobot tidak ada'

    if os.path.exists('./static/modelCNN.png'):
        cnn_model_exists = 1
    else:
        cnn_model_exists = 0
        message = 'Data Model CNN gagal dimuat model tidak ada'
    if os.path.exists('./bobot/bobotCNN.h5'):
        cnn_bobot_exists = 1
    else:
        cnn_bobot_exists = 0
        message = 'Data Bobot CNN gagal dimuat bobot tidak ada'

    if request.method == 'POST':

        fileModelLSTM = request.files['fileModelLSTM']
        fileBobotLSTM = request.files['fileBobotLSTM']
        fileModelCNN = request.files['fileModelCNN']
        fileBobotCNN = request.files['fileBobotCNN']

        if fileModelLSTM and allowed_model(fileModelLSTM.filename):
            filename = secure_filename('modelLSTM.json')
            fileModelLSTM.save(os.path.join('./model/', filename))
            model_file = open('./model/modelLSTM.json', 'r')
            model_json = model_file.read()
            model_file.close()
            model = Sequential()
            model = model_from_json(model_json)
            plot_model(model, to_file='./static/modelLSTM.png', show_shapes=True)
        if fileBobotLSTM and allowed_bobot(fileBobotLSTM.filename):
            filename = secure_filename('bobotLSTM.h5')
            fileBobotLSTM.save(os.path.join('./bobot/', filename))
        
        lstm_model_init()

        if fileModelCNN and allowed_model(fileModelCNN.filename):
            filename = secure_filename('modelCNN.json')
            fileModelCNN.save(os.path.join('./model/', filename))
            model_file = open('./model/modelCNN.json', 'r')
            model_json = model_file.read()
            model_file.close()
            model = Sequential()
            model = model_from_json(model_json)
            plot_model(model, to_file='./static/modelCNN.png', show_shapes=True)

        if fileBobotCNN and allowed_bobot(fileBobotCNN.filename):
            filename = secure_filename('bobotCNN.h5')
            fileBobotCNN.save(os.path.join('./bobot/', filename))
        cnn_model_init()

        with open('setting.json', 'w') as f:
            json.dump(request.form, f)
        return redirect(url_for('Setting'))
    return render_template('setting.html', 
            data=data, 
            lstm_model_exists=lstm_model_exists, 
            lstm_bobot_exists=lstm_bobot_exists, 
            cnn_model_exists=cnn_model_exists, 
            cnn_bobot_exists=cnn_bobot_exists)

@app.route('/delete_model_lstm')
def delModelLSTM():
    os.remove(os.path.join(os.getcwd(),'model/modelLSTM.json'))
    os.remove(os.path.join(os.getcwd(),'static/modelLSTM.png'))
    lstm_model_init()
    return redirect(url_for('Setting'))

@app.route('/delete_bobot_lstm')
def delBobotLSTM():
    os.remove(os.path.join(os.getcwd(),'bobot/bobotLSTM.h5'))
    lstm_model_init()
    return redirect(url_for('Setting'))

@app.route('/delete_model_cnn')
def delModelCNN():
    os.remove(os.path.join(os.getcwd(),'model/modelCNN.json'))
    os.remove(os.path.join(os.getcwd(),'static/modelCNN.png'))
    cnn_model_init()
    return redirect(url_for('Setting'))

@app.route('/delete_bobot_cnn')
def delBobotCNN():
    os.remove(os.path.join(os.getcwd(),'bobot/bobotCNN.h5'))
    cnn_model_init()
    return redirect(url_for('Setting'))

@app.route('/stream')
def Stream():
    with open('sjd_alert.full') as f:
        data = f.read().replace('\n', '\r')
    return render_template('stream.html', data=data)

@app.route('/live')
def Live():
    data = os.listdir('./dataset')
    return render_template('live.html', data=data)

@app.route('/getstatus')
def getStatus():
    print(owd)
    with open('./dataset/dataset.json') as f:
        dataset = json.load(f)
    status = []
    response = []
    for i in dataset:
        status_file = re.sub(r'.pcap','.status', i)
        with open('./dataset/'+status_file) as f:
            statusn = f.read()
        response.append([i,statusn])
    #response = [[dataset], [status]]
    print(response)
    return jsonify(response)

@app.route('/resettesting', methods=['POST'])
def resetTesting():
    if request.method == 'POST':
        print(request)
        dataset = json.loads(request.data)
#        dataset = request.get_json()
        print(request.data)
        for i in dataset:
            print(i[0]);
            a = re.sub(r'.pcap','',i[0])
            print("Menghapus direktori "+a+"...")
            shutil.rmtree('./dataset/'+a)
            print("Direktori "+a+" sudah terhapus")
            print("Mereset status menjadi 0 kembali...")
            with open('./dataset/'+a+'.status','w') as tulis:
                tulis.write('0')
            print("Status sudah direset menjadi 0")
    return jsonify(1);
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

def allowed_pcap(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_PCAP


if __name__ == '__main__':
    app.run()
    nav.init_app(app)
