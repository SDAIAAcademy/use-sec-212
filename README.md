<!-- academy:title -->
# الذكاء الاصطناعي في المدن والسياحة والحج

AI in Cities, Tourism and Pilgrimage

مسار الطلاقة في البيانات والذكاء الاصطناعي · أكاديمية سدايا · USE-SEC-212 · المستوى 200

تحكم على التنبؤ في أيام الذروة، وتحاكي خطة البوابات قبل يوم الحشد، وتختبر مساعد الزوار بأربع لغات، وتتحقق من ادعاء توفير الطاقة، وتختار أقل خيارات الكاميرات تدخلًا، ثم تدافع عن خريطة الفرص والمخاطر

يختبر مديرو المدن والمنشآت والسياحة وخدمات الحج التنبؤ ومحاكاة الحشود والمساعدة متعددة اللغات وادعاءات توفير الطاقة على بيانات اصطناعية وعامة، ويوازنون بين خيارات الكاميرات والقياسات الحيوية وقواعد الخصوصية، ويبنون خريطة الفرص والمخاطر لمدينة مضيفة افتراضية.

**الصيغة:** ورشة عمل: يومان يضمان ثماني جلسات مع مختبرات، وعمل تحضيري متعقَّب، وخريطة تُناقَش

**صفحة المقرر:** https://sdaiaacademy.github.io/use-sec-212/
<!-- /academy:title -->

## نواتج التعلم

| | نواتج التعلم | المستوى | الدليل |
|---|---|---|---|
| LO1 | يشرح أي استخدامات الذكاء الاصطناعي في المدن وخدمة الزوار تنطوي على أعلى المخاطر في السلامة والخصوصية، استنادًا إلى ستة أوصاف لحالات نشر | Awareness | جدول مرتب يسمي البيانات والأشخاص المتأثرين |
| LO2 | يقارن بين تنبؤ بأعداد الوافدين وخط أساس موسمي ويبيّن الخطأ في فترات الذروة التي يُبنى عليها توزيع الموظفين، على بيانات اصطناعية لأعداد الوافدين خلال ثلاثة مواسم | Applied | جدول لأخطاء الذروة وهامش احتياطي للتوظيف |
| LO3 | يستخدم محاكاة لحركة المشاة لاختبار ما إذا كانت خطة البوابات تُبقي الكثافة دون حد معين، باستخدام نموذج مقدَّم لساحة عامة وخطتين | Applied | كثافات الذروة وخطة مختارة |
| LO4 | يختبر مساعدًا متعدد اللغات للزوار للكشف عن الإجابات الخاطئة وحالات إخفاق الإحالة إلى الموظفين، على 40 سؤالًا وجوابًا معدة مسبقًا بأربع لغات | Applied | ورقة تقدير للدرجات بحسب اللغة |
| LO5 | يبني خريطة الفرص والمخاطر ترتب حالات الاستخدام مع ضوابط لبيانات الكاميرات والموقع والقياسات الحيوية، استنادًا إلى ملف تعريفي لمدينة مضيفة افتراضية | Performance | خريطة من صفحة واحدة تُناقَش في خمس دقائق |

<!-- academy:units -->
## الوحدات

| الوحدة | العنوان | الجلسات | الشرائح |
|---|---|---|---|
| اليوم 1 | التنبؤ والنقل والحشد: احكم في الذروة وحاكِ قبل يوم الحشد | أين تكون المخاطر أعلى; التنبؤ مقابل خط أساس; الحكم على التنبؤ في الذروة; النقل والإجهاد الحراري في يوم الذروة; كيف تعمل محاكاة حركة المشاة; مقارنة خطتين للبوابات; اختبار الخطة تحت الضغط; إنسان يقود ويملك قرار الإيقاف | [`slides/day1.html`](slides/day1.html) |
| اليوم 2 | المساعد والطاقة والخصوصية والخريطة | اختبر المساعد قبل أن يختبره الزوار; لغات لا تقرؤها; ورقة التقدير بحسب اللغة; ادعاءات توفير الطاقة; عدّل قبل أن تصدّق; العدّ ليس تعرّفًا; الحفظ والتقليل وقواعد التعرف الحيوي; خريطة الفرص والمخاطر | [`slides/day2.html`](slides/day2.html) |
| المناقشة الختامية | خريطة الرفادة: الفرص والمخاطر |  | [`slides/capstone.html`](slides/capstone.html) |
<!-- /academy:units -->

## دراسة الحالة

