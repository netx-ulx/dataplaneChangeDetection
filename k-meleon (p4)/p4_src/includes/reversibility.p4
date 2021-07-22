/********************************************************/
/*********** MAJORITY VOTE ALGORITHM (MJRTY) ************/
/********************************************************/
control RevertRow0(inout metadata meta, inout headers hdr) {
	apply{
        meta.src_offset = SKETCH_WIDTH;
        meta.dst_offset = 2*SKETCH_WIDTH;
        //compare candidate flow key with current flow key
        if (meta.epoch_bit == 0) {
            reg_mv_sketch0_row0.read(meta.tempsrc, meta.hash0+meta.src_offset);
            reg_mv_sketch0_row0.read(meta.tempdst, meta.hash0+meta.dst_offset);
            reg_mv_sketch0_row0.read(meta.tempcount, meta.hash0);
            if (meta.tempsrc!= hdr.ipv4.srcAddr || meta.tempdst != hdr.ipv4.dstAddr) { //if keys are different check counter
                if (meta.tempcount == 0){ //if counter is zero, add new key and compute absolute value of the resulting subtraction 1 - count
                    reg_mv_sketch0_row0.write(meta.hash0+meta.src_offset, hdr.ipv4.srcAddr);
                    reg_mv_sketch0_row0.write(meta.hash0+meta.dst_offset, hdr.ipv4.dstAddr);
                    meta.tempcount = 1;
                    reg_mv_sketch0_row0.write(meta.hash0, meta.tempcount);
                } else if (meta.tempcount > 0) { //if counter is not zero decrement counter by 1
                    meta.tempcount = meta.tempcount - 1;
                    reg_mv_sketch0_row0.write(meta.hash0, meta.tempcount);
                }		
            } else { // if keys are equal increment counter by 1
                meta.tempcount = meta.tempcount + 1;
                reg_mv_sketch0_row0.write(meta.hash0, meta.tempcount);
            }
        } else {
            reg_mv_sketch1_row0.read(meta.tempsrc, meta.hash0+meta.src_offset);
            reg_mv_sketch1_row0.read(meta.tempdst, meta.hash0+meta.dst_offset);
            reg_mv_sketch1_row0.read(meta.tempcount, meta.hash0);
            if (meta.tempsrc != hdr.ipv4.srcAddr || meta.tempdst != hdr.ipv4.dstAddr) { //if keys are different check counter
                if (meta.tempcount == 0){ //if counter is zero, add new key and compute absolute value of the resulting subtraction 1 - count
                    reg_mv_sketch1_row0.write(meta.hash0+meta.src_offset, hdr.ipv4.srcAddr);
                    reg_mv_sketch1_row0.write(meta.hash0+meta.dst_offset, hdr.ipv4.dstAddr);
                    meta.tempcount = 1;
                    reg_mv_sketch1_row0.write(meta.hash0, meta.tempcount);
                } else if (meta.tempcount > 0) { //if counter is not zero decrement counter by 1
                    meta.tempcount = meta.tempcount - 1;
                    reg_mv_sketch1_row0.write(meta.hash0, meta.tempcount);
                }		
            } else { // if keys are equal increment counter by 1
                meta.tempcount = meta.tempcount + 1;
                reg_mv_sketch1_row0.write(meta.hash0, meta.tempcount);
            }
        }
    }
}

