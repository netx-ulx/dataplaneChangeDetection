/* -* P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

#include "includes/constants.p4"
#include "includes/types.p4"
#include "includes/headers.p4"
#include "includes/registers.p4"


/***************** PARSER *********************************/

#include "includes/parser.p4"


/*********************************************************
***************** CHECKSUM VERIFICATION *******************
**********************************************************/

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply { }
}

/*********************************************************
***************** UPDATE CONTROL BLOCKS ******************
**********************************************************/

#include "includes/controls.p4"


/*********************************************************
************** REVERSIBILITY CONTROL BLOCKS **************
**********************************************************/

#include "includes/reversibility.p4"


/*********************************************************
***************** INGRESS PROCESSING *******************
**********************************************************/

control MyIngress(inout headers hdr,
		  inout metadata meta,
		  inout standard_metadata_t standard_metadata) {
    
	UpdateRow0() update_row0;
	UpdateRow1() update_row1;
	UpdateRow2() update_row2;
	
	UpdateEpoch1Row0() update_epoch1_row0;
	UpdateEpoch1Row1() update_epoch1_row1;
	UpdateEpoch1Row2() update_epoch1_row2;
	
	RevertRow() revert_row;
	
	
	
	action drop() {
	mark_to_drop(standard_metadata);
    }

    //forward packets to the specified port
    action set_egr(egressSpec_t port) {
	standard_metadata.egress_spec = port;
    }

    //action: calculate hash functions
    //store hash index of each packet in metadata
    action cal_hash() {
	hash(meta.hash0, HashAlgorithm.crc32_custom, 64w0, {hdr.ipv4.srcAddr,hdr.ipv4.dstAddr}, SKETCH_WIDTH); //hash for first row
	hash(meta.hash1, HashAlgorithm.crc32_custom, 64w0, {hdr.ipv4.srcAddr,hdr.ipv4.dstAddr}, SKETCH_WIDTH); //hash for second row
	hash(meta.hash2, HashAlgorithm.crc32_custom, 64w0, {hdr.ipv4.srcAddr,hdr.ipv4.dstAddr}, SKETCH_WIDTH); //hash for third row
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


    apply {
		reg_total_num_packets.read(meta.num_packets,0);
		meta.num_packets = meta.num_packets + 1;
		reg_total_num_packets.write(0,meta.num_packets);

		if (hdr.ipv4.isValid()) {
			forward.apply();

			//calculate hash value
			cal_hash();

			/********************************************************/
			/***************** EPOCH VERIFICATION *******************/

			reg_epoch_value.read(meta.epoch_value,0);
			reg_epoch_bit.read(meta.epoch_bit,0);
			reg_first_epoch_flag.read(meta.first_epoch_flag,0);
			//check if new packet is inside current epoch or in the next one
			if (meta.epoch_value >= EPOCH_SIZE) { 
				reg_epoch_value.write(0,1); //reset packet counter
				meta.first_epoch_flag = 1;
				reg_first_epoch_flag.write(0,meta.first_epoch_flag);
				// start new epoch by changing sketch flag and resetting other counters
				if (meta.epoch_bit == 0) {
					meta.epoch_bit = 1;
					reg_epoch_bit.write(0,meta.epoch_bit);
				} else {
					meta.epoch_bit = 0;
					reg_epoch_bit.write(0,meta.epoch_bit);
				}
				reg_extraOp_counter.write(0,0);
				reg_extraOp_counter.write(1,0);
				reg_extraOp_counter.write(2,0);
				reg_packet_changed.write(0,meta.num_packets);
			} else {
				// increment number of packets in this epoch
				meta.epoch_value = meta.epoch_value + 1;
				reg_epoch_value.write(0,meta.epoch_value);
			}

			/********************************************************/
			/******************* UPDATE "CYCLE" *********************/

			if(meta.first_epoch_flag == 0) {
				// first row
				update_epoch1_row0.apply(meta);

				// second row
				update_epoch1_row1.apply(meta);

				// third row
				update_epoch1_row2.apply(meta);
			} else {
				// first row
				meta.hash = meta.hash0;
				update_row0.apply(meta);
				revert_row.apply(meta,hdr);

				// second row
				meta.offset = SKETCH_WIDTH;
				meta.hash = meta.hash1;
				update_row1.apply(meta);
				revert_row.apply(meta,hdr);

				// third row
				meta.offset = SKETCH_WIDTH + SKETCH_WIDTH;
				meta.hash = meta.hash2 + meta.offset;
				update_row2.apply(meta);
				revert_row.apply(meta,hdr);
			}

		} else {
			//reg_epoch.read(meta.epoch,0);
			//meta.epoch = meta.epoch + 1;
			//epoch.write(0,meta.epoch); //reset packet counter
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
