import asyncio
import subprocess
import json
import time
import os

# We run quic_server.py first in Terminal 1:
#   python3 quic_server.py
# Then run this here in terminal 2
#
# quic_client.py explicitly sets:
#   config.congestion_control_algorithm = "reno"
# This matches TCP Reno on the loopback setup,
# ensuring we compare transport behavior only —
# not congestion control algorithm differences.

LOSS_RATES = [0, 1, 3, 5, 10]
TRIALS = 10

async def run_trial():
    """
    Launch quic_client.py as a subprocess.
    Captures its JSON stdout output and returns
    the parsed result dict, or None on failure.
    """
    proc = await asyncio.create_subprocess_exec(
        "python3", "quic_client.py",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    try:
        return json.loads(stdout.decode().strip())
    except:
        return None

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

async def main():
    all_results = {}

    for loss in LOSS_RATES:
        set_loss(loss)
        time.sleep(1)  

        results = []

        for trial in range(1, TRIALS + 1):
            print(f"  Loss {loss}% — Trial {trial}/{TRIALS}...")

            result = await run_trial()

            if result:
                results.append(result)
                print(f"    FCT: {result['fct_ms']}ms  Goodput: {result['goodput_mbps']} Mbps")
            else:
                print(f"    Trial failed — skipping")

            await asyncio.sleep(2)  

        all_results[str(loss)] = results

    clear_loss()

    with open("quic_results.json", "w") as f:
        json.dump(all_results, f, indent=2)

    print("\nDone. Results saved to quic_results.json")
    print("Verify with: cat quic_results.json | python3 -m json.tool | head -30")

asyncio.run(main())