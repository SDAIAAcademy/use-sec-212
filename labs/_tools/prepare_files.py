# /// script
# requires-python = ">=3.11"
# dependencies = ["openpyxl>=3.1"]
# ///
"""Writes the Al-Rifada file pack into labs/files/ and the planted values into labs/solutions/key.json.

    uv run labs/_tools/prepare_files.py

Fixed seed (212): the same content on every run (only the save time inside xlsx files changes).
The simulation results in labs/files/sim/ come from labs/sim/plaza_sim.py (`--all`), not from here.
"""
import datetime
import json
import math
import random
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

sys.path.insert(0, str(Path(__file__).parent))
import texts as T  # noqa: E402

SEED = 212
LABS = Path(__file__).resolve().parents[1]
FILES = LABS / "files"
SOL = LABS / "solutions"
FIXED = datetime.datetime(2026, 11, 1, 9, 0, 0)
HEAD = PatternFill("solid", fgColor="DCEBEA")
FILL = PatternFill("solid", fgColor="FFF6DA")
KEY = {}


def text(path, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.strip() + "\n", encoding="utf-8", newline="\n")


def book():
    wb = Workbook()
    wb.properties.created = FIXED
    wb.properties.modified = FIXED
    wb.properties.creator = "SDAIA Academy"
    return wb


def sheet(wb, title, header, rows, widths=None, first=False, fill_cols=(), rtl=True):
    ws = wb.active if first else wb.create_sheet()
    ws.title = title
    ws.sheet_view.rightToLeft = rtl
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        ws.append(list(r))
    for col in fill_cols:
        for row in ws.iter_rows(min_row=2, min_col=col, max_col=col):
            row[0].fill = FILL
    for i, w in enumerate(widths or [], 1):
        ws.column_dimensions[ws.cell(1, i).column_letter].width = w
    ws.freeze_panes = "A2"
    return ws


def save(wb, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)


# ---------- pre-work ----------
def prework():
    text(FILES / "prework" / "prework_guide.txt", T.PREWORK_GUIDE)
    wb = book()
    sheet(wb, "الحصر", ["#", "الخدمة", "النظام اليوم أو المقترح", "ماذا يفعل: يتنبأ أم يعدّ أم يتعرف أم يجيب",
                        "البيانات التي يلمسها", "من يتأثر بخطئه"],
          [[i, "", "", "", "", ""] for i in range(1, 8)], [5, 28, 30, 26, 30, 30], first=True, fill_cols=(2, 3, 4, 5, 6))
    save(wb, FILES / "prework" / "prework_inventory.xlsx")


# ---------- lab 1.1 ----------
def lab11():
    body = "ست حالات نشر في هيئة الرفادة للمدينة المضيفة (حالات افتراضية)\n\n"
    body += "\n\n".join(f"{cid} · {title}\n{desc}" for cid, title, desc in T.DEPLOYMENTS)
    text(FILES / "deployments" / "six_deployments.txt", body)
    wb = book()
    sheet(wb, "الترتيب", ["الحالة", "العنوان", "البيانات التي يلمسها", "الأشخاص المتأثرون", "أسوأ خطأ ممكن",
                          "على من يقع", "مخاطر السلامة (1-3)", "مخاطر الخصوصية (1-3)", "الترتيب (1 الأعلى)", "السبب في سطر"],
          [[cid, title, "", "", "", "", "", "", "", ""] for cid, title, _ in T.DEPLOYMENTS],
          [7, 34, 28, 28, 30, 22, 12, 12, 12, 40], first=True, fill_cols=(3, 4, 5, 6, 7, 8, 9, 10))
    save(wb, FILES / "deployments" / "ranking_sheet.xlsx")
    KEY["1.1"] = T.DEPLOY_KEY


# ---------- labs 1.2 and 1.3 ----------
DAYS, GROWTH, PER_STAFF, PEAK = 60, 0.06, 450, list(range(43, 49))


