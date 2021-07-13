//*--------------------------------------------------------------------------------------------------------------*//
//*---------------------------------------------------MV Sketch--------------------------------------------------*//
//*--------------------------------------------------------------------------------------------------------------*//

register<bit<32>>(SKETCH_WIDTH*SKETCH_DEPTH) reg_srcAddr_f0;        // key field: src, when the sketch flag is 0
register<bit<32>>(SKETCH_WIDTH*SKETCH_DEPTH) reg_dstAddr_f0;        // key_field: dst, when the sketch flag is 0
register<bit<32>>(SKETCH_WIDTH*SKETCH_DEPTH) reg_srcAddr_f1;        // key field: src, when the sketch flag is 1
register<bit<32>>(SKETCH_WIDTH*SKETCH_DEPTH) reg_dstAddr_f1;        // key_field: dst, when the sketch flag is 1

register<int<32>>(SKETCH_WIDTH*SKETCH_DEPTH) reg_sketch_count_f0;   // count field for the mjrty, when the sketch flag is 0
register<int<32>>(SKETCH_WIDTH*SKETCH_DEPTH) reg_sketch_count_f1;   // count field for the mjrty, when the sketch flag is 1

//*--------------------------------------------------------------------------------------------------------------*//
//*-------------------------------------------------K-Ary Sketch-------------------------------------------------*//
//*--------------------------------------------------------------------------------------------------------------*//

register<bit<1>>(1) reg_epoch_bit;                                        // 1 bit flag for forecast sketch selection

register<int<32>>(SKETCH_WIDTH) reg_forecast_sketch_row0;    // forecast sketch Sf(t) 
register<int<32>>(SKETCH_WIDTH) reg_forecast_sketch_row1;
register<int<32>>(SKETCH_WIDTH) reg_forecast_sketch_row2;

register<int<32>>(SKETCH_WIDTH) reg_error_sketch0_row0;       // error sketch Se(t) 
register<int<32>>(SKETCH_WIDTH) reg_error_sketch0_row1;
register<int<32>>(SKETCH_WIDTH) reg_error_sketch0_row2;

register<int<32>>(SKETCH_WIDTH) reg_error_sketch1_row0;       // error sketch Se(t) 
register<int<32>>(SKETCH_WIDTH) reg_error_sketch1_row1;
register<int<32>>(SKETCH_WIDTH) reg_error_sketch1_row2;

register<bit<1>>(SKETCH_WIDTH)  reg_controlFlag_sketch_row0;   // control-flag sketch
register<bit<1>>(SKETCH_WIDTH)  reg_controlFlag_sketch_row1;
register<bit<1>>(SKETCH_WIDTH)  reg_controlFlag_sketch_row2;

//*--------------------------------------------------------------------------------------------------------------*//
//*---------------------------------------------Application Registers--------------------------------------------*//
//*--------------------------------------------------------------------------------------------------------------*//

register<bit<1>>(1)             reg_first_epoch_flag;                  // 1 bit flag for forecast sketch selection
register<bit<32>>(1)            reg_epoch_value;                  // epoch is number of packets
register<bit<32>>(SKETCH_DEPTH) reg_extraOp_counter;       // counter for extra operation
register<int<32>>(1)            reg_total_num_packets;      // total_num_packets
register<int<32>>(1)            reg_packet_changed;         // total_num_packets
register<bit<1>>(3)             reg_mv_flag;                // mv flag: only update mv sketch if the error for that bucket is positive (currently testing)                          