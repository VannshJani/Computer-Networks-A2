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

- **Linux Environment**: To modify kernel parameters.
- **tcpdump**: For capturing network packets.
- **tshark**: For processing pcap files.

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
   - Use the second Python script (`analyze_pcap.py`) to analyze pcap files.
   - Example command:
     ```
     python3 analyze_pcap.py pcap_file.pcap
     ```
   - This will print goodput, packet loss rate, and maximum TCP window size, and display plots for throughput and window size over time.

### Task-2 Part A

Instructions for Task-2 Part A will be provided separately.

## Example Use Cases

- **Experiment Part A**:
  - Run an experiment with BBR congestion control and no packet loss:
    ```
    python3 experiment.py --option=a --cc=bbr --loss=0
    ```
  - Analyze the resulting pcap file:
    ```
    python3 analyze_pcap.py pcap_captures/capture_a_bbr_0_h7_0.pcap
    ```

- **Experiment Part B**:
  - Run a staggered client experiment with Westwood congestion control:
    ```
    python3 experiment.py --option=b --cc=westwood --loss=0
    ```
  - Analyze the pcap file:
    ```
    python3 analyze_pcap.py pcap_captures/capture_b_westwood_0_h7_0.pcap
    ```

## Contributing

Contributions are welcome. Please ensure that any new code adheres to the existing structure and style.

## Acknowledgments

- This project uses Mininet for network emulation and iPerf3 for throughput measurement.
- Scapy is used for parsing pcap files, and Matplotlib for plotting.
