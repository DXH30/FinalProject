from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten, BatchNormalization
from keras.layers.embeddings import Embedding
from keras.layers import  Reshape
from keras import optimizers
import numpy as np

lstack = Sequential()

vocab_size = 257
emb_dimension = 25
dim1 = 1000
dim2 = 1
channel = 1

# disini di setting ConvNet untuk Classify Malware nya

lstack.add(Embedding(vocab_size, emb_dimension, input_length=dim1))
lstack.add(Reshape((dim1, emb_dimension, channel)))
lstack.add(Conv2D(32,kernel_size=(3, 25),activation='relu',padding='valid'))
lstack.add(BatchNormalization())
lstack.add(Conv2D(64,kernel_size=(3, 1),activation='relu',padding='valid'))
lstack.add(BatchNormalization())
lstack.add(MaxPooling2D(pool_size=(100, 1),padding='valid'))
lstack.add(Flatten())
lstack.add(Dense(128,activation='relu',))
lstack.add(Dropout(0.25))
lstack.add(Dense(2, activation='softmax'))

# optimzer
optm = optimizers.Adam(lr=0.001, clipnorm=0.5)
from keras import metrics
lstack.compile(optimizer=optm,loss='categorical_crossentropy',metrics=['accuracy', metrics.mae, metrics.categorical_accuracy])

from keras.utils import plot_model
plot_model(lstack, show_shapes=True, to_file="model.png")

import os
import numpy as np
import csv

filename = 'malware_js_stream_1254.txt'
c = []
results = []
with open(filename,'r') as f:
  c = csv.reader(f)
  for row in c:
    results.append(row)

ln = os.path.getsize(filename);

# data preparation
X = None # dataset of shape (#instance, #feature)
Y = None # one-hot vectors (#instance, #class)
shape_x = np.shape(X)
data_x = np.reshape(X, shape_x)
shape_y = np.shape(Y)
data_y = np.reshape(Y, shape_y)

X = []
Y = []
Z = []
source = []
content = []
label = []
for i in range(len(results)):
  source.append(results[i][0])
  label.append(results[i][1])
  content.append(results[i][2:])


X.append(content)
# Memetakan dari X string ke X int
X1 = np.zeros([len(X),len(X[0]),1000])
for a in range(len(X)):
  for b in range(len(X[a])):
    for c in range(len(X[a][b])):
      X[a][b][c] = int(X[a][b][c],16);
      X1[a,b,c] = np.array(X[a][b][c])
Z.append(label)

X = X1
# mengubah results
# Mengubah X dan Y dari List of List ke Array

#X = np.array([np.array(xi) for xi in X])

Y = np.array([np.array(xi) for xi in Z])

# Cara mengubah X array of List jadi array of array ?

# Mengubah ukuran Y Label Menjadi 5000
#Y = np.append(Y,[np.array(0) for xi in range(5000-len(Z[0]))])
#X = np.append(X,[np.array(0) for xi in range(5000-len(Z[0]))])

from keras.utils import to_categorical
Y = to_categorical(Y)
Y = np.reshape(Y, (2612, -1))
X = np.reshape(X, (2612, -1))

#Y = Y.astype(object)

shape_x = np.shape(X)
data_x = np.reshape(X, shape_x)
shape_y = np.shape(Y)
data_y = np.reshape(Y, shape_y)

lstack.fit(data_x, data_y, epochs=50, verbose=2)

# Setelah di training model di save
lstack.save('mydata50.h5')
