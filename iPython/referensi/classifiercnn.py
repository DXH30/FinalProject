from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten, BatchNormalization
from keras.layers.embeddings import Embedding
from keras.layers import Reshape
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
lstack.compile(optimizer=optm,loss='categorical_crossentropy',metrics=['accuracy'])

from keras.utils import plot_model
plot_model(lstack, show_shapes=True, to_file="model.png")
