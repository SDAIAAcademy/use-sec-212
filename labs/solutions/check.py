# /// script
# requires-python = ">=3.11"
# dependencies = ["openpyxl>=3.1"]
# ///
"""Reference solutions of the sixteen labs, recomputed from the files participants get.

    uv run labs/solutions/check.py              # every lab
    uv run labs/solutions/check.py 1.3 2.5      # some

Prints what it recomputed and PASS per lab. Writes nothing and calls no model: no step of the
labs needs one (the assistant of labs 2.1 to 2.3 is a set of recorded answers). The simulation
labs read labs/files/sim/results_*.csv; labs/sim/plaza_sim.py reproduces it.
"""
import csv
import json
import math
import sys
from pathlib import Path

from openpyxl import load_workbook

LABS = Path(__file__).resolve().parents[1]
F = LABS / "files"
KEY = json.loads((LABS / "solutions" / "key.json").read_text(encoding="utf-8"))
LIMIT = 2.0


def rows(path, sheet):
    ws = load_workbook(path, read_only=True, data_only=True)[sheet]
    data = list(ws.iter_rows(values_only=True))
    return data[0], data[1:]


def pct(x, d=1):
    return f"{100 * x:.{d}f}%"


def close(a, b, tol=1e-3):
    assert abs(a - b) <= tol, (a, b)


def lab11():
    text = (F / "deployments" / "six_deployments.txt").read_text(encoding="utf-8")
    _, sheet = rows(F / "deployments" / "ranking_sheet.xlsx", "الترتيب")
    ids = [r[0] for r in sheet]
    assert ids == ["D1", "D2", "D3", "D4", "D5", "D6"], ids
    assert all(i in text for i in ids)
    k = KEY["1.1"]
    assert set(k["order"][:3]) == set(k["top_set"]) and set(k["order"][-2:]) == set(k["bottom_set"])
    assert "بيانات حيوية" in text or "بصمة" in text  # D3 handles biometric data for identification
    print("  reference order:", " > ".join(k["order"]), "| top three:", ", ".join(k["top_set"]))


def arrivals():
    _, data = rows(F / "forecast" / "arrivals_seasons.xlsx", "الوافدون")
    actual = {(r[0], r[1]): r[2] for r in data}
    taw = {r[1]: r[3] for r in data if r[0] == 3}
    _, consts = rows(F / "forecast" / "arrivals_seasons.xlsx", "الثوابت")
    growth, per_staff = consts[0][1], consts[1][1]
    base = {d: actual[(2, d)] * (1 + growth) for d in range(1, 61)}
    a3 = {d: actual[(3, d)] for d in range(1, 61)}
    return a3, taw, base, per_staff


def lab12():
    a3, taw, base, _ = arrivals()
    mt = sum(abs(taw[d] - a3[d]) / a3[d] for d in a3) / 60
    mb = sum(abs(base[d] - a3[d]) / a3[d] for d in a3) / 60
    close(mt, KEY["1.2"]["mape_tawaqqu"], 1e-4)
    close(mb, KEY["1.2"]["mape_baseline"], 1e-4)
    assert mt < mb  # over the whole season the vendor looks better
    print(f"  season mean % error: Tawaqqu {pct(mt)}, seasonal baseline {pct(mb)}")


