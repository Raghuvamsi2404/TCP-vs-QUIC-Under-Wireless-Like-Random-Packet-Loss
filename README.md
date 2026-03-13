# TCP-vs-QUIC-Under-Wireless-Like-Random-Packet-Loss
EE6750 - Transport over Wireless Networks

## Milestones Schedule 

- Milestone 1 - Project Checkpoint

   - 10-slide narrated presentation with full rubric alignment
  
   - Problem statement, layered reasoning, hypotheses, experimental design
     
   - WSL2 + tc netem environment set up and working

   - TCP baseline experiments completed across all 5 loss rates
      
   - Real data chart (TCP throughput vs packet loss) generated and embedded
      
   - GitHub repo live with README, scripts, and plot_results.py documented
     
- Milestone 2 - Full Data Collection & Analysis

  - QUIC (aioquic) server and client fully working and tested

  - QUIC file transfer experiment run across all 5 loss rates (0%, 1%, 3%, 5%, 10%)
  
  - Both TCP and QUIC run 10 trials each per loss rate equals to 100 total runs

  - Side-by-side comparison charts: TCP vs QUIC throughput

  - Flow Completion Time (FCT) measured and compared for both

  - Retransmission counts collected and compared

  - CDF plots of latency and FCT generated, beyond just averages

  - 95% confidence intervals calculated for all metrics
  
- Milestone 3 - Final Report & Presentation
    
  - Full written report covering: introduction, methodology, results, analysis, conclusions
  
  - All final graphs embedded with proper interpretation

  - Hypotheses H1, H2, H3 confirmed or rejected with data evidence
  
  - Limitations section: loopback vs real wireless, netem model constraints
  
  - Updated GitHub repo with all final scripts and data

# Milestone 1

## Linux 

- We set up Windows Subsystem for Linux (wsl --install)

    - Default account: adminlinux

    - Password: 31257363

- Update WSL (sudo apt update)

`sudo apt install iproute2 iperf3 python3 python3-pip -y`

## Setting up, working directory 

`mkdir tcp-vs-quic`

`cd tcp-vs-quic`

`python3 -m venv venv`

- Activate Virtual Environment

`source venv/bin/activate`

 - Install aioquic inside the Virtual Environment

`pip install aioquic`

- Using requiremnt.txt 

`nano requirements.txt`

`pip install -r requirements.txt --break-system-packages`
  
## TCP throughput experiment at different loss rates

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
    
## Milestone 1 Presentation 

[EE6750_Project_Group2.pdf](/milestones/one/EE6750_Project_Group2.pdf)

[Zipped_code_milestone_1](/milestones/one/TCP-vs-QUIC-Under-Wireless-Like-Random-Packet-Loss.zip)

# Milestone 2

## Navigating to WSL terminal root directory 

`cd tcp-vs-quic`

`source venv/bin/activate`

- Verified aioquic installation

`python3 -c "import aioquic; print('aioquic ready')"`

<img width="1063" height="950" alt="image" src="/screenshots/aioquic_ready.png" />

## Setting up SSL certificates required for QUIC

`openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"`

<img width="1063" height="950" alt="image" src="/screenshots/ssl_cert_generation.png" />

## Setting up QUIC server

`nano quic_server.py`

<img width="1063" height="950" alt="image" src="/screenshots/quic_server.png" />

## Setting up QUIC client

`nano quic_client.py`

<img width="1063" height="950" alt="image" src="/screenshots/quic_client.png" />

- Test file:

  - We're using a test pdf file of 10.1 mb from open file (Cartographic Perspectives) 

  - https://cartographicperspectives.org/index.php/journal/article/view/cp13-full/pdf 

  - We copy our test pdf file to the 'testfile.bin'

  `cp /mnt/c/Users/ADMIN/Desktop/pkpadmin_1008-4741-1-CE.pdf ~/tcp-vs-quic/testfile.bin`

  `ls -lh ~/tcp-vs-quic/testfile.bin`

  <img width="1063" height="950" alt="image" src="/screenshots/testfile_bin.png" />

## QUIC Baseline Test (Loopback Functional Verification)

- Terminal 1: Server

`python3 quic_server.py`

<img width="1063" height="950" alt="image" src="/screenshots/quic_server_test.png" />

- Terminal 2: Client

`python3 quic_client.py`

<img width="1063" height="950" alt="image" src="/screenshots/quic_client_output.png" />

## QUIC experiments at all 5 loss rates × 10 trials

`nano run_quic_experiments.py`

<img width="1063" height="950" alt="image" src="/screenshots/run_quic_experiments.png" />

`python3 run_quic_experiments.py`

<img width="1063" height="950" alt="image" src="/screenshots/run_quic_experiments_output.png" />

<img width="1063" height="950" alt="image" src="/screenshots/run_quic_experiments_output2.png" />

`cat quic_results.json | python3 -m json.tool | head -50`

## TCP re-run at 10 trials per loss rate.

`nano run_tcp_experiments.py`

<img width="1063" height="950" alt="image" src="/screenshots/run_tcp_experiments.png" />

- We stop the QUIC server (quic_server.py) and start the iperf3 server running in Terminal 1 first.

`iperf3 -s`

<img width="1063" height="950" alt="image" src="/screenshots/TCP_re-run_iperf3 -s.png" />

- Terminal 2

`python3 run_tcp_experiments.py`

<img width="1063" height="950" alt="image" src="/screenshots/run_tcp_experiments.png" />

`cat tcp_results.json | python3 -m json.tool`

## Side-by-side charts, FCT, and goodput.

`nano plot_comparison.py`

<img width="1063" height="950" alt="image" src="/screenshots/plot_comparison.png" />

`python3 plot_comparison.py`

<img width="1063" height="950" alt="image" src="/screenshots/plot_comparison2.png" />

- Transfering chart to my project root folder.

`cp ~/tcp-vs-quic/comparison_charts.png /mnt/c/Users/ADMIN/Desktop/`

<img width="1063" height="950" alt="image" src="/screenshots/comparison_charts.png" />

## CDF and 95% Confidence Intervals

`nano plot_cdf_ci.py`

<img width="1063" height="950" alt="image" src="/screenshots/nano_plot_cdf_ci.png" />

`python3 plot_cdf_ci.py`

<img width="1063" height="950" alt="image" src="/screenshots/plot_cdf_ci.png" />

- Copy output to project root.

`cp ~/tcp-vs-quic/cdf_charts.png /mnt/c/Users/ADMIN/Desktop/`

<img width="1063" height="950" alt="image" src="/screenshots/cdf_charts.png" />

`cp ~/tcp-vs-quic/ci95_charts.png /mnt/c/Users/ADMIN/Desktop/`

<img width="1063" height="950" alt="image" src="/screenshots/ci95_charts.png" />

## Transfering json outputs to project root. 

<img width="1063" height="950" alt="image" src="/screenshots/json_files.png" />

`cp ~/tcp-vs-quic/quic_results.json /mnt/c/Users/ADMIN/Desktop/`

[quic_results.json](/milestones/two/quic_results.json)

`cp ~/tcp-vs-quic/tcp_results.json /mnt/c/Users/ADMIN/Desktop/`

[tcp_results.json](/milestones/two/tcp_results.json)

## Milestone 2 Code state

[Zipped_code_milestone_2](/milestones/two/TCP-vs-QUIC-Under-Wireless-Like-Random-Packet-Loss.zip)