#!/usr/bin/env python

# Spring 2024 CSCI 4211: Introduction to Computer Networks
# This program serves as a script that constructs topology D.
# It was written in Python v3.

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.node import RemoteController
from scapy.all import ARP, Ether, srp1, ICMP, IP, send

class AssignmentNetworks(Topo):
    def __init__(self, **opts):
        Topo.__init__(self, **opts)

        # TODO: Define all of the hosts with subnets.
        h1 = self.addHost('h1', ip="10.0.1.100/24", defaultRoute="via 10.0.1.1")
        h2 = self.addHost('h2', ip="10.0.2.100/24", defaultRoute="via 10.0.2.1")
        h3 = self.addHost('h3', ip="10.0.3.100/24", defaultRoute="via 10.0.3.1")
        
        
        # TODO: Define the IP router.
        router = self.addHost('router')

        # TODO: Add links between the hosts and router.
        self.addLink(h1, router, intfName1='h1-eth0', intfName2='router-eth0')
        self.addLink(h2, router, intfName1='h2-eth0', intfName2='router-eth1')
        self.addLink(h3, router, intfName1='h3-eth0', intfName2='router-eth2')
        
    def handle_arp(self, packet, port):
        if packet.op == 1:  # ARP Request
            arp_reply = Ether(dst=packet.src, src=packet.dst) / ARP(op=2, hwsrc=packet.hwsrc, psrc=packet.pdst, hwdst=packet.hwsrc, pdst=packet.psrc)
            send(arp_reply, iface=port)
        elif packet.op == 2:  # ARP Reply
            pass  # No action needed for ARP Replies

    def handle_icmp(self, packet, port):
        if packet[ICMP].type == 8:  # ICMP Echo Request
            icmp_reply = IP(dst=packet[IP].src) / ICMP(type=0, id=packet[ICMP].id, seq=packet[ICMP].seq) / packet[ICMP].load
            send(icmp_reply, iface=port)

    def handle_routing(self, packet):
        static_routing_table = {
            '10.0.1.0/24': {'next_hop': '10.0.1.1', 'out_intf': 'router-eth0'},
            '10.0.2.0/24': {'next_hop': '10.0.2.1', 'out_intf': 'router-eth1'},
            '10.0.3.0/24': {'next_hop': '10.0.3.1', 'out_intf': 'router-eth2'}
        }
        dst_ip = packet[IP].dst
        for subnet, route_info in static_routing_table.items():
            if IP(dst_ip) in IP(subnet):
                next_hop = route_info['next_hop']
                out_intf = route_info['out_intf']
                return next_hop, out_intf
        return None, None  # No matching route found
    def handle_packet(self, packet, port):
    # Handle ARP requests
        if ARP in packet:
            self.handle_arp(packet, port)
    # Handle ICMP echo requests
        elif ICMP in packet and packet[ICMP].type == 8:
            self.handle_icmp(packet, port)
    # Handle routing
        elif IP in packet:
            next_hop, out_intf = self.handle_routing(packet)
            if next_hop and out_intf:
                packet[Ether].src = packet[Ether].dst
                packet[Ether].dst = None
                packet[IP].ttl -= 1
                send(packet, iface=out_intf)

if __name__ == '__main__':
    setLogLevel( 'info' )

    topo = AssignmentNetworks()
    # TODO: You can comment in the following code line if you wish to test the
    # construction of your topology without having the controller implemented.
    # You will need to also comment out the subsequent code line.
    #net = Mininet(topo = topo, link = TCLink, autoSetMacs = True, autoStaticArp = True)
    net = Mininet(controller = RemoteController, topo = topo, link = TCLink, autoSetMacs = True, autoStaticArp = True)

    # Run network
    net.start()
    CLI( net )
    net.stop()