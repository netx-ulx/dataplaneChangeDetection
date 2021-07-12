/*********************************************************
***************** MAIN UPDATE FUNCTION ********************
**********************************************************/

control UpdateRow0(inout metadata meta) {
	apply {
        //SKETCH + FORECASTING MODULE
        reg_controlFlag_sketch_row0.read(meta.ctrl,meta.hash0); 
        if (meta.ctrl != meta.flag) { //If equals, copy forecast_sketch
            reg_controlFlag_sketch_row0.write(meta.hash0,meta.flag);
            
            reg_forecast_sketch_row0.read(meta.forecast,meta.hash0);

            //update error
            meta.new_err = 10 - meta.forecast;
            if (meta.flag == 0) {
                reg_error_sketch0_row0.write(meta.hash0,meta.new_err);
            } else {
                reg_error_sketch1_row0.write(meta.hash0,meta.new_err);
            }

            //update forecast
            meta.obs = 10 >> 1; //division by 2
            meta.aux_forecast = meta.forecast >> 1; //division by 2
            meta.new_forecast = meta.obs + meta.aux_forecast; //sum of both

            reg_forecast_sketch_row0.write(meta.hash0,meta.new_forecast); //update
        } else { //else, only update with observed
            //update error
            if (meta.flag == 0) {
                reg_error_sketch0_row0.read(meta.err,meta.hash0);
                meta.new_err = meta.err + 10;
                reg_error_sketch0_row0.write(meta.hash0,meta.new_err);
            } else {
                reg_error_sketch1_row0.read(meta.err,meta.hash0);
                meta.new_err = meta.err + 10;
                reg_error_sketch1_row0.write(meta.hash0,meta.new_err);
            }
            //update forecast
            reg_forecast_sketch_row0.read(meta.forecast,meta.hash0);
            meta.obs = 10 >> 1; //division by 2
            meta.new_forecast = meta.obs + meta.forecast; //sum with old value
            reg_forecast_sketch_row0.write(meta.hash0,meta.new_forecast); //update

            //compute one extra op
            reg_extra_op_counter.read(meta.counter,0);
            if (meta.counter < SKETCH_WIDTH) {
                reg_controlFlag_sketch_row0.read(meta.ctrl,meta.counter); 
                if (meta.ctrl != meta.flag) { //If diff, copy forecast_sketch
                    reg_controlFlag_sketch_row0.write(meta.counter,meta.flag);
                    reg_forecast_sketch_row0.read(meta.forecast,meta.counter);

                    //update error
                    meta.new_err_op = -meta.forecast; //negative
                    if (meta.flag == 0) {
                        reg_error_sketch0_row0.write(meta.counter,meta.new_err_op);
                    } else {
                        reg_error_sketch1_row0.write(meta.counter,meta.new_err_op);
                    }
                    //update forecast
                    meta.new_forecast = meta.forecast >> 1; //division by 2
                    reg_forecast_sketch_row0.write(meta.counter,meta.new_forecast);
                }
                reg_extra_op_counter.write(0,meta.counter+1);
            }
        }
    }
}

control UpdateRow1(inout metadata meta) {
	apply{
        //SKETCH + FORECASTING MODULE
        reg_controlFlag_sketch_row1.read(meta.ctrl,meta.hash1); 
        if (meta.ctrl != meta.flag) { //If equals, copy forecast_sketch
            reg_controlFlag_sketch_row1.write(meta.hash1,meta.flag);
            
            reg_forecast_sketch_row1.read(meta.forecast,meta.hash1);
            
            //update error
            meta.new_err = 10 - meta.forecast;
            if (meta.flag == 0) {
                reg_error_sketch0_row1.write(meta.hash1,meta.new_err);
            } else {
                reg_error_sketch1_row1.write(meta.hash1,meta.new_err);
            }

            //update forecast
            meta.obs = 10 >> 1; //division by 2
            meta.aux_forecast = meta.forecast >> 1; //division by 2
            meta.new_forecast = meta.obs + meta.aux_forecast; //sum of both

            reg_forecast_sketch_row1.write(meta.hash1,meta.new_forecast); //update
        } else { //else, only update with observed
            //update error
            
            if (meta.flag == 0) {
                reg_error_sketch0_row1.read(meta.err,meta.hash1);
                meta.new_err = meta.err + 10;
                reg_error_sketch0_row1.write(meta.hash1,meta.new_err);
            } else {
                reg_error_sketch1_row1.read(meta.err,meta.hash1);
                meta.new_err = meta.err + 10;
                reg_error_sketch1_row1.write(meta.hash1,meta.new_err);
            }

            //update forecast
            reg_forecast_sketch_row1.read(meta.forecast,meta.hash1);
            meta.obs = 10 >> 1; //division by 2
            meta.new_forecast = meta.obs + meta.forecast; //sum with old value
            reg_forecast_sketch_row1.write(meta.hash1,meta.new_forecast); //update

            //compute one extra op
            reg_extra_op_counter.read(meta.counter,1);
            if (meta.counter < SKETCH_WIDTH) {
                reg_controlFlag_sketch_row1.read(meta.ctrl,meta.counter); 
                if (meta.ctrl != meta.flag) { //If diff, copy forecast_sketch
                    reg_controlFlag_sketch_row1.write(meta.counter,meta.flag);
                    reg_forecast_sketch_row1.read(meta.forecast,meta.counter);

                    //update error
                    meta.new_err_op = -meta.forecast; //negative
                    if (meta.flag == 0) {
                        reg_error_sketch0_row1.write(meta.counter,meta.new_err_op);
                    } else {
                        reg_error_sketch1_row1.write(meta.counter,meta.new_err_op);
                    }
                    
                    //update forecast
                    meta.new_forecast = meta.forecast >> 1; //division by 2
                    reg_forecast_sketch_row1.write(meta.counter,meta.new_forecast);
                }
                reg_extra_op_counter.write(1,meta.counter+1);
            }
        }
    }
}

