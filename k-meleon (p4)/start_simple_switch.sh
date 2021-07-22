#!/bin/bash

p4c --target bmv2 --arch v1model -DEPOCH_PKT p4_src/k-meleon.p4

sudo /home/vagrant/behavioral-model/tools/veth_setup.sh

sudo simple_switch --log-console -i 0@veth2 -i 1@veth4 --nanolog ipc:///tmp/bm-log.ipc k-meleon.json

