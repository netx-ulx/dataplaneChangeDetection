# P4 implementation of %SOMENAME%

---
### Files
- p4/K-Ary\kary.p4: P4 implementation of %SOMENAME% for 5-tuple flow key
---

### Compile and Run
The implementations should be run on the BMV2 v1model. We show how to compile the p4 files with the p4 compiler.

#### Requirements
- Install the p4 behavioral model (follow the steps [here](https://github.com/p4lang/behavioral-model)).
- Install the p4 compiler ([details](https://github.com/p4lang/p4c))

#### Compile
- Compile p4 files with p4 compiler

```
    $ p4c --target bmv2 --arch v1model --std p4-16 kary.p4
```

#### Run

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
        $ python controller.py --option detect
    ```

- Note that our implementations only include the simple forwarding rules based on ingress ports. For example, packets entering from port 0 are emitted to port 1. You may add your own forwarding logic in the ingress pipeline.
