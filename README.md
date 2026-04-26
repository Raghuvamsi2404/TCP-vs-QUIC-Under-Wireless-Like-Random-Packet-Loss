# TCP vs QUIC Under Wireless-Like Random Packet Loss
**EE6750 - Transport over Wireless Networks**

**Team:** Raghuvamsi Lekkala (Implementation, experiments, data collection) | Krishna Sri Mannam (Experiment design, analysis, report writing)

## Research Question

How does QUIC compare to TCP in throughput and flow completion time when transferring a 10 MB file under random wireless-like packet loss rates of 0%, 1%, 3%, 5%, and 10%?


## Repository Structure

```
TCP-vs-QUIC-Under-Wireless-Like-Random-Packet-Loss/
├── tcp_server.py                  # TCP file transfer server (Python sockets)
├── run_tcp_experiments.py         # Runs 10 TCP trials per loss rate → tcp_results.json
├── quic_server.py                 # QUIC file transfer server (aioquic)
├── quic_client.py                 # QUIC file transfer client (aioquic, CC = Reno)
├── run_quic_experiments.py        # Runs 10 QUIC trials per loss rate → quic_results.json
├── plot_comparison.py             # 4-panel comparison chart → comparison_charts.png
├── plot_cdf_ci.py                 # CDF + CI charts + FCT CDF → 3 PNG files
├── requirements.txt               # Python dependencies
└── results/
    ├── testfile.bin               # 10.124 MB test file used for all transfers
    ├── quic_results.json          # QUIC experiment results (50 trials)
    └── tcp_results.json           # TCP experiment results (50 trials)
```

## Congestion Control - Design Decision

Both protocols are configured to use **Reno** congestion control:

- **TCP:** Linux kernel default on WSL2 loopback is Reno
- **QUIC:** `config.congestion_control_algorithm = "reno"` set explicitly in `quic_client.py`

This ensures the comparison isolates **transport protocol behavior** (how TCP and QUIC respond to loss), not congestion control algorithm differences. Without this, we would be comparing TCP Reno against QUIC's unspecified default.

## TCP Methodology - Why We Use Python Sockets

In Milestone 1 TCP experiment was used `iperf3 -t 10` (a 10-second throughput flood). This did not match our research question, which asks about transferring a specific 10 MB file.

In Milestone 2, TCP was rewritten to use Python sockets (`tcp_server.py` + `run_tcp_experiments.py`):
- Server loads `testfile.bin` (10.124 MB) and sends it on each connection
- Client connects, receives all bytes, records FCT and goodput
- This mirrors exactly how `quic_server.py` and `quic_client.py` work
- Both protocols now produce identical output: `fct_ms`, `size_mb`, `goodput_mbps`

## Setup Instructions

### 1. Install WSL2 (Windows only)
```bash
wsl --install
```

### 2. Install system dependencies
```bash
sudo apt update
sudo apt install iproute2 python3 python3-pip python3-venv -y
```

### 3. Create working directory and virtual environment
```bash
mkdir tcp-vs-quic
cd tcp-vs-quic
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 5. Generate TLS certificates for QUIC
```bash
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem \
  -days 365 -nodes -subj "/CN=localhost"
```

### 6. Prepare test file
Place a ~10 MB file as `testfile.bin` in the working directory:
```bash
cp /mnt/c/Users/user/Desktop/tcp2/file.pdf ~/tcp-vs-quic/testfile.bin
ls -lh ~/tcp-vs-quic/testfile.bin
```

## Running the Experiments

### TCP Experiments

**Terminal 1 - Start TCP server:**
```bash
cd ~/tcp-vs-quic && source venv/bin/activate
python3 tcp_server.py
```
Expected: `TCP server listening on port 5201...`

**Terminal 2 - Run all 50 TCP trials:**
```bash
cd ~/tcp-vs-quic && source venv/bin/activate
sudo tc qdisc del dev lo root 2>/dev/null || true
python3 run_tcp_experiments.py
```
Results saved to `tcp_results.json` automatically.

### QUIC Experiments

**Terminal 1 - Start QUIC server:**
```bash
cd ~/tcp-vs-quic && source venv/bin/activate
python3 quic_server.py
```
Expected: `QUIC server running on port 4433...`

**Terminal 2 - Run all 50 QUIC trials:**
```bash
cd ~/tcp-vs-quic && source venv/bin/activate
python3 run_quic_experiments.py
```
Results saved to `quic_results.json` automatically.

### Verify Both JSON Files Match Structure
```bash
python3 -c "
import json
tcp = json.load(open('tcp_results.json'))
quic = json.load(open('quic_results.json'))
for loss in ['0','1','3','5','10']:
    print(f'Loss {loss}%')
    print(f'  TCP  keys: {list(tcp[loss][0].keys())}')
    print(f'  QUIC keys: {list(quic[loss][0].keys())}')