def expected(season, d):
    level = 34000 * (1 + GROWTH) ** (season - 1)
    ramp = 0.75 + 0.5 * min(1.0, d / 40)        # the season builds up to the big week
    week = 1 + 0.05 * math.sin(2 * math.pi * (d + 3 * season) / 7)  # weekdays shift between seasons
    bump = 1.6 if d in PEAK else (1.15 if d in (42, 49) else 1.0)
    tail = 0.8 if d > 52 else 1.0
    return level * ramp * week * bump * tail


def forecast_files():
    rng = random.Random(SEED)
    actual = {}
    for s in (1, 2, 3):
        for d in range(1, DAYS + 1):
            actual[(s, d)] = round(expected(s, d) * (1 + rng.gauss(0, 0.045)))
    exp3 = [expected(3, d) for d in range(1, DAYS + 1)]
    tawaqqu = {}
    for d in range(1, DAYS + 1):  # a smooth model: a centred 7-day average of the expected curve
        win = exp3[max(0, d - 4):min(DAYS, d + 3)]
        tawaqqu[d] = round(sum(win) / len(win) * (1 + rng.gauss(0, 0.015)))
    rows = []
    for s in (1, 2, 3):
        for d in range(1, DAYS + 1):
            rows.append([s, d, actual[(s, d)], tawaqqu[d] if s == 3 else None])
    wb = book()
    sheet(wb, "الوافدون", ["الموسم", "اليوم", "الوافدون الفعليون", "تنبؤ «توقّع» (الموسم 3)"], rows, [10, 10, 18, 22], first=True)
    sheet(wb, "الثوابت", ["الثابت", "القيمة"], [["نمو الخطة للموسم 3", GROWTH], ["وافدون يخدمهم موظف استقبال في اليوم", PER_STAFF],
                                                 ["أيام الذروة في تقويم الموسم 3", "43 إلى 48"]], [40, 16])
    calc = [[d, actual[(2, d)], actual[(3, d)], tawaqqu[d], None, None, None, None, None] for d in range(1, DAYS + 1)]
    sheet(wb, "الحساب", ["اليوم", "الموسم 2 في اليوم نفسه", "الفعلي", "«توقّع»", "خط الأساس الموسمي", "خطأ «توقّع»", "نسبة خطأ «توقّع»",
                          "خطأ خط الأساس", "نسبة خطأ خط الأساس"], calc, [8, 16, 12, 12, 18, 14, 16, 14, 18], fill_cols=(5, 6, 7, 8, 9))
    save(wb, FILES / "forecast" / "arrivals_seasons.xlsx")
    text(FILES / "forecast" / "README.txt", T.FORECAST_NOTE)

    base = {d: actual[(2, d)] * (1 + GROWTH) for d in range(1, DAYS + 1)}
    a3 = {d: actual[(3, d)] for d in range(1, DAYS + 1)}

    def ape(f, d):
        return abs(f[d] - a3[d]) / a3[d]

    mape_t = sum(ape(tawaqqu, d) for d in a3) / DAYS
    mape_b = sum(ape(base, d) for d in a3) / DAYS
    peak_rows = []
    for d in PEAK:
        peak_rows.append({"day": d, "actual": a3[d], "tawaqqu": tawaqqu[d], "baseline": round(base[d]),
                          "err_t": (tawaqqu[d] - a3[d]) / a3[d], "err_b": (base[d] - a3[d]) / a3[d]})
    under_t = max(-r["err_t"] for r in peak_rows)
    need_t = max(r["actual"] / r["tawaqqu"] - 1 for r in peak_rows)  # the buffer is applied to the forecast
    need_b = max(r["actual"] / r["baseline"] - 1 for r in peak_rows)
    buf_t = math.ceil(round(need_t * 100, 6) / 5) * 5 / 100
    buf_b = math.ceil(round(max(need_b, 0) * 100, 6) / 5) * 5 / 100
    staff = [{"day": r["day"], "plain_t": math.ceil(r["tawaqqu"] / PER_STAFF), "buffer_t": math.ceil(r["tawaqqu"] * (1 + buf_t) / PER_STAFF),
              "needed": math.ceil(r["actual"] / PER_STAFF)} for r in peak_rows]
    KEY["1.2"] = {"mape_tawaqqu": round(mape_t, 4), "mape_baseline": round(mape_b, 4)}
    KEY["1.3"] = {"peak_mape_tawaqqu": round(sum(abs(r["err_t"]) for r in peak_rows) / 6, 4),
                  "peak_mape_baseline": round(sum(abs(r["err_b"]) for r in peak_rows) / 6, 4),
                  "peak_bias_tawaqqu": round(sum(r["err_t"] for r in peak_rows) / 6, 4),
                  "peak_bias_baseline": round(sum(r["err_b"] for r in peak_rows) / 6, 4),
                  "max_under_tawaqqu": round(under_t, 4), "need_tawaqqu": round(need_t, 4), "need_baseline": round(need_b, 4), "buffer_tawaqqu": buf_t, "buffer_baseline": buf_b,
                  "rows": peak_rows, "staff": staff}

    # start file of lab 1.3: part 1 completed
    wb = book()
    done = []
    for d in range(1, DAYS + 1):
        b = round(base[d])
        done.append([d, a3[d], tawaqqu[d], b, tawaqqu[d] - a3[d], round((tawaqqu[d] - a3[d]) / a3[d], 4),
                     b - a3[d], round((b - a3[d]) / a3[d], 4)])
    sheet(wb, "الحساب", ["اليوم", "الفعلي", "«توقّع»", "خط الأساس الموسمي", "خطأ «توقّع»", "نسبة خطأ «توقّع»",
                          "خطأ خط الأساس", "نسبة خطأ خط الأساس"], done, [8, 12, 12, 18, 14, 16, 14, 18], first=True)
    sheet(wb, "الذروة", ["اليوم", "الفعلي", "«توقّع»", "خط الأساس", "نسبة خطأ «توقّع»", "نسبة خطأ خط الأساس"],
          [[d, None, None, None, None, None] for d in PEAK], [8, 12, 12, 12, 16, 18], fill_cols=(2, 3, 4, 5, 6))
    sheet(wb, "التوظيف", ["اليوم", "موظفون بتنبؤ «توقّع» وحده", "موظفون بـ«توقّع» والهامش", "موظفون يلزمون فعلًا"],
          [[d, None, None, None] for d in PEAK], [8, 24, 24, 22], fill_cols=(2, 3, 4))
    sheet(wb, "الثوابت", ["الثابت", "القيمة"], [["وافدون يخدمهم موظف استقبال في اليوم", PER_STAFF],
                                                 ["أيام الذروة في تقويم الموسم 3", "43 إلى 48"]], [40, 16])
    save(wb, FILES / "forecast" / "forecast_part2_start.xlsx")


