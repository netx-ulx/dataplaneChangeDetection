/*
*					MODULO FUNCTIONALITY
* The basic design of k-meleon has the limitation that the cells of the 
* sketch data structures are only updated whether a packet is hashed into
* those. However, in the ideal case, the algorithm should copy entirely the
* forecast sketch Sf(t) into the error sketch Se(t) and in the forecast for
* the next epoch Sf(t+1). 
* In this bmv2 design, to reduce the likelihood of not copying some cells
* of Sf(t), we have tried to copy an additional cell per packet after the
* actual copies for the current packet are performed.
*/

/* 
*  The three control blocks here presented contain the same exact code
*  yet applied to different register memories. So, it is sufficient to 
*  check only the logic of one block to understand the operations which
*  are performed identically on the different h=3 rows of the sketch
*  data structures.
*/

control ExtraOpRow0(inout metadata meta) {

apply{

		// Read the extra operations available per this sketch row
		// if there are some for the current epoch, perform one (next block of code)
		// decrement the counter
		meta.extraOp = 0;
		reg_extraOp_counter.read(meta.extraOp_counter,0)

		if( meta.extraOp_counter > 0 ){

			reg_extraOp_counter.write(0,meta.extraOp_counter-1);

			meta.extraOp = 1;

		}

		// if there are extra operations to be performed in the current epoch
		// Max number of extra operations per epoch equals the sketch width
		if ( meta.extraOp == 1 ) {

			reg_controlFlag_sketch0.read(meta.ctrl_bit,meta.extraOp_counter); 

			if (meta.ctrl_bit != meta.epoch_flag) {

				// to me the next is an error, you should update with the value of the epoch_flag 
				//reg_controlFlag_sketch0.write(meta.extraOp_counter,1);
				reg_controlFlag_sketch0.write(meta.extraOp_counter,meta.epoch_flag);

				// update the forecast sketch with Sf(t+1) = (1-alpha) * Sf(t)
				reg_forecast_sketch_row0.read(meta.forecast,meta.extraOp_counter);
				meta.new_forecast = meta.forecast >> BIT_SHIFT; // multiplication by (1-alpha)
				reg_forecast_sketch_row0.write(meta.extraOp_counter,meta.new_forecast);

				//update the error sketch: the Se(t) = - Sf(t)
				meta.new_err = - meta.forecast;
				reg_error_sketch_row0.write(meta.extraOp_counter,meta.new_err);

			}

		}

	} /* end of the apply block */
}

control ExtraOpRow1(inout metadata meta) {

apply{

		// Read the extra operations available per this sketch row
		// if there are some for the current epoch, perform one (next block of code)
		// decrement the counter
		meta.extraOp = 0;
		reg_extraOp_counter.read(meta.extraOp_counter,1)

		if( meta.extraOp_counter > 0 ){

			reg_extraOp_counter.write(1,meta.extraOp_counter-1);

			meta.extraOp = 1;

		}

		// if there are extra operations to be performed in the current epoch
		// Max number of extra operations per epoch equals the sketch width
		if ( meta.extraOp == 1 ) {

			reg_controlFlag_sketch1.read(meta.ctrl_bit,meta.extraOp_counter); 

			if (meta.ctrl_bit != meta.epoch_flag) {

				// to me the next is an error, you should update with the value of the epoch_flag 
				//reg_controlFlag_sketch0.write(meta.extraOp_counter,1);
				reg_controlFlag_sketch1.write(meta.extraOp_counter,meta.epoch_flag);

				// update the forecast sketch with Sf(t+1) = (1-alpha) * Sf(t)
				reg_forecast_sketch_row1.read(meta.forecast,meta.extraOp_counter);
				meta.new_forecast = meta.forecast >> BIT_SHIFT; // multiplication by (1-alpha)
				reg_forecast_sketch_row1.write(meta.extraOp_counter,meta.new_forecast);

				//update the error sketch: the Se(t) = - Sf(t)
				meta.new_err = - meta.forecast;
				reg_error_sketch_row1.write(meta.extraOp_counter,meta.new_err);

			}

		}

	} /* end of the apply block */
}

control ExtraOpRow2(inout metadata meta) {

apply{

		// Read the extra operations available per this sketch row
		// if there are some for the current epoch, perform one (next block of code)
		// decrement the counter
		meta.extraOp = 0;
		reg_extraOp_counter.read(meta.extraOp_counter,2)

		if( meta.extraOp_counter > 0 ){

			reg_extraOp_counter.write(2,meta.extraOp_counter-1);

			meta.extraOp = 1;

		}

		// if there are extra operations to be performed in the current epoch
		// Max number of extra operations per epoch equals the sketch width
		if ( meta.extraOp == 1 ) {

			reg_controlFlag_sketch2.read(meta.ctrl_bit,meta.extraOp_counter); 

			if (meta.ctrl_bit != meta.epoch_flag) {

				// to me the next is an error, you should update with the value of the epoch_flag 
				//reg_controlFlag_sketch0.write(meta.extraOp_counter,1);
				reg_controlFlag_sketch2.write(meta.extraOp_counter,meta.epoch_flag);

				// update the forecast sketch with Sf(t+1) = (1-alpha) * Sf(t)
				reg_forecast_sketch_row2.read(meta.forecast,meta.extraOp_counter);
				meta.new_forecast = meta.forecast >> BIT_SHIFT; // multiplication by (1-alpha)
				reg_forecast_sketch_row2.write(meta.extraOp_counter,meta.new_forecast);

				//update the error sketch: the Se(t) = - Sf(t)
				meta.new_err = - meta.forecast;
				reg_error_sketch_row2.write(meta.extraOp_counter,meta.new_err);

			}

		}

	} /* end of the apply block */
}
