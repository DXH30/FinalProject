#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

struct damping {
	uint8_t satu;
	uint8_t dua;
	uint8_t tiga;
	uint8_t empat;
	uint16_t lima;
	uint16_t enam;
	uint32_t tujuh;
	char *content;
	uint32_t footer;
};

int main() {
	FILE *fh;
	fh = fopen("testing.abc.def", "wb");
	struct damping sesuatu;
	sesuatu.satu = 5;
	sesuatu.dua = 8;
	sesuatu.tiga = 9;
	sesuatu.empat = 10;
	sesuatu.lima = 18;
	sesuatu.enam = 20;
	sesuatu.tujuh = 25;
	sesuatu.content = malloc(sizeof(char)*100);
	sesuatu.footer = 100;
	fwrite(&sesuatu, sizeof(struct damping), 1, fh);
	fclose(fh);
}
