#!/bin/bash

for perintah in $(ls -1 payload*)
do
	../bin/raw2bmp $perintah $perintah.png
done
