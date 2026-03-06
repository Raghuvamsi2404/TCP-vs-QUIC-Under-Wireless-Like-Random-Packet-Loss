# TCP-vs-QUIC-Under-Wireless-Like-Random-Packet-Loss
EE6750 - Transport over Wireless Networks

# Linux 

- We set up Windows Subsystem for Linux (wsl --install)

    - Default account: adminlinux

    - Password: 31257363

- Update WSL (sudo apt update)

`sudo apt install iproute2 iperf3 python3 python3-pip -y`

# Setting up, working directory 

`mkdir tcp-vs-quic`

`cd tcp-vs-quic`

`python3 -m venv venv`

- Activate Virtual Environment

`source venv/bin/activate`

 - Install aioquic inside the Virtual Environment

`pip install aioquic`
  
# TCP throughput experiment at different loss rates

- Step 1: We navigated to the project route in two different terminals

`cd tcp-vs-quic`

`source venv/bin/activate`

- Step 2: Execution from two terminals

    - Terminal 1 - starts iperf3 server:
 
      `iperf3 -s`

      <img width="1063" height="950" alt="image" src="/screenshots/iperf3 -s.png" />

    - Terminal 2 - sequential test runs:

    ```
    # 0% loss - clean baseline
    sudo tc qdisc add dev lo root netem loss 0%
    iperf3 -c 127.0.0.1 -t 10 -J > result_0.json

    # 1% loss
    sudo tc qdisc change dev lo root netem loss 1%
    iperf3 -c 127.0.0.1 -t 10 -J > result_1.json

    # 3% loss
    sudo tc qdisc change dev lo root netem loss 3%
    iperf3 -c 127.0.0.1 -t 10 -J > result_3.json

    # 5% loss
    sudo tc qdisc change dev lo root netem loss 5%
    iperf3 -c 127.0.0.1 -t 10 -J > result_5.json

    # 10% loss
    sudo tc qdisc change dev lo root netem loss 10%
    iperf3 -c 127.0.0.1 -t 10 -J > result_10.json

    # Final clean up
    sudo tc qdisc del dev lo root
    ```

    <img width="1063" height="950" alt="image" src="/screenshots/tc-qdisc-tests.png" />

- Step 3 - Results plots

    - plot_results.py (We used nano to create and edit the plot_results.py file)

    `nano plot_results.py` and then ctr + X to exit and Y to save. 
    
    To verify successful file save we used:

    `ls` - To list files in the directory.
            
    `cat plot_results.py` - To display the files. 

    Then we followed this steps to display the result:

    `pip install matplotlib`

    `python3 plot_results.py`

    `cp early_results.png /mnt/c/Users/ADMIN/Desktop/` - To transfer the plot to windows for easy access. 

    <img width="1063" height="950" alt="image" src="/screenshots/early_results.png" />