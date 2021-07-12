/* -* P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

#include "includes/constants.p4"
#include "includes/macros.p4"
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

#ifdef REVERT
	#include "includes/reversibility.p4"
#endif

/*********************************************************
***************** INGRESS PROCESSING *******************
**********************************************************/

control MyIngress(inout headers hdr,
		  inout metadata meta,
		  inout standard_metadata_t standard_metadata) {

	UpdateRow0() update_row0;
	UpdateRow1() update_row1;
	UpdateRow2() update_row2;

	UpdateRow_Epoch1_Row0() update_epoch1_row0;
	UpdateRow_Epoch1_Row1() update_epoch1_row1;
	UpdateRow_Epoch1_Row2() update_epoch1_row2;


	#ifdef REVERT
	RevertRow0() revert_row0;
	RevertRow1() revert_row1;
	RevertRow2() revert_row2;
	#endif


    action drop() {
		mark_to_drop(standard_metadata);
    }

    // specify the output port for the current pkt
    action set_egr(egressSpec_t port) {
		standard_metadata.egress_spec = port;
    }

    // calculate hash functions and store values in metadata
    action calc_hash() {

		hash(meta.hash0_value, HashAlgorithm.crc32_custom, 64w0, {hdr.ipv4.srcAddr,hdr.ipv4.dstAddr}, SKETCH_WIDTH); //hash value for first row of the count sketch
		hash(meta.hash1_value, HashAlgorithm.crc32_custom, 64w0, {hdr.ipv4.srcAddr,hdr.ipv4.dstAddr}, SKETCH_WIDTH); //hash value for second row of the count sketch
		hash(meta.hash2_value, HashAlgorithm.crc32_custom, 64w0, {hdr.ipv4.srcAddr,hdr.ipv4.dstAddr}, SKETCH_WIDTH); //hash value for third row of the count sketch
    }

    // add the offset to the indexes
    action update_indexes() {
		meta.hash0_value = meta.hash0_value + meta.offset;
		meta.hash1_value = meta.hash1_value + meta.offset;
		meta.hash2_value = meta.hash2_value + meta.offset;
    }


    table forward_tbl {
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

		// above a certain rate bmv2 starts dropping pkts, so we used to track the packets processed by it
		#ifdef COUNT_PKT

		reg_total_num_packets.read(meta.num_packets,0);
		meta.num_packets = meta.num_packets + 1;
		reg_total_num_packets.write(0,meta.num_packets);

		#endif /* COUNT_PKT */



		if (hdr.ipv4.isValid()) {

			forward_tbl.apply(); // simple fw table to specify egress port based on the input port

			//calculate hash values for the the h rows of the count sketch - h=3 in this program
			calc_hash();

			/***************** EPOCH VERIFICATION *******************/

			reg_epoch_value.read(meta.epoch_value,0);
			
			#ifdef EPOCH_PKT /* epoch calculated with the number of packets processed */

			if ( meta.epoch_value >= EPOCH_SIZE) { 

				reg_epoch_value.write(0,1); //reset packet counter for the current epoch

			#elif EPOCH_TS /* epoch calculated as time interval */

			if ( (standard_metadata.ingress_global_timestamp - meta.epoch_value) >= EPOCH_SIZE) { 

				reg_epoch_value.write(0, standard_metadata.ingress_global_timestamp);

			#endif /* EPOCH TS Or PKT */

				// start new epoch by flipping the epoch bit
				reg_epoch_bit.read(meta.epoch_bit,0);

				if (meta.epoch_bit == 0) {
					reg_epoch_bit.write(0,1);
					meta.offset = SKETCH_WIDTH;
				} else {
					reg_epoch_bit.write(0,0);
					meta.offset = 0;
				}

				# flag to signal that epoch has changed
				meta.epoch_changed_flag = 1;

			}

			/********************************************************/
		

			// we have 1-bit register to apply a different forecast formula (EWMA for t=2) to the sketch structures only in the 1st epoch
			// we use a somehow counterintuitive choice of a value of 0 meaning this is the first epoch and a value of 1 otherwise
 			// since a register cannot be initialized to any value in the P4 program itself
			reg_first_epoch_flag.read(meta.first_epoch_flag,0);

			if ( meta.epoch_changed_flag == 1) {
				
				meta.first_epoch_flag = 1;
				reg_first_epoch_flag.write(0,meta.first_epoch_flag); // from now on, this register will always hold the value 1 

				// update the indexes with the offsets to read sketch values for the current epoch
				update_indexes();

				#ifdef EXTRA_OP
					// reset the extraOp counters
					reg_extraOp_counter.write(0,SKETCH_WIDTH-1);
					reg_extraOp_counter.write(1,SKETCH_WIDTH-1);
					reg_extraOp_counter.write(2,SKETCH_WIDTH-1);
				#endif
			}
			else {

				reg_epoch_bit.read(meta.epoch_bit,0);

				#ifdef EPOCH_PKT /* epoch calculated with the number of packets processed */
	
				// increment the number of packets in the current epoch
				reg_epoch_value.write(0,meta.epoch_value + 1);

				#endif
			}



			#ifdef COUNT_PKT
			reg_packet_changed.write(0,meta.num_packets); // I am not sure what this was meant for
			#endif
			

			/******************* UPDATE "CYCLE" *********************/
			// the same set of operations are applied to the h=3 rows of k-meleon data structures

			//update first row - h0
			update_row0.apply(meta);

			// the following additional update of the data structures only happens once in the first epoch (EWMA for t=2)
			if(meta.first_epoch_flag == 0) {
				update_epoch1_row0.apply(meta);
			}

			#ifdef REVERT
			meta.current_flowsrc = hdr.ipv4.srcAddr;
			meta.current_flowdst = hdr.ipv4.dstAddr;
			revert_row0.apply(meta);
			#endif

			//update second row - h1
			update_row1.apply(meta);

			// the following additional update of the data structures only happens once in the first epoch (EWMA for t=2)
			if(meta.first_epoch_flag == 0) {
				update_epoch1_row1.apply(meta);
			}

			#ifdef REVERT
			revert_row1.apply(meta);
			#endif

			//update third row - h2
			update_row2.apply(meta);

			// the following additional update of the data structures only happens once in the first epoch (EWMA for t=2)
			if(meta.first_epoch_flag == 0) {
				update_epoch1_row2.apply(meta);
			}

			#ifdef REVERT
			revert_row2.apply(meta);
			#endif

		}

    } // endif ipv4.isValid()

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
