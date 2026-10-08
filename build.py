#!/usr/bin/env python3
"""Builds schedule.json (+ index.html preview) for the live Body Fixing class schedule.
Reads classes.json, pulls live seats from the ThriveCart checkout, marks sold-out options full."""
import json, re, html, urllib.request, pathlib, datetime
HERE = pathlib.Path(__file__).resolve().parent
cfg = json.loads((HERE / "classes.json").read_text())
try:
    t = html.unescape(urllib.request.urlopen(urllib.request.Request(cfg["reserve_url"], headers={"User-Agent": "Mozilla/5.0"}), timeout=20).read().decode("utf-8", "ignore"))
    plans = []
    for p in re.findall(r'data-payment_plan="(\{.*?\})"', t):
        try: plans.append(json.loads(p))
        except Exception: pass
except Exception:
    plans = []
for c in cfg["classes"]:
    c.pop("seats_left", None)
    if not c.get("match"): continue
    for p in plans:
        if c["match"].lower() in (p.get("plan_name") or "").lower():
            if p.get("quantity") == "limited":
                r = int(p.get("quantity_remaining") or 0)
                c["seats_left"] = r
                if r == 0: c["status"] = "full"
DAYS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
today = datetime.date.today()
for c in cfg["classes"]:
    first = datetime.date.fromisoformat(c.get("first_class", today.isoformat()))
    nxt = today + datetime.timedelta(days=(DAYS.index(c["day"]) - today.weekday()) % 7)
    nxt = max(nxt, first)
    c["next_class"] = nxt.strftime("%a, %b ") + str(nxt.day)
out = {k: cfg[k] for k in ("reserve_url", "phone", "email")}
out["classes"] = cfg["classes"]
(HERE / "schedule.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out["classes"], indent=1))
