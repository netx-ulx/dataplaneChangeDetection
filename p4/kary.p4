/* -* P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

const bit<16> TYPE_IPV4 = 0x800;
const bit<8> IP_PROTOCOLS_TCP        =   6;
const bit<8> IP_PROTOCOLS_UDP        =  17;
const bit<48> EPOCH_SIZE       		 =  20000000;
const bit<32> SKETCH_WIDTH			 =  20;
const bit<32> SKETCH_DEPTH			 =  3;

/*************************************************************
*****************   HEADERS *********************************
**************************************************************/

typedef bit<9> egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;

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

//define register arrays
//key fields
register<bit<64>>(SKETCH_WIDTH) sketch_key0; //src, dst
register<bit<64>>(SKETCH_WIDTH) sketch_key1; //sport, dport, proto

//sum fields
register<bit<1>>(1) sketch_flag; // 1 bit flag for forecasting sketch selection
register<bit<32>>(1) extra_op_counter; // counter for extra operation
register<bit<48>>(1) epoch; //timestamps require bit<48>

register<int<32>>(SKETCH_WIDTH*SKETCH_DEPTH) forecast_sketch0; 
register<int<32>>(SKETCH_WIDTH*SKETCH_DEPTH) forecast_sketch1; 
register<int<32>>(SKETCH_WIDTH*SKETCH_DEPTH) error_sketch0; // value for the count sketch
register<int<32>>(SKETCH_WIDTH*SKETCH_DEPTH) error_sketch1; // value for the count sketch
register<bit<1>>(SKETCH_WIDTH*SKETCH_DEPTH) control_flag; // 1 bit flag sketch


//count fields
register<int<32>>(SKETCH_WIDTH) sketch_count; // count for the mjrty

struct metadata {
    bit<32> hash;
	bit<32> hash0;
	bit<32> hash1;
	bit<32> hash2;
    bit<64> flowkey1;
    bit<64> flowkey2;
    bit<64> tempkey1;
    bit<64> tempkey2;
    int<32> tempcount;
    int<32> tempsum;
    bit<1> repass;
    bit<1> flag;

	bit<1> ctrl;
	bit<32> counter;
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


/*********************************************************
***************** PARSER *********************************
**********************************************************/

parser MyParser(packet_in packet,
	 	out headers hdr,
		inout metadata meta,
		inout standard_metadata_t standard_metadata) {

    state start {
	transition parse_ethernet;
    }

    state parse_ethernet {
	packet.extract(hdr.ethernet);
	transition select(hdr.ethernet.etherType) {
	    TYPE_IPV4: parse_ipv4;
	    default: accept;
	}
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition select(hdr.ipv4.fragOffset, hdr.ipv4.ihl,
                          hdr.ipv4.protocol) {
            (13w0x0, 4w0x5, IP_PROTOCOLS_TCP): parse_tcp;
            (13w0x0, 4w0x5, IP_PROTOCOLS_UDP): parse_udp;
            default: accept;
        }
    }

    state parse_tcp {
	packet.extract(hdr.tcp);
	transition accept;
    }

    state parse_udp {
	packet.extract(hdr.udp);
	transition accept;
    }
}

/*********************************************************
***************** CHECKSUM VERIFICATION *******************
**********************************************************/

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply { }
}


