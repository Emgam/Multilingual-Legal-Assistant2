# =============================================================
# scripts/tunbert_qa/finetune_tunbert_qa.py
# Fine-tunes TunBERT on your Tunisian QA dataset using HuggingFace Transformers
# =============================================================
# Install first:
#   pip install transformers datasets torch accelerate
# =============================================================

import json
import torch
from pathlib import Path
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForQuestionAnswering,
    TrainingArguments,
    Trainer,
    DefaultDataCollator,
)

# =============================
# CONFIG
# =============================
# TunBERT is hosted on HuggingFace as "instadeepai/tunbert"
# We use it via the HuggingFace transformers API directly
MODEL_NAME   = "CAMeL-Lab/bert-base-arabic-camelbert-da"  # best Arabic dialect BERT available on HF
# NOTE: TunBERT's original weights are on GCS (not HuggingFace).
# CAMeL-Lab's dialect BERT is the closest available on HuggingFace and
# works excellently for Tunisian Darija. See explanation below.

TRAIN_PATH = r"C:\Users\pc\Documents\dataset\datasets\tunbert_train.json"
VALID_PATH = r"C:\Users\pc\Documents\dataset\datasets\tunbert_valid.json"
OUTPUT_DIR = r"C:\Users\pc\Documents\dataset\models\tunbert-qa-finetuned"

MAX_LENGTH    = 384
DOC_STRIDE    = 128
BATCH_SIZE    = 8
EPOCHS        = 3
LEARNING_RATE = 2e-5


# =============================
# LOAD DATA
# =============================
def load_squad_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# =============================
# TOKENIZE FOR QA
# =============================
def preprocess_function(examples, tokenizer):
    questions = [q.strip() for q in examples["question"]]
    inputs = tokenizer(
        questions,
        examples["context"],
        max_length=MAX_LENGTH,
        truncation="only_second",
        stride=DOC_STRIDE,
        return_overflowing_tokens=True,
        return_offsets_mapping=True,
        padding="max_length",
    )

    offset_mapping   = inputs.pop("offset_mapping")
    sample_map       = inputs.pop("overflow_to_sample_mapping")
    answers          = examples["answers"]
    start_positions  = []
    end_positions    = []

    for i, offset in enumerate(offset_mapping):
        sample_idx    = sample_map[i]
        answer        = answers[sample_idx]
        start_char    = answer["answer_start"][0]
        end_char      = start_char + len(answer["text"][0])
        sequence_ids  = inputs.sequence_ids(i)

        # Find start and end of context tokens
        idx = 0
        while sequence_ids[idx] != 1:
            idx += 1
        context_start = idx
        while idx < len(sequence_ids) and sequence_ids[idx] == 1:
            idx += 1
        context_end = idx - 1

        # If answer is out of span, label (0, 0)
        if offset[context_start][0] > end_char or offset[context_end][1] < start_char:
            start_positions.append(0)
            end_positions.append(0)
        else:
            idx = context_start
            while idx <= context_end and offset[idx][0] <= start_char:
                idx += 1
            start_positions.append(idx - 1)

            idx = context_end
            while idx >= context_start and offset[idx][1] >= end_char:
                idx -= 1
            end_positions.append(idx + 1)

    inputs["start_positions"] = start_positions
    inputs["end_positions"]   = end_positions
    return inputs


# =============================
# MAIN
# =============================
def main():
    print(f"🔄 Loading tokenizer and model: {MODEL_NAME}")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model     = AutoModelForQuestionAnswering.from_pretrained(MODEL_NAME)

    print("📂 Loading datasets...")
    train_raw = load_squad_json(TRAIN_PATH)
    valid_raw = load_squad_json(VALID_PATH)

    train_dataset = Dataset.from_list(train_raw)
    valid_dataset = Dataset.from_list(valid_raw)

    print(f"   Train: {len(train_dataset)} | Valid: {len(valid_dataset)}")

    print("🔨 Tokenizing...")
    tokenized_train = train_dataset.map(
        lambda x: preprocess_function(x, tokenizer),
        batched=True,
        remove_columns=train_dataset.column_names,
    )
    tokenized_valid = valid_dataset.map(
        lambda x: preprocess_function(x, tokenizer),
        batched=True,
        remove_columns=valid_dataset.column_names,
    )

    training_args = TrainingArguments(
        output_dir                  = OUTPUT_DIR,
        num_train_epochs            = EPOCHS,
        per_device_train_batch_size = BATCH_SIZE,
        per_device_eval_batch_size  = BATCH_SIZE,
        learning_rate               = LEARNING_RATE,
        weight_decay                = 0.01,
        evaluation_strategy         = "epoch",
        save_strategy               = "epoch",
        load_best_model_at_end      = True,
        logging_dir                 = f"{OUTPUT_DIR}/logs",
        logging_steps               = 10,
        fp16                        = torch.cuda.is_available(),  # use GPU fp16 if available
        report_to                   = "none",
    )

    trainer = Trainer(
        model           = model,
        args            = training_args,
        train_dataset   = tokenized_train,
        eval_dataset    = tokenized_valid,
        tokenizer       = tokenizer,
        data_collator   = DefaultDataCollator(),
    )

    print("🚀 Starting fine-tuning...")
    trainer.train()

    print(f"✅ Fine-tuning complete! Model saved to: {OUTPUT_DIR}")
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)


if __name__ == "__main__":
    main()