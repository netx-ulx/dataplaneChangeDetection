/*************************************************************
*****************   HEADERS *********************************
**************************************************************/

header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16> etherType;
}


header ipv4_t {
    bit<4>  version;
    bit<4>  ihl;
    bit<8>  diffserv;
    bit<16> totalLen;
    bit<16> identification;
    bit<3>  flags;
    bit<13> fragOffset;
    bit<8>  ttl;
    bit<8>  protocol;
    bit<16> hdrChecksum;
    ip4Addr_t srcAddr;
    ip4Addr_t dstAddr;
}

header tcp_t {
    bit<16> srcPort;
    bit<16> dstPort;
    bit<32> seqNo;
    bit<32> ackNo;
    bit<4> dataOffset;
    bit<4> res;
    bit<8> flags;
    bit<16> window;
    bit<16> checksum;
    bit<16> urgentPtr;
}

header udp_t {
    bit<16> srcPort;
    bit<16> dstPort;
    bit<16> length_;
    bit<16> checksum;
}

struct metadata {
    bit<32> hash;
	bit<32> hash0;
	bit<32> hash1;
	bit<32> hash2;
    bit<64> key;
    bit<64> flowkey;
    bit<32> tempsrc;
    bit<32> tempdst;
    int<32> tempcount;
    int<32> tempsum;
    bit<1> repass;
    bit<1> flag;

	bit<1> ctrl;
	bit<32> counter;
	bit<32> offset;
	int<32> obs;
	int<32> err;
	bit<48> epoch; //timestamps require bit<48>
	bit<48> new_epoch; //timestamps require bit<48>
	int<32> forecast;
	int<32> aux_forecast;
	int<32> new_forecast;
	int<32> new_err;
}

struct headers {
    ethernet_t ethernet;
    ipv4_t ipv4;
    tcp_t tcp;
    udp_t udp;
}
