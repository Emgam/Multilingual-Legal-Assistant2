# =============================================================
# scripts/tunbert_qa/prepare_dataset.py
# Converts your rag_dataset.json into SQuAD format for TunBERT QA fine-tuning
# =============================================================
import json
import uuid

INPUT_PATH  = r"C:\Users\pc\Documents\dataset\datasets\rag_dataset_darija.json"
OUTPUT_TRAIN = r"C:\Users\pc\Documents\dataset\datasets\tunbert_train.json"
OUTPUT_VALID = r"C:\Users\pc\Documents\dataset\datasets\tunbert_valid.json"


def find_answer_start(context: str, answer: str) -> int:
    """Find character position of answer in context."""
    idx = context.find(answer)
    return idx


def build_squad_entry(doc_id, title, context, question, answer):
    """Build one SQuAD-format QA entry."""
    start = find_answer_start(context, answer)
    if start == -1:
        return None  # skip if answer not found in context

    return {
        "id":      str(uuid.uuid4()),
        "title":   title,
        "context": context,
        "question": question,
        "answers": {
            "text":          [answer],
            "answer_start":  [start]
        }
    }


def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    squad_data = []

    for doc in data:
        simplified = doc.get("simplified_text") or {}
        darija_text = simplified.get("darija", "")
        fr_text     = simplified.get("fr", "")
        en_text     = simplified.get("en", "")

        title_obj = doc.get("title") or {}
        title_darija = title_obj.get("darija") or title_obj.get("fr") or ""
        category = doc.get("procedure_category", "")

        # -------------------------------------------------------
        # Generate QA pairs per section (darija context preferred)
        # -------------------------------------------------------
        sections = doc.get("sections") or []
        for section in sections:
            content = section.get("content") or {}
            darija_content = content.get("darija") or content.get("fr") or ""
            if not darija_content:
                continue

            # Use the simplified_text as context (richer)
            context = darija_text if darija_text else fr_text
            if not context:
                continue

            # Auto-generate questions from section content
            # (In production, replace these with human-annotated questions)
            section_title = (section.get("title") or {}).get("darija") or \
                            (section.get("title") or {}).get("fr") or ""

            # Simple heuristic: use section content as the answer
            answer = darija_content[:200].strip()
            if len(answer) < 10:
                continue

            # Generate a question based on category
            if "startup" in category.lower() or "création" in category.lower():
                question = f"كيفاش نعمل {title_darija}؟"
            elif "cnss" in category.lower():
                question = f"شنية الخطوات باش نسجل في الكناس؟"
            elif "registration" in category.lower():
                question = f"شنية الوثائق المطلوبة باش نسجل؟"
            else:
                question = f"كيفاش نكمل {section_title}؟"

            entry = build_squad_entry(
                doc_id=doc.get("document_id"),
                title=title_darija,
                context=context,
                question=question,
                answer=answer,
            )
            if entry:
                squad_data.append(entry)

    # Split 80/20 train/valid
    split = int(len(squad_data) * 0.8)
    train_data = squad_data[:split]
    valid_data = squad_data[split:]

    # Save in HuggingFace datasets format
    with open(OUTPUT_TRAIN, "w", encoding="utf-8") as f:
        json.dump(train_data, f, ensure_ascii=False, indent=2)

    with open(OUTPUT_VALID, "w", encoding="utf-8") as f:
        json.dump(valid_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Created {len(train_data)} train + {len(valid_data)} valid QA pairs")
    print(f"   Saved to:\n   {OUTPUT_TRAIN}\n   {OUTPUT_VALID}")


if __name__ == "__main__":
    main()