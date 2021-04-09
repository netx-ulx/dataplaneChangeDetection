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
***************** MAIN UPDATE FUNCTION ********************
**********************************************************/

void KARY_UpdateRow(int num, inout metadata meta) {
	//SKETCH + FORECASTING MODULE
	if (meta.flag == 1) { //Select the current forecast sketch
		control_flag.read(meta.ctrl,meta.hash); 
		if (meta.ctrl != meta.flag) { //If equals, copy forecast_sketch
			control_flag.write(meta.hash,1);
			
			forecast_sketch_f1.read(meta.forecast,meta.hash);
			
			//update error
			meta.new_err = 10 - meta.forecast;
			error_sketch_f1.write(meta.hash,meta.new_err);

			//update forecast
			meta.obs = 10 >> 1; //division by 2
			meta.aux_forecast = meta.forecast >> 1; //division by 2

			meta.new_forecast = meta.obs + meta.aux_forecast;

			forecast_sketch_f0.write(meta.hash,meta.new_forecast);
		} else { //else, only update with observed
			//update error
			error_sketch_f1.read(meta.err,meta.hash);
			meta.new_err = meta.err + 10;
			error_sketch_f1.write(meta.hash,meta.new_err);

			//update forecast
			forecast_sketch_f0.read(meta.forecast,meta.hash);
			meta.obs = 10 >> 1; //division by 2
			meta.new_forecast = meta.obs + meta.forecast;

			forecast_sketch_f0.write(meta.hash,meta.new_forecast);

			//compute one extra op
			extra_op_counter.read(meta.counter,num);
			if (meta.counter < SKETCH_WIDTH) {
				control_flag.read(meta.ctrl,meta.counter+meta.offset); 
				if (meta.ctrl != meta.flag) { //If diff, copy forecast_sketch
					control_flag.write(meta.counter+meta.offset,1);
					forecast_sketch_f1.read(meta.forecast,meta.counter+meta.offset);

					//update error
					meta.new_err_op = -meta.forecast; //negative
					error_sketch_f1.write(meta.counter+meta.offset,meta.new_err_op);

					//update forecast
					meta.new_forecast = meta.forecast >> 1; //division by 2
					forecast_sketch_f0.write(meta.counter+meta.offset,meta.new_forecast);
				}
				extra_op_counter.write(num,meta.counter+1);
			}
		}
	} else {
		control_flag.read(meta.ctrl,meta.hash); 
		if (meta.ctrl != meta.flag) { //If equals, copy forecast_sketch
			control_flag.write(meta.hash,0);
			
			forecast_sketch_f0.read(meta.forecast,meta.hash);
			
			//update error
			meta.new_err = 10 - meta.forecast;
			error_sketch_f0.write(meta.hash,meta.new_err);

			//update forecast
			meta.obs = 10 >> 1; //division by 2
			meta.aux_forecast = meta.forecast >> 1; //division by 2

			meta.new_forecast = meta.obs + meta.aux_forecast;

			forecast_sketch_f1.write(meta.hash,meta.new_forecast);

		} else { //else, only update with observed
			//update error
			error_sketch_f0.read(meta.err,meta.hash);
			meta.new_err = meta.err + 10;
			error_sketch_f0.write(meta.hash,meta.new_err);

			//update forecast
			forecast_sketch_f1.read(meta.forecast,meta.hash);
			meta.obs = 10 >> 1; //division by 2
			meta.new_forecast = meta.obs + meta.forecast;

			forecast_sketch_f1.write(meta.hash,meta.new_forecast);

			//compute one extra op
			extra_op_counter.read(meta.counter,num);
			if (meta.counter >= 0) {
				control_flag.read(meta.ctrl,meta.counter+meta.offset); 
				if (meta.ctrl != meta.flag) { //If diff, copy forecast_sketch
					control_flag.write(meta.counter+meta.offset,0);
					forecast_sketch_f0.read(meta.forecast,meta.counter+meta.offset);

					//update error
					meta.new_err_op = -meta.forecast; //negative
					error_sketch_f0.write(meta.counter+meta.offset,meta.new_err_op);

					//update forecast
					meta.new_forecast = meta.forecast >> 1; //division by 2
					forecast_sketch_f1.write(meta.counter+meta.offset,meta.new_forecast);
				}
				if (meta.counter != 0) {
					extra_op_counter.write(num,meta.counter-1);
				}
			}
		}
	}
	if (meta.new_err > 0) {
		mv.write(num,1);
	} else {
		mv.write(num,0);
	}
}

