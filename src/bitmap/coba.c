#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

typedef struct {
	char *contents;
	long f_size;
} fileio;

int main(int argc, char **argv[]) {
	FILE *fp;
	char filename[] = "payload.log.100";
	long f_size;
	unsigned char contents[3000];
	char c;
	int i = 0;
	fp = fopen(filename, "rb");
	fseek(fp, 0, SEEK_END);
	f_size = ftell(fp);
	fseek(fp, 0, SEEK_SET);
	for (i = 0; i<f_size; i++) {
		c = fgetc(fp);
		contents[i] = c;
	}
	contents[i++] = '\0';
	fclose(fp);
	printf("Filesize : %d\n",f_size);
	printf("Contents : \n");
	for (i = 0; i<f_size; i++) {
		//printf("Contents : %s\n",contents);
		if(i%8 == 0) {
			printf("\n");
		}
		printf("%x\t", contents[i]);
	}
	printf("\n");
	return 0;
}
