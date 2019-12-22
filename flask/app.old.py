from flask import Flask, render_template, flash, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from keras.models import Sequential, model_from_json
from keras.layers import Dense, Activation, TimeDistributed, Dropout, LSTM
from keras.utils import plot_model
from keras import optimizers, metrics
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

def ip2int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]

def int2ip(addr):
    return socket.inet_ntoa(struct.pack("!I", addr))

ipmap = interp1d([0, 2**32], [0, 1])
portmap = interp1d([0, 2**16], [0, 1])

def getpcap(pkt):
    ip_src=pkt[IP].src
    ip_dst=pkt[IP].src
    tcp_sport=pkt[TCP].sport
    tcp_dport=pkt[TCP].dport
    return ip_src, ip_dst, tcp_sport, tcp_dport

def getpcapp(pkt):
    payload=pkt[Raw]
    return payload

def getraw(pkt, target=1):
    pack = pkt
    i = 0
    m = 0
    payload = []
    payleng = []
    for pkt in pack:
        if Raw in pkt:
            inpack = []
            inpack = [x for x in pkt[Raw].load]
            payleng.append(len(inpack))
            if len(inpack) <= 1448:
                inpack = np.pad(inpack, (0, 1448-len(inpack)), 'constant', constant_values=0).tolist()
                payload.append(inpack)
            m = m +1
        i = i + 1
    list_x = []
    list_y = []
    list_semua = []
    t = 0
    for i in payload:
        list_semua.append(i)
        if payleng[t] > 1300:
            list_x.append(i)
            list_y.append(target)
        else:
            list_x.append(i)
            list_y.append(0)
        t = t + 1
    input_semua = np.array([np.array(x) for x in list_semua])
    input_x = np.array([np.array(x) for x in list_x])
    input_y = np.array([np.array(x) for x in list_y])
    print("uuran input_x adalah "+str(input_x.shape))
    return input_x, input_y, input_semua


# Disini memastikan model nya ada
message = ''
model = Sequential()
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

def lstm_model_init():
    weight_path = os.path.join(os.getcwd(),'bobot/bobotLSTM.h5')
    model_path = os.path.join(os.getcwd(),'model/modelLSTM.json')
    if os.path.exists(weight_path) and os.path.exists(model_path):
        model_file = open('./model/modelLSTM.json', 'r')
        model_json = model_file.read()
        model_file.close()
        model = model_from_json(model_json)
        model.load_weights(weight_path)
        optm = optimizers.Adam(lr=0.001, clipnorm=0.5)
        message = 'model LSTM berhasil di muat'
        model.summary()
        model.compile(optimizer=optm,loss='mae',metrics=['accuracy', metrics.mae, metrics.categorical_crossentropy]) 
    else:
        message = 'model LSTM gagal di muat'
        if os.path.exists(weight_path):
            message += ' file model tidak ada'
        elif os.path.exists(model_path):
            message += ' file bobot tidak ada'
    return model

def cnn_model_init():
    weight_path = os.path.join(os.getcwd(),'bobot/bobotCNN.h5')
    model_path = os.path.join(os.getcwd(),'model/modelCNN.json')
    if os.path.exists(weight_path) and os.path.exists(model_path):
        model_file = open('./model/modelCNN.json', 'r')
        model_json = model_file.read()
        model_file.close()
        model = model_from_json(model_json)
        model.load_weights(weight_path)
        optm = optimizers.Adam(lr=0.001, clipnorm=0.5)
        message = 'model CNN berhasil di muat'
        model.summary()
        model.compile(optimizer=optm,loss='mae',metrics=['accuracy', metrics.mae, metrics.categorical_crossentropy]) 
    else:
        message = 'model CNN gagal di muat'
        if os.path.exists(weight_path):
            message += ' file model tidak ada'
        elif os.path.exists(model_path):
            message += ' file bobot tidak ada'
    return model

lmodel = lstm_model_init()
cmodel = cnn_model_init()

UPLOAD_FOLDER = './file'
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
            View('Result', 'result')
            )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result')
