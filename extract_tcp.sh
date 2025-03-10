#!/bin/bash
# Check for correct usage
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <input_pcap_file>"
  exit 1
fi

INPUT_PCAP="$1"
OUTPUT_CSV="tcp_details.csv"

echo "Extracting TCP details from $INPUT_PCAP ..."
tshark -r "$INPUT_PCAP" -Y "tcp" -T fields -E header=y -E separator=, \
  -e frame.time_epoch \
  -e ip.src \
  -e ip.dst \
  -e tcp.srcport \
  -e tcp.dstport \
  -e tcp.flags \
  > "$OUTPUT_CSV"

if [ $? -eq 0 ]; then
  echo "Extraction complete. Output saved to $OUTPUT_CSV"
else
  echo "An error occurred during extraction."
fi
