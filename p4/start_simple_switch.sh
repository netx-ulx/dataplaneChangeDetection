#!/bin/bash

p4c --target bmv2 --arch v1model --std p4-16 kary.p4

sudo /home/vagrant/behavioral-model/tools/veth_setup.sh

sudo simple_switch --log-console -i 0@veth2 -i 1@veth4 kary.json