def result():
    cnn_path = os.path.join('./static/','temp_cnn_filter.png')
    ip_dst = os.path.join('./static/','temp_ip_dst.png')
    ip_src = os.path.join('./static/','temp_ip_src.png')
    port_dst = os.path.join('./static/','temp_port_dst.png')
    port_src = os.path.join('./static/','temp_port_src.png')
    return render_template('result.html',
            cnn_path=cnn_path,
            ip_src=ip_src,
            ip_dst=ip_dst,
            port_src=port_src,
            port_dst=port_dst
            )

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
        print(filePcap.filename)
        filename = 'temp.pcap'
        filePcap.save(os.path.join('./temp/', filename))
        pcap = rdpcap(os.path.join('./temp/', filename))
        # Ambill isi paket nya IPSRC, IPDST, PORTSRC, PORTDST

        netw = [] # Net word untuk dijadikan gambar
        nett = [] # Net Test untuk dijadikan input LSTM4
        netp = [] # Berisi payload yang akan di filter CNN
        for pkt in pcap:
            if TCP in pkt:
                if IP in pkt:
                    netw.append(getpcap(pkt))
                    nett.append([
                        float(ipmap(ip2int(getpcap(pkt)[0]))), # IPSRC
                        float(ipmap(ip2int(getpcap(pkt)[1]))), # IPDST
                        float(portmap(getpcap(pkt)[2])), # PORTSRC
                        float(portmap(getpcap(pkt)[3])), # PORTDST
                        ])
        nett = np.array([nett])
        #print(nett)
        netx, nety, nets = getraw(pcap)
        print("Ini adalah payload nya")
        #print(netx)
        print(np.shape(nett))
        nett = nett.reshape(-1, 1, 4)
        print(np.shape(nett))
        model = lmodel
        optm = optimizers.Adam(lr=0.001, clipnorm=0.5)
        model.compile(optimizer=optm,loss='mae',metrics=['accuracy', metrics.mae, metrics.categorical_crossentropy]) 
        start_lstm_time = time.time()
        prediksi = model.predict(nett)
        print("Total waktu LSTM : "+ str(time.time() - start_lstm_time))
        hasil = model.evaluate(nett, prediksi)
        print("Input dan Output Matriks Sama : ")
        print(np.array_equal(nett, prediksi))
        #for pred in prediksi:
        #    print(pred)
        print(np.shape(prediksi))
        src_ip_list = []
        src_port_list = []
        dst_ip_list = []
        dst_port_list = []
        for row in nett:
            #print(row[0][0]) # src_ip
            src_ip_list.append(row[0][0])
            #print(row[0][1]) # src_port
            dst_ip_list.append(row[0][1])
            #print(row[0][2]) # dst_ip
            src_port_list.append(row[0][2])
            #print(row[0][3]) # dst_port
            dst_port_list.append(row[0][3])
        
        p_src_ip_list = []
        p_src_port_list = []
        p_dst_ip_list = []
        p_dst_port_list = []
        for row in prediksi:
            p_src_ip_list.append(row[0])
            p_dst_ip_list.append(row[1])
            p_src_port_list.append(row[2])
            p_dst_port_list.append(row[3])

        # Disini kita plot grafiknya
        fig = plt.figure()
        axe = fig.add_subplot(111)
        x = range(len(nett))
        axe.scatter(x, src_ip_list, s=10, c='g', label='ip_src asli')
        axe.scatter(x, p_src_ip_list, s=10, c='r', label='ip_src prediksi')
        plt.xlabel('Sampel')
        plt.ylabel('Probabilitas')
        plt.legend(loc='upper left')
        plt.grid()
        plt.savefig('./static/temp_ip_src.png')

        fig = plt.figure()
        axe = fig.add_subplot(111)
        x = range(len(nett))
        axe.scatter(x, dst_ip_list, s=10, c='g', label='ip_dst asli')
        axe.scatter(x, p_dst_ip_list, s=10, c='r', label='ip_dst prediksi')
        plt.xlabel('Sampel')
        plt.ylabel('Probabilitas')
        plt.legend(loc='upper left')
        plt.grid()
        plt.savefig('./static/temp_ip_dst.png')

        fig = plt.figure()
        axe = fig.add_subplot(111)
        x = range(len(nett))
        axe.scatter(x,src_port_list, s=10,c='g', label='port_src asli')
        axe.scatter(x,p_src_port_list, s=10, c='r', label='port_src prediksi')
        plt.xlabel('Sampel')
        plt.ylabel('Probabilitas')
        plt.legend(loc='upper left')
        plt.grid()
        plt.savefig('./static/temp_port_src.png')

        fig = plt.figure()
        axe = fig.add_subplot(111)
        x = range(len(nett))
        axe.scatter(x,dst_port_list, s=10,c='g', label='port_dst asli')
        axe.scatter(x,p_dst_port_list, s=10, c='r', label='port_dst prediksi')
        plt.xlabel('Sampel')
        plt.ylabel('Probabilitas')
        plt.legend(loc='upper left')
        plt.grid()
        plt.savefig('./static/temp_port_dst.png')

        model = cmodel
        start_cnn_time = time.time()
        saring = model.predict(netx)
        print("Total waktu CNN : "+str(time.time() - start_cnn_time))
        resu = []
        for sari in saring:
         #   print(sari)
            if sari[0] > sari[1]:
                resu.append(0)
            else:
                resu.append(1)
        fig = plt.figure()
        print("Panjang X CNN : "+str(len(saring)))
        axe = fig.add_subplot(111)
        x = range(len(saring))
        axe.scatter(x, resu, s=10, c='r', label='prediksi')
        plt.xlabel('Sampel')
        plt.ylabel('Probabilitas')
        plt.legend(loc='upper left')
        plt.grid()
        plt.savefig('./static/temp_cnn_filter.png')

        return redirect(url_for('result'))
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
