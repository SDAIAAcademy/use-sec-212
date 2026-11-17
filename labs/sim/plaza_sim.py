# /// script
# requires-python = ">=3.11"
# dependencies = ["jupedsim==1.4.2", "shapely>=2"]
# ///
"""Al-Mashra' plaza model (Al-Rifada, a fictional host city), simulated with JuPedSim.

    uv run plaza_sim.py --plan A --scenario base --seed 1      # one run, prints peak densities
    uv run plaza_sim.py --all --out results                     # every plan, scenario and seed

The plaza is 50 m wide and 30 m deep. Visitors arrive from the train station at the south edge
in waves (one train every 150 seconds, each wave spread over 45 seconds) and walk to the
nearest open gate in the north wall. Density is counted in a measurement area of 8 m by 5 m in
front of each gate, every simulated second, and averaged over 10 seconds, as the safety plan
of the case defines it. Fixed seeds: the same inputs give the same arrivals on every run.
"""
# --- model ---
import random

import jupedsim as jps
import shapely

PLAZA_W, PLAZA_D, DT = 50.0, 30.0, 0.05
LIMIT = 2.0  # persons per square metre: a teaching value from the fictional safety plan of the case
PLANS = {
    "A": [(21.0, 3.0), (29.0, 3.0)],                # two central gates, 3 m each
    "B": [(10.0, 2.0), (25.0, 2.0), (40.0, 2.0)],   # three spread gates, 2 m each
}
CLOSED = {"A": 29.0, "B": 25.0}  # the gate that is closed in the stress test
SCENARIOS = {
    "base": (450, False),           # 450 visitors per train wave, every gate open
    "plus25": (563, False),         # 25 % more visitors (the peak forecast error)
    "gate_closed": (450, True),     # one gate closed
    "both": (563, True),            # both at once
}
WAVES, GAP, WAVE_LEN = 4, 150.0, 45.0


def gates_for(plan, scenario):
    per_wave, closed = SCENARIOS[scenario]
    gates = [g for g in PLANS[plan] if not (closed and g[0] == CLOSED[plan])]
    return gates, per_wave


def run(plan, scenario="base", seed=1, area=(8.0, 5.0), window=10):
    """One simulation. Returns a dict with the density series and the peaks per gate."""
    gates, per_wave = gates_for(plan, scenario)
    plaza = shapely.box(0, 0, PLAZA_W, PLAZA_D)
    corridors = [shapely.box(x - w / 2, PLAZA_D - 0.01, x + w / 2, PLAZA_D + 4) for x, w in gates]
    sim = jps.Simulation(model=jps.CollisionFreeSpeedModel(),
                         geometry=shapely.union_all([plaza] + corridors), dt=DT)
    targets = []
    for x, w in gates:
        exit_id = sim.add_exit_stage(shapely.box(x - w / 2, PLAZA_D + 3, x + w / 2, PLAZA_D + 4))
        targets.append((sim.add_journey(jps.JourneyDescription([exit_id])), exit_id))
    aw, ad = area
    boxes = [(x - aw / 2, x + aw / 2, PLAZA_D - ad, PLAZA_D) for x, _ in gates]
    rng = random.Random(seed)
    arrivals = sorted(k * GAP + rng.random() * WAVE_LEN for k in range(WAVES) for _ in range(per_wave))
    xs = [rng.uniform(1, PLAZA_W - 1) for _ in arrivals]
    nxt, step, series = 0, 0, []
    while True:
        t = step * DT
        while nxt < len(arrivals) and arrivals[nxt] <= t:
            x = xs[nxt]
            g = min(range(len(gates)), key=lambda i: abs(gates[i][0] - x))
            try:
                sim.add_agent(jps.CollisionFreeSpeedModelAgentParameters(
                    journey_id=targets[g][0], stage_id=targets[g][1],
                    position=(x, rng.uniform(0.4, 2.0)), radius=0.2, desired_speed=1.2))
            except Exception:
                xs[nxt] = rng.uniform(1, PLAZA_W - 1)  # the spot is taken: try another next step
                break
            nxt += 1
        sim.iterate()
        step += 1
        if step % int(round(1 / DT)) == 0:
            pts = [a.position for a in sim.agents()]
            series.append([sum(1 for (px, py) in pts if x0 <= px <= x1 and y0 <= py <= y1) / (aw * ad)
                           for x0, x1, y0, y1 in boxes])
        if nxt >= len(arrivals) and sim.agent_count() == 0:
            break
    smooth = []
    for i in range(len(series)):
        part = series[max(0, i - window + 1):i + 1]
        smooth.append([sum(r[g] for r in part) / len(part) for g in range(len(gates))])
    peaks = [round(max(r[g] for r in smooth), 2) for g in range(len(gates))]
    above = [sum(1 for r in smooth if r[g] > LIMIT) for g in range(len(gates))]
    return {"plan": plan, "scenario": scenario, "seed": seed, "gates": [x for x, _ in gates],
            "visitors": per_wave * WAVES, "seconds": len(series), "smooth": smooth,
            "peaks": peaks, "above": above}
# --- end model ---


def main():
    import argparse
    import csv
    from pathlib import Path
    p = argparse.ArgumentParser()
    p.add_argument("--plan", default="A", choices=sorted(PLANS))
    p.add_argument("--scenario", default="base", choices=list(SCENARIOS))
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--all", action="store_true")
    p.add_argument("--out", default="results")
    a = p.parse_args()
    if not a.all:
        r = run(a.plan, a.scenario, a.seed)
        for x, pk, ab in zip(r["gates"], r["peaks"], r["above"]):
            print(f"gate at x={x:g} m: peak {pk:.2f} persons/m2, {ab} s above {LIMIT}")
        print(f"cleared after {r['seconds']} s")
        return
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for scenario in SCENARIOS:
        for plan in PLANS:
            for seed in (1, 2, 3):
                r = run(plan, scenario, seed)
                for i, (x, pk, ab) in enumerate(zip(r["gates"], r["peaks"], r["above"])):
                    rows.append([plan, scenario, seed, f"G{i + 1}", x, r["visitors"], pk, ab, r["seconds"]])
                print(plan, scenario, seed, r["peaks"], r["above"], r["seconds"], flush=True)
                if scenario == "base" and seed == 1:
                    with open(out / f"series_{plan}_base_seed1.csv", "w", newline="", encoding="utf-8") as f:
                        w = csv.writer(f)
                        w.writerow(["second"] + [f"G{i + 1}" for i in range(len(r["gates"]))])
                        for s, row in enumerate(r["smooth"], 1):
                            w.writerow([s] + [f"{v:.3f}" for v in row])
    with open(out / "runs.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["plan", "scenario", "seed", "gate", "gate_x_m", "visitors", "peak_density", "seconds_above_limit", "seconds_to_clear"])
        w.writerows(rows)


if __name__ == "__main__":
    main()
