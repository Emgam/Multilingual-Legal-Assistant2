# scripts/run_evaluation.py
import json
import requests
import statistics

API_URL = "http://localhost:8000/ask/evaluate"

TEST_CASES = [
    {
        "question":  "كيفاش نعمل شركة في تونس خطوة بخطوة؟",
        "lang":      "darija",
        "reference": "باش تعمل شركة لازم تكتب العقد التأسيسي وتفتح حساب بنكي وتسجل في RNE وتصرح في الكناس",
    },
    {
        "question":  "قداش عندي وقت باش نسجل les statuts في القباضة المالية؟",
        "lang":      "darija",
        "reference": "لازم تسجل العقد في قباضة المالية في ظرف 60 يوم",
    },
    {
        "question":  "وقتاش لازم نصرّح بالشركة في CNSS؟",
        "lang":      "darija",
        "reference": "لازم تصرح في الكناس بعد ما تعمل الشركة باش تاخد التغطية الاجتماعية",
    },
    {
        "question":  "شنية الوثائق المطلوبة باش نسجل SARL؟",
        "lang":      "darija",
        "reference": "لازم تجيب بطاقة التعريف وشهادة حجز الاسم والعقد التأسيسي وعقد الكراء",
    },
    {
        "question":  "Comment créer une entreprise en Tunisie?",
        "lang":      "fr",
        "reference": "Pour créer une entreprise il faut rédiger les statuts, ouvrir un compte bancaire, s'immatriculer au RNE et déclarer à la CNSS.",
    },
    {
        "question":  "How to register a startup in Tunisia?",
        "lang":      "en",
        "reference": "To register a startup you need to draft statutes, open a bank account, register at the RNE, and declare to CNSS.",
    },
    {
        "question":  "What documents are needed for SARL registration?",
        "lang":      "en",
        "reference": "You need ID copies, company name reservation certificate, signed statutes, and rental contract.",
    },
    {
        "question":  "كيفاش نسجل في RNE؟",
        "lang":      "darija",
        "reference": "لازم تعبي استمارة التسجيل في RNE وتجيب الوثائق المطلوبة وتخلص معاليم التسجيل تقريباً 50 دينار",
    },
]


def evaluate_one(test_case: dict) -> dict:
    payload = {
        "question":  test_case["question"],
        "lang":      test_case["lang"],
        "evaluate":  True,
        "reference": test_case.get("reference"),
    }

    try:
        resp = requests.post(API_URL, json=payload, timeout=180)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.Timeout:
        return {"error": "timeout", "question": test_case["question"]}
    except Exception as e:
        return {"error": str(e), "question": test_case["question"]}

    ev = data.get("evaluation", {})

    # faithfulness is float, language_check has "correct" key
    faithfulness = ev.get("faithfulness", 0)
    if isinstance(faithfulness, dict):
        faithfulness = faithfulness.get("faithfulness", 0)

    lang_check = ev.get("language_check", {})
    language_ok = lang_check.get("correct", lang_check.get("correct_language", False))

    rouge_ctx = ev.get("rouge_vs_context", {})
    rouge_ref = ev.get("rouge_vs_reference", {})
    bleu_ref  = ev.get("bleu_vs_reference", {})

    return {
        "question":         test_case["question"],
        "lang":             test_case["lang"],
        "answer":           data.get("answer", ""),
        "grounded":         data.get("grounded", False),
        "is_fallback":      "موش موجودة" in data.get("answer", "") or
                            "not available" in data.get("answer", "").lower() or
                            "n'est pas disponible" in data.get("answer", "").lower(),
        "overall_score":    ev.get("overall_score", 0),
        "grade":            ev.get("grade", "N/A"),
        "faithfulness":     round(float(faithfulness), 4),
        "language_ok":      bool(language_ok),
        "arabic_ratio":     lang_check.get("arabic_ratio", 0),
        "french_leak":      lang_check.get("french_leak", 0),
        "rouge1_context":   rouge_ctx.get("rouge1_f", 0),
        "rouge2_context":   rouge_ctx.get("rouge2_f", 0),
        "rouge1_reference": rouge_ref.get("rouge1_f", 0) if test_case.get("reference") else None,
        "rouge2_reference": rouge_ref.get("rouge2_f", 0) if test_case.get("reference") else None,
        "bleu1_reference":  bleu_ref.get("bleu1", 0)    if test_case.get("reference") else None,
        "bleu4_reference":  bleu_ref.get("bleu4", 0)    if test_case.get("reference") else None,
        "word_count":       ev.get("word_count", len(data.get("answer","").split())),
    }


