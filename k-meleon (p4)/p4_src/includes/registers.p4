//*--------------------------------------------------------------------------------------------------------------*//
//*---------------------------------------------------MV Sketch--------------------------------------------------*//
//*--------------------------------------------------------------------------------------------------------------*//

register<bit<32>>(SKETCH_WIDTH*3) reg_mv_sketch0_row0;       // mv sketch Smv(t) 
register<bit<32>>(SKETCH_WIDTH*3) reg_mv_sketch0_row1;
register<bit<32>>(SKETCH_WIDTH*3) reg_mv_sketch0_row2;

register<bit<32>>(SKETCH_WIDTH*3) reg_mv_sketch1_row0;       // mv sketch Smv(t) 
register<bit<32>>(SKETCH_WIDTH*3) reg_mv_sketch1_row1;
register<bit<32>>(SKETCH_WIDTH*3) reg_mv_sketch1_row2;

//*--------------------------------------------------------------------------------------------------------------*//
//*-------------------------------------------------K-Ary Sketch-------------------------------------------------*//
//*--------------------------------------------------------------------------------------------------------------*//

register<bit<1>>(1) reg_epoch_bit;                              // 1 bit flag for forecast sketch selection

register<bit<32>>(SKETCH_WIDTH) reg_forecast_sketch_row0;       // forecast sketch Sf(t) 
register<bit<32>>(SKETCH_WIDTH) reg_forecast_sketch_row1;
register<bit<32>>(SKETCH_WIDTH) reg_forecast_sketch_row2;

register<bit<32>>(SKETCH_WIDTH*2) reg_error_sketch_row0;        // error sketch Se(t) 
register<bit<32>>(SKETCH_WIDTH*2) reg_error_sketch_row1;
register<bit<32>>(SKETCH_WIDTH*2) reg_error_sketch_row2;

register<bit<1>>(SKETCH_WIDTH)  reg_controlFlag_sketch_row0;    // control-flag sketch
register<bit<1>>(SKETCH_WIDTH)  reg_controlFlag_sketch_row1;
register<bit<1>>(SKETCH_WIDTH)  reg_controlFlag_sketch_row2;

//*--------------------------------------------------------------------------------------------------------------*//
//*---------------------------------------------Application Registers--------------------------------------------*//
//*--------------------------------------------------------------------------------------------------------------*//

register<bit<1>>(1)             reg_first_epoch_flag;           // 1 bit flag for forecast sketch selection
register<bit<48>>(1)            reg_epoch_value;                // epoch is number of packets
register<bit<32>>(SKETCH_DEPTH) reg_extraOp_counter;            // counter for extra operation
register<bit<32>>(1)            reg_total_num_packets;          // total_num_packets
register<bit<32>>(1)            reg_packet_changed;             // total_num_packets
register<bit<1>>(3)             reg_mv_flag;                    // mv flag: only update mv sketch if the error for that bucket is positive (currently testing)                          