#ifdef EXTRA_OP
	#include "includes/extraOp_ctrl.p4"
#endif

/* 
*  The three control blocks here presented contain the same exact code
*  yet applied to different register memories. So, it is sufficient to 
*  check only the logic of one block to understand the operations which
*  are performed identically on the different h=3 rows of the sketch
*  data structures.
*/

control UpdateRow0(inout metadata meta) {

#ifdef EXTRA_OP
	ExtraOpRow0() extraOp_row0;
#endif

apply {

		// checking whether or not ctrl and epoch bits are already aligned
		reg_controlFlag_sketch0.read(meta.ctrl_bit,meta.hash0_value); 
		if (meta.ctrl_bit != meta.epoch_bit) {
			reg_controlFlag_sketch0.write(meta.hash0_value,1);
			meta.ctrl_changed_flag = 1;
		}

		// update error and forecast sketch with both observed and forecast
		if ( meta.ctrl_changed_flag == 1) {
			
			/**** update the forecast sketch ****/
			reg_forecast_sketch_row0.read(meta.forecast,meta.hash0_value);

			//compute the new value  Sf(t+1) = aplha * So(t) + (1-alpha) * Sf(t)
			meta.obs = 10 >> BIT_SHIFT; //division by alpha
			meta.aux_forecast = meta.forecast >> BIT_SHIFT; //division by alpha
			meta.new_forecast = meta.obs + meta.aux_forecast;
			
			reg_forecast_sketch_row0.write(meta.hash0_value,meta.new_forecast);
			/***********************************/

			/***** update error sketch - Se(t) = So(t) - Sf(t) ****/
			meta.new_err = 10 - meta.forecast;
			reg_error_sketch_row0.write(meta.hash0_value,meta.new_err);
			/*****************************************************/


		} else { //else, update error and forecast sketch with only observed

			/**** update the forecast sketch ****/
			reg_forecast_sketch_row0.read(meta.forecast,meta.hash0_value);

			//compute the new value  Sf(t+1) += aplha * So(t)
			meta.obs = 10 >> BIT_SHIFT; //division by alpha
			meta.new_forecast = meta.obs + meta.forecast;
			
			reg_forecast_sketch_row0.write(meta.hash0_value,meta.new_forecast);
			/***********************************/


			/***** update error sketch - Se(t) += So(t) ****/
			reg_error_sketch_row0.read(meta.err,meta.hash0_value);
			meta.new_err = meta.err + 10;
			reg_error_sketch_row0.write(meta.hash0_value,meta.new_err);
			/**********************************************/

		}

		#ifdef EXTRA_OP
			// perform an additional update of the sketch data structures at a different index
			extraOp_row0.apply(meta);
		#endif

	} // end of the apply block
}

control UpdateRow1(inout metadata meta) {

#ifdef EXTRA_OP
	ExtraOpRow1() extraOp_row1;
#endif

apply {

		// checking whether or not ctrl and epoch bits are already aligned
		reg_controlFlag_sketch1.read(meta.ctrl_bit,meta.hash1_value); 
		if (meta.ctrl_bit != meta.epoch_bit) {
			reg_controlFlag_sketch1.write(meta.hash1_value,1);
			meta.ctrl_changed_flag = 1;
		}

		// update error and forecast sketch with both observed and forecast
		if ( meta.ctrl_changed_flag == 1) {
			
			/**** update the forecast sketch ****/
			reg_forecast_sketch_row1.read(meta.forecast,meta.hash1_value);

			//compute the new value  Sf(t+1) = aplha * So(t) + (1-alpha) * Sf(t)
			meta.obs = 10 >> BIT_SHIFT; //division by alpha
			meta.aux_forecast = meta.forecast >> BIT_SHIFT; //division by alpha
			meta.new_forecast = meta.obs + meta.aux_forecast;
			
			reg_forecast_sketch_row1.write(meta.hash1_value,meta.new_forecast);
			/***********************************/

			/***** update error sketch - Se(t) = So(t) - Sf(t) ****/
			meta.new_err = 10 - meta.forecast;
			reg_error_sketch_row1.write(meta.hash1_value,meta.new_err);
			/*****************************************************/


		} else { //else, update error and forecast sketch with only observed

			/**** update the forecast sketch ****/
			reg_forecast_sketch_row1.read(meta.forecast,meta.hash1_value);

			//compute the new value  Sf(t+1) += aplha * So(t)
			meta.obs = 10 >> BIT_SHIFT; //division by alpha
			meta.new_forecast = meta.obs + meta.forecast;
			
			reg_forecast_sketch_row1.write(meta.hash1_value,meta.new_forecast);
			/***********************************/

			/***** update error sketch - Se(t) += So(t) ****/
			reg_error_sketch_row1.read(meta.err,meta.hash1_value);
			meta.new_err = meta.err + 10;
			reg_error_sketch_row1.write(meta.hash1_value,meta.new_err);
			/**********************************************/

		}

		#ifdef EXTRA_OP
			// perform an additional update of the sketch data structures at a different index
			extraOp_row1.apply(meta);
		#endif

	} // end of the apply block
}

control UpdateRow2(inout metadata meta) {

#ifdef EXTRA_OP
	ExtraOpRow2() extraOp_row2;
#endif

apply {

		// checking whether or not ctrl and epoch bits are already aligned
		reg_controlFlag_sketch2.read(meta.ctrl_bit,meta.hash2_value); 
		if (meta.ctrl_bit != meta.epoch_bit) {
			reg_controlFlag_sketch2.write(meta.hash2_value,1);
			meta.ctrl_changed_flag = 1;
		}

		// update error and forecast sketch with both observed and forecast
		if ( meta.ctrl_changed_flag == 1) {
			
			/**** update the forecast sketch ****/
			reg_forecast_sketch_row2.read(meta.forecast,meta.hash2_value);

			//compute the new value  Sf(t+1) = aplha * So(t) + (1-alpha) * Sf(t)
			meta.obs = 10 >> BIT_SHIFT; //division by alpha
			meta.aux_forecast = meta.forecast >> BIT_SHIFT; //division by alpha
			meta.new_forecast = meta.obs + meta.aux_forecast;
			
			reg_forecast_sketch_row2.write(meta.hash2_value,meta.new_forecast);
			/***********************************/

			/***** update error sketch - Se(t) = So(t) - Sf(t) ****/
			meta.new_err = 10 - meta.forecast;
			reg_error_sketch_row2.write(meta.hash2_value,meta.new_err);
			/*****************************************************/


		} else { //else, update error and forecast sketch with only observed

			/**** update the forecast sketch ****/
			reg_forecast_sketch_row2.read(meta.forecast,meta.hash2_value);

			//compute the new value  Sf(t+1) += aplha * So(t)
			meta.obs = 10 >> BIT_SHIFT; //division by alpha
			meta.new_forecast = meta.obs + meta.forecast;
			
			reg_forecast_sketch_row2.write(meta.hash2_value,meta.new_forecast);
			/***********************************/

			/***** update error sketch - Se(t) += So(t) ****/
			reg_error_sketch_row2.read(meta.err,meta.hash2_value);
			meta.new_err = meta.err + 10;
			reg_error_sketch_row2.write(meta.hash2_value,meta.new_err);
			/**********************************************/


		}

		#ifdef EXTRA_OP
			// perform an additional update of the sketch data structures at a different index
			extraOp_row2.apply(meta);
		#endif

	} // end of the apply block
}