def print_report(results: list):
    print("\n" + "="*80)
    print("RAG EVALUATION REPORT")
    print("="*80)

    valid  = [r for r in results if "error" not in r]
    errors = [r for r in results if "error" in r]

    for i, r in enumerate(valid, 1):
        grade_icon = "🟢" if r["overall_score"] >= 0.70 else ("🟡" if r["overall_score"] >= 0.45 else "🔴")
        lang_icon  = "✅" if r["language_ok"] else "❌ WRONG LANG"
        fall_tag   = " ⚠️ FALLBACK" if r["is_fallback"] else ""

        print(f"\n[{i}] {r['question'][:65]}")
        print(f"     {grade_icon} Score={r['overall_score']:.3f} | {lang_icon}{fall_tag} | Words={r['word_count']}")
        print(f"     Answer: {r['answer'][:90]}{'...' if len(r['answer'])>90 else ''}")
        print(f"     Faith={r['faithfulness']:.3f} | ROUGE1-ctx={r['rouge1_context']:.3f} | ROUGE2-ctx={r['rouge2_context']:.3f}")
        if r["rouge1_reference"] is not None:
            print(f"     ROUGE1-ref={r['rouge1_reference']:.3f} | ROUGE2-ref={r['rouge2_reference']:.3f} | BLEU1={r['bleu1_reference']:.3f} | BLEU4={r['bleu4_reference']:.4f}")

    if valid:
        scores    = [r["overall_score"] for r in valid]
        fallbacks = sum(1 for r in valid if r["is_fallback"])
        lang_ok   = sum(1 for r in valid if r["language_ok"])
        grounded  = sum(1 for r in valid if r["grounded"])
        avg_faith = statistics.mean(r["faithfulness"] for r in valid)
        avg_r1ctx = statistics.mean(r["rouge1_context"] for r in valid)

        ref_results = [r for r in valid if r["rouge1_reference"] is not None]
        avg_r1ref = statistics.mean(r["rouge1_reference"] for r in ref_results) if ref_results else 0
        avg_bleu4 = statistics.mean(r["bleu4_reference"] for r in ref_results) if ref_results else 0

        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        print(f"  Questions tested:      {len(results)}")
        print(f"  Errors/timeouts:       {len(errors)}")
        print(f"  Avg overall score:     {statistics.mean(scores):.3f}")
        print(f"  Median score:          {statistics.median(scores):.3f}")
        print(f"  Best / Worst:          {max(scores):.3f} / {min(scores):.3f}")
        print(f"  Answered (no fallback):{len(valid)-fallbacks}/{len(valid)} "
              f"({(len(valid)-fallbacks)/len(valid)*100:.0f}%)")
        print(f"  Correct language:      {lang_ok}/{len(valid)} "
              f"({lang_ok/len(valid)*100:.0f}%)")
        print(f"  Grounded:              {grounded}/{len(valid)}")
        print(f"  Avg faithfulness:      {avg_faith:.3f}")
        print(f"  Avg ROUGE-1 (context): {avg_r1ctx:.3f}")
        if ref_results:
            print(f"  Avg ROUGE-1 (ref):     {avg_r1ref:.3f}")
            print(f"  Avg BLEU-4 (ref):      {avg_bleu4:.4f}")

        print("\n  Per-language breakdown:")
        for lang in ["darija", "fr", "en", "ar"]:
            subset = [r for r in valid if r["lang"] == lang]
            if subset:
                avg   = statistics.mean(r["overall_score"] for r in subset)
                falls = sum(1 for r in subset if r["is_fallback"])
                lok   = sum(1 for r in subset if r["language_ok"])
                print(f"    [{lang:8s}] score={avg:.3f} | fallbacks={falls}/{len(subset)} | lang_ok={lok}/{len(subset)}")

    if errors:
        print(f"\n  Errors:")
        for e in errors:
            print(f"    - {e['question'][:55]}: {e['error']}")

    print("\n" + "="*80)

    with open("evaluation_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("✅ Full results saved to evaluation_results.json\n")


if __name__ == "__main__":
    print(f"🔍 Running evaluation — {len(TEST_CASES)} questions")
    print(f"   API: {API_URL}\n")

    results = []
    for i, tc in enumerate(TEST_CASES, 1):
        print(f"[{i}/{len(TEST_CASES)}] {tc['question'][:60]}...")
        result = evaluate_one(tc)
        results.append(result)
        if "error" not in result:
            print(f"         {result['grade']} score={result['overall_score']:.3f} | "
                  f"faith={result['faithfulness']:.3f} | "
                  f"{'FALLBACK' if result['is_fallback'] else 'answered'}")
        else:
            print(f"         ❌ {result['error']}")

    print_report(results)