# ---------- lab 1.4 ----------
SHARES = [0.5, 0.3, 0.2, 0.2, 0.4, 1.0, 2.0, 3.0, 3.5, 4.0, 4.5, 5.0, 4.0, 4.5, 4.5, 6.0, 9.0, 15.0, 11.0, 7.5, 6.0, 4.0, 2.5, 1.4]
HEAT = [31, 30, 30, 29, 29, 30, 32, 35, 38, 41, 43, 45, 47, 48, 47, 46, 43, 40, 37, 35, 34, 33, 32, 31]
PEAK_DAY_TOTAL, SHUTTLE_SHARE, BUS_CAP = 72000, 0.30, 60


def heat_cat(h):
    return "خطر" if h >= 46 else ("حذر شديد" if h >= 39 else ("حذر" if h >= 32 else "-"))


def lab14():
    assert abs(sum(SHARES) - 100) < 1e-9, sum(SHARES)
    wb = book()
    rows = [[h, SHARES[h] / 100, HEAT[h], None, None] for h in range(24)]
    ws = sheet(wb, "الساعات", ["الساعة", "حصة الساعة", "مؤشر الحرارة", "الوافدون في الساعة", "فئة الإجهاد الحراري"], rows,
               [10, 14, 14, 20, 20], first=True, fill_cols=(4, 5))
    for row in ws.iter_rows(min_row=2, min_col=2, max_col=2):
        row[0].number_format = "0.0%"
    sheet(wb, "الثوابت", ["الثابت", "القيمة"], [["الوافدون إلى الحي التاريخي في اليوم 45", PEAK_DAY_TOTAL],
                                                 ["حصة الحافلات الترددية", SHUTTLE_SHARE], ["سعة الحافلة", BUS_CAP],
                                                 ["حذر: مؤشر الحرارة من", 32], ["حذر شديد: من", 39], ["خطر: من", 46]], [40, 14])
    save(wb, FILES / "peakday" / "peak_day_hours.xlsx")
    text(FILES / "peakday" / "README.txt", T.PEAK_DAY_NOTE)
    per_hour = [PEAK_DAY_TOTAL * s / 100 for s in SHARES]
    peak_h = max(range(24), key=lambda h: per_hour[h])
    overlap = [h for h in range(24) if per_hour[h] >= 0.06 * PEAK_DAY_TOTAL and HEAT[h] >= 39]
    KEY["1.4"] = {"peak_hour": peak_h, "peak_hour_arrivals": round(per_hour[peak_h]),
                  "shuttle_trips": math.ceil(per_hour[peak_h] * SHUTTLE_SHARE / BUS_CAP),
                  "danger_hours": [h for h in range(24) if HEAT[h] >= 46], "overlap_hours": overlap,
                  "plaza_per_wave": round(per_hour[peak_h] / 24)}


