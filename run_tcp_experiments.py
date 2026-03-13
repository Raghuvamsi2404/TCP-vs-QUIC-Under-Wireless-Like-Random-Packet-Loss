import subprocess
import json
import time

LOSS_RATES = [0, 1, 3, 5, 10]
TRIALS = 10

def set_loss(loss):
    subprocess.run("sudo tc qdisc del dev lo root 2>/dev/null || true", shell=True)
    if loss > 0:
        subprocess.run(f"sudo tc qdisc add dev lo root netem loss {loss}%", shell=True)
    print(f"Loss set to {loss}%")

def clear_loss():
    subprocess.run("sudo tc qdisc del dev lo root 2>/dev/null || true", shell=True)

def run_iperf_trial():
    try:
        result = subprocess.run(
            ["iperf3", "-c", "127.0.0.1", "-t", "10", "-J"],
            capture_output=True, text=True,
            timeout=30
        )
        data = json.loads(result.stdout)
        bits_per_second = data["end"]["sum_received"]["bits_per_second"]
        mbps = round(bits_per_second / 1e6, 2)
        return {"goodput_mbps": mbps}
    except:
        return None

all_results = {}
for loss in LOSS_RATES:
    set_loss(loss)
    time.sleep(1)
    results = []
    for trial in range(1, TRIALS + 1):
        print(f"  Loss {loss}% — Trial {trial}/{TRIALS}...")
        result = run_iperf_trial()
        if result:
            results.append(result)
            print(f"    Goodput: {result['goodput_mbps']} Mbps")
        else:
            print(f"    Trial failed or timed out — skipping")
        time.sleep(1)
    all_results[str(loss)] = results

clear_loss()
with open("tcp_results.json", "w") as f:
    json.dump(all_results, f, indent=2)
print("\nDone and results saved to tcp_results.json")