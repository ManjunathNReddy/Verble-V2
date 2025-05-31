from ui.widgets import GuessRow, HintModal

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Footer, Static, Button
from textual import events

from game import VerbleGame
from constants import *

class VerbleApp(App):
    CSS_PATH = TCSS_PATH
    TITLE = "Verble V2"
    BINDINGS = [("ctrl+q", "quit", "Quit"),("ctrl+r", "restart", "Restart")]
    def __init__(self):
        super().__init__()
        self.game = None
        self.guess_rows = []
        self.current_row = 0
        self.messages = []
        self.game_over = False

    def compose(self) -> ComposeResult:
        with Container(id="game-container"):
            yield Static(WELCOME, classes="centered", markup=False)
            yield Static(WELCOME_QUESTION, classes="centered", markup=False)
            yield Static(INSTRUCTIONS, id="instructions", markup=False)
            with Vertical(id="game-board"):
                for i in range(NUM_GUESSES):
                    row = GuessRow(classes="guess-row")
                    self.guess_rows.append(row)
                    yield row
            with Horizontal(id="controls"):
                yield Button("New Game", id="new-game")
                yield Button("Get Hint", id="hint-btn")
                yield Button("Quit", id="quit-btn")
            yield Static("", id="message-area", markup=False)
        yield Footer()

    def on_mount(self) -> None:
        self.start_new_game()

    def start_new_game(self):
        self.game = VerbleGame()
        self.current_row = 0
        self.messages = []
        self.game_over = False
        for i, row in enumerate(self.guess_rows):
            row.update_guess("", None)
            row.set_active(i == 0)
        self.query_one("#message-area").update("")
        self.add_message(WELCOME_NOTE)

    def add_message(self, text: str):
        if len(self.messages) > 2:
            self.messages.pop(0)
        self.messages.append(text)       
        self.query_one("#message-area").update("\n".join(self.messages))

    async def on_key(self, event: events.Key) -> None:
        if self.game_over:
            return
        key = event.key
        if key.isalpha() and len(key) == 1 and self.current_row < len(self.guess_rows):
            row = self.guess_rows[self.current_row]
            if row.add_letter(key.upper()):
                filled = row.filled_count()
                if filled == NUM_LETTERS:
                    self.add_message(SUBMIT_NOTE)
            event.stop()
            return
        if key == "backspace":
            if self.current_row < len(self.guess_rows):
                self.guess_rows[self.current_row].remove_letter()          
            event.stop()
            return
        if key == "space":
            self.action_submit_guess()
            event.stop()
            return

    def action_submit_guess(self):
        if self.game_over or self.current_row >= len(self.guess_rows):
            return
        row = self.guess_rows[self.current_row]
        if not row.is_full():
            needed = NUM_LETTERS - row.filled_count()
            self.add_message(NEEDED_LETTERS(needed))
            return
        guess = row.get_current_word()
        if guess == HINTER:
            self.action_hint()
            return
        if not self.game.is_valid_guess(guess):
            self.add_message(UNRECOGNIZED_GUESS_TEXT)
            return
        validity = self.game.apply_guess(guess)
        row.update_guess(guess, validity)
        row.set_active(False)
        if self.game.is_win(validity):
            title, _ = self.game.get_title_and_color()
            self.add_message(WIN_TEXT)
            self.add_message(WIN_TITLE(title))
            self.add_message(WIKI(self.game.word.lower()))
            self.game_over = True
        elif self.game.is_lost():
            self.add_message(LOSE_TEXT)
            self.add_message(LOSE_REVEAL + self.game.word.lower())
            self.add_message(WIKI(self.game.word.lower()))
            self.game_over = True
        else:
            self.current_row += 1
            self.guess_rows[self.current_row].set_active(True)
            self.add_message(GUESS_I_OF_J(self.current_row,NUM_GUESSES))

    def action_hint(self) -> None:
        if not self.game_over and not self.game.is_lost():
            row = self.guess_rows[self.current_row]
            if row.get_current_word() == HINTER:
                row.update_guess("", None)
                row.set_active(True)

            def on_result(res):
                if res and res[0] == "hint":
                    indices = res[1]
                    hint_word = "".join(
                        self.game.word[i] if i in indices else "_" for i in range(NUM_LETTERS)
                    )
                    self.add_message(f"Hint: {hint_word}")

            self.push_screen(HintModal(self.game), on_result)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "hint-btn":
            self.action_hint()
        elif event.button.id == "new-game":
            self.action_restart()
        elif event.button.id == "quit-btn":
            self.action_quit()

    def action_restart(self) -> None:
        self.start_new_game()

    def action_quit(self) -> None:
        self.exit()