# ---------- lab 1.8 ----------
def lab18():
    text(FILES / "command" / "safety_plan_excerpt.txt", T.SAFETY_PLAN)
    text(FILES / "command" / "command_card_template.txt", T.COMMAND_TEMPLATE)


# ---------- labs 2.1 to 2.3 ----------
VERDICTS = ["صحيحة", "خاطئة", "إحالة فاشلة", "لغة أخرى"]
LANGS = {"ar": "العربية", "en": "الإنجليزية", "ur": "الأردية", "id": "الإندونيسية"}


def assistant():
    text(FILES / "assistant" / "fact_sheet.txt", T.FACT_SHEET)
    text(FILES / "assistant" / "handover_rules.txt", T.HANDOVER_RULES)
    text(FILES / "assistant" / "translator_note.txt", T.TRANSLATOR_NOTE)
    text(FILES / "assistant" / "acceptance_rule.txt", T.ACCEPT_RULE)
    assert len(T.QA) == 40
    wb = book()
    rows = []
    for qid, lang, q, a, back, _ in T.QA:
        n = int(qid[2:])
        fact, hand = T.INTENTS[n - 1]
        rows.append([qid, LANGS[lang], q, a, back, fact, "نعم" if hand else "لا", "", ""])
    header = ["الرقم", "اللغة", "السؤال", "إجابة «مِضياف» المسجلة", "الترجمة العكسية المعتمدة", "بند صحيفة الحقائق",
              "يلزم إحالة؟", "التقدير", "ملاحظة"]
    sheet(wb, "الإجابات", header, rows, [8, 12, 40, 60, 50, 10, 10, 14, 30], first=True, fill_cols=(8, 9))
    sheet(wb, "التصنيف", ["التقدير المسموح"], [[v] for v in VERDICTS], [20])
    save(wb, FILES / "assistant" / "scoring_sheet.xlsx")
    # start file of lab 2.3: every answer scored
    wb = book()
    full = [r[:7] + [v, ""] for r, (*_, v) in zip(rows, T.QA)]
    sheet(wb, "الإجابات", header, full, [8, 12, 40, 60, 50, 10, 10, 14, 30], first=True)
    sheet(wb, "الملخص", ["اللغة", "صحيحة", "خاطئة", "إحالة فاشلة", "لغة أخرى", "نسبة الصحيحة", "قرار التشغيل"],
          [[name, None, None, None, None, None, None] for name in LANGS.values()] + [["المجموع", None, None, None, None, None, None]],
          [14, 10, 10, 12, 10, 14, 30], fill_cols=(2, 3, 4, 5, 6, 7))
    save(wb, FILES / "assistant" / "scored_complete.xlsx")
    summary = {}
    for lang in LANGS:
        vs = [v for qid, lg, *_, v in T.QA if lg == lang]
        summary[lang] = {v: vs.count(v) for v in VERDICTS}
        summary[lang]["live"] = vs.count("صحيحة") >= 9 and vs.count("إحالة فاشلة") == 0
    KEY["2.x"] = {"by_language": summary, "overall_correct": sum(1 for *_, v in T.QA if v == "صحيحة"),
                  "verdicts": {qid: v for qid, *_, v in T.QA}}


