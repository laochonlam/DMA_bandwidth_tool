import time

interval = 1.0
last_tx1 = 0
last_rx1 = 0
last_tx2 = 0
last_rx2 = 0

init = False

def read_counter(interface, counter):
    with open(f'/sys/class/net/{interface}/statistics/{counter}', 'r') as f:
        return int(f.read().strip())

while True:
    print("####################################")
    interface = 'enp37s0f0np0'
    
    current_tx = read_counter(interface, 'tx_bytes')
    current_rx = read_counter(interface, 'rx_bytes')

    if not init:
        bandwidth_tx = (current_tx - current_tx) / interval
        bandwidth_rx = (current_rx - current_rx) / interval
    else:
        bandwidth_tx = (current_tx - last_tx1) / interval
        bandwidth_rx = (current_rx - last_rx1) / interval

    print(interface + ':')
    print('Tx BW: ' + str(0.0 if bandwidth_tx < 200 else round(bandwidth_tx/1024.0/1024.0/1024.0*8, 4)) + ' Gbps')
    print('Rx BW: ' + str(0.0 if bandwidth_rx < 200 else round(bandwidth_rx/1024.0/1024.0/1024.0*8, 4)) + ' Gbps')

    last_tx1 = current_tx
    last_rx1 = current_rx

    interface = 'enp37s0f1np1'
    
    current_tx = read_counter(interface, 'tx_bytes')
    current_rx = read_counter(interface, 'rx_bytes')

    if not init:
        bandwidth_tx = (current_tx - current_tx) / interval
        bandwidth_rx = (current_rx - current_rx) / interval
        init = True
    else:
        bandwidth_tx = (current_tx - last_tx2) / interval
        bandwidth_rx = (current_rx - last_rx2) / interval

    print(interface + ':')
    print('Tx BW: ' + str(0.0 if bandwidth_tx < 200 else round(bandwidth_tx/1024.0/1024.0/1024.0*8, 4)) + ' Gbps')
    print('Rx BW: ' + str(0.0 if bandwidth_rx < 200 else round(bandwidth_rx/1024.0/1024.0/1024.0*8, 4)) + ' Gbps')

    last_tx2 = current_tx
    last_rx2 = current_rx

    time.sleep(interval)
