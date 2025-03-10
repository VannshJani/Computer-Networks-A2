# Computer Networks Assignment-2

This repository contains code for assignment-2:

1. **Task-1: Comparison of Congestion Control Protocols**
   - This task involves creating a Mininet topology and running experiments to compare different TCP congestion control protocols.
   - The code includes scripts to run experiments and analyze the results from pcap files.

2. **Task-2 Part A: Implementation of SYN Flood Attack**
   - This task involves modifying Linux kernel parameters to implement a SYN flood attack.
   - The code for this part is not included here but will be provided separately.

## Dependencies

For Task-1:

- **Mininet**: A network emulator for creating custom network topologies.
- **iPerf3**: A tool for measuring network throughput.
- **Python 3.x**: For scripting the experiments and analyzing pcap files.
- **Scapy**: A Python library for parsing pcap files.
- **Matplotlib**: For plotting throughput and window size over time.

For Task-2 Part A:

- **Mininet**: A network emulator for creating custom network topologies.
- **iPerf3**: A tool for measuring network throughput.
- **hping3**: A tool for generating network traffic, used here to simulate a SYN flood attack.
- **tcpdump**: For capturing network packets.
- **tshark**: For processing pcap files.
- **Python 3.x**: For scripting the experiment.
- **Pandas**: For data manipulation and analysis.
- **Matplotlib**: For plotting connection durations.

## Usage

### Task-1

1. **Running Experiments**:
   - Use the first Python script (`topology.py`) to run the experiments.
   - Example command:
     ```
     python3 topology.py --option=a --cc=bbr --loss=0
     ```
   - Options:
     - `--option`: Choose the experiment part (`a`, `b`, `c`, `d`).
     - `--cc`: Select the congestion control algorithm (`bbr`, `westwood`, `scalable`).
     - `--loss`: Specify packet loss percentage on the S2-S3 link (default: 0).

2. **Analyzing and Visualizing Metrics**:
   - Use the second Python script (`analysis.py`) to analyze pcap files.
   - The pcap files from running the above code will be generated in a pcap_captures folder, replace <pcap_file.pcap> with actual pcap file name from this directory.
   - Example command:
     ```
     python3 analysis.py pcap_file.pcap
     ```
   - This will print goodput, packet loss rate, and maximum TCP window size, and display plots for throughput and window size over time.



### Task 2: Part A

#### Running the Experiment

1. **Starting Mininet and Configuring the Network**:
   - Use the provided Python script (`syn_flood_experiment.py`) to start Mininet and configure the network.
   - This script sets up a single switch topology with two hosts, configures sysctl settings on one host to facilitate the SYN flood attack, starts an iperf3 server, and begins capturing packets with tcpdump.
   - Example command:
     ```
     python3 syn_flood_experiment.py
     ```

2. **Generating the SYN Flood Attack**:
   - The script automatically starts a SYN flood attack using hping3 after 20 seconds of legitimate traffic.
   - The attack runs for 100 seconds.

3. **Stopping the Experiment**:
   - After stopping the SYN flood attack, the script allows legitimate traffic to continue for another 20 seconds before stopping it.
   - Finally, it stops tcpdump and exits Mininet.

#### Analyzing the pcap File

1. **Extracting TCP Details**:
   - Use the provided Bash script (`extract_tcp_details.sh`) to extract TCP packet details from the pcap file using tshark.
   - Example command:
     ```
     bash extract_tcp.sh capture.pcap
     ```

2. **Computing Connection Durations**:
   - Use the Python script (`compute_connection_durations.py`) to compute connection durations from the extracted TCP details.
   - This script saves the results to a CSV file.
   - Example command:
     ```
     python3 compute_connection_durations.py
     ```

3. **Plotting Connection Durations**:
   - Use the Python script (`plot_connection_durations.py`) to plot connection durations over time.
   - This script loads the computed connection durations and plots them with key event markers (legitimate traffic start, attack start/end, legitimate traffic end).
   - Example command:
     ```
     python3 plot_connection_durations.py
     ```

#### Example Use Cases

- **Running the Full Experiment**:
  1. Start the Mininet experiment:
     ```
     python3 syn_flood_experiment.py
     ```
  2. Extract TCP details from the pcap file:
     ```
     bash extract_tcp.sh capture.pcap
     ```
  3. Compute and plot connection durations:
     ```
     python3 compute_connection_durations.py
     python3 plot_connection_durations.py
     ```



## Running Task 2(B): SYN Flood Mitigation

This section provides instructions for running our SYN flood mitigation experiment.

### Prerequisites
We require the following prerequisites to be installed:
- Python 3.6+
- Mininet
- pexpect
- tcpdump
- hping3
- iperf3
- tshark
- matplotlib, pandas, numpy (for processing and visualization)
- Linux OS (preferably, as the below commands are for Linux)

We can install the Python dependencies using:
```
pip install pexpect pandas matplotlib numpy
```

And system packages using:
```
sudo apt install mininet tcpdump hping3 iperf3 tshark
```

### Execution Steps

**Step 1: Run the baseline experiment (no mitigation)**
```
sudo python3 2a.py
```
This creates `capture.pcap` and generates baseline data without SYN flood protection.