**هيئة الرِّفادة للمدينة المضيفة**، جهة افتراضية تدير استقبال الزوار والمعتمرين في مدينة الرفادة الافتراضية، وتدرس تنبؤ «توقّع» بالوافدين، ومساعد الزوار «مِضياف»، ونظام «نسيم» للتكييف، وخيارات الكاميرات في ساحة المشرع. كل الملفات اصطناعية ومولّدة ببذرة ثابتة (`labs/_tools/`)، ولا جهة حقيقية ولا شخص حقيقي فيها، وللمدرّب مفتاح إجابة في `labs/solutions/`.

<!-- academy:labs -->
## المختبرات

كل مختبر صفحة في `labs/` تُفتح من صفحة المقرر ومن شريحة المختبر في جلسته.

| | الجلسة | المختبر | الملف |
|---|---|---|---|
| 1.1 | اليوم 1 · الجلسة 1 | ترتيب ستة استخدامات | [`D1_1_rank_deployments.html`](labs/D1_1_rank_deployments.html) |
| 1.2 | اليوم 1 · الجلسة 2 | فحص التنبؤ: الجزء الأول | [`D1_2_forecast_error.html`](labs/D1_2_forecast_error.html) |
| 1.3 | اليوم 1 · الجلسة 3 | فحص التنبؤ: الجزء الثاني | [`D1_3_peak_error.html`](labs/D1_3_peak_error.html) |
| 1.4 | اليوم 1 · الجلسة 4 | يوم الذروة بالساعات | [`D1_4_peak_day_hours.html`](labs/D1_4_peak_day_hours.html) |
| 1.5 | اليوم 1 · الجلسة 5 | المحاكاة: الخطة أ | [`D1_5_plan_a.html`](labs/D1_5_plan_a.html) |
| 1.6 | اليوم 1 · الجلسة 6 | المحاكاة: الخطة ب | [`D1_6_plan_b.html`](labs/D1_6_plan_b.html) |
| 1.7 | اليوم 1 · الجلسة 7 | المحاكاة: اختبار الضغط | [`D1_7_stress_test.html`](labs/D1_7_stress_test.html) |
| 1.8 | اليوم 1 · الجلسة 8 | بطاقة القيادة والإيقاف | [`D1_8_command_card.html`](labs/D1_8_command_card.html) |
| 2.1 | اليوم 2 · الجلسة 1 | تقدير الإجابات: العربية والإنجليزية | [`D2_1_score_ar_en.html`](labs/D2_1_score_ar_en.html) |
| 2.2 | اليوم 2 · الجلسة 2 | تقدير الإجابات: الأردية والإندونيسية | [`D2_2_score_ur_id.html`](labs/D2_2_score_ur_id.html) |
| 2.3 | اليوم 2 · الجلسة 3 | ورقة التقدير وقرار التشغيل | [`D2_3_scores_by_language.html`](labs/D2_3_scores_by_language.html) |
| 2.4 | اليوم 2 · الجلسة 4 | الطاقة: المقارنة الخام | [`D2_4_energy_raw.html`](labs/D2_4_energy_raw.html) |
| 2.5 | اليوم 2 · الجلسة 5 | الطاقة: التوفير المعدّل | [`D2_5_energy_adjusted.html`](labs/D2_5_energy_adjusted.html) |
| 2.6 | اليوم 2 · الجلسة 6 | مراجعة الخصوصية: الخيارات | [`D2_6_privacy_options.html`](labs/D2_6_privacy_options.html) |
| 2.7 | اليوم 2 · الجلسة 7 | مراجعة الخصوصية: السجل | [`D2_7_privacy_record.html`](labs/D2_7_privacy_record.html) |
| 2.8 | اليوم 2 · الجلسة 8 | بداية الخريطة | [`D2_8_map_kickoff.html`](labs/D2_8_map_kickoff.html) |
<!-- /academy:labs -->

## المشروع الختامي

الخريطة، وتُناقَش مباشرة؛ ثم مهمة متابعة متعقَّبة يقيّم فيها المشارك حالتي استخدام من عمله

**التسليم:** عمل فردي يُسلَّم رابطًا لمجلد مشترك في Google Drive، فيه الخريطة من صفحة واحدة وسجلات المختبرات، ثم دفاع مباشر: خمس دقائق للعرض وثلاث للأسئلة. وبعد الورشة يُضاف إلى المجلد نفسه تقدير لحالتي استخدام من عمل المشارك.

## المتطلبات السابقة