void UpdateRow(int num, inout metadata meta) {
	//SKETCH + FORECASTING MODULE
	sketch_flag.read(meta.flag,0);
	if (meta.flag == 1) { //Select the current forecast sketch
		control_flag.read(meta.ctrl,meta.hash); 
		if (meta.ctrl != meta.flag) { //If equals, copy forecast_sketch
			control_flag.write(meta.hash,1);
			
			forecast_sketch0.read(meta.forecast,meta.hash);
			
			//update error
			meta.new_err = 10 - meta.forecast;
			error_sketch1.write(meta.hash,meta.new_err);

			//update forecast
			meta.obs = 10 >> 1; //division by 2
			meta.aux_forecast = meta.forecast >> 1; //division by 2

			meta.new_forecast = meta.obs + meta.aux_forecast;

			forecast_sketch1.write(meta.hash,meta.new_forecast);

		} else { //else, only update with observed
			//update error
			error_sketch1.read(meta.err,meta.hash);
			meta.new_err = meta.err + 10;
			error_sketch1.write(meta.hash,meta.new_err);

			//update forecast
			forecast_sketch1.read(meta.forecast,meta.hash);
			meta.obs = 10 >> 1; //division by 2
			meta.new_forecast = meta.obs + meta.forecast;

			forecast_sketch1.write(meta.hash,meta.new_forecast);

			//compute one extra op
			extra_op_counter.read(meta.counter,0);
			if (meta.counter < SKETCH_WIDTH) {
				control_flag.read(meta.ctrl,meta.counter); 
				if (meta.ctrl != meta.flag) { //If diff, copy forecast_sketch
					control_flag.write(meta.counter,1);
					forecast_sketch0.read(meta.forecast,meta.counter);

					//update error
					meta.new_err = -meta.forecast; //negative
					error_sketch1.write(meta.counter,meta.new_err);

					//update forecast
					meta.new_forecast = meta.forecast >> 1; //division by 2
					forecast_sketch1.write(meta.counter,meta.new_forecast);
				}
				extra_op_counter.write(0,meta.counter+1);
			}
		}
	} else {
		control_flag.read(meta.ctrl,meta.hash); 
		if (meta.ctrl != meta.flag) { //If equals, copy forecast_sketch
			control_flag.write(meta.hash,0);
			
			forecast_sketch1.read(meta.forecast,meta.hash);
			
			//update error
			meta.new_err = 10 - meta.forecast;
			error_sketch0.write(meta.hash,meta.new_err);

			//update forecast
			meta.obs = 10 >> 1; //division by 2
			meta.aux_forecast = meta.forecast >> 1; //division by 2

			meta.new_forecast = meta.obs + meta.aux_forecast;

			forecast_sketch0.write(meta.hash,meta.new_forecast);

		} else { //else, only update with observed
			//update error
			error_sketch0.read(meta.err,meta.hash);
			meta.new_err = meta.err + 10;
			error_sketch0.write(meta.hash,meta.new_err);

			//update forecast
			forecast_sketch0.read(meta.forecast,meta.hash);
			meta.obs = 10 >> 1; //division by 2
			meta.new_forecast = meta.obs + meta.forecast;

			forecast_sketch0.write(meta.hash,meta.new_forecast);

			//compute one extra op
			extra_op_counter.read(meta.counter,0);
			if (meta.counter >= 0) {
				control_flag.read(meta.ctrl,meta.counter); 
				if (meta.ctrl != meta.flag) { //If diff, copy forecast_sketch
					control_flag.write(meta.counter,0);
					forecast_sketch1.read(meta.forecast,meta.counter);

					//update error
					meta.new_err = -meta.forecast; //negative
					error_sketch0.write(meta.counter,meta.new_err);

					//update forecast
					meta.new_forecast = meta.forecast >> 1; //division by 2
					forecast_sketch0.write(meta.counter,meta.new_forecast);
				}
				if (meta.counter != 0) {
					extra_op_counter.write(0,meta.counter-1);
				}
			}
		}
	}
} 

/*********************************************************
***************** INGRESS PROCESSING *******************
**********************************************************/

