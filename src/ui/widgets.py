from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Static, Button
from textual.containers import Container, Horizontal, Center

from constants import *

class LetterBox(Static):
    def __init__(self, letter: str = "", validity=None, is_active=False, **kwargs):
        self.letter = letter.upper() if letter else ""
        self.validity = validity
        self.is_active = is_active
        super().__init__(self.letter, **kwargs)
        self.update_style()

    def update_letter(self, letter: str, validity=None, is_active=False):
        self.letter = letter.upper() if letter else ""
        self.validity = validity
        self.is_active = is_active
        self.update(self.letter)
        self.update_style()

    def update_style(self):
        if self.validity is True:
            self.styles.background, self.styles.color, self.styles.border = STYLE_BY_LETTER_STATE["good"]
        elif self.validity is False:
            self.styles.background, self.styles.color, self.styles.border = STYLE_BY_LETTER_STATE["ok"]
        elif self.validity is None and self.letter and not self.is_active:
            self.styles.background, self.styles.color, self.styles.border = STYLE_BY_LETTER_STATE["bad"]
        elif self.is_active:
            self.styles.background, self.styles.color, self.styles.border = STYLE_BY_LETTER_STATE["active"]
            if not self.letter:
                self.styles.border = HIGHLIGHT_BORDER
        else:
            self.styles.background, self.styles.color, self.styles.border = STYLE_BY_LETTER_STATE["empty"]

class GuessRow(Horizontal):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.letter_boxes = []
        self.is_active = False

    def compose(self) -> ComposeResult:
        for _ in range(NUM_LETTERS):
            box = LetterBox(classes="letter-box")
            self.letter_boxes.append(box)
            yield box

    def set_active(self, active: bool):
        self.is_active = active
        for box in self.letter_boxes:
            box.is_active = active
            box.update_style()

    def update_guess(self, guess: str, validity=None):
        for i, box in enumerate(self.letter_boxes):
            letter = guess[i] if i < len(guess) else ""
            val = validity[i] if validity and i < len(validity) else None
            box.update_letter(letter, val, self.is_active)

    def get_current_word(self) -> str:
        return "".join(box.letter for box in self.letter_boxes)

    def filled_count(self) -> int:
        return sum(1 for box in self.letter_boxes if box.letter)

    def add_letter(self, letter: str) -> bool:
        for box in self.letter_boxes:
            if not box.letter:
                box.update_letter(letter, None, True)
                return True
        return False

    def remove_letter(self) -> bool:
        for i in range(len(self.letter_boxes) - 1, -1, -1):
            if self.letter_boxes[i].letter:
                self.letter_boxes[i].update_letter("", None, True)
                return True
        return False

    def is_full(self) -> bool:
        return all(box.letter for box in self.letter_boxes)

class HintModal(ModalScreen):
    def __init__(self, game, **kwargs):
        self.game = game
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        with Container(id="hint-dialog"):
            yield Static(HINT_GREETING, classes="centered", markup=False)
            if self.game.hints == 0:
                yield Static(NO_HINT_TEXT, classes="centered", markup=False)
                yield Center(Button("OK", id="hint-ok"))
            elif self.game.hints == 1:
                yield Static(HINT_SMALL_PROMPT, classes="centered", markup=False)
                yield Center(
                    Button("Small Hint", id="small-hint"),
                    Button("Cancel", id="cancel"),
                    )
            else:
                yield Static(HINT_PROMPT, classes="centered", markup=False)
                yield Center(
                    Button("Big Hint", id="big-hint"),
                    Button("Small Hint", id="small-hint"),
                    Button("Cancel", id="cancel"),
                    )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "big-hint":
            indices = self.game.get_hint_indices(HintKind.big)
            self.dismiss(("hint", indices))
        elif event.button.id == "small-hint":
            indices = self.game.get_hint_indices(HintKind.small)
            self.dismiss(("hint", indices))
        else:
            self.dismiss(None)