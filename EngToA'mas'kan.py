

import speech_recognition as sr
import re
# Define your custom language dictionary
AmaskanMappings = {
    # Root words expanded to full meanings
    "act": "⅂⦵",                  # "do"
    "water": "X⦵|ပ",              # (from "aqua")
    "hear": "Γ⦵⅂",                # (from "aud")
    "air": "⦵",                   # (from "aero")
    "self": "ɸ/",                  # (from "auto")
    "good": r"|ɤ\\",                # (from "bene")
    "life": "ɤ|ပ",                 # (from "bio")
    "block": "⅂ပ⅂",
    "body": "ပX",
    "container": "|ɤ",             # (from "box/container")
    "cause": "Xɤ/",
    "can": "⦵/",                   # (ability)
    "take": "ΓɤX",                 # (from "cap/capt/cept")
    "time": "–ɤ",                  # (from "chron")
    "cover": "/⦵",
    "confident": "ɤ",
    "believe": "Γɸ",               # (from "cred")
    "circle": "ɤΓ",                # (from "cycle")
    "say": "o/",                   # (from "dict")
    "emotion": "⅂ɤ–",
    "eat": "ပ",
    "end": "o",                    # (from "fin")
    "shape": "|o|ပ",               # (from "form")
    "break": "–ɸ",                 # (from "fract/frag")
    "fear": "ပΓ",
    "food": "Xပ",
    "fight": "⦵X",
    "fix": "–⦵X",                  # (repair)
    "earth": "ɤ–",                 # (from "Geo")
    "gas": "ɸ|ပ",
    "step": r"⅂⦵\\",               # (from "grad/gress")
    "write": "XɸΓ",                # (from "graph")
    "stick": "⅂o",                 # (from "her/hes")
    "hole": "/ပΓ",
    "important": "|o–",
    "information": "Γɤ",           # (from "Info")
    "join": "ɸ–",                  # (from "junct")
    "judge": "–oΓ",                # (from "jud")
    "kind": "–⦵|ပ",                # (type/gentle)
    "land": r"Xɸ\\",
    "liquid": "ɸX",
    "place": "oX",                 # (from "loc")
    "word": "|ပ–",                 # (from "log/logue")
    "hand": "/ɤ",                  # (from "man")
    "measure": "–ɤΓ",              # (from "meter/metr")
    "small": "|⦵",                 # (from "min")
    "mouth": "⅂ပ–",                # (from "Mouth part/tounge")
    "send": "⅂ɸX",                 # (from "mit/miss")
    "many": "|⦵/",                 # (from "multi")
    "move": r"\\ɸ",                 # (from "mob/mov/mot")
    "cure": r"\\ပ",                 # (from "med")
    "name": "Xo⅂",
    "night": r"⅂ပ\\",               # (from "Noct")
    "born": "o⅂",                  # (from "nat")
    "new": "Xo",                   # (from "nov")
    "paper": "/o",
    "parent": r"\\⦵Γ",
    "person": "⅂ɤ|ပ",
    "planet": "ပ–",
    "carry": "/o–",                # (from "port")
    "put": "|o⅂",                  # (from "pos/pon")
    "rule": r"\\ɤ|ပ",               # (from "reg/rect")
    "rest": "o–",
    "cut": "–⦵",                   # (from "sect")
    "feel": "Γɸ–",                 # (from "sens/sent")
    "see": "⦵|ပ",                  # (from "spec/spect")
    "bottom": "XɤX",               # (from "sub")
    "build": r"\\ɤ\\",              # (from "struct")
    "string": "/⦵–",
    "solid": "ΓoX",
    "square": "|ပX",
    "story": "–ပX",
    "follow": r"–ɤ\\",              # (from "sequ/sec")
    "same": "Γo",                  # (from "simil/simul")
    "alone": "XoX",                # (from "sol")
    "breathe": "–ပ",               # (from "spir")
    "symbol": r"\\ပ\\",
    "hold": "⅂ɸ–",                 # (from "ten/tain")
    "far": "Γɤ⅂",                  # (from "tele")
    "heat": "⅂ပ|ပ",                # (from "therm")
    "pull": "|ပ",                  # (from "tract")
    "trait": "Xပ–",
    "touch": "X⦵",                 # (from "tact/tang")
    "thing": "⦵–",
    "give": "ပ/",                  # (from "trib")
    "triangle": "o|ပ",
    "empty": r"–ɸ\\",               # (from "vac")
    "truth": "/ɸX",                # (from "ver")
    "call": r"\\o–",                # (from "voc/vok")
    "come": "ɸ⅂",                  # (from "vent")
    "value": r"\\ပX",
    "method": r"⦵\\",               # (from "way/method")
    "want": "⅂ɸ/",
    "animal": "Xɸ⅂",               # (from "zoo")
    "change": "⅂ɤX",
    "get": "|o",
    "give": "⅂ပ",
    "go": "–o|ပ",
    "grow": r"\\ɤ",
    "have": "/ɸ",                  # (from "Have/possess/control")
    "help": "Γ⦵",
    "know": r"\\ɸ|ပ",
    "keep": "/ပ/",
    "love": "/ပ",
    "lose": "ɸΓ",
    "make": r"–o\\",
    "put": r"⅂ɤ\\",
    "play": "⅂ɸ",
    "plan": "/ɤ|ပ",
    "start": r"ပ\\",
    "stop": "⦵Γ",
    "stand": "ɤ⅂",
    "think": "Γပ",
    "trade": "ɤ/",
    "use": "ပ|ပ",
    "work": "Xɤ",
    # Numbers, directions, adjectives, etc. (unchanged)
    "one": "Γɸ/",
    "two": "Xɤ⅂",
    "three": "Γɤ–",
    "four": "X⦵X",
    "five": "⅂ပX",
    "six": "⅂o–",
    "seven": "|ɸ",
    "eight": "|⦵⅂",
    "nine": "/oΓ",
    "zero": r"\\o/",
    "appearance": r"\\ɸ/",
    "north": "⅂⦵X",
    "east": "⅂ပΓ",
    "front": r"Γɸ\\",               # (from "Forward/front")
    "right": "ပ⅂",                 # (direction)
    "up": r"\\oX",
    "state": r"o\\",
    "city": "Xɸ",
    "dimension": "⅂ɤ",
    "smell": "XɸX",
    "become": "⅂⦵/",
    "color": "–ပ/",
    "blue": "–ɸ/",
    "red": r"\\⦵X",
    "yellow": "Xo/",
    "good": "/ɸ⅂",
    "happy": "/ɤ⅂",
    "big": "|⦵|ပ",
    "warm": "/ပX",
    "easy": "–ɤX",
    "fast": "⅂oΓ",
    "old": "|ɤ|ပ",
    "new": "–oX",
    "tall": "X⦵⅂",
    "low": "|ပΓ",
    "clean": "|ɸ–",
    "hungry": "Xɸ–",
    "full": r"⅂ɸ\\",
    "fun": "|ပ/",
    "nice": r"Xo\\",
    "loud": "|⦵Γ",
    "pretty": r"ɤ\\",
    "strong": "ΓɤΓ",
    "smart": "–ပ–",
    "kind": "–ɤ/",
    "wet": r"/o\\",
    "open": "/⦵/",
    "early": "Γɤ|ပ",
    "correct": "–o/",              # (from "right (correct)")
    "cool": r"|⦵\\",
    "flat": r"|o\\",
    "vertical": r"\\⦵–",
    # Pronouns/prepositions (unchanged)
    "me": "/ɤΓ",                   # (from "First POV (Me/Us) Objective")
    "I": "ɸ",                      # (from "First POV (I/We) Subjective")
    "it": "/ɤ/",                   # (from "Third POV (it/them) Objective")
    "they": r"\\o\\",               # (from "Third POV (it/they) Subjective")
    "to": "/o⅂",
    "next": r"\\ɸ⅂",
    "behind": "Γ⦵|ပ",
    "below": "Xo|ပ",
    "above": "–⦵/",
    "in front of": "⅂o/",
    "in": "/ɸΓ",
    "near": "–ɤ⅂",
    "after": r"Xပ\\",
    "before": r"\\ပΓ",
    "a": "Xɤ|ပ",                   # (indefinite article)
    "the": r"|ပ\\",                 # (demonstrative article)
    "all": r"\\o",                  # (indefinite pronoun)
    "and": "XoΓ",
    "but": "|ɸ/",
    "or": "⅂ɤ/",
    "so": "Xပ/",
}



# Text translator
def translate_text(text, dictionary):
    words = re.findall(r"\w+|[^\w\s]", text, re.UNICODE)
    translated = []

    for word in words:
        lower = word.lower()
        translation = dictionary.get(lower, word)  # Keep unchanged if not found
        if word.istitle():
            translation = translation.capitalize()
        elif word.isupper():
            translation = translation.upper()
        translated.append(translation)

    return "'".join(translated)

# Speech-to-text function
def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("\nSpeak now...")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        english_text = recognizer.recognize_google(audio)
        print(f"\nYou said: {english_text}")
        return english_text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand your voice.")
    except sr.RequestError as e:
        print(f"Speech recognition service error: {e}")
    return ""

# Menu logic
def main():
    print("English --> A'mas'kan Translator")
    print("Choose an input method:")
    print("1. Speak")
    print("2. Type text")

    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        english = recognize_speech()
    elif choice == "2":
        english = input("\nType your English sentence: ")
    else:
        print("Invalid choice. Exiting.")
        return

    if english:
        translated = translate_text(english, AmaskanMappings)
        print(f"\nA'mas'kan Translation: {translated}")

if __name__ == "__main__":
    main()
