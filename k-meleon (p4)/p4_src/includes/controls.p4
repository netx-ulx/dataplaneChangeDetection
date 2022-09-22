/*********************************************************
***************** BIT-SHIFT BLOCKS ******************
**********************************************************/

#include "bit-shifts.p4"

/*********************************************************
***************** MAIN UPDATE FUNCTION ********************
**********************************************************/

control UpdateRow0(inout metadata meta) {
	apply {
        // SKETCH + FORECASTING MODULE
        reg_controlFlag_sketch_row0.read(meta.ctrl,meta.hash0); 
        if (meta.ctrl != meta.epoch_bit) { // If equals, copy forecast_sketch
            reg_controlFlag_sketch_row0.write(meta.hash0,meta.epoch_bit);           // Flip  control  flag
            
            reg_forecast_sketch_row0.read(meta.forecast,meta.hash0);                // Sf(t)

            // update error
            meta.new_err = SKETCH_UPDATE - meta.forecast;                           // S’o(t) - Sf(t)
            reg_error_sketch_row0.write(meta.hash0+meta.err_offset,meta.new_err);   // Se(t) = S’o(t) - Sf(t)

            // update forecast
            observedShift(meta);
            forecastShift(meta);
            //meta.obs = SKETCH_UPDATE >> 1;                                // alpha*S’o(t)
            //meta.aux_forecast = meta.forecast >> 1;                       // (1-alpha)*Sf(t)
            meta.new_forecast = meta.obs + meta.aux_forecast;               // alpha*S’o(t) + (1-alpha)*Sf(t)

            // Sf(t+1) = alpha*S’o(t) + (1-alpha)*Sf(t)
            reg_forecast_sketch_row0.write(meta.hash0,meta.new_forecast); 
        } else { //else, only update with observed
            // update error
            reg_error_sketch_row0.read(meta.err,meta.hash0+meta.err_offset);        // Se(t)
            meta.new_err = meta.err + SKETCH_UPDATE;                                // Se(t) + S’o(t)
            reg_error_sketch_row0.write(meta.hash0+meta.err_offset,meta.new_err);   // Se(t) = Se(t) + S’o(t)

            // update forecast
            reg_forecast_sketch_row0.read(meta.forecast,meta.hash0);    // Sf(t+1)
            observedShift(meta);                                        // alpha*S’o(t)
            meta.new_forecast = meta.obs + meta.forecast;               // Sf(t+1) + alpha*S’o(t)

            // Sf(t+1) = Sf(t+1) + alpha*S’o(t)
            reg_forecast_sketch_row0.write(meta.hash0,meta.new_forecast);
        }
    }
}

control UpdateRow1(inout metadata meta) {
	apply{
        // SKETCH + FORECASTING MODULE
        reg_controlFlag_sketch_row1.read(meta.ctrl,meta.hash1); 
        if (meta.ctrl != meta.epoch_bit) {  // If equals, copy forecast_sketch
            reg_controlFlag_sketch_row1.write(meta.hash1,meta.epoch_bit);           //  Flip  control  flag
            
            reg_forecast_sketch_row1.read(meta.forecast,meta.hash1);                // Sf(t)
            
            // update error
            meta.new_err = SKETCH_UPDATE - meta.forecast;                           // S’o(t) - Sf(t)
            reg_error_sketch_row1.write(meta.hash1+meta.err_offset,meta.new_err);   // Se(t) = S’o(t) - Sf(t)

            // update forecast
            observedShift(meta);
            forecastShift(meta);
            //meta.obs = SKETCH_UPDATE >> 1;                                // alpha*S’o(t)
            //meta.aux_forecast = meta.forecast >> 1;                       // (1-alpha)*Sf(t)
            meta.new_forecast = meta.obs + meta.aux_forecast;               // alpha*S’o(t) + (1-alpha)*Sf(t)

            // Sf(t+1) = alpha*S’o(t) + (1-alpha)*Sf(t)
            reg_forecast_sketch_row1.write(meta.hash1,meta.new_forecast);
        } else {    // else, only update with observed
            // update error
            reg_error_sketch_row1.read(meta.err,meta.hash1+meta.err_offset);        // Se(t)
            meta.new_err = meta.err + SKETCH_UPDATE;                                // Se(t) + S’o(t)
            reg_error_sketch_row1.write(meta.hash1+meta.err_offset,meta.new_err);   // Se(t) = Se(t) + S’o(t)

            // update forecast
            reg_forecast_sketch_row1.read(meta.forecast,meta.hash1);    // Sf(t+1)
            observedShift(meta);                                        // alpha*S’o(t)
            meta.new_forecast = meta.obs + meta.forecast;               // Sf(t+1) + alpha*S’o(t)
            
            // Sf(t+1) = Sf(t+1) + alpha*S’o(t)
            reg_forecast_sketch_row1.write(meta.hash1,meta.new_forecast); 
        }
    }
}