control UpdateRow2(inout metadata meta) {
	apply{
        //SKETCH + FORECASTING MODULE
        reg_controlFlag_sketch_row2.read(meta.ctrl,meta.hash2); 
        if (meta.ctrl != meta.flag) { //If equals, copy forecast_sketch
            reg_controlFlag_sketch_row2.write(meta.hash2,meta.flag);
            
            reg_forecast_sketch_row2.read(meta.forecast,meta.hash2);
            
            //update error
            meta.new_err = 10 - meta.forecast;
            if (meta.flag == 0) {
                reg_error_sketch0_row2.write(meta.hash2,meta.new_err);
            } else {
                reg_error_sketch1_row2.write(meta.hash2,meta.new_err);
            }

            //update forecast
            meta.obs = 10 >> 1; //division by 2
            meta.aux_forecast = meta.forecast >> 1; //division by 2
            meta.new_forecast = meta.obs + meta.aux_forecast; //sum of both

            reg_forecast_sketch_row2.write(meta.hash2,meta.new_forecast); //update
        } else { //else, only update with observed
            //update error
            
            if (meta.flag == 0) {
                reg_error_sketch0_row2.read(meta.err,meta.hash2);
                meta.new_err = meta.err + 10;
                reg_error_sketch0_row2.write(meta.hash2,meta.new_err);
            } else {
                reg_error_sketch1_row2.read(meta.err,meta.hash2);
                meta.new_err = meta.err + 10;
                reg_error_sketch1_row2.write(meta.hash2,meta.new_err);
            }

            //update forecast
            reg_forecast_sketch_row2.read(meta.forecast,meta.hash2);
            meta.obs = 10 >> 1; //division by 2
            meta.new_forecast = meta.obs + meta.forecast; //sum with old value
            reg_forecast_sketch_row2.write(meta.hash2,meta.new_forecast); //update

            //compute one extra op
            reg_extra_op_counter.read(meta.counter,2);
            if (meta.counter < SKETCH_WIDTH) {
                reg_controlFlag_sketch_row2.read(meta.ctrl,meta.counter); 
                if (meta.ctrl != meta.flag) { //If diff, copy forecast_sketch
                    reg_controlFlag_sketch_row2.write(meta.counter,meta.flag);
                    reg_forecast_sketch_row2.read(meta.forecast,meta.counter);

                    //update error
                    meta.new_err_op = -meta.forecast; //negative
                    if (meta.flag == 0) {
                        reg_error_sketch0_row2.write(meta.counter,meta.new_err_op);
                    } else {
                        reg_error_sketch1_row2.write(meta.counter,meta.new_err_op);
                    }
                    
                    //update forecast
                    meta.new_forecast = meta.forecast >> 1; //division by 2
                    reg_forecast_sketch_row2.write(meta.counter,meta.new_forecast);
                }
                reg_extra_op_counter.write(2,meta.counter+1);
            }
        }
    }
}

control UpdateEpoch1Row0(inout metadata meta) {
	
    apply{
        //update forecast
        reg_forecast_sketch_row0.read(meta.forecast,meta.hash0);
        meta.new_forecast = 10 + meta.forecast; //sum with old value
        reg_forecast_sketch_row0.write(meta.hash0,meta.new_forecast); //update
    }
}

control UpdateEpoch1Row1(inout metadata meta) {
    apply{
        //update forecast
        reg_forecast_sketch_row1.read(meta.forecast,meta.hash1);
        meta.new_forecast = 10 + meta.forecast; //sum with old value
        reg_forecast_sketch_row1.write(meta.hash1,meta.new_forecast); //update
    }
}

control UpdateEpoch1Row2(inout metadata meta) {
    apply{
        //update forecast
        reg_forecast_sketch_row2.read(meta.forecast,meta.hash2);
        meta.new_forecast = 10 + meta.forecast; //sum with old value
        reg_forecast_sketch_row2.write(meta.hash2,meta.new_forecast); //update
    }
}
