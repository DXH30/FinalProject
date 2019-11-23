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

@app.route('/')
def index():
    return 
