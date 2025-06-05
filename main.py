import time
import subprocess

interval = 2.0
# List of interfaces to monitor
interfaces = [
    'eth0', 'eth1', 'eth2', 'eth3', 'eth4', 'eth5', 'eth6', 'eth7', 'eth8', 'eth9',
]

# Configuration
USE_ETHTOOL = True  # Set to True to use ethtool, False to use sysfs

# Initialize dictionary to store last values for each interface
last_tx = {interface: 0 for interface in interfaces}
last_rx = {interface: 0 for interface in interfaces}
init = False

def read_counter(interface, counter):
    if USE_ETHTOOL:
        try:
            cmd = f"sudo ethtool -S {interface}"
            result = subprocess.check_output(cmd, shell=True).decode().split()
            
            if counter == 'tx_bytes':
                index = result.index('tx_bytes_phy:') + 1
            else:  # rx_bytes
                index = result.index('rx_bytes_phy:') + 1
                
            return int(result[index])
        except (subprocess.CalledProcessError, ValueError, IndexError):
            return 0
    else:
        try:
            with open(f'/sys/class/net/{interface}/statistics/{counter}', 'r') as f:
                return int(f.read().strip())
        except FileNotFoundError:
            return 0

def format_bw(bw):
    if bw < 1:  # Less than 1 byte
        return "0.0"
    # Convert to Gbps directly
    return f"{round(bw/1024.0/1024.0/1024.0*8, 2)}"  # Always show in Gbps with 2 decimal places

while True:
    print("\n" + "="*80)
    print(f"Network Bandwidth Monitor - {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    print(f"{'Interface':<15} {'Tx':>12} {'Rx':>12}")
    print("-"*80)
    
    # Monitor all interfaces
    for interface in interfaces:
        try:
            current_tx = read_counter(interface, 'tx_bytes')
            current_rx = read_counter(interface, 'rx_bytes')

            if not init:
                bandwidth_tx = (current_tx - current_tx) / interval
                bandwidth_rx = (current_rx - current_rx) / interval
            else:
                bandwidth_tx = (current_tx - last_tx[interface]) / interval
                bandwidth_rx = (current_rx - last_rx[interface]) / interval

            tx_str = format_bw(bandwidth_tx)
            rx_str = format_bw(bandwidth_rx)
            
            print(f"{interface:<15} {tx_str:>10}Gbps {rx_str:>10}Gbps")

            last_tx[interface] = current_tx
            last_rx[interface] = current_rx
            
        except Exception as e:
            print(f"{interface:<15} {'Error':>12} {'Error':>12}")
            continue

    if not init:
        init = True

    time.sleep(interval)
