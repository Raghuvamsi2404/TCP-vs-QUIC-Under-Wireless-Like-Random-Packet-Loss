import json
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

with open("tcp_results.json") as f:
    tcp_data = json.load(f)
with open("quic_results.json") as f:
    quic_data = json.load(f)

loss_rates = [0, 1, 3, 5, 10]
colors = ["steelblue", "tomato", "green", "purple", "orange"]

def ci95(data):
    n = len(data)
    mean = np.mean(data)
    se = stats.sem(data)
    interval = stats.t.interval(0.95, df=n-1, loc=mean, scale=se)
    return mean, mean - interval[0]

# CDF of TCP Goodput per loss rate
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

for i, loss in enumerate(loss_rates):
    tcp_vals = sorted([t["goodput_mbps"] for t in tcp_data[str(loss)]])
    cdf = np.arange(1, len(tcp_vals)+1) / len(tcp_vals)
    axes[0].plot(tcp_vals, cdf, marker="o", label=f"{loss}% loss", color=colors[i])

axes[0].set_xlabel("Goodput (Mbps)")
axes[0].set_ylabel("CDF")
axes[0].set_title("CDF of TCP Goodput by Loss Rate")
axes[0].legend()
axes[0].grid(True)
axes[0].set_xscale("log")

for i, loss in enumerate(loss_rates):
    quic_vals = sorted([t["goodput_mbps"] for t in quic_data[str(loss)]])
    cdf = np.arange(1, len(quic_vals)+1) / len(quic_vals)
    axes[1].plot(quic_vals, cdf, marker="s", label=f"{loss}% loss", color=colors[i])

axes[1].set_xlabel("Goodput (Mbps)")
axes[1].set_ylabel("CDF")
axes[1].set_title("CDF of QUIC Goodput by Loss Rate")
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.savefig("cdf_charts.png", dpi=150)
print("CDF charts saved to cdf_charts.png")

# 95% CI bar chart
tcp_means, tcp_ci = zip(*[ci95([t["goodput_mbps"] for t in tcp_data[str(l)]]) for l in loss_rates])
quic_means, quic_ci = zip(*[ci95([t["goodput_mbps"] for t in quic_data[str(l)]]) for l in loss_rates])

fig2, ax = plt.subplots(figsize=(10, 5))
x = np.arange(len(loss_rates))
w = 0.35
ax.bar(x-w/2, tcp_means, w, yerr=tcp_ci, label="TCP", color="steelblue", capsize=5)
ax.bar(x+w/2, quic_means, w, yerr=quic_ci, label="QUIC", color="tomato", capsize=5)
ax.set_xticks(x)
ax.set_xticklabels([f"{l}%" for l in loss_rates])
ax.set_xlabel("Packet Loss Rate")
ax.set_ylabel("Goodput (Mbps)")
ax.set_title("TCP vs QUIC Goodput with 95% Confidence Intervals")
ax.legend()
ax.set_yscale("log")
ax.grid(True, axis="y")

plt.tight_layout()
plt.savefig("ci95_charts.png", dpi=150)
print("95% CI charts saved to ci95_charts.png")