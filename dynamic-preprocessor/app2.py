from flask import Flask, request
import csv
import numpy as np
from keras.models import Sequential
from kears import optimizers, metrics, losses

app = Flask(__name__)

@app.route('/')
def root_example():
    print("Selamat datang di root untuik services")


@app.route('/data')
def data_process():
    ip_src = request.args.get('ip_src')
    ip_dst = request.args.get('ip_dst')
    src_port = request.args.get('src_port')
    dst_port = requets.args.get('dst_port')
