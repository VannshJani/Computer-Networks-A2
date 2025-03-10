#!/usr/bin/env python3
import pexpect
import time

def main():
    # Start Mininet with the given topology and configuration.
    print("Starting Mininet...")
    mininet_cmd = "sudo mn --topo=single,2 --mac --switch=ovsk --controller=default"
    child = pexpect.spawn(mininet_cmd, encoding='utf-8')
    child.logfile = open('mininet_session.log', 'w')  # Log session output for debugging

    # Wait for the Mininet prompt.
    child.expect("mininet>")

    # Configure h2 with sysctl settings.
    print("Configuring h2...")
    child.sendline("h2 sysctl -w net.ipv4.tcp_max_syn_backlog=1024")
    child.expect("mininet>")
    child.sendline("h2 sysctl -w net.ipv4.tcp_syncookies=0")
    child.expect("mininet>")
    child.sendline("h2 sysctl -w net.ipv4.tcp_synack_retries=2")
    child.expect("mininet>")

    # Start iperf3 server on h2 in the background.
    print("Starting iperf3 server on h2...")
    child.sendline("h2 iperf3 -s -p 5201 &")
    child.expect("mininet>")

    # Start tcpdump on h1 in the background.
    print("Starting tcpdump on h1...")
    child.sendline("h1 tcpdump -i h1-eth0 -w capture.pcap &")
    child.expect("mininet>")


    # Start iperf3 client on h1.
    print("Starting iperf3 client on h1...")
    child.sendline("h1 iperf3 -c 10.0.0.2 -p 5201 -t 150 -b 5M &")
    child.expect("mininet>")

    print("Waiting 20 seconds before starting SYN flood on h1...")
    time.sleep(20)

    # Start SYN flood attack using hping3.
    print("Starting SYN flood on h1...")
    child.sendline("h1 hping3 -S -p 5201 --flood 10.0.0.2 &")
    child.expect("mininet>")

    print("SYN flood running. Waiting 100 seconds before stopping attack...")
    time.sleep(100)

    # Stop hping3 to allow proper connection termination.
    print("Stopping SYN flood (graceful stop)...")
    child.sendline("h1 killall -SIGINT hping3")
    child.expect("mininet>")


    # Ensure hping3 is fully stopped if still running.
    print("Ensuring hping3 is fully stopped...")
    child.sendline("h1 killall -9 hping3")
    child.expect("mininet>")

    # Allow iperf3 to run for another 20 seconds after stopping SYN flood.
    print("Allowing iperf3 client to run for another 20 seconds...")
    time.sleep(20)

    # Gracefully stop iperf3 on h1.
    print("Stopping iperf3 client on h1 gracefully...")
    child.sendline("h1 killall -SIGINT iperf3")
    child.expect("mininet>")
    time.sleep(5)  # Give time for FIN packets to be sent

    # Forcefully kill iperf3 if it's still running.
    print("Ensuring iperf3 is fully stopped...")
    child.sendline("h1 killall -9 iperf3")
    child.expect("mininet>")

    # Stop tcpdump on h1.
    print("Stopping tcpdump on h1...")
    child.sendline("h1 pkill tcpdump")
    child.expect("mininet>")

    # Exit Mininet CLI.
    print("Exiting Mininet...")
    child.sendline("exit")
    child.close()
    print("Script completed.")

if __name__ == "__main__":
    main()
