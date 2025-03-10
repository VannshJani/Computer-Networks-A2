import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Load the connection durations CSV (computed from the pcap)
df_conn = pd.read_csv('connection_durations.csv')

# Convert the 'start_time' from epoch (absolute time) to datetime
df_conn['datetime'] = pd.to_datetime(df_conn['start_time'], unit='s')

# Define t0 as the earliest packet time (absolute)
t0 = df_conn['datetime'].min()

# Compute relative time in seconds from t0 for each connection
df_conn['rel_time'] = (df_conn['datetime'] - t0).dt.total_seconds()

# Known event times (in seconds, relative to t0) based on your experiment:
LEGIT_START = 0    # at t=4 s, legitimate traffic starts
ATTACK_START = 20  # at t=24 s, SYN flood attack starts
ATTACK_END   = 120 # at t=124 s, SYN flood attack ends
LEGIT_END    = 140 # at t=144 s, legitimate traffic stops

# Plot the connection durations using relative time on the x-axis
plt.figure(figsize=(10, 5))
plt.scatter(df_conn['rel_time'], df_conn['duration'], color='blue', label='TCP Connections')

# Draw vertical lines for the key events
plt.axvline(LEGIT_START, color='orange', linestyle='--', label='Legitimate Traffic Start')
plt.axvline(ATTACK_START, color='red',    linestyle='--', label='Attack Start')
plt.axvline(ATTACK_END,   color='green',  linestyle='--', label='Attack End')
plt.axvline(LEGIT_END,    color='purple', linestyle='--', label='Legitimate Traffic End')

plt.xlabel('Time (s) from start of capture')
plt.ylabel('Connection Duration (s)')
plt.title('TCP Connection Durations (Relative Time)')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
