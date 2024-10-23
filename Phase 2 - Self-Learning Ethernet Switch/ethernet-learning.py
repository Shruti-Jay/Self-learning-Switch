#!/usr/bin/env python

# Spring 2024 CSCI 4211: Introduction to Computer Networks
# This program serves as the SDN controller for the Ethernet-based
# self-learning switches. It was written in Python v3.

from pox.core import core
import pox.openflow.libopenflow_01 as of

# Even a simple usage of the logger is much nicer than print!
log = core.getLogger()

# TODO: Define your global data structures here.

network_topology = {} #added here
flood_counter = 0
packets_received = 0

def _handle_PacketIn(event):
  '''
  Handle an OFPacketIn message that a switch has sent to the controller because
  the switch doesn't have a matching rule for the packet it received.
  '''
  global flood_counter
  global packets_received
  packets_received += 1
  log.info('Number of packets received so far: {}'.format(packets_received))
  
  # Get the port the packet came in on for the switch that's contacting the 
  # controller.
  packet_input_port = event.port

  # Get the number of ports attached to the sending switch except for the
  # packet's input port. This variable should be used when updating your 
  # global flood counter.
  other_ports = len(event.connection.ports) - 2

  # Use POX to parse the packet.
  packet = event.parsed

  # Get the packet's source and destination MAC addresses.
  src_mac = str(packet.src)
  dst_mac = str(packet.dst)

  # Get the sending switch's ID.
  switch_ID = str(event.connection.dpid) + str(event.connection.ID)
  
  # This line of code prints infomation about packets that are sent to the 
  # controller.
  log.info('Packet has arrived: SRCMAC:{} DSTMAC:{} from switch:{} in-port:{}'.format(src_mac, dst_mac, switch_ID, packet_input_port))

  # TODO: Update the controller's global data structure that stores the 
  # information it learns about the network topology to include an entry for 
  # the packet's source host and the sending switch's port that can reach it, 
  # if such an entry does not already exist.

  # Update network topology if necessary. Added new code below
  if src_mac not in network_topology: 
    network_topology[src_mac] = (switch_ID, packet_input_port)



  # TODO: If the network topology already has an entry for the sending switch 
  # and the destination host, then install a new match-action rule or rules 
  # in the sending switch and have the original packet be fowarded to the 
  # correct output port. This is where you should use the code setting
  # message.match that was provided in Section 2.3 of the Phase 3 
  # instructions. Note: You will need to implement more code than the single 
  # line that is given to you.

  # If destination host is known, install flow table rules
  if dst_mac in network_topology:
    output_port = network_topology[dst_mac][1]
    if output_port != packet_input_port:
        msg = of.ofp_flow_mod()
        # msg.match = of.ofp_match.from_packet(packet, event.port)
        msg.match = of.ofp_match(dl_src=packet.src, dl_dst=packet.dst)
        # the commented-out line is from 2.3 step 4. The new line is step 5.
        msg.actions.append(of.ofp_action_output(port=output_port))
        event.connection.send(msg)
        # also for step 5
        reverse_msg = of.ofp_flow_mod()
        reverse_msg.match = of.ofp_match(dl_src=packet.dst, dl_dst=packet.src)
        reverse_msg.actions.append(of.ofp_action_output(port=packet_input_port))
        event.connection.send(reverse_msg)
  # If destination host is unknown, flood packet
  else:
    msg = of.ofp_packet_out()
    msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
    msg.data = event.ofp
    event.connection.send(msg)
    flood_counter += other_ports

  # TODO: Otherwise, have the sending switch flood the original packet to 
  # every port except for the one the packet came in from originally. No rules
  # should be installed in the switch in this case. Also, don't forget to 
  # update your global counter for the number of flooded messages.



def launch ():
  core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
  log.info("Pair-Learning switch running.")