def lab13():
    a3, taw, base, per_staff = arrivals()
    peak = range(43, 49)
    et = [(taw[d] - a3[d]) / a3[d] for d in peak]
    eb = [(base[d] - a3[d]) / a3[d] for d in peak]
    k = KEY["1.3"]
    close(sum(map(abs, et)) / 6, k["peak_mape_tawaqqu"], 1e-4)
    close(sum(map(abs, eb)) / 6, k["peak_mape_baseline"], 1e-4)
    close(sum(et) / 6, k["peak_bias_tawaqqu"], 1e-4)
    need = max(a3[d] / taw[d] - 1 for d in peak)
    buf = math.ceil(round(need * 100, 6) / 5) * 5 / 100
    assert buf == k["buffer_tawaqqu"], buf
    short_plain = sum(1 for d in peak if math.ceil(taw[d] / per_staff) < math.ceil(a3[d] / per_staff))
    short_buf = sum(1 for d in peak if math.ceil(taw[d] * (1 + buf) / per_staff) < math.ceil(a3[d] / per_staff))
    assert short_plain >= 4 and short_buf == 0, (short_plain, short_buf)
    needb = max(a3[d] / base[d] - 1 for d in peak)
    bufb = math.ceil(round(needb * 100, 6) / 5) * 5 / 100
    assert bufb == k["buffer_baseline"]
    extra_t = sum(math.ceil(taw[d] * (1 + buf) / per_staff) for d in peak)
    extra_b = sum(math.ceil(base[d] * (1 + bufb) / per_staff) for d in peak)
    print(f"  peak days 43-48: mean % error Tawaqqu {pct(k['peak_mape_tawaqqu'])} (bias {pct(k['peak_bias_tawaqqu'])}), "
          f"baseline {pct(k['peak_mape_baseline'])} (bias {pct(k['peak_bias_baseline'])})")
    print(f"  largest under-forecast {pct(k['max_under_tawaqqu'])} of actual = {pct(need)} of the forecast; buffer {pct(buf, 0)}")
    print(f"  short-staffed peak days: {short_plain} of 6 without buffer, {short_buf} with it; "
          f"staff-days over the week: Tawaqqu+{pct(buf, 0)} {extra_t}, baseline+{pct(bufb, 0)} {extra_b}, needed "
          f"{sum(math.ceil(a3[d] / per_staff) for d in peak)}")


def lab14():
    _, hours = rows(F / "peakday" / "peak_day_hours.xlsx", "الساعات")
    _, consts = rows(F / "peakday" / "peak_day_hours.xlsx", "الثوابت")
    c = {r[0]: r[1] for r in consts}
    total = c["الوافدون إلى الحي التاريخي في اليوم 45"]
    per = {r[0]: total * r[1] for r in hours}
    heat = {r[0]: r[2] for r in hours}
    close(sum(r[1] for r in hours), 1.0, 1e-9)
    ph = max(per, key=per.get)
    trips = math.ceil(per[ph] * c["حصة الحافلات الترددية"] / c["سعة الحافلة"])
    overlap = [h for h in per if per[h] >= 0.06 * total and heat[h] >= c["حذر شديد: من"]]
    k = KEY["1.4"]
    assert ph == k["peak_hour"] and trips == k["shuttle_trips"] and overlap == k["overlap_hours"], (ph, trips, overlap)
    print(f"  peak hour {ph} with {round(per[ph])} arrivals = {round(per[ph] / 24)} per train wave of 150 s; "
          f"{trips} shuttle trips; crowd and heat overlap in hours {overlap}")


def sim_runs():
    data = []
    for name in ("results_plan_A.csv", "results_plan_B.csv", "results_stress.csv"):
        with open(F / "sim" / name, encoding="utf-8") as f:
            data += list(csv.DictReader(f))
    with open(LABS / "solutions" / "sim_runs.csv", encoding="utf-8") as f:
        assert len(list(csv.DictReader(f))) == len(data)
    out = {}
    for r in data:
        out.setdefault((r["plan"], r["scenario"]), []).append((int(r["seed"]), r["gate"], float(r["peak_density"]), int(r["seconds_above_limit"])))
    return out


def worst(runs, plan, scenario):
    return max(p for _, _, p, _ in runs[(plan, scenario)])


def lab15():
    runs = sim_runs()
    a1 = [(g, p, s) for seed, g, p, s in runs[("A", "base")] if seed == 1]
    assert len(a1) == 2 and all(p <= LIMIT for _, p, _ in a1)
    with open(F / "sim" / "series_A_base_seed1.csv", encoding="utf-8") as f:
        series = list(csv.DictReader(f))
    for g, p, _ in a1:
        close(max(float(r[g]) for r in series), p, 0.006)
    print("  plan A, seed 1, every gate open:", ", ".join(f"{g} peak {p:.2f}, {s} s above {LIMIT}" for g, p, s in a1))


