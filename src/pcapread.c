#define AUTHOR "Didik Hadumi Setiaji"
#define APPNAME "pcapread"
#define APPVER "v1.0 a"
#define APPDESC "untuk membaca dan mengeksport dalam bentuk bmp"

#include "pcapread.h"
#include <stdio.h>

void banner() {
  printf("=================================\n");
  printf("Author     : %s\n", AUTHOR);
  printf("Name       : %s %s\n", APPNAME, APPVER);
  printf("Deskripsi  : %s\n", APPDESC);
  printf("=================================\n");
}

void usage(int argc, char *argv[]) {
  printf("Petunjuk : %s -r namafile.pcap prefix\n", APPNAME);
  printf("           %s -i interface prefix\n", APPNAME);
  printf("prefix untuk awalan, contoh payload\n");
  return;
}

int main(int argc, char *argv[]) {
  if(argc <= 1) {
    banner();
    usage(argc, argv);
  } else {
    printf("The Program is running %d\n", argc);
  }
  return 0;
}
