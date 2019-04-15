#define AUTHOR "Didik Hadumi Setiaji"
#define APPNAME "pcapread"
#define APPVER "v1.0 a"
#define APPDESC "untuk membaca dan mengeksport dalam bentuk bmp"

#include "pcapread.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void banner() {
  printf("=================================\n");
  printf("Author     : %s\n", AUTHOR);
  printf("Name       : %s %s\n", APPNAME, APPVER);
  printf("Deskripsi  : %s\n", APPDESC);
  printf("=================================\n");
}

void usage() {
  printf("Petunjuk : %s -r namafile.pcap prefix\n", APPNAME);
  printf("           %s -i interface prefix\n", APPNAME);
  printf("prefix untuk awalan, contoh payload\n");
  return;
}

int main(int argc, char *argv[]) {
	if (argc <= 1) {
		banner();
		usage(argc, argv);
		exit(1);
	} else {
		printf("The Program is running with %d argv\n", argc);
	}

	/* Memeriksa opsi yang digunakan */
	if (strcmp(argv[1], "-r") == 0) {
		printf("Reading File\n");
		file_read(argc, argv);
	}
	else if (strcmp(argv[1], "-i") == 0) {
		printf("Reading Interface\n");
		interface_read(argc, argv);
	} else {
		usage();
		return 0;
	}
	/* Memeriksa tidak ada argument yang digunakan */

	return 0;
}