def lab16():
    runs = sim_runs()
    wa, wb = worst(runs, "A", "base"), worst(runs, "B", "base")
    assert wb < LIMIT and wa > wb, (wa, wb)
    print(f"  usual day, worst gate over three seeds: plan A {wa:.2f}, plan B {wb:.2f} (limit {LIMIT}); "
          f"seconds above: A {sum(s for *_, s in runs[('A', 'base')])}, B {sum(s for *_, s in runs[('B', 'base')])}")


def lab17():
    runs = sim_runs()
    table = {}
    for sc in ("plus25", "gate_closed", "both"):
        for plan in ("A", "B"):
            table[(plan, sc)] = (worst(runs, plan, sc), max(s for *_, s in runs[(plan, sc)]))
            assert table[(plan, sc)][0] > LIMIT  # every stress test breaks both plans
        assert table[("B", sc)][0] < table[("A", sc)][0]  # but B always stays lower
    for (plan, sc), (p, s) in table.items():
        print(f"  {plan} {sc}: worst peak {p:.2f}, longest time above the limit {s} s")


def lab18():
    plan = (F / "command" / "safety_plan_excerpt.txt").read_text(encoding="utf-8")
    assert "2.0" in plan and "مدير العمليات المناوب" in plan
    need = (F / "privacy" / "safety_need.txt").read_text(encoding="utf-8")
    assert "1.5 و2.0 و2.5" in need
    print("  reference card: 1.5 meter the inflow (shift supervisor), 2.0 hold arrivals at the station (duty manager), "
          "2.5 stop entry (duty manager decides, gate supervisors carry out); counter down: manual counts every 2 min, treat as level 1")


def lab2x(which):
    _, data = rows(F / "assistant" / "scored_complete.xlsx", "الإجابات")
    _, blank = rows(F / "assistant" / "scoring_sheet.xlsx", "الإجابات")
    assert len(data) == len(blank) == 40 and all(b[7] in ("", None) for b in blank)
    verdicts = {r[0]: r[7] for r in data}
    assert verdicts == KEY["2.x"]["verdicts"]
    langs = {"ar": "العربية", "en": "الإنجليزية", "ur": "الأردية", "id": "الإندونيسية"}
    summary = {}
    for code, name in langs.items():
        vs = [r[7] for r in data if r[1] == name]
        summary[code] = {v: vs.count(v) for v in ("صحيحة", "خاطئة", "إحالة فاشلة", "لغة أخرى")}
        summary[code]["live"] = vs.count("صحيحة") >= 9 and vs.count("إحالة فاشلة") == 0
    assert summary == KEY["2.x"]["by_language"]
    for r in data:  # every handover item that is not a failure starts with a number to call
        if r[6] == "نعم" and r[7] == "صحيحة":
            assert any(n in r[3] for n in ("1912", "997")), r[0]
    if which == "2.1":
        for code in ("ar", "en"):
            print(f"  {langs[code]}: {summary[code]}")
    elif which == "2.2":
        for code in ("ur", "id"):
            print(f"  {langs[code]}: {summary[code]}")
        assert all(r[4] for r in data if r[1] in ("الأردية", "الإندونيسية"))
    else:
        total = sum(s["صحيحة"] for s in summary.values())
        print(f"  overall {total}/40 correct ({pct(total / 40, 0)}); go live: " +
              ", ".join(langs[c] for c, s in summary.items() if s["live"]) +
              "; handover failures: " + ", ".join(f"{langs[c]} {s['إحالة فاشلة']}" for c, s in summary.items()))


def meter():
    _, data = rows(F / "energy" / "meter_daily.xlsx", "العداد")
    return data


def lab24():
    data = meter()
    def per(lo, hi):
        p = [r for r in data if lo <= r[1] <= hi]
        return len(p), sum(r[5] for r in p), sum(r[3] for r in p) / len(p), sum(r[4] for r in p) / len(p)
    nb, sb, cb, vb = per(1, 6)
    na, sa, ca, va = per(13, 18)
    raw_sum, raw_mean = 1 - sa / sb, 1 - (sa / na) / (sb / nb)
    close(raw_sum, KEY["2.4"]["raw_saving_sum"], 1e-4)
    close(raw_mean, KEY["2.4"]["raw_saving_mean"], 1e-4)
    claim = (F / "energy" / "naseem_claim.txt").read_text(encoding="utf-8")
    assert f"{round(raw_sum * 100)}%" in claim  # the vendor's number is the raw sum comparison
    print(f"  days {nb} before, {na} after (9 missing); raw saving by sums {pct(raw_sum)}, by daily means {pct(raw_mean)}; "
          f"cooling degree days {cb:.1f} -> {ca:.1f}, visitors {vb:.0f} -> {va:.0f}")


