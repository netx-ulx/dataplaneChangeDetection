# P4 implementation of MV-Sketch


---
### Files
- p4/K-Ary\kary.p4: P4 implementation of K-ary for 5-tuple flow key
---

### Compile and Run
The implementations should be run on the BMV2 v1model. We show how to compile the p4 files with
p4 compiler.

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
    $ sudo ./send.py ../traces/ping-of-death-100k-1.pcap
```

- Dump the counter table of MV-Sketch via CLI of BMV2

    - enter the CLI 
	    $ python controller.py --option detect

        ```
            $ simple_switch_CLI
        ```
    - dump register tables in CLI 
        ```
            $ register_read sketch_sum 
            $ register_read sketch_key 
            $ register_read sketch_count 
        ```

- Note that our implementations only include the simple forwarding rules based
  on ingress ports. For example, packets entering from port 0 are emitted to
  port 1. You may add your own forwarding logic in the ingress pipeline.
