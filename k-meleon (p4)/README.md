<!-- PROJECT LOGO -->
<p align="center">

  <h3 align="center">P4 implementation of K-MELEON</h3>

  <p align="center">
    An implementation of the K-MELEON.
  </p>
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [Files](#files)
* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Compile](#compile)
  * [Run](#run)

<!-- FILES -->
---
## Files
- kary.p4: P4 implementation of %SOMENAME% for 5-tuple flow key.
- send.py: Python script to send packets from .pcap file.
- start_simple_switch.sh: Shell script to start the behavioural model.
- controller/controller.py : Python implementation of the thrift controller.
- controller/kary_sketch.py : K-ary sketch data-structure implementation.
---

<!-- ABOUT THE PROJECT -->
## About The Project

<!-- GETTING STARTED -->
## Getting Started
There a few design choices in the program that may not be easy to grasp at a first sight. We include hereby a few notes hoping to ease the understanding of k-meleon code.

* Separate Registers for the same's sketch rows: each sketch data structures is made of h=3 rows. A different register per row is istantiated. We have designed this having in mind a P4-target where the same instance of a register cannot be accessed multiple times, so to perform h changes to the same sketch, its structure must be split and stored across different register instances. 

* Atomic Read&Reset of registers: the error sketch register in this program has double size, since only half of the register is active at each epoch. When one half is active, the other half can be read by the control plane. This mechanism is used to achieve atomic reads of the register values. The access to the currently active part of these registers is controlled through a simple offset computed when the epoch is checked at the beginning of the program. 

* Close read and write operations to the same registers: where possible, even though this requirement is not strictly followed in this bmv2 version of k-meleon, we have tried to reduce the number of operations between the read and write of the same register, because this reflects a constraint available on some P4-capable target platforms.

* Alpha values: Because this solution uses bit-shift operations to perform floating-point operations with the alpha values the user should provide an alpha value expressable as combinations of negtive powers of 2. For example, alpha = 0.75 can be expressed like 2^(-1) + 2^(-2).

<!-- PREREQUISITES -->
### Prerequisites
- Install the p4 behavioral model (follow the steps [here](https://github.com/p4lang/behavioral-model)).
- Install the p4 compiler ([details](https://github.com/p4lang/p4c))

<!-- COMPILE -->
### Compile
The implementations should be run on the BMV2 v1model. We show how to compile the p4 files with the p4 compiler.

This source code includes a few pre-processing directives meant to slightly custom the k-meleon program at compile time. Those are the following:

- EPOCH_PKT/EPOCH_TS: you can decide to compute epochs based either on # of packets or on time intervals. Only one of this should be defined at each time, by the default EPOCH_TS is defined where EPOCH_PKT is not.

To control the values of the above at compile time, you may simply use the -D option of the compiler. Example:
```
    $ p4c --target bmv2 --arch v1model -DEPOCH_TS p4_src/k-meleon.p4
```

<!-- RUN -->
### Run

- Create virtual Ethernet devices with the script under your
  behavioral\_model directory
```
    $ sudo /home/vagrant/behavioral-model/tools/veth_setup.sh
```

- Run the behavioral model 
```
    $ sudo simple_switch --log-console -i 0@veth2 -i 1@veth4 k-meleon.json
```

- Send packets to the veth with the python script send.py
```
    $ sudo ./send.py ../traces/<filename>.pcap
```

- Run the thrift controller with python3
```
    $ python3 controller.py [--options][--epoch;--depth;--thresh;--width;--port]
```

- Run the debugger
```
    $ sudo /home/vagrant/behavioral-model/tools/nanomsg_client.py --thrift-port 9090
```
