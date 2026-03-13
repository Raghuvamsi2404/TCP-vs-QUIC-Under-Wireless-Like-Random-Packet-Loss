import json
import numpy as np
import matplotlib.pyplot as plt

with open("tcp_results.json") as f:
    tcp_data = json.load(f)
with open("quic_results.json") as f:
    quic_data = json.load(f)

loss_rates = [0, 1, 3, 5, 10]

tcp_means = [np.mean([t["goodput_mbps"] for t in tcp_data[str(l)]]) for l in loss_rates]
tcp_stds  = [np.std([t["goodput_mbps"]  for t in tcp_data[str(l)]]) for l in loss_rates]
quic_means = [np.mean([t["goodput_mbps"] for t in quic_data[str(l)]]) for l in loss_rates]
quic_stds  = [np.std([t["goodput_mbps"]  for t in quic_data[str(l)]]) for l in loss_rates]

# Normalized (% of baseline)
tcp_norm  = [m/tcp_means[0]*100  for m in tcp_means]
quic_norm = [m/quic_means[0]*100 for m in quic_means]

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Absolute Goodput
x = np.arange(len(loss_rates))
w = 0.35
axes[0].bar(x-w/2, tcp_means, w, yerr=tcp_stds, label="TCP", color="steelblue", capsize=4)
axes[0].bar(x+w/2, quic_means, w, yerr=quic_stds, label="QUIC", color="tomato", capsize=4)
axes[0].set_xticks(x)
axes[0].set_xticklabels([f"{l}%" for l in loss_rates])
axes[0].set_xlabel("Packet Loss Rate")
axes[0].set_ylabel("Goodput (Mbps)")
axes[0].set_title("Absolute Goodput: TCP vs QUIC")
axes[0].legend()
axes[0].set_yscale("log")

# Normalized Goodput
axes[1].plot(loss_rates, tcp_norm,  "o-", color="steelblue", label="TCP",  linewidth=2)
axes[1].plot(loss_rates, quic_norm, "s-", color="tomato",    label="QUIC", linewidth=2)
axes[1].set_xlabel("Packet Loss Rate (%)")
axes[1].set_ylabel("Goodput (% of baseline)")
axes[1].set_title("Normalized Goodput Degradation")
axes[1].legend()
axes[1].grid(True)

# QUIC FCT
quic_fcts = [np.mean([t["fct_ms"] for t in quic_data[str(l)]]) for l in loss_rates]
quic_fct_stds = [np.std([t["fct_ms"] for t in quic_data[str(l)]]) for l in loss_rates]
axes[2].bar([f"{l}%" for l in loss_rates], quic_fcts, yerr=quic_fct_stds,
            color="tomato", capsize=4)
axes[2].set_xlabel("Packet Loss Rate")
axes[2].set_ylabel("Flow Completion Time (ms)")
axes[2].set_title("QUIC Flow Completion Time vs Loss")

plt.tight_layout()
plt.savefig("comparison_charts.png", dpi=150)
print("Charts saved to comparison_charts.png")