# ---------- labs 2.4 and 2.5 ----------
def energy():
    rng = random.Random(SEED + 1)
    rows, truth = [], []
    missing = set(range(16 * 30 - 29 + 8, 16 * 30 - 29 + 17))  # nine days in month 16
    for day in range(1, 18 * 30 + 1):
        month = (day - 1) // 30 + 1
        m12 = (month - 1) % 12 + 1
        temp = 27 + 9 * math.sin(math.pi * (m12 - 1.5) / 6.5) ** 2 * (1 if m12 <= 9 else 0.6) + rng.gauss(0, 1.3)
        if month >= 13:
            temp -= 1.4  # a cooler first half year after the start
        cdd = max(0.0, temp - 21)
        visitors = 5200 + 1200 * math.sin(2 * math.pi * day / 7) ** 2 + rng.gauss(0, 300)
        if month in (15, 16):
            visitors *= 0.78  # the main hall closed for maintenance
        kwh = 2400 + 210 * cdd + 0.35 * visitors
        if month >= 13:
            kwh *= 0.94  # what Naseem really saves
        if month >= 14:
            kwh -= 180  # the lighting retrofit
        kwh *= 1 + rng.gauss(0, 0.025)
        truth.append((day, month, round(temp, 1), round(cdd, 1), round(visitors), round(kwh)))
        if day in missing:
            continue
        rows.append([day, month, round(temp, 1), round(cdd, 1), round(visitors), round(kwh)])
    wb = book()
    header = ["اليوم", "الشهر", "متوسط الحرارة", "درجات التبريد (أساس 21)", "الزوار", "الكهرباء (كيلوواط ساعة)"]
    sheet(wb, "العداد", header, rows, [8, 8, 14, 22, 10, 22], first=True)
    sheet(wb, "المقارنة", ["الفترة", "الأشهر", "عدد الأيام", "مجموع الكهرباء", "متوسط اليوم", "متوسط درجات التبريد", "متوسط الزوار"],
          [["قبل «نسيم»", "1 إلى 6", None, None, None, None, None], ["بعد «نسيم»", "13 إلى 18", None, None, None, None, None]],
          [14, 12, 12, 16, 14, 20, 14], fill_cols=(3, 4, 5, 6, 7))
    save(wb, FILES / "energy" / "meter_daily.xlsx")
    text(FILES / "energy" / "naseem_claim.txt", T.ENERGY_CLAIM)

    def period(lo, hi):
        part = [r for r in rows if lo <= r[1] <= hi]
        return {"days": len(part), "sum": sum(r[5] for r in part), "mean": sum(r[5] for r in part) / len(part),
                "cdd": sum(r[3] for r in part) / len(part), "visitors": sum(r[4] for r in part) / len(part)}

    before, after = period(1, 6), period(13, 18)
    raw_sum = 1 - after["sum"] / before["sum"]
    raw_mean = 1 - after["mean"] / before["mean"]
    # baseline: ordinary least squares on the first 12 months
    base = [r for r in rows if r[1] <= 12]
    coef = ols([[1, r[3], r[4]] for r in base], [r[5] for r in base])
    post = [r for r in rows if r[1] >= 13]
    pred = sum(coef[0] + coef[1] * r[3] + coef[2] * r[4] for r in post)
    actual_post = sum(r[5] for r in post)
    led = 180 * sum(1 for r in post if r[1] >= 14)
    adj = 1 - actual_post / pred
    naseem = (pred - actual_post - led) / pred
    KEY["2.4"] = {"before": before, "after": after, "raw_saving_sum": round(raw_sum, 4), "raw_saving_mean": round(raw_mean, 4),
                  "missing_days": len(missing)}
    KEY["2.5"] = {"coef": [round(c, 4) for c in coef], "predicted_post": round(pred), "actual_post": actual_post,
                  "adjusted_saving": round(adj, 4), "led_kwh": led, "naseem_saving": round(naseem, 4)}
    # start file of lab 2.5: the raw comparison completed
    wb = book()
    sheet(wb, "العداد", header, rows, [8, 8, 14, 22, 10, 22], first=True)
    sheet(wb, "المقارنة", ["الفترة", "الأشهر", "عدد الأيام", "مجموع الكهرباء", "متوسط اليوم", "متوسط درجات التبريد", "متوسط الزوار"],
          [["قبل «نسيم»", "1 إلى 6", before["days"], before["sum"], round(before["mean"]), round(before["cdd"], 1), round(before["visitors"])],
           ["بعد «نسيم»", "13 إلى 18", after["days"], after["sum"], round(after["mean"]), round(after["cdd"], 1), round(after["visitors"])]],
          [14, 12, 12, 16, 14, 20, 14])
    sheet(wb, "خط الأساس", ["البند", "القيمة"], [["الثابت", None], ["معامل درجات التبريد", None], ["معامل الزوار", None],
                                                  ["الاستهلاك المتوقع بعد «نسيم» (مجموع)", None], ["الاستهلاك الفعلي بعد «نسيم» (مجموع)", None],
                                                  ["التوفير المعدّل", None], ["أثر الإنارة (مجموع)", None], ["توفير «نسيم» وحده", None]],
          [40, 18], fill_cols=(2,))
    save(wb, FILES / "energy" / "energy_part2_start.xlsx")