/********************************************************/
/*********** MAJORITY VOTE ALGORITHM (MJRTY) ************/
/********************************************************/
void MV_UpdateRow(inout metadata meta, inout headers hdr) {
	//compare candidate flow key with current flow key
	if (meta.flag == 0) {
		srcAddr_f0.read(meta.tempsrc, meta.hash);
		dstAddr_f0.read(meta.tempdst, meta.hash);
		sketch_count_f0.read(meta.tempcount, meta.hash);
		if (meta.tempsrc!= hdr.ipv4.srcAddr || meta.tempdst != hdr.ipv4.dstAddr) { //if keys are different check counter
			if (meta.tempcount == 0){ //if counter is zero, add new key and compute absolute value of the resulting subtraction 1 - count
				srcAddr_f0.write(meta.hash, hdr.ipv4.srcAddr);
				dstAddr_f0.write(meta.hash, hdr.ipv4.dstAddr);
				meta.tempcount = 1;
				sketch_count_f0.write(meta.hash, meta.tempcount);
			} else if (meta.tempcount > 0) { //if counter is not zero decrement counter by 1
				meta.tempcount = meta.tempcount - 1;
				sketch_count_f0.write(meta.hash, meta.tempcount);
			}		
		} else { // if keys are equal increment counter by 1
			meta.tempcount = meta.tempcount + 1;
			sketch_count_f0.write(meta.hash, meta.tempcount);
		}
	} else {
		srcAddr_f1.read(meta.tempsrc, meta.hash);
		dstAddr_f1.read(meta.tempdst, meta.hash);
		sketch_count_f1.read(meta.tempcount, meta.hash);
		if (meta.tempsrc != hdr.ipv4.srcAddr || meta.tempdst != hdr.ipv4.dstAddr) { //if keys are different check counter
			if (meta.tempcount == 0){ //if counter is zero, add new key and compute absolute value of the resulting subtraction 1 - count
				srcAddr_f1.write(meta.hash, hdr.ipv4.srcAddr);
				dstAddr_f1.write(meta.hash, hdr.ipv4.dstAddr);
				meta.tempcount = 1;
				sketch_count_f1.write(meta.hash, meta.tempcount);
			} else if (meta.tempcount > 0) { //if counter is not zero decrement counter by 1
				meta.tempcount = meta.tempcount - 1;
				sketch_count_f1.write(meta.hash, meta.tempcount);
			}		
		} else { // if keys are equal increment counter by 1
			meta.tempcount = meta.tempcount + 1;
			sketch_count_f1.write(meta.hash, meta.tempcount);
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
		total_num_packets.read(meta.num_packets,0);
		meta.num_packets = meta.num_packets + 1;
		total_num_packets.write(0,meta.num_packets);

		if (hdr.ipv4.isValid()) {
			forward.apply();

			//calculate hash value
			cal_hash();

			/********************************************************/
			/***************** EPOCH VERIFICATION *******************/

			epoch.read(meta.epoch,0);
			sketch_flag.read(meta.flag,0);
			first.read(meta.first,0);
			//check if new packet is inside current epoch or in the next one
			if (meta.epoch >= EPOCH_SIZE) { 
				epoch.write(0,1); //reset packet counter
				first.write(0,1);
				// start new epoch by changing sketch flag and resetting other counters
				if (meta.flag == 0) {
					meta.flag = 1;
					sketch_flag.write(0,meta.flag);
					extra_op_counter.write(0,0);
					extra_op_counter.write(1,0);
					extra_op_counter.write(2,0);
				} else {
					meta.flag = 0;
					sketch_flag.write(0,meta.flag);
					extra_op_counter.write(0,SKETCH_WIDTH-1);
					extra_op_counter.write(1,SKETCH_WIDTH-1);
					extra_op_counter.write(2,SKETCH_WIDTH-1);
				}
				packet_changed.write(0,meta.num_packets);
			} else {
				// increment number of packets in this epoch
				meta.epoch = meta.epoch + 1;
				epoch.write(0,meta.epoch);
			}

			/********************************************************/
			/******************* UPDATE "CYCLE" *********************/

			//compute offset for first row, update first row
			meta.hash = meta.hash0;
			KARY_UpdateRow(0,meta);
			if(meta.first == 0) {
				KARY_UpdateRow(0,meta);
			}

			MV_UpdateRow(meta,hdr);

			//compute offset for second row, update second row
			meta.offset = SKETCH_WIDTH;
			meta.hash = meta.hash1 + meta.offset;
			KARY_UpdateRow(1,meta);
			if(meta.first == 0) {
				KARY_UpdateRow(1,meta);
			}

			MV_UpdateRow(meta,hdr);

			//compute offset for third row, update third row
			meta.offset = SKETCH_WIDTH + SKETCH_WIDTH;
			meta.hash = meta.hash2 + meta.offset;

			KARY_UpdateRow(2,meta);
			if(meta.first == 0) {
				KARY_UpdateRow(2,meta);
			}

			MV_UpdateRow(meta,hdr);

		} else {
			//epoch.read(meta.epoch,0);
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
