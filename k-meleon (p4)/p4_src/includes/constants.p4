const bit<16> TYPE_IPV4             = 0x800;
const bit<8> IP_PROTOCOLS_TCP       =   6;
const bit<8> IP_PROTOCOLS_UDP       =  17;

#ifdef EPOCH_PKT /* epoch calculated with the number of packets processed */
const bit<48> EPOCH_SIZE       		=  1000; // epoch size in # of packets
#else
const bit<48> EPOCH_SIZE       		=  1000000; // epoch size in us (1 sec)
#endif

const bit<32> SKETCH_WIDTH			=  64;  // width of the sketch
const bit<32> SKETCH_DEPTH			=  3;   // depth of the sketch

const bit<32> SKETCH_UPDATE         =  2;

const bit<32> ALPHA                 =  5; // 5 represents alpha = 0.5; 25 represents alpha = 0.25; 875 represents alpha = 0.875
