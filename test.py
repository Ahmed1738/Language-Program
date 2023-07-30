import random
import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter import messagebox
import json
import os
import tkinter.ttk as ttk
from PIL import Image, ImageTk, ImageSequence
import sys

class FlashcardApp:
    def __init__(self):
        # Initialize instance variables
        self.words = {}
        self.pronunciations = {}
        self.total_words = 0
        self.current_word_index = 0
        self.username = ""
        self.learned_words = set()

        # Create the main window
        self.window = tk.Tk()
        self.window.title("Flashcard App")
        self.window.geometry("600x500")
        self.window.resizable(False, False)

        # Set background color and font for all widgets
        bg_color = "#F4E1D2"
        fg_color = "#473E37"
        font_family = "Arial"

        self.window.configure(bg=bg_color)

        # Create labels to display the word, its translation, and its pronunciation
        self.word_label = tk.Label(self.window, text="", bg=bg_color, fg=fg_color, font=(font_family, 32, "bold"))
        self.word_label.pack(pady=20)
        self.translation_label = tk.Label(self.window, text="", bg=bg_color, fg=fg_color, font=(font_family, 20))
        self.translation_label.pack(pady=10)
        self.pronunciation_label = tk.Label(self.window, text="", bg=bg_color, fg=fg_color, font=(font_family, 16))
        self.pronunciation_label.pack(pady=10)

        # Create buttons for user interaction with updated colors and fonts
        button_bg_color = "#F8CECC"
        button_fg_color = "#473E37"
        button_font = (font_family, 14, "bold")

        self.next_button = tk.Button(self.window, text="Next Word", command=self.next_word, bg=button_bg_color, fg=button_fg_color, font=button_font)
        self.next_button.pack(pady=20)
        self.previous_button = tk.Button(self.window, text="Previous Word", command=self.previous_word, bg=button_bg_color, fg=button_fg_color, font=button_font)
        self.previous_button.pack(pady=10)
        self.knowledge_button = tk.Button(self.window, text="I Know This Word", command=self.knowledge, bg=button_bg_color, fg=button_fg_color, font=button_font)
        self.knowledge_button.pack(pady=10)
        self.quit_button = tk.Button(self.window, text="Quit", command=self.quit, bg="#FF5555", fg="white", font=button_font)
        self.quit_button.pack(pady=20)

        # Create a progress bar to visualize the user's learning progress
        self.progress_bar = ttk.Progressbar(self.window, length=400, mode='determinate')
        self.progress_bar.pack(pady=20)

        # Create the "Review Learned Words" button with updated color
        self.review_button = tk.Button(self.window, text="Review Learned Words", command=self.review_words, bg=button_bg_color, fg=button_fg_color, font=button_font)
        self.review_button.pack(pady=20)

        # Load words from a JSON file
        self.load_words('words_3.json')

        # Display the first word
        self.display_word()

    def load_words(self, filename):
        # Load words, their translations, and their pronunciations from a JSON file
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.words = data.get('words', {})
                self.pronunciations = data.get('pronunciations', {})
                self.total_words = len(self.words)

                # Load learned_words and counter from the JSON data
                self.learned_words = set(data.get('learned_words', []))
                counter = data.get('counter', 0)
                self.progress_bar['value'] = (counter / self.total_words) * 100

    def save_progress(self, filename):
        # Save user progress to a JSON file without overwriting the file
        data = {
            "username": self.username,
            "counter": len(self.learned_words),  # Add the counter to the data
            "learned_words": list(self.learned_words)
        }
        with open(filename, 'a') as file:  # Use 'a' mode to append data to the file
            json.dump(data, file)
            file.write('\n')  # Add a new line after each JSON object to separate entries


    def knowledge(self):
        current_word = list(self.words.keys())[self.current_word_index]
        
        # Check if the current word is not in the learned_words set to avoid duplicate counting
        if current_word not in self.learned_words:
            # Increment the counter when the user indicates they know the word
            self.learned_words.add(current_word)
            self.progress_bar['value'] = (len(self.learned_words) / self.total_words) * 100
            # Display the next word
            self.next_word()

        else:
            # If the word is already learned, show a pop-up message
            message = f"You already learned the word '{current_word}'."
            messagebox.showinfo("Word Already Learned", message)

    def previous_word(self):
        # Display the previous word if there are learned words available
        if self.current_word_index > 0:
            self.current_word_index -= 1
            self.display_word()

        # Enable the "Next word" button if the user can continue learning
        if len(self.learned_words) < self.total_words:
            self.next_button.config(state="normal")

    def next_word(self):
        # Increment the current word index
        self.current_word_index += 1

        # Check if the last word is reached
        if self.current_word_index >= self.total_words:
            self.current_word_index = 0

        self.display_word()

    def display_word(self):
        # Get the current word from the list
        current_word = list(self.words.keys())[self.current_word_index]
        translation = self.words[current_word]
        pronunciation = self.pronunciations[current_word]

        # Update labels with new word, translation, and pronunciation
        self.word_label.config(text=current_word)
        self.translation_label.config(text=translation)
        self.pronunciation_label.config(text=pronunciation)

        # Disable the "Next word" button if all words are learned
        if len(self.learned_words) == self.total_words:
            self.next_button.config(state="disabled")

    def review_words(self):
        # Display a pop-up with the words the user learned
        if self.learned_words:
            learned_words_str = "\n".join(self.learned_words)
            messagebox.showinfo("Words You Learned", f"Words you learned:\n{learned_words_str}")
        else:
            messagebox.showinfo("Words You Learned", "You haven't learned any words yet.")

    def quit(self):
        # Save the user's progress to a JSON file called 'progress.json'
        self.save_progress("progress.json")

        # Show a popup with the user's progress
        progress_message = f"You learned {len(self.learned_words)} out of {self.total_words} words."
        messagebox.showinfo("Progress", progress_message)

        # Quit the entire application
        self.window.destroy()
        sys.exit()

    def ask_for_name(self):
        # Create a new Toplevel window to ask for the user's name
        name_window = tk.Toplevel(self.window)
        name_window.title("Username")
        name_window.geometry("300x100")

        # Function to save the entered name and close the window
        def save_name():
            self.username = name_entry.get().strip()
            name_window.destroy()

        name_label = tk.Label(name_window, text="Enter your name:")
        name_label.pack(pady=5)
        name_entry = tk.Entry(name_window)
        name_entry.pack(pady=5)
        name_entry.focus_set()  # Set focus to the entry widget
        name_entry.bind('<Return>', lambda event: save_name())  # Allow pressing Enter to save the name

        save_button = tk.Button(name_window, text="Save", command=save_name)
        save_button.pack(pady=5)

        # Make sure the Toplevel window remains on top until the name is provided
        name_window.transient(self.window)
        name_window.grab_set()

        # Run the Toplevel window's event loop
        name_window.wait_window()

    def run(self):
        # Ask for the user's name using the new method ask_for_name
        self.ask_for_name()

        # Run the main loop of the window
        self.window.mainloop()

# Function to start the language learning app
def start_flashcard_app():
    # Hide the start screen
    root.withdraw()

    # Create an instance of the FlashcardApp class
    app = FlashcardApp()

    # Run the app
    app.run()

# Create a new tk.Tk() instance for the start screen
root = tk.Tk()
root.title("Start Screen")
root.geometry("600x500")
root.resizable(False, False)

# Load and process the animated GIF
file = "introVid.gif"
frames = Image.open(file)
image_frame_list = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(frames)]

# Function to animate the frames of the GIF
def animation(count, seconds):
    im = image_frame_list[count]
    gif_label.configure(image=im)
    count += 1
    if count < len(image_frame_list):
        root.after(50, lambda: animation(count, seconds))
    else:
        # After the animation finishes, start the FlashcardApp
        start_flashcard_app()
        hide_start()

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
image_button1 = tk.Button(root, image=photo1, bg="#F1EFE7", borderwidth=0, highlightthickness=0, command=lambda: animation(0, 10))
image_button1.pack(pady=(100, 50))

# Start the main event loop for the start screen
root.mainloop()