- USE-FLU-201 العمل مع المساعدات الذكية: التفويض والوصف والحكم وتحمل المسؤولية
- يعرف كيف تخطط المدينة أو المنشأة أو خدمة الحج لاستقبال الزوار؛ ويستخدم جداول البيانات

<!-- academy:tools -->
## الأدوات

كل سطر قدرة، والأمثلة قابلة للتبديل.

- **محاكاة حركة المشاة:** JuPedSim, Vadere
- **المساعد قيد الاختبار:** نموذج مفتوح الأوزان يعمل عبر Open WebUI, مساعد مؤسسي معتمد
- **بيانات طاقة المباني:** Building Data Genome Project 2, عينة مجهولة الهوية من عدادات مرفق خدمي
- **جدول بيانات:** LibreOffice Calc, Microsoft Excel, Google Sheets
<!-- /academy:tools -->

<!-- academy:sources -->
## المصادر

### المراجع الوطنية

- [سدايا: نظام حماية البيانات الشخصية](https://sdaia.gov.sa/ar/SDAIA/about/Documents/PersonalDataProtectionLawAr.pdf)
- [SDAIA: Personal Data Protection Law (English)](https://sdaia.gov.sa/en/SDAIA/about/Documents/PersonalDataProtectionLaw.pdf)
- [SDAIA: Implementing Regulation of the Personal Data Protection Law](https://sdaia.gov.sa/en/SDAIA/about/Documents/ImplementingRegulationPersonalDataProtectionLaw.pdf)
- [مكتب إدارة البيانات الوطنية: سياسة مشاركة البيانات](https://sdaia.gov.sa/ar/SDAIA/about/Documents/DataSharingPolicyAR.pdf)
- [سدايا: مبادئ أخلاقيات الذكاء الاصطناعي](https://sdaia.gov.sa/ar/SDAIA/about/Documents/ai-principles.pdf)
- [SDAIA: AI Ethics Principles (English)](https://sdaia.gov.sa/en/SDAIA/about/Documents/ai-principles.pdf)
- [سدايا: الإطار الوطني لإدارة مخاطر الذكاء الاصطناعي (أبريل 2026)](https://sdaia.gov.sa/ar/MediaCenter/KnowledgeCenter/ResearchLibrary/ExecutiveSummaryAr.pdf)
- [SDAIA: National AI Risk Management Framework, executive summary (April 2026)](https://sdaia.gov.sa/en/MediaCenter/KnowledgeCenter/ResearchLibrary/ExecutiveSummaryEn.pdf)

### الحشود والمحاكاة

- [Helbing, Johansson, Al-Abideen: Dynamics of crowd disasters, an empirical study (arXiv physics/0701203)](https://arxiv.org/abs/physics/0701203)
- [JuPedSim: documentation](https://www.jupedsim.org/stable/)
- [JuPedSim on PyPI (version and licence)](https://pypi.org/project/jupedsim/)
- [Vadere: source repository](https://gitlab.lrz.de/vadere/vadere)

### التنبؤ والطاقة

- [Hyndman and Athanasopoulos: Forecasting, Principles and Practice (3rd ed.), Some simple forecasting methods](https://otexts.com/fpp3/simple-methods.html)
- [Building Data Genome Project 2 (BDG2): open meter data set](https://github.com/buds-lab/building-data-genome-project-2)

### قواعد التعرف بالقياسات الحيوية

- [Regulation (EU) 2024/1689 (Artificial Intelligence Act), EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)

### الأدوات

- [Open WebUI: documentation](https://docs.openwebui.com/)
<!-- /academy:sources -->

### المرجعيات الوطنية

- نظام حماية البيانات الشخصية ولوائحه التنفيذية: <https://sdaia.gov.sa/ar/SDAIA/about/Documents/PersonalDataProtectionLawAr.pdf> واللائحة التنفيذية: <https://sdaia.gov.sa/en/SDAIA/about/Documents/ImplementingRegulationPersonalDataProtectionLaw.pdf>
- سياسة مشاركة البيانات الصادرة عن مكتب إدارة البيانات الوطنية: <https://sdaia.gov.sa/ar/SDAIA/about/Documents/DataSharingPolicyAR.pdf>
- مبادئ أخلاقيات الذكاء الاصطناعي الصادرة عن سدايا: <https://sdaia.gov.sa/ar/SDAIA/about/Documents/ai-principles.pdf>
- الإطار الوطني لإدارة مخاطر الذكاء الاصطناعي (الملخص التنفيذي، أبريل 2026): <https://sdaia.gov.sa/ar/MediaCenter/KnowledgeCenter/ResearchLibrary/ExecutiveSummaryAr.pdf>
