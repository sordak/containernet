#!/usr/bin/python
"""
This is the most simple example to showcase Containernet.
"""
from mininet.net import Containernet
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI
from mininet.link import Link, TCLink
from mininet.log import info, setLogLevel
setLogLevel('info')

info('*** How much nodes do you need [MIN = 3; MAX = 15]:\n')
node_count = 3
node_count = int(input())
if node_count > 15:
    node_count = 15
elif node_count < 3:
    node_count = 3

net = Containernet(controller=Controller)
info('*** Adding controller\n')
net.addController('c0')
info('*** Adding switches\n')
s1 = net.addSwitch('s1', cls=OVSSwitch)
info('*** Adding docker containers\n')

last_octet = 1
d = []
for i in range(node_count):
    d.append(net.addDocker('d' + str(i + 1), dimage="ubuntu:trusty"))
    Link(d[i], s1, intfName1='d' + str(i + 1) + '-eth1')
    d[i].cmd('ifconfig d' + str(i + 1) + '-eth1 10.0.0.' + str(last_octet) + ' netmask 255.0.0.0')
    if i == 0:
        last_octet += 1
        continue
    if i == (node_count - 1):
        break
    Link(d[i], s1, intfName1='d' + str(i + 1) + '-eth2')
    d[i].cmd('ifconfig d' + str(i + 1) + '-eth2 10.0.0.' + str(100 + last_octet) + ' netmask 255.0.0.0')
    last_octet += 1

info('*** Starting network\n')
net.start()
info('*** Testing connectivity\n')
for i in range(len(d)):
    for j in range(len(d)):
        if i == j:
            continue
        net.ping([d[i], d[j]])

info('*** Tuning end-points\n')
d[0].cmd('apt update && apt install -y arping tcpdump')
#d[1].cmd('apt update && apt install -y bridge-utils tcpdump && ip addr flush dev d2-eth1 && ip addr flush dev d2-eth2 && brctl addbr d2-br1 && brctl addif d2-br1 d2-eth1 d2-eth2 && ip link set dev d2-br1 up')
d[node_count-1].cmd('apt update && apt install -y arping tcpdump')

info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()

