import os
from datetime import datetime

pending = {}
rows = []

for filename in os.listdir("."):
    if not filename.endswith(".log"):
        continue

    with open(filename) as f:
        for line in f:

            if ":blah-req" not in line and ":blah-res" not in line:
                continue

            if "id=" not in line:
                continue

            try:
                ts_str = line.split()[0]
                ts = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%S,%f")

                id_ = line.split("id=")[1].split("}")[0]

                if ":blah-req" in line:
                    pending.setdefault(id_, []).append(ts)

                elif ":blah-res" in line:
                    if id_ in pending and pending[id_] :
                        req_time = pending[id_].pop(0)
                        latency = (ts - req_time).total_seconds() * 1000
                        rows.append((id_, req_time, ts, latency))

            except Exception:
                # skip malformed lines
                continue


print("ID,REQ_TIME,RES_TIME,LATENCY_MS")
for r in rows:
    print(f"{r[0]},{r[1]},{r[2]},{r[3]:.3f}")
