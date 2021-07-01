This source code includes a few pre-processing directives meant to slightly custom the k-meleon program at compile time. Those are the following:

- EPOCH_PKT/EPOCH_TS: you can decide to compute epochs based either on # of packets or on time intervals. Only one of this should be defined at each time, by the default EPOCH_TS is defined where EPOCH_PKT is not.

- BIT_SHIFT: a few values of the alpha constant in the EWMA model can be controlled by specifying different values of this bit-shift operation. (TODO: here we should explicitely list those values)

- EXTRA_OP: to activate the extraOperation module, see code in "./includes/extraOp_ctrl.p4"

- REVERT: to activate the reversibility module, see code in "./includes/reversibility.p4"

To control the values of the above at compile time, you may simply use the -D option of the compiler. Example:

$ p4c --target bmv2 --arch v1model -DREVERT p4_src/k-meleon.p4

There a few design choices in the program that may not be easy to grasp at a first sight. We include hereby a few notes hoping to ease the understanding of k-meleon code.

* Separate Registers for the same's sketch rows: each sketch data structures is made of h=3 rows. A different register per row is istantiated. We have designed this having in mind a P4-target where the same instance of a register cannot be accessed multiple times, so to perform h changes to the same sketch, its structure must be split and stored across different register instances. 

* Atomic Read&Reset of registers: all the registers in this program have double size (controlled by the DUPL_LEVEL constant), since only half of the register is active at each epoch. When one half is active, the other half can be read and cleaned by the control plane. This is mechanism to achieve atomic reads of the register values. The access to the currently active part of these registers is controlled through a simple offset computed when the epoch is checked at the beginning of the program. 

* Close read and write operations to the same registers: where possible, even though this requirement is not strictly followed in this bmv2 version of k-meleon, we have tried to reduce the number of operations between the read and write of the same register, because this reflects a constraint available on some P4-capable target platforms.

