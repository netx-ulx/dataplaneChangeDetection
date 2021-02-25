//key fields (MV SKETCH)
register<bit<64>>(SKETCH_WIDTH) sketch_key0; //src, dst
register<bit<64>>(SKETCH_WIDTH) sketch_key1; //sport, dport, proto

//count fields (MV SKETCH)
register<int<32>>(SKETCH_WIDTH) sketch_count; //count for the mjrty

//control-aux registers
register<bit<1>>(1) sketch_flag; // 1 bit flag for forecasting sketch selection
register<bit<32>>(SKETCH_DEPTH) extra_op_counter; // counter for extra operation
register<bit<48>>(1) epoch; //timestamps require bit<48>
register<bit<1>>(SKETCH_WIDTH*SKETCH_DEPTH) control_flag; // 1 bit flag sketch

//error and forecast sketches
register<int<32>>(SKETCH_WIDTH*SKETCH_DEPTH) forecast_sketch0; 
register<int<32>>(SKETCH_WIDTH*SKETCH_DEPTH) forecast_sketch1; 
register<int<32>>(SKETCH_WIDTH*SKETCH_DEPTH) error_sketch0;
register<int<32>>(SKETCH_WIDTH*SKETCH_DEPTH) error_sketch1;
