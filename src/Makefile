all: pcapread pcaptrain pcaptest complete

pcapread: pcapread.c pcapread.h
	gcc -lpcap -Wall pcapread.c -o pcapread

pcaptrain: pcaptrain.c pcaptrain.h
	gcc -lpcap -Wall pcaptrain.c -o pcaptrain

pcaptest: pcaptest.c pcaptest.h
	gcc -lpcap -Wall pcaptest.c -o pcaptest

complete:
	echo "Makefile selesai !D"