def ols(X, y):
    n = len(X[0])
    a = [[sum(X[k][i] * X[k][j] for k in range(len(X))) for j in range(n)] for i in range(n)]
    b = [sum(X[k][i] * y[k] for k in range(len(X))) for i in range(n)]
    for i in range(n):  # Gauss-Jordan
        p = a[i][i]
        for j in range(n):
            a[i][j] /= p
        b[i] /= p
        for r in range(n):
            if r != i:
                f = a[r][i]
                for j in range(n):
                    a[r][j] -= f * a[i][j]
                b[r] -= f * b[i]
    return b


# ---------- labs 2.6 and 2.7 ----------
def privacy():
    body = "ستة خيارات للكاميرات والحساسات في ساحة المشرع (مقترحات افتراضية)\n\n"
    body += "\n\n".join(f"{oid} · {title}\n{desc}" for oid, title, desc in T.OPTIONS)
    text(FILES / "privacy" / "options_6.txt", body)
    text(FILES / "privacy" / "safety_need.txt", T.SAFETY_NEED)
    text(FILES / "privacy" / "lost_child_proposal.txt", T.LOST_CHILD_PROPOSAL)
    text(FILES / "privacy" / "review_record_template.txt", T.REVIEW_TEMPLATE)
    header = ["الخيار", "العنوان", "يعدّ أم يتعرف", "البيانات التي يلمسها", "بيانات حساسة؟", "أثره على الأطفال والزوار الأضعف",
              "يلبي الحاجة 1 (البوابات)", "يلبي الحاجة 2 (الساحة كلها)", "ملاحظة"]
    wb = book()
    sheet(wb, "الخيارات", header, [[o, t, "", "", "", "", "", "", ""] for o, t, _ in T.OPTIONS],
          [7, 34, 14, 30, 12, 30, 14, 16, 30], first=True, fill_cols=(3, 4, 5, 6, 7, 8, 9))
    save(wb, FILES / "privacy" / "options_sheet.xlsx")
    ref = {
        "O1": ["يعدّ", "لا بيانات شخصية", "لا", "لا أثر", "جزئيًا", "لا"],
        "O2": ["يعدّ", "أعداد فقط، الصورة لا تُخزَّن", "لا", "يُعدّ الأطفال كغيرهم دون تعرف", "نعم", "لا"],
        "O3": ["يعدّ", "أعداد، وتسجيل فيديو لكل من في الساحة", "لا", "تسجيل الأطفال 90 يومًا", "نعم", "نعم"],
        "O4": ["يتعرف على الجهاز", "معرّفات أجهزة ومسارات", "لا (موقع شخصي)", "لا يعدّ من لا يحمل هاتفًا", "جزئيًا", "جزئيًا"],
        "O5": ["يتعرف", "بيانات حيوية لتحديد الهوية", "نعم", "يعالج وجوه الأطفال", "نعم", "نعم"],
        "O6": ["يعدّ", "صور للساحة وما حولها", "لا", "تصوير البيوت والأسطح", "لا", "نعم"],
    }
    wb = book()
    sheet(wb, "الخيارات", header, [[o, t] + ref[o] + [""] for o, t, _ in T.OPTIONS],
          [7, 34, 14, 30, 12, 30, 14, 16, 30], first=True)
    save(wb, FILES / "privacy" / "options_complete.xlsx")
    wb = book()
    sheet(wb, "الحفظ", ["نوع البيانات", "مدة الحفظ", "السبب", "ما يحدث بعدها"], [[t, "", "", ""] for t in T.RETENTION_TYPES],
          [40, 16, 40, 30], first=True, fill_cols=(2, 3, 4))
    save(wb, FILES / "privacy" / "retention_template.xlsx")
    KEY["2.6"] = {"meets_both": ["O3", "O5", "O6"], "meets_gates": ["O2", "O3", "O5"], "identifies": ["O4", "O5"],
                  "sensitive": ["O5"], "least_intrusive": ["O2", "O3"]}
    KEY["2.7"] = {"proposal": "مرفوض", "triggers": ["بيانات حساسة", "معالجة واسعة لبيانات من يفتقدون الأهلية", "مراقبة مستمرة", "تقنية جديدة"]}


