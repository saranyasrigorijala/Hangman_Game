import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
import random
from kivy.uix.button import Button
from word_dictionary import word_dictionary
kivy.require('2.0.0')
# Hangman Game UI Class
class HangmanApp(App):
    def build(self):
        self.word, self.word_info = self.get_random_word()
        self.word_completion = "_" * len(self.word)
        self.guessed_letters = []
        self.total_tries = len(self.word) - 1
        self.tries_left = self.total_tries
        self.guessed = False
        # Main Layout
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        # BoxLayout for side-by-side Hangman and Word display
        self.side_by_side_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='200dp')
        # Displaying Hangman Stage with color
        self.hangman_label = Label(text=self.display_hangman(self.tries_left, self.total_tries), font_size='20sp', color=(1, 0, 0, 1))
        self.side_by_side_layout.add_widget(self.hangman_label)
        # Displaying Word Completion Status with color
        self.word_label = Label(text=self.word_completion, font_size='24sp', color=(0, 0, 1, 1))
        self.side_by_side_layout.add_widget(self.word_label)
        # Add side-by-side layout to the main layout
        self.layout.add_widget(self.side_by_side_layout)
        # Label instructing user to press Enter after guessing
        self.instruction_label = Label(text="After typing your guess, press Enter to submit.", font_size='16sp', color=(0, 1, 0, 1))
        self.layout.add_widget(self.instruction_label)
        # Input Layout for Guessing
        self.input_layout = GridLayout(cols=2, size_hint_y=None, height='50dp')
        self.input_label = Label(text="Guess a letter:", size_hint_x=0.3)
        self.input_layout.add_widget(self.input_label)
        self.guess_input = TextInput(multiline=False, size_hint_x=0.7)
        self.guess_input.bind(on_text_validate=self.submit_guess)  # Bind Enter key to submit guess
        self.input_layout.add_widget(self.guess_input)
        self.layout.add_widget(self.input_layout)
        # Displaying Attempts Left
        self.tries_label = Label(text=f"Remaining attempts: {self.tries_left}", font_size='18sp')
        self.layout.add_widget(self.tries_label)
        # Result Message and Word Details
        self.result_label = Label(text="", font_size='20sp', halign="center")
        self.layout.add_widget(self.result_label)
        return self.layout
    def get_random_word(self):
        word = random.choice(list(word_dictionary.keys()))
        return word, word_dictionary[word]
    def display_hangman(self, tries_left, total_tries):
        stages = [
            "   -----\n   |   |\n       |\n       |\n       |\n-------",
            "   -----\n   |   |\n   O   |\n       |\n       |\n-------",
            "   -----\n   |   |\n   O   |\n   |   |\n       |\n-------",
            "   -----\n   |   |\n   O   |\n  /|   |\n       |\n-------",
            "   -----\n   |   |\n   O   |\n  /|\\  |\n       |\n-------",
            "   -----\n   |   |\n   O   |\n  /|\\  |\n  /    |\n-------",
            "   -----\n   |   |\n   O   |\n  /|\\  |\n  / \\  |\n-------"
        ]
        stage_index = total_tries - tries_left
        return stages[stage_index]
    def submit_guess(self, instance):
        guess = self.guess_input.text.upper()
        self.guess_input.text = ""  # Clear the input field after the guess
        if len(guess) == 1 and guess.isalpha():
            if guess in self.guessed_letters:
                self.result_label.text = f"You already guessed the letter {guess}"
            elif guess not in self.word.upper():
                self.result_label.text = f"{guess} is not in the word."
                self.tries_left -= 1
                self.guessed_letters.append(guess)
            else:
                self.result_label.text = f"Good job, {guess} is in the word!"
                self.guessed_letters.append(guess)
                word_as_list = list(self.word_completion)
                indices = [i for i, letter in enumerate(self.word.upper()) if letter == guess]
                for index in indices:
                    word_as_list[index] = self.word[index]
                self.word_completion = "".join(word_as_list)
                if "_" not in self.word_completion:
                    self.guessed = True
        else:
            self.result_label.text = "Invalid input. Please enter a single letter."
        # Update labels after each guess
        self.word_label.text = self.word_completion
        self.hangman_label.text = self.display_hangman(self.tries_left, self.total_tries)
        self.tries_label.text = f"Remaining attempts: {self.tries_left}"
        if self.guessed:
            self.show_word_details("Congrats, you guessed the word!")
        elif self.tries_left <= 0:
            self.show_word_details(f"Sorry, you ran out of tries. The word was: {self.word}")
    def show_word_details(self, message):
        self.result_label.text = message
        self.result_label.text += f"\n\n[b][color=ff0000]DESCRIPTION:[/color][/b] {self.word_info['description']}"
        self.result_label.text += f"\n\n[b][color=ff0000]SYNONYMS:[/color][/b] {', '.join(self.word_info['synonyms'])}"
        self.result_label.text += f"\n\n[b][color=ff0000]EXAMPLE:[/color][/b] {self.word_info['example']}"
        self.result_label.markup = True  # Enable markup for the label
        self.guess_input.disabled = True  # Disable input after game ends
# Running the application
if __name__ == "__main__":
    HangmanApp().run()
