from flask import Flask, request
import csv
import numpy as np
# Untuk menganalisis input, definisikan model terlebih dahulu
from keras.models import Sequential
from keras import optimizers, metrics, losses
from keras.layers import Conv2D, Conv1D, Dense, Embedding, Reshape, BatchNormalization, MaxPooling2D, Flatten, Dropout, MaxPooling1D
import tensorflow as tf
global graph
vocab_size = 257
emb_dimension = 50
dim1 = 1448
dim2 = 1
channel = 1
# Ubah model agar tinggal di load dengan path model
model = Sequential();
model.add(Embedding(vocab_size, emb_dimension, input_length=dim1))
model.add(Reshape((dim1, emb_dimension, channel)))
model.add(Conv2D(32,kernel_size=(50, 50),activation='sigmoid',padding='valid'))
model.add(BatchNormalization())
model.add(Conv2D(64,kernel_size=(50, 1),activation='sigmoid',padding='valid'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(100, 1),padding='valid'))
model.add(BatchNormalization())
model.add(Flatten())
model.add(Dense(128,activation='sigmoid'))
#model.add(Dropout(0.4))
model.add(Dense(2, activation='sigmoid'))
sgd = optimizers.SGD(lr=1e-3, momentum=0.0, decay=0.0, nesterov=False)
model.compile(optimizer = sgd, loss='categorical_crossentropy', metrics=['accuracy', metrics.mae, metrics.categorical_accuracy])
#model.load_weights("/content/data/My Drive/VirusData/1neris/Neris.hs5")
model.summary()
model.load_weights("Neris.hs5")
graph = tf.get_default_graph()
app = Flask(__name__)

@app.route('/')
def root_example():
    payload = request.args.get('payload');
    return '''<h1>Payload is: {}</h1>'''.format(payload)

@app.route('/query-example')
def query_example():
    payload = request.args.post('payload');
    return '''<h1>Payload is: {}</h1>'''.format(payload)

count = 0
@app.route('/data', methods=['GET', 'POST'])
def data():
    payload = []
    payloadi = []
    data = request.args.get('payload');
    ip_src = request.args.get('ip_src');
    ip_dst = request.args.get('ip_dst');
    src_port = request.args.get('src_port');
    dst_port = request.args.get('dst_port');
    tos = request.args.get('tos');
    ttl = request.args.get('ttl');
    plen = request.args.get('len');
    pid = request.args.get('id');
    proto = request.args.get('proto');
    offset = request.args.get('off');
    lip_src.append(ip_src)
    lip_dst.append(ip_dst)
    lsrc_port.append(src_port)
    ldst_port.append(dst_port)
    count = count + 1
    if (count % 1000) == 0:
        count = 0
        # ubah setiap lip_src, lip_dst menjadi integer dari 0 - 2^32
        # lalu kita mapping nilainya
        # ubah setiap lsrc_port, ldst_port menjadi integer dari 0 - 2^16
        input_data = 1 # diambil dari gabungan numpy lsrc_port, ldst_port, lip_src, lip_dst
        model.fit(input_data, input_data, epochs=1000, verbose=1, validation_data=(input_data[:,0], input_data[:,0]))
        # Disini reset semuanya
        # Harusnya bobot di reset setiap 1 jam
        lip_src = []
        lip_dst = []
        lsrc_port = []
        ldst_port = []
        model.reset_weight()

#    data = data.rstrip()
    if (len(data) == 0):
        data = "00"
    data = data.rstrip(',')
    payload = [int(i, 16) for i in data.split(',')]
    ukuran_payload = len(data)
    if (len(payload) <= 1448):
        payloadi.append(np.pad(payload, (0, 1448-len(payload)), 'constant', constant_values=0))
    else:
        payloadi.append(payload[0:1448])
    payloadj = np.array([np.array(x) for x in payloadi])
    src_port = request.args.get('src_port');
#    print("Data is %s " % (payload));
    with graph.as_default():
        print("Menerima data menghitung prediksi.. " );
        prediksi = model.predict_classes(payloadj)
#        graph.finalize()
#        graph.reset_default_graph()
    if ukuran_payload <= 10:
        prediksi[0] = 0
    print("Ukurannya adalah :  ")
    print(len(data))
    print("Hasil Prediksi : ")
    print(prediksi)
    f = open("prediction.log", "a+")
    f.write(str(ip_src)+" > "+str(ip_dst)+" : "+str(prediksi[0])+"\n")
    f.close()
    g = open("condition.log", "w+")
    g.write(str(prediksi[0])+"\n")
    g.close()
    if (prediksi[0] < 1):
        print("Data aman")
    else:
        print("Data tidak aman")
    return str(prediksi[0]);

@app.route('/form-example')
def formexample():
    return 'Todo...'

@app.route('/json-example')
def jsonexample():
    return 'Todo...'

if __name__ == '__main__':
    app.run(port=45)
