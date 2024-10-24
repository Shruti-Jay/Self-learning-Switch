# Project Overview
This project is a culmination of the skills and knowledge acquired in Python programming, mininet, ping,  and iPerf throughout the course of the semester in CSCI 4211 Introduction to Computer Networks.

## Phase 1 Decription (Topology Creations and Evaluations)
Phase 1 is a learning phase to understand how to estimate and explain latency numbers. This phase estimates the throughput and latency for each of the links between the switches
by measuring them. Then, a new custom virtual Network is built using mininet (Called "Topology B").
### Notes:
- Each level of the topology (i.e., Core, Aggregation, Edge, and Host) is composed
of a single layer of switches or hosts.
- All links at the same level in the network topology will have the same predefined
latency and bandwidth performance parameters.

## Phase 2 Description (Self-Learning Ethernet Switches)
In this phase, Mininet was used to implement an Ethernet-based self-learning algorithm using an SDN controller.
The controller is implemented using Python’s POX. Provides framework for communicating with SDN switches using the
well-defined application programming interface (API), OpenFlow protocol. The
controller exercises direct control over the state in the SDN switches via
OpenFlow protocol.


