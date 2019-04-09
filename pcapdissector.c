#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef struct {
	uint16_t src_port;
	uint16_t dst_port;
	uint32_t seq_num;
	uint32_t ack_num;
	short hl;
	short rsvd;
	bool cwr;
	bool ece;
	bool urg;
	bool ack;
	bool psh;
	bool rst;
	bool syn;
	bool fin;
} tcp_header;