control UpdateRow2(inout metadata meta) {
	apply{
        // SKETCH + FORECASTING MODULE
        reg_controlFlag_sketch_row2.read(meta.ctrl,meta.hash2); 
        if (meta.ctrl != meta.epoch_bit) {                                      // If equals, copy forecast_sketch
            reg_controlFlag_sketch_row2.write(meta.hash2,meta.epoch_bit);       //  Flip  control  flag
            
            reg_forecast_sketch_row2.read(meta.forecast,meta.hash2);            // Sf(t)
            
            // update error
            meta.new_err = SKETCH_UPDATE - meta.forecast;                           // S’o(t) - Sf(t)
            reg_error_sketch_row2.write(meta.hash2+meta.err_offset,meta.new_err);   // Se(t) = S’o(t) - Sf(t)

            // update forecast
            observedShift(meta);
            forecastShift(meta);            
            //meta.obs = SKETCH_UPDATE >> 1;                                // alpha*S’o(t)
            //meta.aux_forecast = meta.forecast >> 1;                       // (1-alpha)*Sf(t)
            meta.new_forecast = meta.obs + meta.aux_forecast;               // alpha*S’o(t) + (1-alpha)*Sf(t)

            // Sf(t+1) = alpha*S’o(t) + (1-alpha)*Sf(t)
            reg_forecast_sketch_row2.write(meta.hash2,meta.new_forecast);
        } else {    // else, only update with observed
            // update error
            reg_error_sketch_row2.read(meta.err,meta.hash2+meta.err_offset);        // Se(t)
            meta.new_err = meta.err + SKETCH_UPDATE;                                // Se(t) + S’o(t)
            reg_error_sketch_row2.write(meta.hash2+meta.err_offset,meta.new_err);   // Se(t) = Se(t) + S’o(t)

            // update forecast
            reg_forecast_sketch_row2.read(meta.forecast,meta.hash2);    // Sf(t+1)
            observedShift(meta);                                        // alpha*S’o(t)
            meta.new_forecast = meta.obs + meta.forecast;               // Sf(t+1) + alpha*S’o(t)
            
            // Sf(t+1) = Sf(t+1) + alpha*S’o(t)
            reg_forecast_sketch_row2.write(meta.hash2,meta.new_forecast);
        }
    }
}

control UpdateEpoch1Row0(inout metadata meta) {	
    apply{
        // update forecast
        reg_forecast_sketch_row0.read(meta.forecast,meta.hash0);        // Sf(t)
        meta.new_forecast = SKETCH_UPDATE + meta.forecast;              // Sf(t) + S'o(t)
        reg_forecast_sketch_row0.write(meta.hash0,meta.new_forecast);   // Sf(t) = Sf(t) + S'o(t)
    }
}

control UpdateEpoch1Row1(inout metadata meta) {
    apply{
        // update forecast
        reg_forecast_sketch_row1.read(meta.forecast,meta.hash1);        // Sf(t)
        meta.new_forecast = SKETCH_UPDATE + meta.forecast;              // Sf(t) + S'o(t)
        reg_forecast_sketch_row1.write(meta.hash1,meta.new_forecast);   // Sf(t) = Sf(t) + S'o(t)
    }
}

control UpdateEpoch1Row2(inout metadata meta) {
    apply{
        // update forecast
        reg_forecast_sketch_row2.read(meta.forecast,meta.hash2);        // Sf(t)
        meta.new_forecast = SKETCH_UPDATE + meta.forecast;              // Sf(t) + S'o(t)
        reg_forecast_sketch_row2.write(meta.hash2,meta.new_forecast);   // Sf(t) = Sf(t) + S'o(t)
    }
}