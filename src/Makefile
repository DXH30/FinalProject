all: pcapread pcaptrain pcaptest complete

pcapread: pcapread.c pcapread.h
	gcc -lpcap -Wall pcapread.c -o ./bin/pcapread

pcaptrain: pcaptrain.c pcaptrain.h
	gcc -lpcap -Wall pcaptrain.c -o ./bin/pcaptrain

pcaptest: pcaptest.c pcaptest.h
	gcc -lpcap -Wall pcaptest.c -o ./bin/pcaptest

complete:
	echo "Makefile selesai !D"
