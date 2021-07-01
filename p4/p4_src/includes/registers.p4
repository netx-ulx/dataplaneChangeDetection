//*--------------------------------------------------------------------------------------------------------------*//
//*------------------------------------------Reversibility Data Structures --------------------------------------*//
//*--------------------------------------------------------------------------------------------------------------*//

#ifdef REVERT
register<bit<KEY_SIZE>>(SKETCH_WIDTH*DUPL_LEVEL) reg_flowKey_row0;   // Storing keys for the error sketch 
register<bit<KEY_SIZE>>(SKETCH_WIDTH*DUPL_LEVEL) reg_flowKey_row1;        
register<bit<KEY_SIZE>>(SKETCH_WIDTH*DUPL_LEVEL) reg_flowKey_row2;        

register<int<32>>(SKETCH_WIDTH*DUPL_LEVEL) reg_flowKey_count_row0;   // Storing counters for the error sketch keys
register<int<32>>(SKETCH_WIDTH*DUPL_LEVEL) reg_flowKey_count_row1;
register<int<32>>(SKETCH_WIDTH*DUPL_LEVEL) reg_flowKey_count_row2;
#endif

//*--------------------------------------------------------------------------------------------------------------*//
//*-------------------------------------------------K-meleon Sketch Data Structures------------------------------*//
//*--------------------------------------------------------------------------------------------------------------*//

register<int<32>>(SKETCH_WIDTH*DUPL_LEVEL) reg_forecast_sketch_row0;    // forecast sketch Sf(t) 
register<int<32>>(SKETCH_WIDTH*DUPL_LEVEL) reg_forecast_sketch_row1;
register<int<32>>(SKETCH_WIDTH*DUPL_LEVEL) reg_forecast_sketch_row2;

register<int<32>>(SKETCH_WIDTH*DUPL_LEVEL) reg_error_sketch_row0;       // error sketch Se(t) 
register<int<32>>(SKETCH_WIDTH*DUPL_LEVEL) reg_error_sketch_row1;
register<int<32>>(SKETCH_WIDTH*DUPL_LEVEL) reg_error_sketch_row2;

register<bit<1>>(SKETCH_WIDTH*DUPL_LEVEL)  reg_controlFlag_sketch0;   // control-flag sketch
register<bit<1>>(SKETCH_WIDTH*DUPL_LEVEL)  reg_controlFlag_sketch1;
register<bit<1>>(SKETCH_WIDTH*DUPL_LEVEL)  reg_controlFlag_sketch2;

//*--------------------------------------------------------------------------------------------------------------*//
//*---------------------------------------------Auxiliary Registers----------------------------------------------*//
//*--------------------------------------------------------------------------------------------------------------*//

register<bit<1>>(1)             reg_first_epoch_flag;      // flag for computing the forecast (EWMA) differently only at t=1
register<bit<1>>(1)             reg_epoch_bit;             // this bit signals the currently active epoch
register<bit<48>>(1)            reg_epoch_value;           // epoch holds either number of packets (EPOCH_PKT) or timestamp (EPOCH_TS)

#ifdef EXTRA_OP
register<bit<32>>(SKETCH_DEPTH) reg_extraOp_counter;       // counters for the extra operation module
#endif

#ifdef COUNT_PKT
register<int<32>>(1)            reg_total_num_packets;      // total_num_packets
register<int<32>>(1)            reg_packet_changed;         // NOT SURE WHAT THIS IS FOR
#endif
