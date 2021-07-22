/*
*						MODULO FUNCTIONALITY
* These control blocks are meant to store keys for k-meleon error sketch so to enable
* the sketch reversibility, that is, the possibility to track keys responsible for large errors (changes). 
* To reduce the number of keys to be stored per epoch to the size (SKETCH_DEPTH*SKETCH_WIDTH) of the error
* sketch at worst, this modulo uses the voting algorithm1 proposed in the MV-Sketch paper (INFOCOM19) to 
* elect a key to be stored based on observed counters for stored keys. 
*/


/* 
*  The three control blocks here presented contain the same exact code
*  yet applied to different register memories. So, it is sufficient to 
*  check only the logic of one block to understand the operations which
*  are performed identically on the different h=3 rows of the sketch
*  data structures.
*/

control RevertRow0(inout metadata meta) {

apply {

	    //compare candidate flow key with current flow key
		reg_flowsrc_row0.read(meta.stored_flowsrc, meta.hash0_value);
		reg_flowdst_row0.read(meta.stored_flowdst, meta.hash0_value);
		reg_flowKey_count_row0.read(meta.flowKey_count, meta.hash0_value);

		if ( meta.stored_flowsrc != meta.current_flowsrc || meta.stored_flowdst != meta.current_flowdst ) { //if keys are different check counter

			if (meta.flowKey_count == 0) { 

				reg_flowsrc_row0.write(meta.hash0_value, meta.current_flowsrc);
				reg_flowdst_row0.write(meta.hash0_value, meta.current_flowdst);
				reg_flowKey_count_row0.write(meta.hash0_value, meta.flowKey_count + 1);

			} else if (meta.flowKey_count > 0) { //if counter is not zero decrement counter by 1

				reg_flowKey_count_row0.write(meta.hash0_value, meta.flowKey_count - 1);

			}	

		} else { // the current key corresponds to the stored key, then increment the counter

			reg_flowKey_count_row0.write(meta.hash0_value, meta.flowKey_count + 1);
		}
	}
}

control RevertRow1(inout metadata meta) {

apply {

	    //compare candidate flow key with current flow key
		reg_flowsrc_row1.read(meta.stored_flowsrc, meta.hash0_value);
		reg_flowdst_row1.read(meta.stored_flowdst, meta.hash0_value);
		reg_flowKey_count_row1.read(meta.flowKey_count, meta.hash1_value);

		if ( meta.stored_flowsrc != meta.current_flowsrc || meta.stored_flowdst != meta.current_flowdst ) { //if keys are different check counter

			if (meta.flowKey_count == 0) { 

				reg_flowsrc_row1.write(meta.hash0_value, meta.current_flowsrc);
				reg_flowdst_row1.write(meta.hash0_value, meta.current_flowdst);
				reg_flowKey_count_row1.write(meta.hash1_value, meta.flowKey_count + 1);

			} else if (meta.flowKey_count > 0) { //if counter is not zero decrement counter by 1

				reg_flowKey_count_row1.write(meta.hash1_value, meta.flowKey_count - 1);

			}	

		} else { // the current key corresponds to the stored key, then increment the counter

			reg_flowKey_count_row1.write(meta.hash1_value, meta.flowKey_count + 1);
		}
	}
}

control RevertRow2(inout metadata meta) {

apply {

	    //compare candidate flow key with current flow key
		reg_flowsrc_row2.read(meta.stored_flowsrc, meta.hash0_value);
		reg_flowdst_row2.read(meta.stored_flowdst, meta.hash0_value);
		reg_flowKey_count_row2.read(meta.flowKey_count, meta.hash2_value);

		if ( meta.stored_flowsrc != meta.current_flowsrc || meta.stored_flowdst != meta.current_flowdst ) { //if keys are different check counter

			if (meta.flowKey_count == 0) { 

				reg_flowsrc_row2.write(meta.hash0_value, meta.current_flowsrc);
				reg_flowdst_row2.write(meta.hash0_value, meta.current_flowdst);
				reg_flowKey_count_row2.write(meta.hash2_value, meta.flowKey_count + 1);

			} else if (meta.flowKey_count > 0) { //if counter is not zero decrement counter by 1

				reg_flowKey_count_row2.write(meta.hash2_value, meta.flowKey_count - 1);

			}	

		} else { // the current key corresponds to the stored key, then increment the counter

			reg_flowKey_count_row2.write(meta.hash2_value, meta.flowKey_count + 1);
		}
	}
}
