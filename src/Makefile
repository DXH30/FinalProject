all: pcapread pcaptrain pcaptest complete

pcapread: pcapread.c pcapread.h
	gcc -g -lpcap pcapread.c -o ./bin/pcapread

pcaptrain: pcaptrain.c pcaptrain.h
	gcc -g -lpcap pcaptrain.c -o ./bin/pcaptrain

pcaptest: pcaptest.c pcaptest.h
	gcc -g -lpcap pcaptest.c -o ./bin/pcaptest

complete:
	echo "Makefile selesai !D"

tensorflow: tf_install 

tf_install:
	tar -C /usr -zxvf ./lib/libtensorflow*.tar.gz

tf_complete:
	echo "Install C_lang Tensorflow selesai"

payload2bitmap:
	gcc -g ./bitmap/payload2bitmap.c -o ./bin/pay2bmp
