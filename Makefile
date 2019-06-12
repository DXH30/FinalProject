all: build bitmap linking

build:
	cd ./src; \
	make; \
	cd ..;

bitmap:
	cd ./src/bitmap; \
	make; \
	cd ../..;

linking:
	ln -v ./src/bin/pcapread ./bin/pcapread; \
	ln -v ./src/bin/pcaptrain ./bin/pcaptrain; \
	ln -v ./src/bin/pcaptest ./bin/pcaptest; \
	ln -v ./src/bitmap/raw2bmp.py ./bin/raw2bmp; \
	ln -v ./src/bin/raw2bmp ./bin/raw2bmp.o

clean: bersihkan bersih

bersihkan:
	rm -v ./bin/*; \
	rm -v ./src/bin/*

bersih:
	echo "Sudah dibersihkan.. "
