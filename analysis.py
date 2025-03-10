#!/usr/bin/env python3
import sys
import numpy as np
import matplotlib.pyplot as plt
from scapy.all import rdpcap, TCP, IP

def parse_pcap(pcap_file):
    # Read all packets from the pcap file
    packets = rdpcap(pcap_file)
    # Filter only TCP over IP packets
    tcp_packets = [pkt for pkt in packets if TCP in pkt and IP in pkt]
    if not tcp_packets:
        print("No TCP packets found in the provided pcap.")
        sys.exit(1)
    return tcp_packets

def analyze_packets(tcp_packets):
    # Get start and end times of the capture
    start_time = tcp_packets[0].time
    end_time = tcp_packets[-1].time
    duration = end_time - start_time

    total_bytes = 0            # Total bytes (all packet sizes)
    total_payload_bytes = 0    # Total payload (data) bytes
    retransmission_count = 0   # Count of retransmitted packets
    max_window = 0             # Overall maximum window size

    # To roughly detect retransmissions, track the highest seen TCP sequence number per flow.
    # Using flow key: (src IP, dst IP, src port, dst port)
    seq_tracker = {}

    # For plotting, aggregate data into one-second bins.
    nbins = int(np.ceil(duration))
    throughput_per_bin = np.zeros(nbins)  # payload bytes per second
    window_per_bin = np.zeros(nbins)      # max window observed in each bin

    for pkt in tcp_packets:
        pkt_time = pkt.time
        tcp = pkt[TCP]
        ip = pkt[IP]
        pkt_len = len(pkt)
        total_bytes += pkt_len

        # Extract TCP payload (if any)
        payload = bytes(tcp.payload)
        payload_len = len(payload)
        total_payload_bytes += payload_len

        # Check the TCP window size field (an unsigned 16-bit value)
        win_size = tcp.window
        if win_size > max_window:
            max_window = win_size

        # Determine the time bin index (0-indexed)
        bin_index = int(pkt_time - start_time)
        if bin_index < nbins:
            throughput_per_bin[bin_index] += payload_len
            # Update maximum window size in this time bin if needed
            if win_size > window_per_bin[bin_index]:
                window_per_bin[bin_index] = win_size

        # Use flow tuple to detect retransmissions
        flow_key = (ip.src, ip.dst, tcp.sport, tcp.dport)
        seq = tcp.seq
        if flow_key in seq_tracker:
            # If we see a sequence number lower than the highest seen, mark as a retransmission
            if seq < seq_tracker[flow_key]:
                retransmission_count += 1
            else:
                seq_tracker[flow_key] = seq
        else:
            seq_tracker[flow_key] = seq

    # Calculate overall throughput and goodput in Mbps
    throughput_mbps = (total_bytes * 8) / (duration * 1e6)
    goodput_mbps = (total_payload_bytes * 8) / (duration * 1e6)
    # Estimate packet loss rate as a fraction of retransmitted packets
    total_tcp_packets = len(tcp_packets)
    packet_loss_rate = (retransmission_count / total_tcp_packets) * 100

    metrics = {
        'duration': duration,
        'throughput_mbps': throughput_mbps,
        'goodput_mbps': goodput_mbps,
        'packet_loss_rate': packet_loss_rate,
        'max_window': max_window,
        'throughput_per_bin': throughput_per_bin,
        'window_per_bin': window_per_bin,
        'time_bins': np.arange(nbins)
    }
    return metrics

def plot_throughput(metrics):
    time_bins = metrics['time_bins']
    # Convert per-bin payload bytes to Mbps (bytes -> bits, then divide by 1e6)
    throughput_mbps_bins = (metrics['throughput_per_bin'] * 8) / 1e6

    plt.figure()
    plt.plot(time_bins, throughput_mbps_bins, marker='o')
    plt.xlabel("Time (s)")
    plt.ylabel("Throughput (Mbps)")
    plt.title("Throughput Over Time (Payload Data)")
    plt.grid(True)
    plt.show()

def plot_max_window(metrics):
    time_bins = metrics['time_bins']
    plt.figure()
    plt.plot(time_bins, metrics['window_per_bin'], marker='o', color='red')
    plt.xlabel("Time (s)")
    plt.ylabel("TCP Window Size")
    plt.title("Maximum TCP Window Size Over Time")
    plt.grid(True)
    plt.show()

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <pcap file>")
        sys.exit(1)
    pcap_file = sys.argv[1]

    # Parse pcap and analyze packets
    tcp_packets = parse_pcap(pcap_file)
    metrics = analyze_packets(tcp_packets)

    print("Goodput: {:.2f} Mbps".format(metrics['goodput_mbps']))
    print("Packet Loss Rate: {:.2f}%".format(metrics['packet_loss_rate']))
    print("Maximum TCP Window Size Observed: {}".format(metrics['max_window']))

    # Plot the results in separate figures
    plot_throughput(metrics)
    plot_max_window(metrics)

if __name__ == "__main__":
    main()
