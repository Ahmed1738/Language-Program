import random
import tkinter as tk
from tkinter.simpledialog import askstring
import json
import os
from tkinter import messagebox

class FlashcardApp:
    def __init__(self):
        # Initialize instance variables
        self.words = {}  # Dictionary to store words and their translations
        self.pronunciations = {}  # Dictionary to store pronunciations of words
        self.counter = 0  # Counter to keep track of user's progress
        self.total_words = 0  # Total number of words in the dictionary
        self.username = ""  # Username of the user

        # Create the main window
        self.window = tk.Tk()
        self.window.title("Flashcard App")
        self.window.geometry("500x500")
        self.window.resizable(False, False)

        # Create labels to display the word, its translation, and its pronunciation
        self.word_label = tk.Label(self.window, text="", bg="lightblue", fg="black")
        self.word_label.pack()
        self.translation_label = tk.Label(self.window, text="", bg="lightblue", fg="black")
        self.translation_label.pack()
        self.pronunciation_label = tk.Label(self.window, text="", bg="lightblue", fg="black")
        self.pronunciation_label.pack()

        # Create buttons for user interaction
        self.next_button = tk.Button(self.window, text="Next word", command=self.next_word, bg="lightblue", fg="black")
        self.next_button.pack()
        self.previous_button = tk.Button(self.window, text="Previous word", command=self.previous_word,
                                          bg="lightblue", fg="black")
        self.previous_button.pack()
        self.knowledge_button = tk.Button(self.window, text="I know this word", command=self.knowledge,
                                          bg="lightblue", fg="black")
        self.knowledge_button.pack()
        self.quit_button = tk.Button(self.window, text="Quit", command=self.quit, bg="lightblue", fg="black")
        self.quit_button.pack()

        # Create the "Review" button
        self.create_review_button()

        # Load words from a JSON file
        self.load_words('words_3.json')

        # Initialize the learned_words list
        self.learned_words = []

    def load_words(self, filename):
        # Load words, their translations, and their pronunciations from a JSON file
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.words = data.get('words', {})
                self.pronunciations = data.get('pronunciations', {})
                self.total_words = len(self.words)

    def add_word(self, word, translation, pronunciation):
        # Add a word, its translation, and its pronunciation to the dictionaries
        self.words[word] = translation
        self.pronunciations[word] = pronunciation
        self.total_words += 1

    def save_progress(self, filename):
        # Save user progress to a JSON file
        with open(filename, 'a') as file:
            data = {"username": self.username, "counter": self.counter}
            json.dump(data, file)
            file.write('\n')  # Add a newline for the next entry

    def knowledge(self):
        # Increment the counter when the user indicates they know the word
        self.counter += 1

        # Add the current word to the learned_words list
        if self.counter <= self.total_words:
            current_word = random.choice(list(self.words.keys()))
            self.learned_words.append(current_word)

        # Display the next word
        self.next_word()

    def previous_word(self):
        # Display the previous word if there are learned words available
        if self.learned_words:
            previous_word = self.learned_words.pop()
            self.word_label.config(text=previous_word)
            self.translation_label.config(text=self.words[previous_word])
            self.pronunciation_label.config(text=self.pronunciations[previous_word])

        # Enable the "Next word" button if the user can continue learning
        if self.counter < self.total_words:
            self.next_button.config(state="normal")

    def next_word(self):
        # Select a random word from the dictionary and update the labels
        word = random.choice(list(self.words.keys()))
        translation = self.words[word]
        pronunciation = self.pronunciations[word]

        # Add animation here

        # Update labels with new word, translation, and pronunciation
        self.word_label.config(text=word)
        self.translation_label.config(text=translation)
        self.pronunciation_label.config(text=pronunciation)

        # Disable the "Next word" button if the user has learned all the words
        if self.counter >= self.total_words:
            self.next_button.config(state="disabled")

    def review_words(self):
        # Display a pop-up with the words the user learned
        if self.learned_words:
            learned_words_str = "\n".join(self.learned_words)
            messagebox.showinfo("Words You Learned", f"Words you learned:\n{learned_words_str}")
        else:
            messagebox.showinfo("Words You Learned", "You haven't learned any words yet.")

    def create_review_button(self):
        # Create a "Review" button
        self.review_button = tk.Button(self.window, text="Review", command=self.review_words, bg="lightblue", fg="black")
        self.review_button.pack()

    def quit(self):
        # saves the user's progress to a JSON file called 'progress.json'
        self.save_progress("progress.json")

        # Show a popup with the user's progress
        messagebox.showinfo("Progress", f"You know {self.counter} words!")

        # Quit the app
        self.window.destroy()

    def run(self):
        # Ask for the user's name
        username = askstring("Username", "What's your name?")
        if username:
            self.username = username

        # Run the main loop of the window
        self.window.mainloop()

# Create an instance of the FlashcardApp class
app = FlashcardApp()

# Run the app
app.run()
