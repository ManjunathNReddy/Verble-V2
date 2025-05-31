from random import choice, randrange
from collections import Counter
from constants import *

class VerbleGame:
    def __init__(self):
        self.word = choice(TOP_VERBS).upper()
        self._counts = Counter(self.word)
        self.hints = NUM_HINTS
        self.hint_indices = list(range(NUM_LETTERS))
        self.guesses = []

    def is_valid_guess(self, guess):
        return len(guess) == NUM_LETTERS and guess.lower() in VERBS
    
    # Letter validity indicates how each letter corresponds to the guess:
    #   correct position: True, incorrect position: False, not in the word: None
    def check_guess(self, guess):
        guess = guess.upper()
        validity = [True if g == w else None for g, w in zip(guess, self.word)]
        used_counts = Counter()
        used_counts.update(g for g, w in zip(guess, self.word) if g == w)

        for i, g in enumerate(guess):
            if validity[i] is None and used_counts[g] < self._counts[g]:
                validity[i] = False
                used_counts[g] += 1
        
        return validity

    def apply_guess(self, guess):
        guess = guess.upper()
        self.guesses.append(guess)
        return self.check_guess(guess)

    def is_win(self, validity):
        return all(v is True for v in validity)

    def is_lost(self):
        return len(self.guesses) >= NUM_LETTERS + 1

    def get_title_and_color(self):
        i = len(self.guesses)
        return TITLE_BY_GUESSES.get(i, TITLE_BY_GUESSES[6]), COLOR_BY_GUESSES.get(i, COLOR_BY_GUESSES[6])

    def get_hint_indices(self, kind=HintKind.small):
        if not self.hint_indices or self.hints < 1:
            return []

        if kind == HintKind.big and self.hints > 1 and len(self.hint_indices) > 1:
            self.hints -= 2
            return [self.hint_indices.pop(0), self.hint_indices.pop(-1)]
        else:
            self.hints -= 1
            index = self.hint_indices.pop(randrange(len(self.hint_indices)))
            return [index]
