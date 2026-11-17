# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Writes labs/sim/plaza_sim.ipynb from labs/sim/plaza_sim.py (the model part between the markers).

    uv run labs/_tools/make_notebook.py
"""
import json
from pathlib import Path

SIM = Path(__file__).resolve().parents[1] / "sim"
src = (SIM / "plaza_sim.py").read_text(encoding="utf-8")
model = src.split("# --- model ---\n", 1)[1].split("# --- end model ---", 1)[0].strip()


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.strip().splitlines(keepends=True)}


def code(text):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
            "source": text.strip().splitlines(keepends=True)}


cells = [
    md("""
# دفتر محاكاة ساحة المشرع

المختبرات 1.5 إلى 1.7 · هيئة الرفادة للمدينة المضيفة (حالة افتراضية).

دفتر جاهز، لا تكتب فيه كودًا. تختار الخطة والظرف والبذرة في الخلية الثانية، ثم تشغّل كل الخلايا.

- **في Google Colab:** File ثم Upload notebook، واختر هذا الملف. ثم Runtime ثم Run all. أول تشغيل يثبّت JuPedSim في دقيقة أو اثنتين.
- **على حاسوبك:** `uv run plaza_sim.py --plan A --scenario base --seed 1` من مجلد `labs/sim`.
- **إن لم يعمل أي منهما:** النتائج الجاهزة في `labs/files/sim/runs.csv` هي نفسها.

الساحة 50 مترًا عرضًا و30 مترًا عمقًا. يصل الزوار من الطرف الجنوبي في موجات (قطار كل 150 ثانية) ويمشون إلى أقرب بوابة مفتوحة.
تُقاس الكثافة في مستطيل 8 × 5 أمتار أمام كل بوابة كل ثانية، ويؤخذ متوسط عشر ثوانٍ، كما تعرّفها خطة السلامة. الحد 2.0 شخص في المتر المربع.
"""),
    code("""
# Installs the simulation library when it is missing (Colab), then nothing more
import importlib.util, subprocess, sys
missing = [p for p, m in (("jupedsim==1.4.2", "jupedsim"), ("shapely", "shapely"), ("matplotlib", "matplotlib")) if importlib.util.find_spec(m) is None]
if missing:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", *missing], check=True)
print("ready")
"""),
    code("""
# Choose here, then run every cell
PLAN = "A"          # @param ["A", "B"]
SCENARIO = "base"   # @param ["base", "plus25", "gate_closed", "both"]
SEED = 1            # @param [1, 2, 3]
"""),
    md("""
## النموذج

لا تغيّر هذه الخلية. فيها الساحة والخطتان والظروف الأربعة: `base` يوم معتاد، و`plus25` وافدون أكثر بالربع، و`gate_closed` بوابة مغلقة، و`both` الاثنان معًا.
"""),
    code(model),
    code("""
result = run(PLAN, SCENARIO, SEED)
print(f"plan {PLAN}, scenario {SCENARIO}, seed {SEED}: {result['visitors']} visitors, plaza clear after {result['seconds']} s")
for i, (x, peak, above) in enumerate(zip(result["gates"], result["peaks"], result["above"]), 1):
    print(f"G{i} (x = {x:g} m): peak density {peak:.2f} persons/m2, {above} s above the limit of {LIMIT}")
"""),
    code("""
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(9, 4))
for g in range(len(result["gates"])):
    ax.plot([row[g] for row in result["smooth"]], label=f"G{g + 1}")
ax.axhline(LIMIT, color="red", linestyle="--", label="limit 2.0")
ax.set_xlabel("second"); ax.set_ylabel("persons per m2 (10 s mean)")
ax.set_title(f"Plan {PLAN}, {SCENARIO}, seed {SEED}")
ax.legend(); plt.show()
"""),
    md("""
## ما تسجله

في جدول المقارنة: قمة الكثافة لكل بوابة، والثواني فوق الحد، والبذرة. اقرأ المنحنى أيضًا: متى ترتفع الكثافة؟ بعد كل قطار؟ وهل تعود إلى الصفر قبل القطار التالي؟

مهمة إضافية (1.5): غيّر مساحة القياس في السطر `run(PLAN, SCENARIO, SEED, area=(4.0, 3.0))` وانظر كيف تتغير القمة للتشغيل نفسه.
"""),
]
for i, c in enumerate(cells):
    c["id"] = f"cell-{i + 1}"
nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                                   "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}
(SIM / "plaza_sim.ipynb").write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
print("wrote", SIM / "plaza_sim.ipynb")
