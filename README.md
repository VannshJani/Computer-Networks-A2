# Computer-Networks-A2

# CS 331: Computer Networks Assignment #2 - Task 1

This repository contains the code and scripts for Task 1 of Assignment 2. The goal of Task 1 is to compare different TCP congestion control protocols using a custom Mininet topology. The experiments involve generating TCP traffic with iPerf3, capturing packets with tcpdump, and analyzing key performance metrics such as throughput, goodput, packet loss rate, and maximum TCP window size.

---

## Table of Contents

- [Assignment Overview](#assignment-overview)
- [Team & Protocol Assignment](#team--protocol-assignment)
- [Topology and Experiment Description](#topology-and-experiment-description)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Experiment Script Usage](#experiment-script-usage)
- [Visualization Script Usage](#visualization-script-usage)
- [File Structure](#file-structure)
- [Notes](#notes)
- [Submission Guidelines](#submission-guidelines)
- [License](#license)

---

## Assignment Overview

**Task 1: Comparison of Congestion Control Protocols [50 Points]**

- **Objective:**  
  Create a Mininet topology with 7 hosts (H1 to H7) connected to 4 switches (S1, S2, S3, S4). H1–H6 act as TCP clients and H7 as the TCP server. Generate TCP traffic using iPerf3 with configurable congestion control schemes and network parameters, capture the traffic, and analyze key performance metrics.
  
- **Performance Metrics to Measure:**  
  1. Throughput over time (with Wireshark I/O graphs)  
  2. Goodput  
  3. Packet loss rate  
  4. Maximum TCP window size achieved (with Wireshark I/O graphs)

---

## Team & Protocol Assignment

- **Teamwork:**  
  The assignment must be completed in pairs. Only one team member (Member 1) should submit the assignment on behalf of the team.

- **Protocol Assignment Scheme:**  
  Each team will work on three congestion control protocols based on their team number using the formulas below:

  1. **Protocol 1:** `(team_number % 10)`
  2. **Protocol 2:** `((team_number + 3) % 10)`
  3. **Protocol 3:** `((team_number + 6) % 10)`

- **List of Available Protocols:**

  | Protocol No. | Protocol    |
  | ------------ | ----------- |
  | 0            | Reno        |
  | 1            | CUBIC       |
  | 2            | BBR         |
  | 3            | BIC         |
  | 4            | Vegas       |
  | 5            | Westwood    |
  | 6            | HighSpeed   |
  | 7            | H-TCP       |
  | 8            | Scalable    |
  | 9            | Yeah        |

---

## Topology and Experiment Description

The Mininet topology is designed as follows:

- **Topology:**
  - **Switches:** S1, S2, S3, S4
  - **Hosts:** H1 to H7
  - **Connections:**  
    - Hosts H1–H2 connect to S1  
    - Hosts H3–H4 connect to S2  
    - Hosts H5–H6 connect to S3  
    - Host H7 connects to S4  
    - Inter-switch links:
      - S1–S2 with 100 Mbps (no loss)
      - S2–S3 with 50 Mbps (configurable loss)
      - S3–S4 with 100 Mbps (no loss)

- **Experiment Scenarios:**

  1. **Part (a):**  
     - Run a single TCP client on H1 connecting to the TCP server on H7.
     - Measure throughput, goodput, packet loss, and maximum window size.

  2. **Part (b):**  
     - Run staggered TCP clients on H1, H3, and H4 with different start times and durations:
       - H1: Start at T=0s, run for 150s
       - H3: Start at T=15s, run for 120s
       - H4: Start at T=30s, run for 90s
     - Measure and compare the performance parameters.

  3. **Part (c):**  
     - Use the defined inter-switch link bandwidths.
     - Conduct experiments under various conditions:
       - **Condition 1:** Only client on H3 is active.
       - **Condition 2:** Different combinations of clients (H1 & H2, H1 & H3, H1, H3 & H4) connect to H7.
     - Repeat experiments with link loss on S2–S3 set to 1% and 5% for further analysis.

---

## Prerequisites

Ensure you have the following installed:

- **Python 3.x**
- **Mininet** – Follow the [Mininet installation guide](http://mininet.org/download/) for setup.
- **iPerf3** – For generating TCP traffic.
- **tcpdump** – For packet capturing.
- **Scapy** – For PCAP file parsing.
- **NumPy** and **Matplotlib** – For numerical analysis and plotting.

Install required Python libraries using pip:

```bash
pip install numpy matplotlib scapy
