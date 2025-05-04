import os
from datasets import load_dataset, Audio
from transformers import (
    WhisperForConditionalGeneration,
    WhisperProcessor,
    WhisperTokenizer,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments
)
import torch
import numpy as np

# === CONFIGURATION ===
MODEL_NAME = "openai/whisper-small"  # Or "openai/whisper-tiny"
DATA_PATH = r"C:\Users\Vedant Finavia\Desktop\data\metadata.jsonl.txt"  # Dataset file path
OUTPUT_DIR = r"C:\Users\Vedant Finavia\Desktop\FineTunedWhisper"  # Output directory for model & tokenizer

# === LOAD DATASET ===
dataset = load_dataset("json", data_files={"train": DATA_PATH})
dataset = dataset.cast_column("audio_filepath", Audio(sampling_rate=16000))

# === LOAD MODEL, PROCESSOR, TOKENIZER ===
processor = WhisperProcessor.from_pretrained(MODEL_NAME)
model = WhisperForConditionalGeneration.from_pretrained(MODEL_NAME)
tokenizer = WhisperTokenizer.from_pretrained(MODEL_NAME)

# === PREPROCESS FUNCTION ===
def preprocess(example):
    # Load audio file and extract features using the processor
    audio = example["audio_filepath"]
    # Extract input features from the audio (returns a list; take the first element)
    input_features = processor(audio["array"], sampling_rate=16000).input_features[0]
    # Tokenize the text labels using the tokenizer
    labels = tokenizer(example["text"]).input_ids
    return {
        "input_features": input_features,
        "labels": labels,
    }

# Preprocess the dataset and remove original columns
dataset = dataset["train"].map(preprocess, remove_columns=dataset["train"].column_names)

# === CUSTOM DATA COLLATOR ===
class DataCollatorWhisper:
    def __init__(self, label_pad_token_id=-100, input_feature_pad_value=0.0):
        self.label_pad_token_id = label_pad_token_id
        self.input_feature_pad_value = input_feature_pad_value

    def __call__(self, features):
        # Each feature is a dict with keys "input_features" and "labels"
        # Pad input_features (assumed to be 1D arrays) to max length
        input_features = [torch.tensor(f["input_features"], dtype=torch.float) for f in features]
        max_input_len = max(x.shape[0] for x in input_features)
        padded_input_features = []
        for x in input_features:
            pad_len = max_input_len - x.shape[0]
            padded = torch.nn.functional.pad(x, (0, pad_len), value=self.input_feature_pad_value)
            padded_input_features.append(padded)
        padded_input_features = torch.stack(padded_input_features)

        # Pad labels (assumed to be 1D arrays of ints) to max length
        labels = [torch.tensor(f["labels"], dtype=torch.long) for f in features]
        max_label_len = max(x.shape[0] for x in labels)
        padded_labels = []
        for x in labels:
            pad_len = max_label_len - x.shape[0]
            padded = torch.nn.functional.pad(x, (0, pad_len), value=self.label_pad_token_id)
            padded_labels.append(padded)
        padded_labels = torch.stack(padded_labels)

        return {
            "input_features": padded_input_features,
            "labels": padded_labels,
        }

data_collator = DataCollatorWhisper()

# === TRAINING ARGUMENTS ===
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

training_args = Seq2SeqTrainingArguments(
    output_dir=OUTPUT_DIR,
    per_device_train_batch_size=4,
    num_train_epochs=10,
    logging_steps=10,
    save_steps=500,
    fp16=True if torch.cuda.is_available() else False,
    fp16_full_eval=True if torch.cuda.is_available() else False,
    predict_with_generate=True,
    push_to_hub=False,
)

# === TRAINER ===
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    # Use the tokenizer only for its configuration (if needed)
    tokenizer=tokenizer,
    data_collator=data_collator,
)

# === TRAIN THE MODEL ===
trainer.train()

# === SAVE MODEL AND TOKENIZER/PROCESSOR ===
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
processor.save_pretrained(OUTPUT_DIR)

print("Fine-tuning complete. Model, tokenizer, and processor saved to", OUTPUT_DIR)
