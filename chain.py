import hashlib, json, os, time
FILE = "chain.json"
def _h(o): return hashlib.sha256(json.dumps(o, sort_keys=True).encode()).hexdigest()
def load(): return json.load(open(FILE)) if os.path.exists(FILE) else []
def data_hash(df): return hashlib.sha256(df.to_csv(index=False).encode()).hexdigest()
def block_hash(b): return _h({k: v for k, v in b.items() if k != "hash"})

def add(city, lat, lon, start, end, df, difficulty=3):
    c = load()
    b = {"index": len(c), "time": time.time(), "city": city, "lat": lat, "lon": lon, "start": start, "end": end,
         "rows": len(df), "mean_temp": round(float(df.tmean.mean()), 3), "data_hash": data_hash(df),
         "prev": c[-1]["hash"] if c else "0" * 64, "nonce": 0}
    while not block_hash(b).startswith("0" * difficulty): b["nonce"] += 1   # proof of work
    b["hash"] = block_hash(b); c.append(b); json.dump(c, open(FILE, "w"), indent=1)
    return b

def verify(c):
    for i, b in enumerate(c):
        if block_hash(b) != b["hash"]: return False, i, "Block ka data badla gaya (hash mismatch)"
        if i and b["prev"] != c[i - 1]["hash"]: return False, i, "Chain link toota (prev hash mismatch)"
    return True, None, "Poori chain valid hai"
