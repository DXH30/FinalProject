#!/usr/bin/bash

for i in $(ls -1 payload*)
do
	./raw2bmp $i $i.bmp
done
