#!/usr/bin/python2
from PIL import Image
import leargist
image = Image.open('payload.log.453.bmp');
New_im = image.resize((60,60));
des = leargist.color_gist(New_im);

Feature_Vector = des[0:320];
