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
    """Calculate mean and 95% confidence interval half-width."""
    n = len(data)
    mean = np.mean(data)
    se = stats.sem(data)
    interval = stats.t.interval(0.95, df=n-1, loc=mean, scale=se)
    return mean, mean - interval[0]

# Figure 1: CDF of Goodput — TCP and QUIC
# Both subplots now use LOG scale for consistency
# since TCP spans 70-700 Mbps and QUIC spans 1.5-2.7 Mbps

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# TCP Goodput CDF — log scale
for i, loss in enumerate(loss_rates):
    tcp_vals = sorted([t["goodput_mbps"] for t in tcp_data[str(loss)]])
    cdf = np.arange(1, len(tcp_vals) + 1) / len(tcp_vals)
    axes[0].plot(tcp_vals, cdf, marker="o", label=f"{loss}% loss", color=colors[i])

axes[0].set_xlabel("Goodput (Mbps)")
axes[0].set_ylabel("CDF")
axes[0].set_title("CDF of TCP Goodput by Loss Rate\n(10 MB file transfer, log scale)")
axes[0].legend(title="Loss Rate")
axes[0].grid(True, linestyle="--", alpha=0.5)
axes[0].set_xscale("log")

# QUIC Goodput CDF — log scale
for i, loss in enumerate(loss_rates):
    quic_vals = sorted([t["goodput_mbps"] for t in quic_data[str(loss)]])
    cdf = np.arange(1, len(quic_vals) + 1) / len(quic_vals)
    axes[1].plot(quic_vals, cdf, marker="s", label=f"{loss}% loss", color=colors[i])

axes[1].set_xlabel("Goodput (Mbps)")
axes[1].set_ylabel("CDF")
axes[1].set_title("CDF of QUIC Goodput by Loss Rate\n(10 MB file transfer, log scale)")
axes[1].legend(title="Loss Rate")
axes[1].grid(True, linestyle="--", alpha=0.5)
axes[1].set_xscale("log")

plt.tight_layout()
plt.savefig("cdf_charts.png", dpi=150)
print("CDF charts saved to cdf_charts.png")

# Figure 2: 95% Confidence Interval Bar Chart — Goodput
tcp_means,  tcp_ci  = zip(*[ci95([t["goodput_mbps"] for t in tcp_data[str(l)]])  for l in loss_rates])
quic_means, quic_ci = zip(*[ci95([t["goodput_mbps"] for t in quic_data[str(l)]]) for l in loss_rates])

fig2, ax = plt.subplots(figsize=(10, 5))
x = np.arange(len(loss_rates))
w = 0.35
ax.bar(x - w/2, tcp_means,  w, yerr=tcp_ci,  label="TCP",  color="steelblue", capsize=5)
ax.bar(x + w/2, quic_means, w, yerr=quic_ci, label="QUIC", color="tomato",    capsize=5)
ax.set_xticks(x)
ax.set_xticklabels([f"{l}%" for l in loss_rates])
ax.set_xlabel("Packet Loss Rate (%)")
ax.set_ylabel("Goodput (Mbps)")
ax.set_title("TCP vs QUIC Goodput with 95% Confidence Intervals\n(log scale — different implementations)")
ax.legend()
ax.set_yscale("log")
ax.grid(True, axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("ci95_charts.png", dpi=150)
print("95% CI charts saved to ci95_charts.png")

# Figure 3: CDF of FCT — TCP vs QUIC
# Both protocols now have FCT data — direct comparison possible
# Linear scale used since FCT values are in same order of magnitude
# TCP: 115ms - 1220ms  |  QUIC: 30000ms - 51000ms

fig3, axes3 = plt.subplots(1, 2, figsize=(14, 5))

# TCP FCT CDF
for i, loss in enumerate(loss_rates):
    tcp_fct_vals = sorted([t["fct_ms"] for t in tcp_data[str(loss)]])
    cdf = np.arange(1, len(tcp_fct_vals) + 1) / len(tcp_fct_vals)
    axes3[0].plot(tcp_fct_vals, cdf, marker="o", label=f"{loss}% loss", color=colors[i])

axes3[0].set_xlabel("Flow Completion Time (ms)")
axes3[0].set_ylabel("CDF")
axes3[0].set_title("CDF of TCP Flow Completion Time by Loss Rate\n(10 MB file transfer)")
axes3[0].legend(title="Loss Rate")
axes3[0].grid(True, linestyle="--", alpha=0.5)

# QUIC FCT CDF
for i, loss in enumerate(loss_rates):
    quic_fct_vals = sorted([t["fct_ms"] for t in quic_data[str(loss)]])
    cdf = np.arange(1, len(quic_fct_vals) + 1) / len(quic_fct_vals)
    axes3[1].plot(quic_fct_vals, cdf, marker="s", label=f"{loss}% loss", color=colors[i])

axes3[1].set_xlabel("Flow Completion Time (ms)")
axes3[1].set_ylabel("CDF")
axes3[1].set_title("CDF of QUIC Flow Completion Time by Loss Rate\n(10 MB file transfer)")
axes3[1].legend(title="Loss Rate")
axes3[1].grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("fct_cdf.png", dpi=150)
print("FCT CDF charts saved to fct_cdf.png")