**Step 2: Run the mitigation experiment**
```
sudo python3 2b.py
```
This creates `capture_mitigated.pcap` with SYN flood mitigation enabled.

**Step 3: Process and analyze the results**
```
python3 processing_and_compute_mitigated.py
```
This generates comparative visualizations and metrics in the `results/` directory:
- `results/syn_flood_mitigation_comparison.png`: Visualization comparing connection durations
- `results/connection_durations_original.csv`: Original connection data
- `results/connection_durations_mitigated.csv`: Mitigated connection data

### Experiment Details

**Key mitigation techniques we implemented:**
- SYN cookies enabled (`net.ipv4.tcp_syncookies=1`)
- Increased SYN-ACK retries (`net.ipv4.tcp_synack_retries=5`)
- Optimized TCP resource management

**Analysis**

To examine the packet captures in Wireshark, we use:
```
wireshark capture.pcap
wireshark capture_mitigated.pcap
```

Useful Wireshark filters for our analysis:
- SYN packets: `tcp.flags.syn == 1 and tcp.flags.ack == 0`
- SYN-ACK responses: `tcp.flags.syn == 1 and tcp.flags.ack == 1`
- Attack traffic: `tcp.port == 5201`



# Task 3: Analysis of Nagle's Algorithm on TCP/IP Performance

## What is Nagle's Algorithm?

Nagle's algorithm is a method used to improve the efficiency of TCP/IP networks by reducing the number of small packets sent over the network. It works by combining multiple small outgoing messages into a single, larger packet before transmission.

Key characteristics:
- It buffers small packets until either:
  - The previous packet is acknowledged
  - Enough data accumulates to fill a maximum segment size (MSS)
- It's especially useful for applications that send small amounts of data frequently

## What is Delayed ACK?

Delayed ACK is a TCP/IP optimization technique that:
- Allows TCP to delay sending an acknowledgment for received data
- Typically waits up to 200ms to see if there is any response data to be sent that the ACK can be "piggybacked" on
- Reduces network overhead by decreasing the number of small ACK packets

# Step-by-Step Execution Guide for Task 3:

This guide provides detailed instructions for setting up and running the experiments to analyze the effect of Nagle's algorithm on TCP/IP performance.

## Prerequisites

- Two machines (can be virtual machines) running Linux
- Python 3.6 or higher installed
- Basic networking tools (Wireshark, netstat, etc.)
- Administrator/root access to modify system settings

## Step 1: File Setup

1. Save the following files to your working directory:
   - `tcp_server.py`
   - `tcp_client.py`
   - `run_tests.py`

2. Ensure the files have execution permissions:
   ```bash
   chmod +x tcp_server.py tcp_client.py run_tests.py
   ```

## Step 2: Manual Testing (For Understanding)

Before running the automated tests, we can manually test each configuration to understand what's happening:

### Configure and Run Server

1. Start the server with the desired configuration:

   ```bash
   # Configuration 1: Nagle's Algorithm enabled, Delayed-ACK enabled
   python tcp_server.py --port 9999
   
   # Configuration 2: Nagle's Algorithm enabled, Delayed-ACK disabled
   python tcp_server.py --port 9999 --disable-delayed-ack
   
   # Configuration 3: Nagle's Algorithm disabled, Delayed-ACK enabled
   python tcp_server.py --port 9999 --disable-nagle
   
   # Configuration 4: Nagle's Algorithm disabled, Delayed-ACK disabled
   python tcp_server.py --port 9999 --disable-nagle --disable-delayed-ack
   ```

### Configure and Run Client

2. In a separate terminal or machine, run the client:

   ```bash
   # Configuration 1: Nagle's Algorithm enabled, Delayed-ACK enabled
   python tcp_client.py --server SERVER_IP --port 9999 --file-size 4096 --rate 40 --duration 120
   
   # Configuration 2: Nagle's Algorithm enabled, Delayed-ACK disabled
   python tcp_client.py --server SERVER_IP --port 9999 --file-size 4096 --rate 40 --duration 120 --disable-delayed-ack
   
   # Configuration 3: Nagle's Algorithm disabled, Delayed-ACK enabled
   python tcp_client.py --server SERVER_IP --port 9999 --file-size 4096 --rate 40 --duration 120 --disable-nagle
   
   # Configuration 4: Nagle's Algorithm disabled, Delayed-ACK disabled
   python tcp_client.py --server SERVER_IP --port 9999 --file-size 4096 --rate 40 --duration 120 --disable-nagle --disable-delayed-ack
   ```

   (We are supposed to replace SERVER_IP with the actual IP address as per our server machine)

3. Observe the output and log files for the performance metrics.

## Step 3: Automated Testing

For consistent results and easier comparison, use the automated test script:

```bash
python run_tests.py
```

This script will:
1. Run all four configurations sequentially
2. Collect and log performance metrics

## References

1. RFC 896 - Nagle's Algorithm: https://tools.ietf.org/html/rfc896
2. RFC 1122 - Delayed ACK: https://tools.ietf.org/html/rfc1122
3. TCP Performance: http://www.tcpipguide.com/free/t_TCPConnectionPerformanceFeaturesPipeliningSlidingWind.htm
