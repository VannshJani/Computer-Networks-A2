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
   - Example command:
     ```
     python3 analysis.py pcap_file.pcap
     ```
   - This will print goodput, packet loss rate, and maximum TCP window size, and display plots for throughput and window size over time.

### Task-2 Part A

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
     ./extract_tcp_details.sh capture.pcap
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
     ./extract_tcp_details.sh capture.pcap
     ```
  3. Compute and plot connection durations:
     ```
     python3 compute_connection_durations.py
     python3 plot_connection_durations.py
     ```