def lab25():
    data = meter()
    base = [r for r in data if r[1] <= 12]
    X = [[1, r[3], r[4]] for r in base]
    y = [r[5] for r in base]
    n = 3
    a = [[sum(x[i] * x[j] for x in X) for j in range(n)] for i in range(n)]
    b = [sum(x[i] * t for x, t in zip(X, y)) for i in range(n)]
    for i in range(n):
        p = a[i][i]
        a[i] = [v / p for v in a[i]]
        b[i] /= p
        for r in range(n):
            if r != i:
                f = a[r][i]
                a[r] = [v - f * w for v, w in zip(a[r], a[i])]
                b[r] -= f * b[i]
    post = [r for r in data if r[1] >= 13]
    pred = sum(b[0] + b[1] * r[3] + b[2] * r[4] for r in post)
    act = sum(r[5] for r in post)
    led = 180 * sum(1 for r in post if r[1] >= 14)
    k = KEY["2.5"]
    close(1 - act / pred, k["adjusted_saving"], 1e-4)
    close((pred - act - led) / pred, k["naseem_saving"], 1e-4)
    print(f"  baseline kWh/day = {b[0]:.0f} + {b[1]:.1f} x CDD + {b[2]:.3f} x visitors; predicted {pred:,.0f}, actual {act:,}; "
          f"adjusted saving {pct(1 - act / pred)}; lighting {led:,} kWh; Naseem alone {pct((pred - act - led) / pred)} (claim 19%)")


def lab26():
    _, data = rows(F / "privacy" / "options_complete.xlsx", "الخيارات")
    ref = {r[0]: r for r in data}
    k = KEY["2.6"]
    assert sorted(o for o, r in ref.items() if r[4] == "نعم") == k["sensitive"]
    assert sorted(o for o, r in ref.items() if r[7] == "نعم") == k["meets_both"]
    assert sorted(o for o, r in ref.items() if r[6] == "نعم") == k["meets_gates"]
    print(f"  meet need 1 (gates): {k['meets_gates']}; need 2 (whole plaza): {k['meets_both']}; sensitive: {k['sensitive']}; "
          f"least intrusive that meet the need: {k['least_intrusive']} (O2 at the gates, O3 counts with short video retention)")


def lab27():
    prop = (F / "privacy" / "lost_child_proposal.txt").read_text(encoding="utf-8")
    assert "بصمة وجه" in prop and "سنة" in prop
    print("  proposal: " + KEY["2.7"]["proposal"] + "; impact assessment triggers: " + "، ".join(KEY["2.7"]["triggers"]))


def lab28():
    _, data = rows(F / "map" / "map_template.xlsx", "الخريطة")
    assert [r[0] for r in data] == list(KEY["2.8"]["scores"])
    pri = {u: v + r - k for u, (v, k, r) in KEY["2.8"]["scores"].items()}
    assert pri == KEY["2.8"]["priority"]
    print("  reference order: " + ", ".join(f"{u}({pri[u]})" for u in KEY["2.8"]["order"]) +
          "; risk 3: " + ", ".join(KEY["2.8"]["high_risk"]))


LABS_RUN = {"1.1": lab11, "1.2": lab12, "1.3": lab13, "1.4": lab14, "1.5": lab15, "1.6": lab16, "1.7": lab17,
            "1.8": lab18, "2.1": lambda: lab2x("2.1"), "2.2": lambda: lab2x("2.2"), "2.3": lambda: lab2x("2.3"),
            "2.4": lab24, "2.5": lab25, "2.6": lab26, "2.7": lab27, "2.8": lab28}


def main():
    which = sys.argv[1:] or list(LABS_RUN)
    for lab in which:
        print(f"Lab {lab}")
        LABS_RUN[lab]()
        print(f"  PASS {lab}")


if __name__ == "__main__":
    main()
