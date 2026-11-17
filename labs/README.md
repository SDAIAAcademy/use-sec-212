# الذكاء الاصطناعي في المدن والسياحة والحج: المختبرات

ستة عشر مختبرًا لمقرر أكاديمية سدايا **USE-SEC-212**: ثمانية في كل يوم، أربعة منها 25 دقيقة وأربعة 20 دقيقة، وعمل
تحضيري متعقَّب قبل اليوم الأول. المختبرات صفحات إرشادية بالعربية: الهدف، والملفات، وخطوات بدقائقها، وأسئلة تحقق، ومهمة
إضافية ✱، وملاحظات للمدرّب. يعمل المشارك في جدول بيانات إلكتروني ومستندات، ولا يكتب كودًا. مختبرات المحاكاة (1.5 إلى 1.7)
تشغّل دفترًا جاهزًا في Google Colab، ولها نتائج جاهزة لمن لم يعمل عنده التشغيل.

كل المختبرات في جهة واحدة: **هيئة الرفادة للمدينة المضيفة**، هيئة افتراضية في مدينة افتراضية. الأعداد والأشخاص والمورِّدون
والإجابات المسجلة كلها اصطناعية ومولَّدة ببذرة ثابتة. لا يستدعي أي مختبر نموذجًا لغويًا: «مِضياف» في المختبرات 2.1 إلى 2.3
إجابات مسجلة، ولا تسجيل صوتي في أي مختبر.

## ما يحتاجه المشارك

