# /// script
# requires-python = ">=3.11"
# dependencies = ["openpyxl>=3.1"]
# ///
"""Splits the output of `plaza_sim.py --all` into the files of labs 1.5 to 1.7.

    uv run labs/sim/plaza_sim.py --all --out <folder>
    uv run labs/_tools/sim_files.py <folder>
"""
import csv
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from prepare_files import FILES, book, save, sheet  # noqa: E402

src = Path(sys.argv[1])
out = FILES / "sim"
out.mkdir(parents=True, exist_ok=True)
with open(src / "runs.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    rows = list(reader)
parts = {"results_plan_A.csv": lambda r: r[0] == "A" and r[1] == "base",
         "results_plan_B.csv": lambda r: r[0] == "B" and r[1] == "base",
         "results_stress.csv": lambda r: r[1] != "base"}
for name, keep in parts.items():
    with open(out / name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(r for r in rows if keep(r))
for plan in "AB":
    shutil.copyfile(src / f"series_{plan}_base_seed1.csv", out / f"series_{plan}_base_seed1.csv")
cols = ["الخطة", "الظرف", "البذرة", "البوابة", "قمة الكثافة", "ثوانٍ فوق الحد"]
base = [r for r in rows if r[1] == "base"]
wb = book()
sheet(wb, "المقارنة", cols, [[r[0], "يوم معتاد", int(r[2]), r[3], None, None] for r in base], [8, 14, 8, 8, 14, 14],
      first=True, fill_cols=(5, 6), rtl=True)
save(wb, out / "comparison_sheet.xlsx")
names = {"base": "يوم معتاد", "plus25": "وافدون أكثر بالربع", "gate_closed": "بوابة مغلقة", "both": "الاثنان معًا"}
wb = book()
sheet(wb, "المقارنة", cols, [[r[0], names[r[1]], int(r[2]), r[3], float(r[6]), int(r[7])] for r in base],
      [8, 14, 8, 8, 14, 14], first=True, rtl=True)
stress = [r for r in rows if r[1] != "base"]
sheet(wb, "الضغط", cols, [[r[0], names[r[1]], int(r[2]), r[3], None, None] for r in stress], [8, 20, 8, 8, 14, 14],
      fill_cols=(5, 6), rtl=True)
sheet(wb, "القرار", ["البند", "إجابتك"], [["الخطة المختارة", ""], ["الظرف الذي تتجاوز فيه الحد", ""],
                                          ["الإجراء في ذلك الظرف", ""]], [30, 60], fill_cols=(2,), rtl=True)
save(wb, out / "comparison_complete.xlsx")
shutil.copyfile(src / "runs.csv", FILES.parent / "solutions" / "sim_runs.csv")
print("wrote", sorted(p.name for p in out.iterdir()))
