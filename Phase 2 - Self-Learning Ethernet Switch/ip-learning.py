#!/usr/bin/env python

# Spring 2024 CSCI 4211: Introduction to Computer Networks
# This program serves as the SDN controller for the IP-based
# self-learning switches. It was written in Python v3.

from pox.core import core
from pox.lib.addresses import IPAddr, EthAddr
from pox.lib.packet.ethernet import ethernet
from pox.lib.packet.arp import arp
import pox.openflow.libopenflow_01 as of
from pox.lib.packet.icmp import *
from pox.lib.packet import *
from pox.lib.packet.ipv4 import ipv4
from scapy.all import ARP, Ether, srp1, ICMP, IP, send


log = core.getLogger()

# Global data structure to store MAC address tables for each switch
mac_address_tables = {}

# Global counter to keep track of flooding
flood_counter = {}

def handle_arp_request(packet, packet_input_port, switch_ID):
    if packet.payload.opcode == arp.REQUEST:
        arp_req = packet.payload
        log.info('ARP Request received from {} for IP {}'.format(arp_req.hwsrc, arp_req.protosrc))
        
        # TODO: Implement your logic to handle ARP requests

def handle_icmp_packet(packet, packet_input_port, switch_ID):
    if packet.find('icmp'):
        icmp_packet = packet.find('icmp')
        if icmp_packet.type == ICMP.TYPE_ECHO_REQUEST:
            log.info('ICMP Echo Request received from {} to {}'.format(packet.src, packet.dst))
            
            # TODO: Implement your logic to handle ICMP Echo Requests

def handle_ipv4_packet(packet, packet_input_port, switch_ID):
    if packet.find('ipv4'):
        ipv4_packet = packet.find('ipv4')
        log.info('IPv4 packet received from {} to {}'.format(ipv4_packet.srcip, ipv4_packet.dstip))
        
        # TODO: Implement your logic to handle IPv4 packets

def _handle_PacketIn(event):
    packet_input_port = event.port
    all_ports = event.connection.ports
    other_ports = len(event.connection.ports) - 2
    packet = event.parsed
    src_mac = str(packet.src)
    dst_mac = str(packet.dst)
    switch_ID = str(event.connection.dpid) + str(event.connection.ID)
    
    log.info('Packet has arrived: SRCMAC:{} DSTMAC:{} from switch:{} in-port:{}'.format(src_mac, dst_mac, switch_ID, packet_input_port))
    
    # Handle ARP requests
    if packet.find('arp'):
        handle_arp_request(packet, packet_input_port, switch_ID)
    # Handle ICMP packets
    elif packet.find('icmp'):
        handle_icmp_packet(packet, packet_input_port, switch_ID)
    # Handle IPv4 packets
    elif packet.find('ipv4'):
        handle_ipv4_packet(packet, packet_input_port, switch_ID)

def launch ():
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    log.info("Pair-Learning switch running.")
