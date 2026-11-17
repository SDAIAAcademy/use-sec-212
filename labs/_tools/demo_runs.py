# /// script
# requires-python = ">=3.11"
# dependencies = ["jupedsim==1.4.2", "shapely>=2"]
# ///
"""Parallel example for the slides of sessions 1.5 to 1.7: the exit hall of the events venue
(30 m by 20 m, one exit 2.5 m wide), not the lab's plaza. Prints the numbers the slides quote.

    uv run labs/_tools/demo_runs.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "sim"))
import plaza_sim as P  # noqa: E402

P.PLAZA_W, P.PLAZA_D, P.WAVES, P.GAP = 30.0, 20.0, 3, 120.0
P.PLANS["hall"] = [(15.0, 2.5)]
P.PLANS["hall2"] = [(8.0, 2.5), (22.0, 2.5)]
P.CLOSED.update({"hall": -1, "hall2": 22.0})
P.SCENARIOS.update({"usual": (300, False), "more": (375, False), "closed": (300, True)})

for seed in (1, 2, 3):
    r = P.run("hall", "usual", seed)
    print("hall usual seed", seed, "peak", r["peaks"], "above", r["above"], "clear", r["seconds"])
for area, window in (((8.0, 5.0), 10), ((4.0, 3.0), 10), ((8.0, 5.0), 1), ((12.0, 8.0), 10)):
    r = P.run("hall", "usual", 1, area=area, window=window)
    print("hall seed 1 area", area, "window", window, "peak", r["peaks"])
for sc in ("usual", "more", "closed"):
    r = P.run("hall2", sc, 1)
    print("hall2", sc, "peak", r["peaks"], "above", r["above"])