"
```
Expected: both show `['fct_ms', 'size_mb', 'goodput_mbps']` for all 5 loss rates.

## Generating Plots

```bash
python3 plot_comparison.py   # → comparison_charts.png (4 panels)
python3 plot_cdf_ci.py       # → cdf_charts.png, ci95_charts.png, fct_cdf.png
```

### Output Charts

| File | Description |
|------|-------------|
| `comparison_charts.png` | 4-panel: absolute goodput, normalized degradation, FCT comparison, normalized FCT |
| `cdf_charts.png` | CDF of goodput for TCP and QUIC across all loss rates |
| `ci95_charts.png` | Goodput with 95% confidence intervals for both protocols |
| `fct_cdf.png` | CDF of flow completion time for TCP and QUIC across all loss rates |

## Experiment Design Summary

| Parameter | Value |
|-----------|-------|
| Loss rates | 0%, 1%, 3%, 5%, 10% |
| Trials per loss rate | 10 |
| Total runs | 100 (50 TCP + 50 QUIC) |
| Transfer size | 10.124 MB |
| TCP implementation | Python sockets, kernel TCP, Reno CC |
| QUIC implementation | aioquic (userspace), Reno CC (explicit) |
| Loss injection | tc netem on loopback interface (lo) |
| Metrics | Goodput (Mbps), FCT (ms), CDF, 95% CI |

## Hypotheses

**H1 (Throughput):** QUIC will maintain higher normalized throughput than TCP as packet loss increases. This is supported by our data.

**H2 (FCT):** QUIC will complete the file transfer more consistently than TCP under loss. This also is supported by our data.

**H3 (Retransmissions):** TCP retransmission count will grow faster than QUIC's under increasing loss. — Not directly measured; inferred from FCT variance.

## Limitations

- **Loopback vs real wireless:** tc netem injects random loss on the loopback interface, not a real wireless channel. Real wireless has correlated loss, fading, and interference not modeled here.
- **Implementation asymmetry:** TCP uses the Linux kernel stack; QUIC uses Python/aioquic userspace. Absolute goodput numbers are not directly comparable — normalized comparisons are used instead.
- **No retransmission counter:** aioquic does not expose retransmission counts directly; H3 is inferred from FCT behavior.
- **Small sample size:** 10 trials per loss rate is sufficient for trends but limits statistical power.

## Milestones

### Milestone 1 - Project Checkpoint
- WSL2 + tc netem environment set up
- TCP baseline experiments (iperf3, time-based) across all 5 loss rates
- Early results chart generated
- GitHub repo initialized

### Milestone 2 - Full Data Collection and Analysis
- TCP rewritten to Python socket-based 10 MB file transfer (matches research question)
- Congestion control explicitly matched: both protocols use Reno
- QUIC experiments run: 50 trials across 5 loss rates
- TCP experiments re-run: 50 trials across 5 loss rates
- All results include FCT, size, and goodput
- 4 charts generated: comparison, CDF, CI, FCT CDF
- JSON structure verified to match between protocols

### Milestone 3 - Final Report and Presentation
- Full written report with introduction, methodology, results, analysis, conclusions
- All hypotheses confirmed or rejected with data evidence
- Limitations section included
- Final GitHub repo with all scripts, data, and charts
