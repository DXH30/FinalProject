#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <malloc.h>

#define _height 60
#define _width 60
#define _bitsperpixel 24
#define _planes 1
#define _compression 0
#define _pixelbytesize _height*_width*_bitsperpixel/8
#define _filesize _pixelbytesize+sizeof(bitmap)
#define _xpixelpermeter 0x130B // 2835, 72 DPI
#define _ypixelpermeter 0x130B // 2835, 72 DPI
#define pixel 0xaa
#pragma pack(push,1)

typedef struct {
	uint8_t signature[2];
	uint32_t filesize;
	uint32_t reserved;
	uint32_t fileoffset_to_pixelarray;
} fileheader;

typedef struct {
	uint32_t dibheadersize;
	uint32_t width;
	uint32_t height;
	uint16_t planes;
	uint16_t bitsperpixel;
	uint32_t compression;
	uint32_t imagesize;
	uint32_t ypixelpermeter;
	uint32_t xpixelpermeter;
	uint32_t numcolorspallette;
	uint32_t mostimpcolor;
} bitmapinfoheader;

typedef struct {
	fileheader fileheader;
	bitmapinfoheader bitmapinfoheader;
} bitmap;

/* File content and length */
typedef struct {
	char *contents;
	long size;
} fileio;

#pragma pack(pop)

long fileinsize;

/* read data to array */
char *readFile(char *fileName) {
	FILE *file = fopen(fileName, "rb");
	char *code;
	size_t n = 0;
	int c;
	fileio myfile;

	if (file == NULL)
		return NULL;
// uncomment to allocate code to 1000 bit
//	code = malloc(1000);
	
	fseek(file, 0, SEEK_END);
	long f_size = ftell(file);
	fseek(file, 0, SEEK_SET);
	code = malloc(f_size);

	for (n = 0; n<f_size; n++)
	{
		c = fgetc(file);
		code[n] = (char) c;
	}
	code[n] = '\0';
	fclose(file);
	fileinsize = f_size;
	return code;
}


int main(int argc, char **argv) {
//	char fileName[] = "payload.log.100";
	char *fileName;
	char *fileOutput;
	if (argc > 1) {
		fileName = argv[1];
		fileOutput = argv[2];
	} else if (argc < 1) {
		fileName = "payload.log.100"; 
		fileOutput = "test.bmp";
	}
	
//	sprintf(fileOutput, "%s.bmp", fileName); 
	FILE *fp = fopen(fileOutput, "wb");
	bitmap *pbitmap = (bitmap*)calloc(1,sizeof(bitmap));
	uint8_t *pixelbuffer = (uint8_t*)malloc(_pixelbytesize);
	const char *payload = readFile(fileName);
	int paylen = _pixelbytesize-sizeof(payload); 
	fileio myfile;
	long f_size;
	/* Bikin header nya dikit aja */
	strcpy(pbitmap->fileheader.signature,"BM");
	pbitmap->fileheader.filesize = _filesize;
	pbitmap->fileheader.fileoffset_to_pixelarray = sizeof(bitmap);
	pbitmap->bitmapinfoheader.dibheadersize = sizeof(bitmapinfoheader);
	pbitmap->bitmapinfoheader.width = _width;
	pbitmap->bitmapinfoheader.height = _height;
	pbitmap->bitmapinfoheader.planes = _planes;
	pbitmap->bitmapinfoheader.bitsperpixel = _bitsperpixel;
	pbitmap->bitmapinfoheader.compression = _compression;
	pbitmap->bitmapinfoheader.imagesize = _pixelbytesize;
	pbitmap->bitmapinfoheader.ypixelpermeter = _ypixelpermeter;
	pbitmap->bitmapinfoheader.xpixelpermeter = _xpixelpermeter;

	fwrite(pbitmap, 1, sizeof(bitmap), fp);
	/* Mulai menggambar */
	pixelbuffer = readFile(fileName);
	fwrite(pixelbuffer,1,3000,fp);

//	printf("size %d\n",sizeof(payload));
	//memset(pixelbuffer,pixel,paylen);
	//fwrite(pixelbuffer,1,paylen,fp);
	fclose(fp);
	free(pbitmap);

	printf("Berhasil dengan input : %s, dan output %s\n",fileName,fileOutput);
	//free(pixelbuffer);
	return 0;
}

/* Raw data to array of bytes 2D */
int *ratoar(FILE *fp) {

}



// Pindah pindah byte dengan fseek dan fread

size_t fpread(void *buffer, size_t size, size_t mitems, size_t offset, FILE *fp) {
	if (fseek(fp, offset, SEEK_SET) != 0)
		return 0;
	return fread(buffer, size, mitems, fp);
}

/* Buat fungsi untuk membaca pcap file */
int pcapReader() {
  
}
