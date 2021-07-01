typedef bit<9> egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;

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
	/* To index the sketch cells */
	bit<32> hash0_value;
	bit<32> hash1_value;
	bit<32> hash2_value;
	/* ------------------------ */
	/* To manage epoch changes  */
    bit<1> epoch_bit;
	bit<1> ctrl_bit;
    bit<1> first_epoch_flag;
    bit<1> epoch_changed_flag;
    bit<1> ctrl_changed_flag;
	bit<32> offset; // to read the proper epoch values from the skecth registers
	bit<48> epoch_value; // epoch in # of packets or bmv2 ingress-timestamp (<48>)
	/* ------------------------ */
	/* To compute sketch updates */
	int<32> obs;
	int<32> err;
	int<32> forecast;
	int<32> aux_forecast;
	int<32> new_forecast;
	int<32> new_err;
	/* ------------------------ */
	#ifdef REVERT
    bit<64> current_flowKey;
    bit<64> stored_flowKey;
    int<32> flowKey_count;
	#endif
	/* ------------------------ */
	#ifdef COUNT_PKT
    int<32> num_packets;
	#endif
	/* ------------------------ */
	#ifdef EXTRA_OP
	bit<32> extraOp_counter;
	#endif
}

struct headers {
    ethernet_t ethernet;
    ipv4_t ipv4;
    tcp_t tcp;
    udp_t udp;
}
