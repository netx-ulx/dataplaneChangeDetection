#ifndef EPOCH_PKT /* epoch calculated with the number of packets processed */
	#define EPOCH_TS 1
#endif

#ifndef BIT_SHIFT /* a few values of the alpha constant in the EWMA model can be controlled by specifying different values of this bit-shift operation */
	#define BIT_SHIFT 1 // alpha = 0.5
#endif
