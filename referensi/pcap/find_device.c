#include <stdio.h>
#include <pcap.h>
#include <ncurses.h>
#include <curses.h>
#include <menu.h>
#include <arpa/inet.h>
#include <string.h>
#include <time.h>
#include <netinet/in.h>
#include <netinet/if_ether.h>


/*
 * Skema 1 : Kumpulkan 1 MTU : 1500b
 * Skema 2 : Simpan dalam bentuk file name timestamp
 *
 */

void print_packet_info(const u_char *packet, struct pcap_pkthdr packet_header) {
    printf("Packet capture length: %d\n", packet_header.caplen);
    printf("Packet total length %d\n", packet_header.len);
}

int main(int argc, char **argv) {
    // Mendefinisikan seluruh variabel untuk digunakan
    pcap_if_t *interfaces, *temp;
    pcap_t *handle;
    const u_char *packet;
    struct pcap_pkthdr packet_header;
    int packet_count_limit = 1;
    int timeout_limit = 10000;
    bpf_u_int32 ip_raw; 
    bpf_u_int32 subnet_mask_raw; 
    int device;
    char error_buffer[PCAP_ERRBUF_SIZE];
    char *devices[100];
    char ip[13];
    char subnet_mask[13];
    int lookup_return_code;
    struct in_addr address;
    char dev[] = "eno1";

    /* Mencoba mencari Device */
    device = pcap_findalldevs(&interfaces,error_buffer);
    if (device == -1) {
        printf("ERROR finding device: %s\n", error_buffer);
        return 1;
    }
    int i = 1;

    /* Memprint Device list */
    for(temp=interfaces;temp;temp=temp->next)
    {
        i++;
        *(devices + i) = temp->name; 
//    printf("Network device found: %s\n", temp->name);
    }

    lookup_return_code = pcap_lookupnet(
            dev,
            &ip_raw,
            &subnet_mask_raw,
            error_buffer
            );
    // Buat IP address lebih manusiawi
    address.s_addr = ip_raw;
    strcpy(ip, inet_ntoa(address));
    if (ip == NULL) {
        perror("inet_ntoa");
        return 1;
    }

    // Buat Subnet Mask lebih manusiawi
    address.s_addr = subnet_mask_raw;
    strcpy(subnet_mask, inet_ntoa(address));
    if (subnet_mask == NULL) {
        perror("inet_ntoa");
        return 1;
    }
    
    // Memulai membuka handler untuk live capture
    handle = pcap_open_live(
            dev,
            BUFSIZ,
            packet_count_limit,
            timeout_limit,
            error_buffer
            );

    packet = pcap_next(handle, &packet_header);

    print_packet_info(packet, packet_header);
    printf("Device : %s\n", dev);
    printf("IP address: %s\n", ip);
    printf("Subnet mask: %s\n", subnet_mask);
    return 0;
}
