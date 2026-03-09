import csv

latencies = []

with open("latest.csv", newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        latencies.append(float(row["latency_ms"]))

# Create bins for histogram
bin_size = 10  # ms per bin
max_latency = int(max(latencies)) + bin_size
bins = [0] * ((max_latency // bin_size) + 1)

for l in latencies:
    index = int(l // bin_size)
    bins[index] += 1

# Print histogram
print(f"Latency Histogram (bin size = {bin_size} ms)")
for i, count in enumerate(bins):
    bar = '*' * min(count, 50)  # scale bar to max 50 stars
    print(f"{i*bin_size:4}-{(i+1)*bin_size-1:4} ms | {bar} ({count})")
