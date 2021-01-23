import subprocess
import time

interval = 1.0
last_index_total_tx1 = 0
last_index_total_rx1 = 0
last_index_total_tx2 = 0
last_index_total_rx2 = 0

init = False

while True:
    print("####################################")
    interface = 'enp178s0f0'
    baescmd = ("sudo  ethtool -S ") + interface

    result = subprocess.check_output(baescmd, shell=True).split()
    index_total_tx = result.index('rx_bytes_phy:') + 1
    index_total_rx = result.index('tx_bytes_phy:') + 1

    if (not init):
        bandwidth_tx = (float(result[index_total_tx]) - float(result[index_total_tx])) / interval
        bandwidth_rx = (float(result[index_total_rx]) - float(result[index_total_rx])) / interval
    else:
        bandwidth_tx = (float(result[index_total_tx]) - float(last_index_total_tx1)) / interval
        bandwidth_rx = (float(result[index_total_rx]) - float(last_index_total_rx1)) / interval

    print(interface + ':')
    # print('rx_bytes_phy: ' + str(result[index_total_tx]))
    # print('tx_bytes_phy: ' + str(result[index_total_rx]))
    print('Tx BW: ' + str(0.0 if bandwidth_tx < 200 else bandwidth_tx/1024.0/1024.0/1024.0*8) + ' Gbps')
    print('Rx BW: ' + str(0.0 if bandwidth_rx < 200 else bandwidth_rx/1024.0/1024.0/1024.0*8) + ' Gbps')

    last_index_total_tx1 = result[index_total_tx]
    last_index_total_rx1 = result[index_total_rx]

    interface = 'enp178s0f1'
    baescmd = ("sudo  ethtool -S ") + interface

    result = subprocess.check_output(baescmd, shell=True).split()
    index_total_tx = result.index('rx_bytes_phy:') + 1
    index_total_rx = result.index('tx_bytes_phy:') + 1

    if (not init):
        bandwidth_tx = (float(result[index_total_tx]) - float(result[index_total_tx])) / interval
        bandwidth_rx = (float(result[index_total_rx]) - float(result[index_total_rx])) / interval
        init = True
    else:
        bandwidth_tx = (float(result[index_total_tx]) - float(last_index_total_tx2)) / interval
        bandwidth_rx = (float(result[index_total_rx]) - float(last_index_total_rx2)) / interval

    print(interface + ':')
    # print('rx_bytes_phy: ' + str(result[index_total_tx]))
    # print('tx_bytes_phy: ' + str(result[index_total_rx]))
    print('Tx BW: ' + str(0.0 if bandwidth_tx < 200 else bandwidth_tx/1024.0/1024.0/1024.0*8) + ' Gbps')
    print('Rx BW: ' + str(0.0 if bandwidth_rx < 200 else bandwidth_rx/1024.0/1024.0/1024.0*8) + ' Gbps')
    last_index_total_tx2 = result[index_total_tx]
    last_index_total_rx2 = result[index_total_rx]

    time.sleep(interval)