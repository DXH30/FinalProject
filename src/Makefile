all: binc pcapread pcaptrain pcaptest complete

binc:
	mkdir ./bin

pcapread: pcapread.c pcapread.h
	gcc -g pcapread.c -o ./bin/pcapread -lpcap

pcaptrain: pcaptrain.c pcaptrain.h
	gcc -g pcaptrain.c -o ./bin/pcaptrain -lpcap

pcaptest: pcaptest.c pcaptest.h
	gcc -g pcaptest.c -o ./bin/pcaptest -lpcap

complete:
	echo "Makefile selesai !D"

tensorflow: tf_install 

tf_install:
	tar -C /usr -zxvf ./lib/libtensorflow*.tar.gz

tf_complete:
	echo "Install C_lang Tensorflow selesai"

payload2bitmap:
	gcc -g ./bitmap/payload2bitmap.c -o ./bin/pay2bmp
