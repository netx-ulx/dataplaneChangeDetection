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

register<bit<1>>(1) reg_sketch_flag;                                        // 1 bit flag for forecast sketch selection
register<int<32>>(SKETCH_WIDTH*SKETCH_DEPTH) reg_forecast_sketch_f0;    // forecast sketch used when the sketch flag is 0
register<int<32>>(SKETCH_WIDTH*SKETCH_DEPTH) reg_forecast_sketch_f1;    // forecast sketch used when the sketch flag is 1
register<int<32>>(SKETCH_WIDTH*SKETCH_DEPTH) reg_error_sketch_f0;       // error sketch used when the sketch flag is 0
register<int<32>>(SKETCH_WIDTH*SKETCH_DEPTH) reg_error_sketch_f1;       // error sketch used when the sketch flag is 1
register<bit<1>>(SKETCH_WIDTH*SKETCH_DEPTH)  reg_control_sketch_flag;   // 1 bit control-flag sketch

//*--------------------------------------------------------------------------------------------------------------*//
//*---------------------------------------------Application Registers--------------------------------------------*//
//*--------------------------------------------------------------------------------------------------------------*//

register<bit<1>>(1)             reg_first;                  // 1 bit flag for forecast sketch selection
register<bit<32>>(1)            reg_epoch;                  // epoch is number of packets
register<bit<32>>(SKETCH_DEPTH) reg_extra_op_counter;       // counter for extra operation
register<int<32>>(1)            reg_total_num_packets;      // total_num_packets
register<int<32>>(1)            reg_packet_changed;         // total_num_packets
register<bit<1>>(3)             reg_mv_flag;                // mv flag: only update mv sketch if the error for that bucket is positive (currently testing)                          