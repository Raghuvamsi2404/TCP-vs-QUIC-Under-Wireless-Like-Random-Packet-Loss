import json
import matplotlib.pyplot as plt
import numpy as np

loss_rates = [0, 1, 3, 5, 10]
result_files = ['result_0.json', 'result_1.json', 
                'result_3.json', 'result_5.json', 
                'result_10.json']

throughputs = []

for f in result_files:
    with open(f) as file:
        data = json.load(file)
        bps = data['end']['sum_received']['bits_per_second']
        mbps = bps / 1_000_000
        throughputs.append(round(mbps, 2))
        print(f"{f}: {round(mbps, 2)} Mbps")

fig, ax = plt.subplots(figsize=(8, 5))

bars = ax.bar(
    [str(x) + '%' for x in loss_rates],
    throughputs,
    color=['green', 'yellowgreen', 'orange', 'tomato', 'red'],
    edgecolor='black',
    width=0.5
)

for bar, val in zip(bars, throughputs):
    ax.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height() + 0.5,
        f'{val} Mbps',
        ha='center',
        va='bottom',
        fontsize=10
    )

ax.set_xlabel('Packet Loss Rate (%)', fontsize=12)
ax.set_ylabel('Throughput (Mbps)', fontsize=12)
ax.set_title('TCP Throughput vs Packet Loss Rate\n(Early Baseline Results)', fontsize=13)
ax.set_ylim(0, max(throughputs) * 1.2)

plt.tight_layout()
plt.savefig('early_results.png', dpi=150)
plt.show()
print("Plot saved as early_results.png")