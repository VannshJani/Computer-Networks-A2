#!/usr/bin/env python3
import argparse
import time
import os
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import DefaultController
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink

class CustomTopo(Topo):
    def build(self, loss=0):
        s1, s2, s3, s4 = self.addSwitch('s1'), self.addSwitch('s2'), self.addSwitch('s3'), self.addSwitch('s4')
        h1, h2, h3, h4, h5, h6, h7 = [self.addHost(f'h{i}') for i in range(1, 8)]

        # Connect hosts to switches
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s2)
        self.addLink(h4, s2)
        self.addLink(h5, s3)
        self.addLink(h6, s3)
        self.addLink(h7, s4)

        # Connect switches with specified bandwidths
        self.addLink(s1, s2, bw=100,loss=0)
        self.addLink(s2, s3, bw=50, loss=loss)  # Loss applied to S2-S3
        self.addLink(s3, s4, bw=100,loss=0)

def count_packets(pcap_file):
    count = os.popen(f"tcpdump -r {pcap_file} 2>/dev/null | wc -l").read().strip()
    return count

def run_experiment(option, cc, loss):
    pcap_folder = "pcap_captures"
    os.system(f"mkdir -p {pcap_folder}")

    topo = CustomTopo(loss=loss)
    net = Mininet(topo=topo, controller=DefaultController, link=TCLink)
    net.start()

    # Get the end host (Server h7)
    h7 = net.get('h7')

    # Start tcpdump on h7 (assumed interface is h7-eth0)
    pcap_filename = f"{pcap_folder}/capture_{option}_{cc}_h7_{loss}.pcap"
    print(f"Starting tcpdump on h7 interface h7-eth0; saving to {pcap_filename}")
    h7.cmd(f"tcpdump -i h7-eth0 tcp -w {pcap_filename} &")

    # Start the iPerf3 server
    print("Starting iPerf3 server on H7 on port 5201")
    h7.cmd("iperf3 -s -p 5201 &")
    time.sleep(2)

    if option == 'a':
        h1 = net.get('h1')
        print(f"Running iPerf3 test from H1 to H7 using {cc}")
        h1.cmd(f'iperf3 -c 10.0.0.7 -p 5201 -b 10M -P 10 -t 150 -C {cc} &')
        time.sleep(155)

    elif option == 'b':
        h1, h3, h4 = net.get('h1', 'h3', 'h4')
        print("Starting staggered clients")
        h1.cmd(f'iperf3 -c 10.0.0.7 -p 5201 -b 10M -P 10 -t 150 -C {cc} &')
        time.sleep(15)
        print("Staring next client")
        h3.cmd(f'iperf3 -c 10.0.0.7 -p 5201 -b 10M -P 10 -t 120 -C {cc} &')
        time.sleep(15)
        print("Staring next client")
        h4.cmd(f'iperf3 -c 10.0.0.7 -p 5201 -b 10M -P 10 -t 90 -C {cc} &')
        time.sleep(155)

    elif option in ['c', 'd']:
        h1, h2, h3, h4 = net.get('h1', 'h2', 'h3', 'h4')

        print("Condition 1: Running H3 -> H7")
        h3.cmd(f'iperf3 -c 10.0.0.7 -p 5201 -b 10M -P 10 -t 60 -C {cc} &')
        time.sleep(65)

        print("Condition 2a: Running H1 and H2 -> H7")
        h1.cmd(f'iperf3 -c 10.0.0.7 -p 5201 -b 10M -P 10 -t 60 -C {cc} &')
        h2.cmd(f'iperf3 -c 10.0.0.7 -p 5201 -b 10M -P 10 -t 60 -C {cc} &')
        time.sleep(65)

        print("Condition 2b: Running H1 and H3 -> H7")
        h1.cmd(f'iperf3 -c 10.0.0.7 -p 5201 -b 10M -P 10 -t 60 -C {cc} &')
        h3.cmd(f'iperf3 -c 10.0.0.7 -p 5201 -b 10M -P 10 -t 60 -C {cc} &')
        time.sleep(65)

        print("Condition 2c: Running H1, H3, and H4 -> H7")
        h1.cmd(f'iperf3 -c 10.0.0.7 -p 5201 -b 10M -P 10 -t 60 -C {cc} &')
        h3.cmd(f'iperf3 -c 10.0.0.7 -p 5201 -b 10M -P 10 -t 60 -C {cc} &')
        h4.cmd(f'iperf3 -c 10.0.0.7 -p 5201 -b 10M -P 10 -t 60 -C {cc} &')
        time.sleep(65)

    # Stop tcpdump capture on h7
    h7.cmd("pkill tcpdump")

    print(f"PCAP capture saved in {pcap_folder} for host h7.")
    net.stop()
    print(f"Experiment complete for option {option} with scheme {cc}.")
    # folders_list = os.listdir(pcap_folder)
    # file1 = folders_list[0]
    # count = count_packets(f"{pcap_folder}/{file1}")
    # print(f"Number of packets in first file are: {count}")

if __name__ == '__main__':
    setLogLevel('info')
    parser = argparse.ArgumentParser(description="Mininet TCP Congestion Control Experiment")
    parser.add_argument('--option', type=str, required=True, choices=['a', 'b', 'c', 'd'],
                        help="Select experiment part (a, b, c, d)")
    parser.add_argument('--cc', type=str, required=True, choices=['bbr', 'westwood', 'scalable'],
                        help="Choose congestion control algorithm (bbr, westwood, scalable)")
    parser.add_argument('--loss', type=int, default=0,
                        help="Packet loss percentage on S2-S3 link (default: 0)")
    
    args = parser.parse_args()

    if args.option == "d":
        print("\nRunning experiment d with 1% and 5% loss")
        run_experiment("c", args.cc, 1)
        run_experiment("c", args.cc, 5)
    else:
        run_experiment(args.option, args.cc, args.loss)