control MyIngress(inout headers hdr,
		  inout metadata meta,
		  inout standard_metadata_t standard_metadata) {
    action drop() {
	mark_to_drop(standard_metadata);
    }

    //forward all packets to the specified port
    action set_egr(egressSpec_t port) {
	standard_metadata.egress_spec = port;
    }

    //action: calculate hash functions
    //store hash index of each packet in metadata
    action cal_hash() {
	hash(meta.hash0, HashAlgorithm.crc32, 32w0, {meta.flowkey1, meta.flowkey2}, 11w19);
	hash(meta.hash1, HashAlgorithm.crc32, 32w0, {meta.flowkey1, meta.flowkey2}, 11w19);
	hash(meta.hash2, HashAlgorithm.crc32, 32w0, {meta.flowkey1, meta.flowkey2}, 11w19);
    }


    action copy_key_tcp() {
	meta.flowkey1[31:0] = hdr.ipv4.srcAddr;
	meta.flowkey1[63:32] = hdr.ipv4.dstAddr;
	meta.flowkey2[15:0] = hdr.tcp.srcPort;
	meta.flowkey2[31:16] = hdr.tcp.dstPort;
	meta.flowkey2[39:32] = hdr.ipv4.protocol;
    }

    action copy_key_udp() {
	meta.flowkey1[31:0] = hdr.ipv4.srcAddr;
	meta.flowkey1[63:32] = hdr.ipv4.dstAddr;
	meta.flowkey2[15:0] = hdr.udp.srcPort;
	meta.flowkey2[31:16] = hdr.udp.dstPort;
	meta.flowkey2[39:32] = hdr.ipv4.protocol;
    }

    table get_flowkey_tcp {
	actions = {
 	    copy_key_tcp;
  	}
	default_action = copy_key_tcp();

    }


    table get_flowkey_udp {
	actions = {
 	    copy_key_udp;
  	}
	default_action = copy_key_udp();

    }

    table forward {
	key = {
	    standard_metadata.ingress_port: exact;
	}
	actions = {
	    set_egr;
	    drop;
	}
	size = 1024;
	default_action = drop();
    }

    //calculate hash values
    table hash_index {
	actions = {
 	    cal_hash;
  	}
	default_action = cal_hash();
    }


    apply {
	if (hdr.ipv4.isValid()) {
	    //first pass
	    if (meta.repass == 0) {
			forward.apply();
			//construct flowkey information
			if (hdr.ipv4.protocol == IP_PROTOCOLS_TCP) {
				get_flowkey_tcp.apply();
			}
			if (hdr.ipv4.protocol == IP_PROTOCOLS_UDP) {
				get_flowkey_udp.apply();
			}

			//calculate hash value
			hash_index.apply();

			//check if new packet is inside current epoch or in the next one
			epoch.read(meta.epoch,0);
			if (standard_metadata.ingress_global_timestamp > meta.epoch) {
				meta.new_epoch = standard_metadata.ingress_global_timestamp + EPOCH_SIZE;
				epoch.write(0,meta.new_epoch);

				sketch_flag.read(meta.flag,0);
				if (meta.flag == 0) {
					sketch_flag.write(0,1);
					extra_op_counter.write(0,0);
				} else {
					sketch_flag.write(0,0);
					extra_op_counter.write(0,SKETCH_WIDTH-1);
				}
			}

			meta.hash = meta.hash0;
			UpdateRow(0,meta);
			meta.hash = meta.hash1 + SKETCH_WIDTH;
			UpdateRow(1,meta);
			meta.hash = meta.hash2 + SKETCH_WIDTH + SKETCH_WIDTH;
			UpdateRow(2,meta);

			//compare candidate flow key with current flow key
			meta.flag = 0;
			sketch_key0.read(meta.tempkey1, meta.hash0);
			if (meta.tempkey1 != meta.flowkey1) {
				meta.flag = 1;
			}
			sketch_key1.read(meta.tempkey2, meta.hash0);
			if (meta.tempkey2 != meta.flowkey2) {
				meta.flag = 1;
			}

			sketch_count.read(meta.tempcount, meta.hash0);
			if (meta.flag == 1 && meta.tempcount == 0) {
				meta.repass = 1;
			}
			if (meta.flag == 0) {
				meta.tempcount = meta.tempcount + 1;
			} else if (meta.tempcount > 0){
				meta.tempcount = meta.tempcount - 1;
			}
			sketch_count.write(meta.hash0, meta.tempcount);

			if (meta.repass  == 1) {
				resubmit({meta.repass, meta.flowkey1, meta.flowkey2, meta.hash0});
			}

		} else { //second pass
			sketch_key0.write(meta.hash0, meta.flowkey1);
			sketch_key1.write(meta.hash0, meta.flowkey2);
			sketch_count.read(meta.tempcount, meta.hash0);
			meta.tempcount = 1 - meta.tempcount;
			sketch_count.write(meta.hash0, meta.tempcount);
		}
	}
    }
}



/*********************************************************
***************** EGRESS PROCESSING *******************
**********************************************************/

control MyEgress(inout headers hdr,
		 inout metadata meta,
		 inout standard_metadata_t standard_metadata) {
    apply { }
}

/*********************************************************
***************** CHECKSUM COMPUTATION *******************
**********************************************************/

control MyComputeChecksum(inout headers hdr, inout metadata meta) {
    apply{
	update_checksum(
	    hdr.ipv4.isValid(),
	    { hdr.ipv4.version,
	      hdr.ipv4.ihl,
	      hdr.ipv4.diffserv,
	      hdr.ipv4.totalLen,
	      hdr.ipv4.identification,
	      hdr.ipv4.flags,
	      hdr.ipv4.fragOffset,
	      hdr.ipv4.ttl,
	      hdr.ipv4.protocol,
	      hdr.ipv4.srcAddr,
	      hdr.ipv4.dstAddr},
	      hdr.ipv4.hdrChecksum,
	      HashAlgorithm.csum16);
    }
}


/*********************************************************
***************** DEPARSER *******************************
**********************************************************/

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
	packet.emit(hdr.ethernet);
	packet.emit(hdr.ipv4);
        packet.emit(hdr.tcp);
        packet.emit(hdr.udp);

    }
}


/*********************************************************
***************** SWITCH *******************************
**********************************************************/

V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main;
