import socket
import time
import json
import subprocess

HOST = "127.0.0.1"
PORT = 5201
LOSS_RATES = [0, 1, 3, 5, 10]
TRIALS = 10

def set_loss(loss):
    """Apply tc netem packet loss on loopback interface."""
    subprocess.run("sudo tc qdisc del dev lo root 2>/dev/null || true", shell=True)
    if loss > 0:
        subprocess.run(f"sudo tc qdisc add dev lo root netem loss {loss}%", shell=True)
    print(f"Loss set to {loss}%")

def clear_loss():
    """Remove all tc netem rules after experiments are done."""
    subprocess.run("sudo tc qdisc del dev lo root 2>/dev/null || true", shell=True)
    print("tc netem rules cleared.")

def run_tcp_trial():
    """
    Connect to tcp_server.py, receive the full file,
    and return fct_ms, size_mb, and goodput_mbps.
    Returns None if the trial fails.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.settimeout(60)

        start = time.time()

        sock.connect((HOST, PORT))

        received = b""

        while True:
            chunk = sock.recv(65536)  # 64KB chunks
            if not chunk:
                break
            received += chunk

        fct_ms = (time.time() - start) * 1000
        size_mb = len(received) / (1024 * 1024)
        goodput_mbps = (size_mb * 8) / (fct_ms / 1000)

        sock.close()

        return {
            "fct_ms": round(fct_ms, 2),
            "size_mb": round(size_mb, 3),
            "goodput_mbps": round(goodput_mbps, 2)
        }

    except Exception as e:
        print(f"    Trial error: {e}")
        return None

all_results = {}

for loss in LOSS_RATES:
    set_loss(loss)
    time.sleep(1)  

    results = []

    for trial in range(1, TRIALS + 1):
        print(f"  Loss {loss}% — Trial {trial}/{TRIALS}...")

        result = run_tcp_trial()

        if result:
            results.append(result)
            print(f"    FCT: {result['fct_ms']} ms  Goodput: {result['goodput_mbps']} Mbps")
        else:
            print(f"    Trial failed — skipping")

        time.sleep(1)  

    all_results[str(loss)] = results

clear_loss()

with open("tcp_results.json", "w") as f:
    json.dump(all_results, f, indent=2)

print("\nDone. Results saved to tcp_results.json")
print("Verify with: cat tcp_results.json | python3 -m json.tool | head -30")