import random
import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter import messagebox
import json
import os
import tkinter.ttk as ttk
from PIL import Image, ImageTk, ImageSequence

class FlashcardApp:
    def __init__(self):
        # Initialize instance variables
        self.words = {}
        self.pronunciations = {}
        self.counter = 0
        self.total_words = 0
        self.username = ""
        self.learned_words = []

        # Create the main window
        self.window = tk.Tk()
        self.window.title("Flashcard App")
        self.window.geometry("500x500")
        self.window.resizable(False, False)

        # Create labels to display the word, its translation, and its pronunciation
        self.word_label = tk.Label(self.window, text="", bg="lightblue", fg="black", font=("Arial", 24))
        self.word_label.pack(pady=10)
        self.translation_label = tk.Label(self.window, text="", bg="lightblue", fg="black", font=("Arial", 18))
        self.translation_label.pack(pady=5)
        self.pronunciation_label = tk.Label(self.window, text="", bg="lightblue", fg="black", font=("Arial", 14))
        self.pronunciation_label.pack(pady=5)

        # Create buttons for user interaction
        self.next_button = tk.Button(self.window, text="Next word", command=self.next_word, bg="lightgreen", fg="black", font=("Arial", 12))
        self.next_button.pack(pady=10)
        self.previous_button = tk.Button(self.window, text="Previous word", command=self.previous_word, bg="lightgreen", fg="black", font=("Arial", 12))
        self.previous_button.pack(pady=5)
        self.knowledge_button = tk.Button(self.window, text="I know this word", command=self.knowledge, bg="lightgreen", fg="black", font=("Arial", 12))
        self.knowledge_button.pack(pady=5)
        self.quit_button = tk.Button(self.window, text="Quit", command=self.quit, bg="lightcoral", fg="black", font=("Arial", 12))
        self.quit_button.pack(pady=10)

        # Create a progress bar to visualize the user's learning progress
        self.progress_bar = ttk.Progressbar(self.window, length=300, mode='determinate')
        self.progress_bar.pack(pady=10)

        # Create the "Review Learned Words" button
        self.review_button = tk.Button(self.window, text="Review Learned Words", command=self.review_words, bg="lightblue", fg="black", font=("Arial", 12))
        self.review_button.pack(pady=10)

        # Load words from a JSON file
        self.load_words('words_3.json')

        # Display the first word
        self.next_word()

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
        self.progress_bar['value'] = (self.counter / self.total_words) * 100

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
        self.review_button = tk.Button(self.window, text="Review", command=self.review_words, bg="lightblue", fg="black", font=("Arial", 12))
        self.review_button.pack()

    def quit(self):
        # Save the user's progress to a JSON file called 'progress.json'
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

# Function to start the language learning app
def start():
    # Hide the start screen
    root.withdraw()

    # Create an instance of the FlashcardApp class
    app = FlashcardApp()

    # Run the app
    app.run()

# Create a new tk.Tk() instance for the start screen
root = tk.Tk()
root.title("Start Screen")
root.geometry("500x500")
root.resizable(False, False)

# Load and process the animated GIF
file = "introVid.gif"
frames = Image.open(file)
image_frame_list = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(frames)]

# Function to animate the frames of the GIF
def animation(count):
    im = image_frame_list[count]
    gif_label.configure(image=im)
    count += 1
    if count < len(image_frame_list):
        root.after(50, lambda: animation(count))

# Creates a label widget to display the animated GIF
gif_label = tk.Label(root, image="")
gif_label.pack()

# Function to hide the start button
def hide_start():
    image_button1.pack_forget()

# Load and resize the first image for the start button
image1 = Image.open("start_image.png")
image1 = image1.resize((300, 100))
photo1 = ImageTk.PhotoImage(image1)

# Creates a button widget for the start button
image_button1 = tk.Button(root, image=photo1, bg="#F1EFE7", borderwidth=0, highlightthickness=0, command=lambda: (root.after(1300, start), hide_start(), animation(0)))
image_button1.pack(pady=(100, 50))

# Start the main event loop for the start screen
root.mainloop()