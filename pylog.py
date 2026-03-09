import os
import re
from datetime import datetime
import csv

pattern = re.compile(
    r'(?P<ts>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2},\d+).*:blah-(?P<type>req|res).*id=(?P<id>\d+)'
)

pending = {}
rows = []

def parse_ts(ts):
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S,%f")

for filename in os.listdir("."):
    if not filename.endswith(".log"):
        continue

    with open(filename) as f:
        for line in f:
            m = pattern.search(line)
            if not m:
                continue

            ts = parse_ts(m.group("ts"))
            msg_type = m.group("type")
            id_ = m.group("id")

            if msg_type == "req":
                pending.setdefault(id_, []).append(ts)

            elif msg_type == "res":
                if id_ in pending and pending[id_]:
                    req_time = pending[id_].pop(0)
                    latency_ms = (ts - req_time).total_seconds() * 1000

                    rows.append((id_, req_time, ts, latency_ms))

# Print simple table
print(f"{'ID':>12} {'REQ TIME':>26} {'RES TIME':>26} {'LATENCY(ms)':>12}")
for r in rows:
    print(f"{r[0]:>12} {str(r[1]):>26} {str(r[2]):>26} {r[3]:>12.3f}")

# Save CSV
with open("latency_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "req_time", "res_time", "latency_ms"])
    writer.writerows(rows)

print("\nSaved results to latency_results.csv")