control RevertRow1(inout metadata meta, inout headers hdr) {
	apply{
        meta.src_offset = SKETCH_WIDTH;
        meta.dst_offset = 2*SKETCH_WIDTH;
        //compare candidate flow key with current flow key
        if (meta.epoch_bit == 0) {
            reg_mv_sketch0_row1.read(meta.tempsrc, meta.hash1+meta.src_offset);
            reg_mv_sketch0_row1.read(meta.tempdst, meta.hash1+meta.dst_offset);
            reg_mv_sketch0_row1.read(meta.tempcount, meta.hash1);
            if (meta.tempsrc!= hdr.ipv4.srcAddr || meta.tempdst != hdr.ipv4.dstAddr) { //if keys are different check counter
                if (meta.tempcount == 0){ //if counter is zero, add new key and compute absolute value of the resulting subtraction 1 - count
                    reg_mv_sketch0_row1.write(meta.hash1+meta.src_offset, hdr.ipv4.srcAddr);
                    reg_mv_sketch0_row1.write(meta.hash1+meta.dst_offset, hdr.ipv4.dstAddr);
                    meta.tempcount = 1;
                    reg_mv_sketch0_row1.write(meta.hash1, meta.tempcount);
                } else if (meta.tempcount > 0) { //if counter is not zero decrement counter by 1
                    meta.tempcount = meta.tempcount - 1;
                    reg_mv_sketch0_row1.write(meta.hash1, meta.tempcount);
                }		
            } else { // if keys are equal increment counter by 1
                meta.tempcount = meta.tempcount + 1;
                reg_mv_sketch0_row1.write(meta.hash1, meta.tempcount);
            }
        } else {
            reg_mv_sketch1_row1.read(meta.tempsrc, meta.hash1+meta.src_offset);
            reg_mv_sketch1_row1.read(meta.tempdst, meta.hash1+meta.dst_offset);
            reg_mv_sketch1_row1.read(meta.tempcount, meta.hash1);
            if (meta.tempsrc != hdr.ipv4.srcAddr || meta.tempdst != hdr.ipv4.dstAddr) { //if keys are different check counter
                if (meta.tempcount == 0){ //if counter is zero, add new key and compute absolute value of the resulting subtraction 1 - count
                    reg_mv_sketch1_row1.write(meta.hash1+meta.src_offset, hdr.ipv4.srcAddr);
                    reg_mv_sketch1_row1.write(meta.hash1+meta.dst_offset, hdr.ipv4.dstAddr);
                    meta.tempcount = 1;
                    reg_mv_sketch1_row1.write(meta.hash1, meta.tempcount);
                } else if (meta.tempcount > 0) { //if counter is not zero decrement counter by 1
                    meta.tempcount = meta.tempcount - 1;
                    reg_mv_sketch1_row1.write(meta.hash1, meta.tempcount);
                }		
            } else { // if keys are equal increment counter by 1
                meta.tempcount = meta.tempcount + 1;
                reg_mv_sketch1_row1.write(meta.hash1, meta.tempcount);
            }
        }
    }
}

control RevertRow2(inout metadata meta, inout headers hdr) {
	apply{
        meta.src_offset = SKETCH_WIDTH;
        meta.dst_offset = 2*SKETCH_WIDTH;
        //compare candidate flow key with current flow key
        if (meta.epoch_bit == 0) {
            reg_mv_sketch0_row2.read(meta.tempsrc, meta.hash2+meta.src_offset);
            reg_mv_sketch0_row2.read(meta.tempdst, meta.hash2+meta.dst_offset);
            reg_mv_sketch0_row2.read(meta.tempcount, meta.hash2);
            if (meta.tempsrc!= hdr.ipv4.srcAddr || meta.tempdst != hdr.ipv4.dstAddr) { //if keys are different check counter
                if (meta.tempcount == 0){ //if counter is zero, add new key and compute absolute value of the resulting subtraction 1 - count
                    reg_mv_sketch0_row2.write(meta.hash2+meta.src_offset, hdr.ipv4.srcAddr);
                    reg_mv_sketch0_row2.write(meta.hash2+meta.dst_offset, hdr.ipv4.dstAddr);
                    meta.tempcount = 1;
                    reg_mv_sketch0_row2.write(meta.hash2, meta.tempcount);
                } else if (meta.tempcount > 0) { //if counter is not zero decrement counter by 1
                    meta.tempcount = meta.tempcount - 1;
                    reg_mv_sketch0_row2.write(meta.hash2, meta.tempcount);
                }		
            } else { // if keys are equal increment counter by 1
                meta.tempcount = meta.tempcount + 1;
                reg_mv_sketch0_row2.write(meta.hash2, meta.tempcount);
            }
        } else {
            reg_mv_sketch1_row2.read(meta.tempsrc, meta.hash2+meta.src_offset);
            reg_mv_sketch1_row2.read(meta.tempdst, meta.hash2+meta.dst_offset);
            reg_mv_sketch1_row2.read(meta.tempcount, meta.hash2);
            if (meta.tempsrc != hdr.ipv4.srcAddr || meta.tempdst != hdr.ipv4.dstAddr) { //if keys are different check counter
                if (meta.tempcount == 0){ //if counter is zero, add new key and compute absolute value of the resulting subtraction 1 - count
                    reg_mv_sketch1_row2.write(meta.hash2+meta.src_offset, hdr.ipv4.srcAddr);
                    reg_mv_sketch1_row2.write(meta.hash2+meta.dst_offset, hdr.ipv4.dstAddr);
                    meta.tempcount = 1;
                    reg_mv_sketch1_row2.write(meta.hash2, meta.tempcount);
                } else if (meta.tempcount > 0) { //if counter is not zero decrement counter by 1
                    meta.tempcount = meta.tempcount - 1;
                    reg_mv_sketch1_row2.write(meta.hash2, meta.tempcount);
                }		
            } else { // if keys are equal increment counter by 1
                meta.tempcount = meta.tempcount + 1;
                reg_mv_sketch1_row2.write(meta.hash2, meta.tempcount);
            }
        }
    }
}