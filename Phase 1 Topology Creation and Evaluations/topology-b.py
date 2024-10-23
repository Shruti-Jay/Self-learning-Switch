#!/usr/bin/env python

# Spring 2024 CSCI 4211: Introduction to Computer Networks
# This program serves as a script that constructs topology B.
# It was written in Python v3.

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.node import RemoteController

class AssignmentNetworks(Topo):
    def __init__(self, **opts):
        Topo.__init__(self, **opts)
        
        # Link performance parameters based on their level in the topology.
        lvl1_bw = 100  # Level 1 bandwidth (Mbps)
        lvl1_delay = '30ms'  # Level 1 delay (ms)
        
        lvl2_bw = 40  # Level 2 bandwidth (Mbps)
        lvl2_delay = '20ms'  # Level 2 delay (ms)
        
        lvl3_bw = 10  # Level 3 bandwidth (Mbps)
        lvl3_delay = '10ms'  # Level 3 delay (ms)

        # Create core switch
        c1 = self.addSwitch('c1')

        # Create aggregation switches
        a1 = self.addSwitch('a1')
        a2 = self.addSwitch('a2')

        # Create edge switches
        e1 = self.addSwitch('e1')
        e2 = self.addSwitch('e2')
        e3 = self.addSwitch('e3')
        e4 = self.addSwitch('e4')

        # Create hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')
        h7 = self.addHost('h7')
        h8 = self.addHost('h8')

        # Connect hosts to edge switches
        self.addLink(h1, e1, bw=lvl3_bw, delay=lvl3_delay)
        self.addLink(h2, e1, bw=lvl3_bw, delay=lvl3_delay)
        self.addLink(h3, e2, bw=lvl3_bw, delay=lvl3_delay)
        self.addLink(h4, e2, bw=lvl3_bw, delay=lvl3_delay)
        self.addLink(h5, e3, bw=lvl3_bw, delay=lvl3_delay)
        self.addLink(h6, e3, bw=lvl3_bw, delay=lvl3_delay)
        self.addLink(h7, e4, bw=lvl3_bw, delay=lvl3_delay)
        self.addLink(h8, e4, bw=lvl3_bw, delay=lvl3_delay)

        # Connect edge switches to aggregation switches
        self.addLink(e1, a1, bw=lvl2_bw, delay=lvl2_delay)
        self.addLink(e2, a1, bw=lvl2_bw, delay=lvl2_delay)
        self.addLink(e3, a2, bw=lvl2_bw, delay=lvl2_delay)
        self.addLink(e4, a2, bw=lvl2_bw, delay=lvl2_delay)

        # Connect aggregation switches to core switch
        self.addLink(a1, c1, bw=lvl1_bw, delay=lvl1_delay)
        self.addLink(a2, c1, bw=lvl1_bw, delay=lvl1_delay)

if (__name__ == '__main__'):
    setLogLevel('info')

    topo = AssignmentNetworks()
    # For Phase 3 only, comment OUT the following code line to test
    # your self-learning ethernet switch.
    net = Mininet(topo=topo, link=TCLink, autoSetMacs=True, autoStaticArp=True)
    # For Phase 3 only, comment IN the following code line to test your
    # self-learning ethernet switch.
    # net = Mininet(controller=RemoteController, topo=topo, link=TCLink, autoSetMacs=True, autoStaticArp=True)
    # Run network
    net.start()
    CLI(net)
    net.stop()
