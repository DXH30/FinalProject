#include <stdio.h>
#include <pcap.h>
#include <netinet/in.h>
#include <netinet/if_ether.h>

void my_packet_handler (
        u_char *args,
        const struct pcap_pkthdr *header,
        const u_char *packet
        )
    {
        struct ether_header *eth_header;
        eth_header = (struct ether_header *) packet;
        if (ntohs(eth_header->ether_type) != ETHERTYPE_IP) {
            printf("Not an IP packet. Skipping...\n\n");
            return;
        }

        printf("Total packet available: %d bytes\n", header->caplen);
        printf("Expected packet size: %d bytes\n", header->len);

        const u_char *ip_header;
        const u_char *tcp_header;
        const u_char *payload;

        int ethernet_header_length = 14;
        int ip_header_length;
        int tcp_header_length;
        int payload_length;

        ip_header = packet + ethernet_header_length;
        ip_header_length = ((*ip_header) & 0x0F);

        ip_header_length = ip_header_length * 4;

        printf("IP header length (IHL) in bytes: %d\n", ip_header_length);

        u_char protocol = *(ip_header + 9);
        if (protocol != IPPROTO_TCP) {
            printf("Not a TCP packet. Skipping...\n\n");
            return;
        }

        tcp_header = packet + ethernet_header_length + ip_header_length;
        tcp_header_length = ((*(tcp_header + 12)) & 0xF0) >> 4;

        printf("TCP header length in bytes: %d\n", tcp_header_length);

        int total_headers_size = ethernet_header_length+ip_header_length+tcp_header_length;
        printf("Size of all headers combined: %d bytes\n", total_headers_size);
        payload_length = header->caplen - 
            (ethernet_header_length + ip_header_length + tcp_header_length);
        printf("Payload size: %d bytes\n", payload_length);
        payload = packet + total_headers_size;
        printf("Memory address where payload begins: %p\n\n", payload);
        return;
    }

int main(int argc, char **argv) {
    char *device = "eth0";
    char error_buffer[PCAP_ERRBUF_SIZE];
    pcap_t *handle;
    int snapshot_length = 1024;
    int total_packet_count = 200;
    u_char *my_arguments = NULL;

    handle = pcap_open_live(device, snapshot_length, 0, 10000, error_buffer);
    pcap_loop(handle, total_packet_count, my_packet_handler, my_arguments);
    return 0;
}
