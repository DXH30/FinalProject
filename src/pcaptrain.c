#include "pcaptrain.h"
#include <stdio.h>

int main(int argc, char *argv[]) {
  if(argc <= 1) {
    banner();
    usage();
  } else {
    printf("The Program is running %d\n", argc);
  }
  return 0;
}
