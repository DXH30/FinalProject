#define APPNAME "rawbitmap"
#define AUTHOR "Didik Hadumi Setiaji"
#define APPDESC "Raw data to Bitmap Converter"

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <malloc.h>
#include <sys/socket.h>

#ifndef WIDTH
#define WIDTH 800
#endif

#ifndef HEIGHT
#define HEIGHT 400
#endif

#ifndef FILESIZE
#define FILESIZE 14+40+HEIGHT*WIDTH*3
#endif

void banner() {
	printf("Author : %s\n", AUTHOR);
	printf("App Name : %s\n", APPNAME);
	printf("Description : %s\n", APPDESC);
	return;
}

void helper() {
	printf("Usage : %s [options] filename\n", APPNAME);
	printf("Example : %s -v filename // verbose\n", APPNAME);
	return;
}

/* 14 byte bitmap file header */
struct bitmapfileheader {
	uint16_t signature; // Harus di isikan "BM" untuk menentukan bitmap 2 byte
	/* untuk ukuran file bitmap dapat dihitung dengan
	 * 14 byte untuk bitmap header
	 * 40 byte untuk bitmap infoheader
	 * sisanya tinggi x lebar pixel
	 * karena jenis nya rgb sehingga
	 * ukuran tiap pixel nya adalah 3 byte
	 * sehingga dapat disimpulkan untuk ukuran filesize adalah
	 * filesize = 14+40+(tinggixlebar)x3 byte
	 * */
	uint32_t filesize;
	/* isikan kosong saja */
	uint16_t reserved1;
	uint16_t reserved2;

	/* offset merupakan dimana dia start pixel array nya
	 * size(header) + 1, atau setelah headernya
	 * */
	uint32_t offset;
};

/* gak terlalu dipake */
struct bitmapv5header {
	uint32_t dibheadersize;
	uint32_t imagewidth;
	uint32_t imageheight;
	uint16_t planes;
	uint16_t bitperpixel;
	uint32_t compression;
	uint32_t imagesize;
	uint32_t ypixelpermeter;
	uint32_t xpixelpermeter;
	uint32_t *colorincolortable;
	uint32_t impcolorcount;
	uint32_t redchannelbitmask;
	uint32_t greenchannelbitmask;
	uint32_t alphachannelbitmask;
	uint32_t colorspacetype;
	uint32_t colorspaceendpoints;
	uint32_t gammaredchannel;
	uint32_t gammagreenchannel;
	uint32_t gammabluechannel;
	uint32_t intent;
	uint32_t icc_profile_data;
	uint32_t icc_profile_size;
	uint32_t reserved;
};

/* bitmapinfoheader berisi informasi metadata untuk filebitmap 
 * ukurannya 40 byte
 * */
struct bitmapinfoheader {
	uint32_t biSize; // ukuran total dari bitmap header 4 byte
	uint32_t biWidth; // lebar dari gambar 4 byte 
	uint32_t biHeight; // tinggi dari gambar 4 byte
	uint16_t biPlanes; // 2 byte
	uint16_t biBitCount; // bit per pixel 2 byte
	uint32_t biCompression; // 4 byte
	uint32_t biSizeImage; // data size bmp 4 byte
	uint32_t biXPelsPerMeter; // 4 byte
	uint32_t biYPelsPerMeter; // 4 byte
	uint32_t biClrUsed; // 4 byte
	uint32_t biClrImportant; // 4 byte
};

int main(int argc, char **argv) {
	
	FILE *file;
	
	/* mendeklarasikan header */
	struct bitmapfileheader fileheader;
	struct bitmapinfoheader infoheader;
	char filename[] = "namafile.txt";
	char gambarnya[] = "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff";

	/* Menampilkan banner */
	banner();

	/* menampilkan petunjuk penggunaan */
	if (argc < 1) {
		helper();
	}

	/* membuat header untuk file bitmap */
	fileheader.signature = "BM";
	fileheader.filesize = FILESIZE; 
	fileheader.reserved1 = "\x00\x00";
	fileheader.reserved2 = "\x00\x00";
	fileheader.offset = 5;

	fopen(filename, "wb");
	fwrite(&fileheader, sizeof(struct bitmapfileheader), 1, file);
	fwrite(&infoheader, sizeof(struct bitmapinfoheader), 1, file);
	fwrite(gambarnya, WIDTH*HEIGHT*3, 1, file);
	fclose(file);
	return 0;
}
