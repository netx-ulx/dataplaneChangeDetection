<!-- PROJECT LOGO -->
<p align="center">

  <h3 align="center">P4 implementation of %SOMENAME%</h3>

  <p align="center">
    An implementation of the %SOMENAME%.
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
The implementations should be run on the BMV2 v1model. We show how to compile the p4 files with the p4 compiler.

<!-- PREREQUISITES -->
### Prerequisites
- Install the p4 behavioral model (follow the steps [here](https://github.com/p4lang/behavioral-model)).
- Install the p4 compiler ([details](https://github.com/p4lang/p4c))

<!-- COMPILE -->
### Compile
- Compile p4 files with p4 compiler

```
    $ p4c --target bmv2 --arch v1model --std p4-16 kary.p4
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
    $ sudo simple_switch --log-console -i 0@veth2 -i 1@veth4 kary.json
```

- Send packets to the veth with the python script send.py

```
    $ sudo ./send.py ../traces/<filename>.pcap
```

- Run the thrift controller with python3
```
    $ python controller.py
```

- Run the debugger

```
    $ sudo /home/vagrant/behavioral-model/tools/nanomsg_client.py --thrift-port 9090
```

- Note that our implementations only include the simple forwarding rules based on ingress ports. For example, packets entering from port 0 are emitted to port 1. You may add your own forwarding logic in the ingress pipeline.
