#!/usr/bin/python2
from PIL import Image
import leargist
image = Image.open('content/drive/My Drive/sesuatu.png');
New_im = image.resize((64,64));
des = leargist.color_gist(New_im);

Feature_Vector = des[0:320];
