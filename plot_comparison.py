import json
import numpy as np
import matplotlib.pyplot as plt

with open("tcp_results.json") as f:
    tcp_data = json.load(f)
with open("quic_results.json") as f:
    quic_data = json.load(f)

loss_rates = [0, 1, 3, 5, 10]

# Goodput stats
tcp_means  = [np.mean([t["goodput_mbps"] for t in tcp_data[str(l)]])  for l in loss_rates]
tcp_stds   = [np.std([t["goodput_mbps"]  for t in tcp_data[str(l)]])  for l in loss_rates]
quic_means = [np.mean([t["goodput_mbps"] for t in quic_data[str(l)]]) for l in loss_rates]
quic_stds  = [np.std([t["goodput_mbps"]  for t in quic_data[str(l)]]) for l in loss_rates]

# Normalized (% of each protocol's own baseline at 0% loss)
tcp_norm  = [m / tcp_means[0]  * 100 for m in tcp_means]
quic_norm = [m / quic_means[0] * 100 for m in quic_means]

# FCT stats
tcp_fct_means  = [np.mean([t["fct_ms"] for t in tcp_data[str(l)]])  for l in loss_rates]
tcp_fct_stds   = [np.std([t["fct_ms"]  for t in tcp_data[str(l)]])  for l in loss_rates]
quic_fct_means = [np.mean([t["fct_ms"] for t in quic_data[str(l)]]) for l in loss_rates]
quic_fct_stds  = [np.std([t["fct_ms"]  for t in quic_data[str(l)]]) for l in loss_rates]

# 4-panel figure
fig, axes = plt.subplots(1, 4, figsize=(24, 5))

x = np.arange(len(loss_rates))
w = 0.35

# Panel 1: Absolute Goodput (log scale)
# TCP uses kernel sockets; QUIC uses Python/aioquic userspace.
# NOT directly comparable in absolute terms.
axes[0].bar(x - w/2, tcp_means,  w, yerr=tcp_stds,  label="TCP (kernel socket)",
            color="steelblue", capsize=4)
axes[0].bar(x + w/2, quic_means, w, yerr=quic_stds, label="QUIC (aioquic/userspace)",
            color="tomato", capsize=4)
axes[0].set_xticks(x)
axes[0].set_xticklabels([f"{l}%" for l in loss_rates])
axes[0].set_xlabel("Packet Loss Rate (%)")
axes[0].set_ylabel("Goodput (Mbps)")
axes[0].set_title("Absolute Goodput: TCP vs QUIC\n(log scale — different implementations)")
axes[0].legend(fontsize=8)
axes[0].set_yscale("log")
axes[0].grid(True, axis="y", linestyle="--", alpha=0.5)

# Panel 2: Normalized Goodput Degradation
# This is the PRIMARY comparison — each protocol as % of its own 0% baseline.
# Removes the implementation speed difference and shows resilience to loss.
axes[1].plot(loss_rates, tcp_norm,  "o-", color="steelblue", label="TCP",  linewidth=2)
axes[1].plot(loss_rates, quic_norm, "s-", color="tomato",    label="QUIC", linewidth=2)
axes[1].set_xlabel("Packet Loss Rate (%)")
axes[1].set_ylabel("Goodput (% of 0% loss baseline)")
axes[1].set_title("Normalized Goodput Degradation\n(Primary Comparison)")
axes[1].legend()
axes[1].grid(True)
axes[1].set_ylim(0, 110)

# Panel 3: FCT Comparison — TCP vs QUIC
# Now both protocols have FCT data — direct side-by-side comparison.
axes[2].bar(x - w/2, tcp_fct_means,  w, yerr=tcp_fct_stds,  label="TCP",
            color="steelblue", capsize=4)
axes[2].bar(x + w/2, quic_fct_means, w, yerr=quic_fct_stds, label="QUIC",
            color="tomato", capsize=4)
axes[2].set_xticks(x)
axes[2].set_xticklabels([f"{l}%" for l in loss_rates])
axes[2].set_xlabel("Packet Loss Rate (%)")
axes[2].set_ylabel("Flow Completion Time (ms)")
axes[2].set_title("Flow Completion Time: TCP vs QUIC\n(10 MB file transfer)")
axes[2].legend()
axes[2].grid(True, axis="y", linestyle="--", alpha=0.5)

# Panel 4: FCT Normalized Degradation
# Shows how much FCT grows relative to each protocol's own 0% baseline.
tcp_fct_norm  = [m / tcp_fct_means[0]  * 100 for m in tcp_fct_means]
quic_fct_norm = [m / quic_fct_means[0] * 100 for m in quic_fct_means]

axes[3].plot(loss_rates, tcp_fct_norm,  "o-", color="steelblue", label="TCP",  linewidth=2)
axes[3].plot(loss_rates, quic_fct_norm, "s-", color="tomato",    label="QUIC", linewidth=2)
axes[3].set_xlabel("Packet Loss Rate (%)")
axes[3].set_ylabel("FCT (% of 0% loss baseline)")
axes[3].set_title("Normalized FCT Degradation\n(lower is better)")
axes[3].legend()
axes[3].grid(True)
axes[3].set_ylim(0, max(max(tcp_fct_norm), max(quic_fct_norm)) * 1.1)

plt.tight_layout()
plt.savefig("comparison_charts.png", dpi=150)
print("Charts saved to comparison_charts.png")