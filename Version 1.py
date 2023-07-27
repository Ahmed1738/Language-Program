import random
import tkinter as tk
import csv

class FlashcardApp:
    def __init__(self):
        # Initialize instance variables
        self.words = {} # Dictionary to store words and their translations
        self.counter = 0 # Counter to keep track of user's progress
        self.total_words = 0 # Total number of words in the dictionary

        # Create the main window
        self.window = tk.Tk()
        self.window.title("Flashcard App")
        self.window.geometry("500x500")
        self.window.resizable(False, False)

        # Create labels to display the word and its translation
        self.word_label = tk.Label(self.window, text="")
        self.word_label.pack()
        self.translation_label = tk.Label(self.window, text="")
        self.translation_label.pack()

        # Create buttons for user interaction
        self.knowledge_button = tk.Button(self.window, text="I know this word", command=self.knowledge)
        self.knowledge_button.pack()
        self.next_button = tk.Button(self.window, text="Next word", command=self.next_word)
        self.next_button.pack()

    def load_words(self, filename):
        # Load words and their translations from a CSV file
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                word, translation = row
                self.add_word(word, translation)

    def add_word(self, word, translation):
        # Add a word and its translation to the dictionary
        self.words[word] = translation
        self.total_words += 1

    def knowledge(self):
        # Increment the counter when the user indicates they know the word
        self.counter += 1

    def next_word(self):
        # Select a random word from the dictionary and update the labels
        word = random.choice(list(self.words.keys()))
        translation = self.words[word]
        
        # Add animation here
        
        # Update labels with new word and translation
        self.word_label.config(text=word)
        self.translation_label.config(text=translation)

    def run(self):
        # Run the main loop of the window
        self.window.mainloop()

# Create an instance of the FlashcardApp class
app = FlashcardApp()

# Load words from a CSV file
app.load_words('words_1.csv')

# Run the app
app.run()