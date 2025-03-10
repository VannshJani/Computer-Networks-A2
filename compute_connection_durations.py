import pandas as pd

# TCP flag definitions (as integers)
SYN_FLAG = 0x02
FIN_FLAG = 0x01
ACK_FLAG = 0x10
RST_FLAG = 0x04

DEFAULT_DURATION = 100.0

# Read the CSV file; assuming tshark added a header row.
df = pd.read_csv('tcp_details.csv')

# Rename columns for convenience (adjust these if your CSV headers differ)
df.rename(columns={
    'frame.time_epoch': 'time',
    'ip.src': 'src_ip',
    'ip.dst': 'dst_ip',
    'tcp.srcport': 'src_port',
    'tcp.dstport': 'dst_port',
    'tcp.flags': 'tcp_flags'
}, inplace=True)

# Convert the time field to float.
df['time'] = df['time'].astype(float)

# Helper to convert flag values to integer, handling hex values if needed
def parse_flags(flag):
    try:
        flag = str(flag).strip()
        if flag.startswith("0x") or flag.startswith("0X"):
            return int(flag, 16)
        return int(flag)
    except Exception as e:
        # If conversion fails, return 0
        return 0

df['tcp_flags'] = df['tcp_flags'].apply(parse_flags)

# Create a unique connection identifier as a tuple:
# (Source IP, Destination IP, Source Port, Destination Port)
df['conn'] = df.apply(lambda row: (row['src_ip'], row['dst_ip'], row['src_port'], row['dst_port']), axis=1)

# Sort by time for chronological processing
df.sort_values('time', inplace=True)

# Dictionary to track connection start times and termination times
connections = {}
connection_results = []

for _, row in df.iterrows():
    conn = row['conn']
    ts = row['time']
    flags = row['tcp_flags']
    
    # If SYN flag is present, register connection start if not already present
    if flags & SYN_FLAG:
        if conn not in connections:
            connections[conn] = {'start': ts, 'end': None}
    
    # Check for termination packets:
    # FIN-ACK is observed if both FIN and ACK flags are set, or a RST is observed.
    if ((flags & FIN_FLAG and flags & ACK_FLAG) or (flags & RST_FLAG)):
        if conn in connections and connections[conn]['end'] is None:
            connections[conn]['end'] = ts

# Compute durations; assign default duration if no proper termination was found.
for conn, times in connections.items():
    start = times['start']
    end = times['end'] if times['end'] is not None else (start + DEFAULT_DURATION)
    duration = end - start
    connection_results.append((start, duration))

# Save the computed connection durations to a CSV file for later plotting.
results_df = pd.DataFrame(connection_results, columns=['start_time', 'duration'])
results_df.to_csv('connection_durations.csv', index=False)
print("Connection durations saved to connection_durations.csv")
