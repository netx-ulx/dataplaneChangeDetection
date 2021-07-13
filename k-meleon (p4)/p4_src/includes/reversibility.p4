/********************************************************/
/*********** MAJORITY VOTE ALGORITHM (MJRTY) ************/
/********************************************************/
control RevertRow(inout metadata meta, inout headers hdr) {
	apply{
        //compare candidate flow key with current flow key
        if (meta.epoch_bit == 0) {
            reg_srcAddr_f0.read(meta.tempsrc, meta.hash);
            reg_dstAddr_f0.read(meta.tempdst, meta.hash);
            reg_sketch_count_f0.read(meta.tempcount, meta.hash);
            if (meta.tempsrc!= hdr.ipv4.srcAddr || meta.tempdst != hdr.ipv4.dstAddr) { //if keys are different check counter
                if (meta.tempcount == 0){ //if counter is zero, add new key and compute absolute value of the resulting subtraction 1 - count
                    reg_srcAddr_f0.write(meta.hash, hdr.ipv4.srcAddr);
                    reg_dstAddr_f0.write(meta.hash, hdr.ipv4.dstAddr);
                    meta.tempcount = 1;
                    reg_sketch_count_f0.write(meta.hash, meta.tempcount);
                } else if (meta.tempcount > 0) { //if counter is not zero decrement counter by 1
                    meta.tempcount = meta.tempcount - 1;
                    reg_sketch_count_f0.write(meta.hash, meta.tempcount);
                }		
            } else { // if keys are equal increment counter by 1
                meta.tempcount = meta.tempcount + 1;
                reg_sketch_count_f0.write(meta.hash, meta.tempcount);
            }
        } else {
            reg_srcAddr_f1.read(meta.tempsrc, meta.hash);
            reg_dstAddr_f1.read(meta.tempdst, meta.hash);
            reg_sketch_count_f1.read(meta.tempcount, meta.hash);
            if (meta.tempsrc != hdr.ipv4.srcAddr || meta.tempdst != hdr.ipv4.dstAddr) { //if keys are different check counter
                if (meta.tempcount == 0){ //if counter is zero, add new key and compute absolute value of the resulting subtraction 1 - count
                    reg_srcAddr_f1.write(meta.hash, hdr.ipv4.srcAddr);
                    reg_dstAddr_f1.write(meta.hash, hdr.ipv4.dstAddr);
                    meta.tempcount = 1;
                    reg_sketch_count_f1.write(meta.hash, meta.tempcount);
                } else if (meta.tempcount > 0) { //if counter is not zero decrement counter by 1
                    meta.tempcount = meta.tempcount - 1;
                    reg_sketch_count_f1.write(meta.hash, meta.tempcount);
                }		
            } else { // if keys are equal increment counter by 1
                meta.tempcount = meta.tempcount + 1;
                reg_sketch_count_f1.write(meta.hash, meta.tempcount);
            }
        }
    }
}