# ---------- lab 2.8 ----------
REF_MAP = {  # value, risk, readiness
    "U01": (2, 1, 3), "U02": (3, 2, 2), "U03": (2, 3, 1), "U04": (3, 2, 2), "U05": (2, 1, 3),
    "U06": (2, 3, 1), "U07": (2, 1, 2), "U08": (3, 1, 3), "U09": (1, 3, 2), "U10": (2, 1, 2),
}


def the_map():
    text(FILES / "map" / "city_profile.txt", T.CITY_PROFILE)
    text(FILES / "map" / "use_cases_10.txt",
         "عشر حالات استخدام مقترحة لمدينة الرفادة (افتراضية)\n\n" + "\n".join(f"{u} · {t} (البيانات: {d})" for u, t, d in T.USE_CASES))
    text(FILES / "map" / "scoring_scale.txt", T.SCALE)
    wb = book()
    sheet(wb, "الخريطة", ["الحالة", "العنوان", "القيمة", "المخاطر", "جاهزية البيانات", "الأولوية", "الترتيب",
                          "ضوابط الكاميرا والموقع والقياسات الحيوية", "صاحب القرار البشري", "إذا تعطل النظام", "الدليل من المختبرات"],
          [[u, t, None, None, None, None, None, "", "", "", ""] for u, t, _ in T.USE_CASES],
          [7, 40, 9, 9, 12, 10, 9, 40, 22, 26, 30], first=True, fill_cols=(3, 4, 5, 6, 7, 8, 9, 10, 11))
    save(wb, FILES / "map" / "map_template.xlsx")
    pri = {u: v + r - k for u, (v, k, r) in REF_MAP.items()}
    KEY["2.8"] = {"scores": REF_MAP, "priority": pri, "order": sorted(pri, key=lambda u: (-pri[u], u)),
                  "high_risk": [u for u, (_, k, _) in REF_MAP.items() if k == 3]}


def main():
    prework()
    lab11()
    forecast_files()
    lab14()
    lab18()
    assistant()
    energy()
    privacy()
    the_map()
    SOL.mkdir(exist_ok=True)
    (SOL / "key.json").write_text(json.dumps(KEY, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: v for k, v in KEY.items() if k not in ("2.x",)}, ensure_ascii=False, indent=1, default=str)[:6000])
    print(json.dumps(KEY["2.x"]["by_language"], ensure_ascii=False))


if __name__ == "__main__":
    main()
