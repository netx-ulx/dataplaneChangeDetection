//*------------------------------------------------------------------*//
//*-----------------------------MV Sketch----------------------------*//
//*------------------------------------------------------------------*//

register<bit<32>>(SKETCH_WIDTH*SKETCH_DEPTH) srcAddr_f0;        //key field: src, when the sketch flag is 0
register<bit<32>>(SKETCH_WIDTH*SKETCH_DEPTH) dstAddr_f0;        //key_field: dst, when the sketch flag is 0
register<bit<32>>(SKETCH_WIDTH*SKETCH_DEPTH) srcAddr_f1;        //key field: src, when the sketch flag is 1
register<bit<32>>(SKETCH_WIDTH*SKETCH_DEPTH) dstAddr_f1;        //key_field: dst, when the sketch flag is 1

register<int<32>>(SKETCH_WIDTH*SKETCH_DEPTH) sketch_count_f0;   //count field for the mjrty, when the sketch flag is 0
register<int<32>>(SKETCH_WIDTH*SKETCH_DEPTH) sketch_count_f1;   //count field for the mjrty, when the sketch flag is 1

//*------------------------------------------------------------------*//
//*---------------------------K-Ary Sketch---------------------------*//
//*------------------------------------------------------------------*//

register<bit<1>>(1) sketch_flag;                                    // 1 bit flag for forecast sketch selection
register<int<32>>(SKETCH_WIDTH*SKETCH_DEPTH) forecast_sketch_f0;    //forecast sketch used when the sketch flag is 0
register<int<32>>(SKETCH_WIDTH*SKETCH_DEPTH) forecast_sketch_f1;    //forecast sketch used when the sketch flag is 1
register<int<32>>(SKETCH_WIDTH*SKETCH_DEPTH) error_sketch_f0;       //error sketch used when the sketch flag is 0
register<int<32>>(SKETCH_WIDTH*SKETCH_DEPTH) error_sketch_f1;       //error sketch used when the sketch flag is 1
register<bit<1>>(SKETCH_WIDTH*SKETCH_DEPTH) control_flag;           // 1 bit control-flag sketch

//*------------------------------------------------------------------*//
//*-----------------------Application Registers----------------------*//
//*------------------------------------------------------------------*//

register<bit<32>>(1) epoch;                         // epoch is number of packets
register<bit<32>>(SKETCH_DEPTH) extra_op_counter;   // counter for extra operation