- جدول بيانات إلكتروني: Excel أو LibreOffice Calc أو Google Sheets.
- قارئ نصوص.
- حساب Google لفتح Colab في مختبرات المحاكاة، أو [uv](https://docs.astral.sh/uv/) على الحاسوب. لا مفتاح ولا اشتراك.
- قواعد الذكاء الاصطناعي: دون مساعد في 1.1 و2.1 و2.2 و2.6 و2.7؛ مساعد بدور المعلّم في مختبرات التنبؤ والمحاكاة والطاقة؛
  مساعد كامل في الخريطة (2.8 والمناقشة الختامية).

## العمل التحضيري

نحو ساعة قبل اليوم الأول: `files/prework/prework_guide.txt` و`files/prework/prework_inventory.xlsx`. حصر لخمس خدمات للزوار
على الأقل في جهة المشارك، يفتحه المدرّب قبل الجلسة الأولى، ويُستخدم في المختبر 1.1. وبعد الورشة مهمة المتابعة المتعقَّبة
(نحو ساعة): تقدير حالتين من الحصر بسلم الخريطة.

## نقطة البداية والحل

كل مختبر يبدأ من ملفات جاهزة. المختبرات التي تكمل مختبرًا قبلها في اليوم نفسه تبدأ من ملف بداية فيه الجزء الأول مكتملًا؛
يجمع المدرّب ملف المشارك من الجزء الأول قبل أن يُفتح ملف البداية، لأنه دليل في سجل المختبرات.

| المختبر | الصفحة | يبدأ من | الحل المرجعي |
|---|---|---|---|
| 1.1 | `D1_1_rank_deployments.html` | `deployments/six_deployments.txt`، `deployments/ranking_sheet.xlsx`، `prework/` | `solutions/answer_key.md` |
| 1.2 | `D1_2_forecast_error.html` | `forecast/arrivals_seasons.xlsx` | `solutions/answer_key.md` |
| 1.3 | `D1_3_peak_error.html` | `forecast/forecast_part2_start.xlsx` | `solutions/answer_key.md` |
| 1.4 | `D1_4_peak_day_hours.html` | `peakday/peak_day_hours.xlsx` | `solutions/answer_key.md` |
| 1.5 | `D1_5_plan_a.html` | `sim/plaza_sim.ipynb` أو `files/sim/results_plan_A.csv` | `solutions/sim_runs.csv` |
| 1.6 | `D1_6_plan_b.html` | `files/sim/comparison_sheet.xlsx`، `files/sim/results_plan_A.csv` | `solutions/sim_runs.csv` |
| 1.7 | `D1_7_stress_test.html` | `files/sim/comparison_complete.xlsx`، `files/sim/results_stress.csv` | `solutions/sim_runs.csv` |
| 1.8 | `D1_8_command_card.html` | `command/safety_plan_excerpt.txt`، `command/command_card_template.txt` | `solutions/answer_key.md` |
| 2.1 | `D2_1_score_ar_en.html` | `assistant/scoring_sheet.xlsx`، `assistant/fact_sheet.txt`، `assistant/handover_rules.txt` | `solutions/key.json` |
| 2.2 | `D2_2_score_ur_id.html` | `assistant/scoring_sheet.xlsx`، `assistant/translator_note.txt` | `solutions/key.json` |
| 2.3 | `D2_3_scores_by_language.html` | `assistant/scored_complete.xlsx`، `assistant/acceptance_rule.txt` | `solutions/answer_key.md` |
| 2.4 | `D2_4_energy_raw.html` | `energy/meter_daily.xlsx`، `energy/naseem_claim.txt` | `solutions/answer_key.md` |
| 2.5 | `D2_5_energy_adjusted.html` | `energy/energy_part2_start.xlsx` | `solutions/answer_key.md` |
| 2.6 | `D2_6_privacy_options.html` | `privacy/options_6.txt`، `privacy/options_sheet.xlsx`، `privacy/safety_need.txt` | `files/privacy/options_complete.xlsx` |
| 2.7 | `D2_7_privacy_record.html` | `privacy/options_complete.xlsx`، `privacy/lost_child_proposal.txt`، `privacy/retention_template.xlsx` | `solutions/answer_key.md` |
| 2.8 | `D2_8_map_kickoff.html` | `map/city_profile.txt`، `map/use_cases_10.txt`، `map/map_template.xlsx` | `solutions/answer_key.md` |

`solutions/answer_key.md` يجمع أرقام المختبرات الستة عشر وفخاخها. ملف `options_complete.xlsx` هو ملف البداية للمختبر 2.7،
فيجمع المدرّب جداول المختبر 2.6 قبل فتحه.

## تشغيل الحلول

```bash
uv run labs/solutions/check.py            # كل المختبرات
uv run labs/solutions/check.py 1.3 2.5    # بعضها
```

ملف واحد يعلن اعتمادياته. يعيد حساب كل رقم في مفتاح الإجابات من الملفات التي يتسلمها المشارك، ويطبع `PASS` لكل مختبر. لا
يكتب شيئًا ولا يتصل بأي نموذج.

## المحاكاة

النموذج في `sim/plaza_sim.py` (JuPedSim 1.4.2، رخصة LGPL-3.0 أو أحدث)، والدفتر `sim/plaza_sim.ipynb` مولَّد منه:

```bash
cd labs/sim
uv run plaza_sim.py --plan B --scenario plus25 --seed 2   # تشغيل واحد، نحو عشر ثوانٍ إلى دقيقة
uv run plaza_sim.py --all --out results                   # كل التشغيلات الأربعة والعشرين، نحو عشرين دقيقة
```

الحد 2.0 شخص/م² ومنطقة القياس 8 × 5 أمتار ونافذة العشر ثوانٍ، والعتبات 1.5 و2.0 و2.5 في بطاقة القيادة، قيم تعليمية لمدينة
افتراضية، وليست معيارًا تشغيليًا لأي فعالية ولا لموسم الحج. الحدود الفعلية تضعها الجهة المختصة في خطة السلامة.

البذور ثابتة: التشغيل نفسه يعطي النتيجة نفسها على الحاسوب نفسه. على نظام آخر قد تختلف القمم في المنزلة الثانية بعد
الفاصلة؛ الأحكام في المختبرات لا تتغير بذلك.

## الملفات

| الملف | ما هو | المزروع فيه |
|---|---|---|
| `deployments/six_deployments.txt` | ست حالات نشر | حالة بلا بيانات شخصية لكن خطأها يمس السلامة («توقّع»)؛ حالة ببيانات حيوية لتحديد الهوية |
| `forecast/arrivals_seasons.xlsx` | ثلاثة مواسم من 60 يومًا، وتنبؤ «توقّع» للموسم 3 | «توقّع» ناعم: أدق على الموسم، ويقصّ قمة الأسبوع الكبير |
| `peakday/peak_day_hours.xlsx` | حصص الساعات ومؤشر الحرارة في يوم الذروة | ساعة الذروة ليست أحر ساعة |
| `sim/` | نتائج المحاكاة للخطتين بأربعة ظروف وثلاث بذور | الخطة أ على الحد في اليوم المعتاد؛ كل اختبار ضغط يكسر الخطتين |
| `assistant/scoring_sheet.xlsx` | 40 سؤالًا بأربع لغات وإجابات «مِضياف» المسجلة | أربع إحالات فاشلة، وأربع معلومات خاطئة، وإجابتان بلغة أخرى، وأكثرها في الأردية. نصوص الأردية والإندونيسية لم يراجعها ناطق باللغة بعد: تُراجع قبل أول دفعة |
| `energy/meter_daily.xlsx` | 18 شهرًا من قراءات العداد اليومية مع الحرارة والزوار | فترة لاحقة أبرد، وزوار أقل، وتبديل إنارة، وتسعة أيام ناقصة |
| `privacy/options_6.txt` | ستة خيارات للكاميرات والحساسات | خياران يلبيان الحاجة دون تعرف؛ خيار ببيانات حيوية يتجاوز الحاجة |
| `map/use_cases_10.txt` | عشر حالات استخدام | ثلاث حالات مخاطرها 3 |

## إعادة توليد الملفات

```bash
uv run labs/_tools/prepare_files.py       # ملفات files/ ومفتاح solutions/key.json، بالبذرة 212
uv run labs/_tools/make_notebook.py       # الدفتر من plaza_sim.py
uv run labs/sim/plaza_sim.py --all --out <مجلد مؤقت>
uv run labs/_tools/sim_files.py <المجلد المؤقت نفسه>
uv run labs/_tools/demo_runs.py           # أرقام المثال الموازي في شرائح الجلسات 5 إلى 7
```

المحتوى نفسه في كل مرة؛ يتغير وقت الحفظ داخل ملفات xlsx فقط.
