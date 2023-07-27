import random
import tkinter as tk
from tkinter import simpledialog
import csv


class FlashcardApp:
    def __init__(self):
        # Initialize instance variables
        self.words = {} # Dictionary to store words and their translations
        self.pronunciations = {} # Dictionary to store pronunciations of words
        self.counter = 0 # Counter to keep track of user's progress
        self.total_words = 0 # Total number of words in the dictionary
        self.username = "" # Username of the user

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
        self.knowledge_button = tk.Button(self.window, text="I know this word", command=self.knowledge, bg="lightblue", fg="black")
        self.knowledge_button.pack()
        self.next_button = tk.Button(self.window, text="Next word", command=self.next_word, bg="lightblue", fg="black")
        self.next_button.pack()
        self.quit_button = tk.Button(self.window, text="Quit", command=self.quit, bg="lightblue", fg="black")
        self.quit_button.pack()


    def load_words(self, filename):
        # Load words, their translations, and their pronunciations from a CSV file
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                word, translation, pronunciation = row
                self.add_word(word, translation, pronunciation)

    def add_word(self, word, translation, pronunciation):
        # Add a word, its translation, and its pronunciation to the dictionaries
        self.words[word] = translation
        self.pronunciations[word] = pronunciation
        self.total_words += 1

    def knowledge(self):
        # Increment the counter when the user indicates they know the word
        self.counter += 1

        # Display the next word
        self.next_word()

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

    def quit(self):
      # saves the user's progress to a CSV file called 'progress'
      with open("progress.csv", 'a') as file:
          writer = csv.writer(file)
          writer.writerow([self.username, self.counter])

      # Show a popup with the user's progress
      tk.messagebox.showinfo("Progress", f"You know {self.counter} words!")

      # Quit the app
      self.window.destroy()

    def run(self):
      # Ask for the user's name
      username = tk.simpledialog.askstring("Username", "What's your name?")
      if username:
          self.username = username

      # Run the main loop of the window
      self.window.mainloop()

# Create an instance of the FlashcardApp class
app = FlashcardApp()

# Load words from a CSV file
app.load_words('words_2.csv')

# Display the first word
app.next_word()

# Run the app
app.run()
