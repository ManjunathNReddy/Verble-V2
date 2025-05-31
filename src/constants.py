import json
import sys
from pathlib import Path
from random import choice
from enum import Enum

WORDS_PATH = None
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    # Running in a PyInstaller bundle
    WORDS_PATH = Path(sys._MEIPASS) / "words"
else:
    # Running in a normal Python environment
    WORDS_PATH = Path(__file__).resolve().parent.parent / "words"

# Sources
CORPUS_VERBS = WORDS_PATH /"31K verbs.txt"
FREQUENT_VERBS = WORDS_PATH /"frequent.json"

# Verble words
VERBLE_CORPUS = WORDS_PATH /"verbs.txt"
VERBLE_FREQUENT = WORDS_PATH /"top_verbs.json"

# Load words : top verbs for choosing and all verbs for checking
TOP_VERBS, VERBS = [], []
with open(VERBLE_FREQUENT, "r") as frequent_verbs:
    freq_verbs = json.load(frequent_verbs)
    TOP_VERBS = list(freq_verbs.keys())
with open(VERBLE_CORPUS, "r") as verb_file:
        VERBS=verb_file.read().splitlines()

# |SETTINGS| #
# NUM_LETTERS must match length of words in the verb list
NUM_LETTERS = 5
NUM_GUESSES = NUM_LETTERS + 1
NUM_HINTS = NUM_LETTERS//2

NAMES = ['KENTO', 'TOSHY', 'TATSO', 'SHINO', 'AKIYO', 'KYOKO', 'EMIKO', 'YUKIY', 'RIEKO', 'KAORY']
HINTER = choice(NAMES)
HINT_GREETING = "KONNICHIWA!"
NO_HINT_TEXT = f"IYA, {HINTER} can't HELP!"
HintKind = Enum('Hint', ['small', 'big'])
HINT_PROMPT = f"HAI, {HINTER} can HELP!"
HINT_SMALL_PROMPT = f"HAI, {HINTER} can HELP with Small HINT!"
WELCOME = "Welcome to VERBLE, the ultimate verb guessing game!"
WELCOME_QUESTION = f"Can you guess the {NUM_LETTERS}-letter verb in {NUM_GUESSES} shots?"
INSTRUCTIONS = "Type letters to fill boxes • SPACE to submit"
WELCOME_NOTE = "Start typing your first guess!"
SUBMIT_NOTE = "Press SPACE to submit or BACKSPACE to delete."
UNRECOGNIZED_GUESS_TEXT = "That's obscure! Please enter a VERB."
LOSE_REVEAL = "The word was: "
WIN_TEXT = "YOU WIN!"
LOSE_TEXT = "YOU LOSE!"
GUESS_I_OF_J = lambda i,j: f"Guess {i+1} of {j}"
NEEDED_LETTERS = lambda i: f"Need {i} more letters to complete your word!"
WIN_TITLE = lambda title: f"Congrats! You're a {title} of VERBLE!"
WIKI = lambda word: f"https://en.wiktionary.org/wiki/{word.lower()}#Verb"

TITLE_BY_GUESSES = { 1: "Master", 2: "Wizard", 3: "Mage", 4: "Warrior", 5: "Knight", 6: "Journeyman" }

# Letter style: BG, Text, Border

STYLE_BY_LETTER_STATE = {"good": ("#538d4e", "white", ("solid", "#538d4e")),
                         "ok": ("#b59f3b", "black", ("solid", "#b59f3b")),
                         "bad": ("#3a3a3c", "white", ("solid", "#3a3a3c")),
                         "active": ("#2e2f31", "white", ("solid", "#6c6e70")),
                         "empty": ("#1e1f21", "white", ("solid", "#3a3a3c"))}

HIGHLIGHT_BORDER = ("solid", "orange") 

COLOR_BY_GUESSES = { -1: 'red', 0: 'blue', 1: 'cyan', 2: 'orange', 3: 'purple', 4: 'lightseagreen', 5: 'green', 6: 'snow' }    