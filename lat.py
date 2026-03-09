import csv

latencies = []

try:
    with open("latest.csv", newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Make sure the column exists
            if "latency_ms" in row and row["latency_ms"]:
                latencies.append(float(row["latency_ms"]))
except FileNotFoundError:
    print("File latest.csv not found")
    exit()

if not latencies:
    print("No latency data found in CSV. Please check the file and column name.")
    exit()

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
