import tkinter as tk
from tkinter import font as tkfont
from threading import Thread
import sounddevice as sd
import numpy as np
import queue
import torch
from transformers import (
    WhisperFeatureExtractor,
    WhisperTokenizer,
    WhisperProcessor,
    WhisperForConditionalGeneration
)
from PIL import Image, ImageTk

# === LOAD WHISPER MODEL ===
MODEL_DIR = "C:/Users/Vedant Finavia/Desktop/FineTunedWhisper"
BASE_MODEL = "openai/whisper-small"
SAMPLE_RATE = 16000

feature_extractor = WhisperFeatureExtractor.from_pretrained(BASE_MODEL)
tokenizer = WhisperTokenizer.from_pretrained(MODEL_DIR)
processor = WhisperProcessor(feature_extractor=feature_extractor, tokenizer=tokenizer)
model = WhisperForConditionalGeneration.from_pretrained(MODEL_DIR)
model.eval()

# === AUDIO RECORDING SETUP ===
audio_queue = queue.Queue()
is_recording = False
recorded_audio = []
full_transcription = []

def audio_callback(indata, frames, time, status):
    if is_recording:
        audio_queue.put(indata.copy())

def start_recording():
    global is_recording, recorded_audio
    is_recording = True
    recorded_audio = []
    stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=SAMPLE_RATE)
    stream.start()
    while is_recording:
        if not audio_queue.empty():
            recorded_audio.append(audio_queue.get())
    stream.stop()
    audio_data = np.concatenate(recorded_audio, axis=0).flatten()
    transcription = transcribe(audio_data)
    full_transcription.append(transcription)
    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, " ".join(full_transcription))

def toggle_recording():
    global is_recording
    if not is_recording:
        mic_button.config(bg="#FF6F61")
        Thread(target=start_recording, daemon=True).start()
    else:
        is_recording = False
        mic_button.config(bg="white")

def transcribe(audio_array):
    inputs = processor(audio_array, sampling_rate=SAMPLE_RATE, return_tensors="pt", language="con", padding=True, truncation=True)
    input_features = inputs["input_features"]
    if input_features.shape[-1] < 3000:
        input_features = torch.nn.functional.pad(input_features, (0, 3000 - input_features.shape[-1]))
    attention_mask = torch.ones(input_features.shape, dtype=torch.long)
    with torch.no_grad():
        generated_ids = model.generate(input_features, attention_mask=attention_mask,
                                       max_length=128, num_beams=5, no_repeat_ngram_size=2, early_stopping=True)
        transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return transcription.strip()

# === GUI SETUP ===
root = tk.Tk()
root.title("A'mas'kan Translator")
root.attributes('-fullscreen', True)
root.configure(bg="#9b59b6")  # Purple background

# === HEADER ===
title_font = tkfont.Font(family="Comic Sans MS", size=36, weight="bold")
title = tk.Label(root, text="A’mas’kan to English Translator!", font=title_font, bg="#9b59b6", fg="white")
title.pack(pady=40)

# === MAIN FRAME ===
main_frame = tk.Frame(root, bg="#9b59b6")
main_frame.pack(fill=tk.BOTH, expand=True, padx=80, pady=20)

# === LEFT SIDE ===
left_frame = tk.Frame(main_frame, bg="#9b59b6")
left_frame.pack(side=tk.LEFT, expand=False, fill=tk.Y, padx=(0,40))  # moved left

mic_icon_pil = Image.open("C:/Users/Vedant Finavia/Downloads/microphone-icon-vector-illustration-removebg-preview.png").resize((100, 100))
mic_icon = ImageTk.PhotoImage(mic_icon_pil)

mic_label = tk.Label(left_frame, text="Record one word\nat a time", font=("Helvetica", 16), bg="#9b59b6", fg="white")
mic_label.pack(pady=(0,5))  # closer to mic

mic_button = tk.Button(left_frame, image=mic_icon, command=toggle_recording, bg="white", relief=tk.FLAT)
mic_button.pack(pady=(5,20))

# === RIGHT SIDE ===
right_frame = tk.Frame(main_frame, bg="#9b59b6")
right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

# Number of Words header centered
word_label = tk.Label(right_frame, text="Number of Words", font=("Helvetica", 16), bg="#9b59b6", fg="white")
word_label.pack(pady=(0,5))
word_entry = tk.Entry(right_frame, font=("Helvetica", 16), bd=2, relief="solid", width=40)
word_entry.pack(pady=(0,20), ipady=6)

# Translation header centered
translation_label = tk.Label(right_frame, text="English Translation", font=("Helvetica", 16), bg="#9b59b6", fg="white")
translation_label.pack(pady=(0,5))
result_box = tk.Text(right_frame, height=4, width=40, font=("Helvetica", 16), wrap=tk.WORD, bd=2, relief="solid")
result_box.pack(pady=(0,20))

# Buttons below translation box, centered
button_frame = tk.Frame(right_frame, bg="#9b59b6")
button_frame.pack(pady=(0,20))
clear_button = tk.Button(button_frame, text="Clear", font=("Helvetica", 14), command=lambda: [result_box.delete("1.0", tk.END), full_transcription.clear()], bg="#87CEEB", fg="black", width=10)
clear_button.pack(side=tk.LEFT, padx=10)
exit_button = tk.Button(button_frame, text="Exit", font=("Helvetica", 14), command=root.destroy, bg="#FF6F61", fg="white", width=10)
exit_button.pack(side=tk.LEFT, padx=10)

root.mainloop()
