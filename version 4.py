# Import necessary modules
import random
import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter import messagebox
import json
import os
import tkinter.ttk as ttk
from PIL import Image, ImageTk, ImageSequence
import sys

# Define the ArabicLearningApp class
class ArabicLearningApp:
    def __init__(self):
        # Initialize instance variables
        self.words = {}                     # Dictionary to store Arabic words and their translations
        self.pronunciations = {}            # Dictionary to store Arabic words and their pronunciations
        self.total_words = 0                # Total number of words in the app
        self.current_word_index = 0         # Index of the currently displayed word
        self._username = ""                 # User's name
        self.learned_words = set()          # Set to store words the user has learned

        # Create the main application window
        self.window = tk.Tk()
        self.window.title("Learn Arabic with Ease")
        self.window.geometry("600x500")
        self.window.resizable(False, False)

        # Set the appearance of the main window
        bg_color = "#E1F3F8"
        fg_color = "#05445E"
        font_family = "Arial"
        self.window.configure(bg=bg_color)

        # Labels to display word, translation, and pronunciation
        self.word_label = tk.Label(self.window, text="", bg=bg_color, fg=fg_color, font=(font_family, 32, "bold"))
        self.word_label.pack(pady=20)
        self.translation_label = tk.Label(self.window, text="", bg=bg_color, fg=fg_color, font=(font_family, 20))
        self.translation_label.pack(pady=10)
        self.pronunciation_label = tk.Label(self.window, text="", bg=bg_color, fg=fg_color, font=(font_family, 16))
        self.pronunciation_label.pack(pady=10)

        # Buttons for navigation and interaction
        button_bg_color = "#B6E3F2"
        button_fg_color = "#05445E"
        button_font = (font_family, 14, "bold")

        self.previous_button = tk.Button(self.window, text="Previous Word", command=self.previous_word, bg=button_bg_color, fg=button_fg_color, font=button_font)
        self.previous_button.pack(side="left", padx=20, pady=20)
        self.next_button = tk.Button(self.window, text="Next Word", command=self.next_word, bg=button_bg_color, fg=button_fg_color, font=button_font)
        self.next_button.pack(side="right", padx=20, pady=20)

        self.learned_button = tk.Button(self.window, text="I know this word", command=self.learned_word, bg=button_bg_color, fg=button_fg_color, font=button_font)
        self.learned_button.pack(pady=20)

        self.quit_button = tk.Button(self.window, text="Quit", command=self.quit_app, bg="#FF5555", fg="white", font=button_font)
        self.quit_button.pack(side="bottom", padx=20, pady=20)

        # Progress bar to show user's progress in learning words
        self.progress_bar = ttk.Progressbar(self.window, length=500, mode='determinate', value=0)
        self.progress_bar.pack(pady=10)

        # Button to review learned words
        self.review_button = tk.Button(self.window, text="Review Learned Words", command=self.review_learned_words, bg=button_bg_color, fg=button_fg_color, font=button_font)
        self.review_button.pack(pady=20)

        # Load words and start displaying the first word
        self.load_words('words_3.json')
        self.display_word()

    def load_words(self, filename):
        # Load words, pronunciations, and user progress from a JSON file
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.words = data.get('words', {})
                self.pronunciations = data.get('pronunciations', {})
                self.total_words = len(self.words)

                self.learned_words = set(data.get('learned_words', []))
                counter = data.get('counter', 0)
                self.progress_bar['value'] = (counter / self.total_words) * 100

    def save_progress(self, filename):
        # Save user's progress and learned words to a JSON file
        data = {
            "username": self._username,
            "counter": len(self.learned_words),
            "learned_words": list(self.learned_words)
        }
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def learned_word(self):
        # Handle when the user marks a word as learned
        current_word = list(self.words.keys())[self.current_word_index]

        if current_word not in self.learned_words:
            self.learned_words.add(current_word)
            self.progress_bar['value'] = (len(self.learned_words) / self.total_words) * 100
            self.next_word()
        else:
            message = f"You already learned the word '{current_word}'."
            messagebox.showinfo("Word Already Learned", message)

    def previous_word(self):
        # Display the previous word in the list
        if self.current_word_index > 0:
            self.current_word_index -= 1
            self.display_word()

        if len(self.learned_words) < self.total_words:
            self.next_button.config(state="normal")

    def next_word(self):
        # Display the next word in the list or wrap around to the first word
        self.current_word_index += 1

        if self.current_word_index >= self.total_words:
            self.current_word_index = 0

        self.display_word()

    def display_word(self):
        # Display the current word's information (word, translation, pronunciation)
        current_word = list(self.words.keys())[self.current_word_index]
        translation = self.words[current_word]
        pronunciation = self.pronunciations.get(current_word, "")

        self.word_label.config(text=current_word)
        self.translation_label.config(text=translation)
        self.pronunciation_label.config(text=pronunciation)

        if len(self.learned_words) == self.total_words:
            self.next_button.config(state="disabled")

    def review_learned_words(self):
        # Show a messagebox with the list of words the user has learned
        if self.learned_words:
            learned_words_str = "\n".join(self.learned_words)
            messagebox.showinfo("Words You Learned", f"Words you learned:\n{learned_words_str}")
        else:
            messagebox.showinfo("Words You Learned", "You haven't learned any words yet.")

    def quit_app(self):
        # Save user progress and show a message with the progress
        self.save_progress("progress.json")

        progress_message = f"You learned {len(self.learned_words)} out of {self.total_words} words."
        messagebox.showinfo("Progress", progress_message)

        # Destroy the window and exit the application
        self.window.destroy()
        sys.exit()

    def ask_for_name(self):
        # Create a popup window to ask for the user's name
        name_window = tk.Toplevel(self.window)
        name_window.title("Username")
        name_window.geometry("300x100")

        # Set appearance of the popup window
        bg_color = "#E1F3F8"
        fg_color = "#05445E"
        font_family = "Arial"
        button_bg_color = "#B6E3F2"
        button_fg_color = "#05445E"
        button_font = (font_family, 14, "bold")

        name_window.configure(bg=bg_color)

        def save_name():
            # Save the user's name and close the popup window
            self._username = name_entry.get().strip()
            name_window.destroy()

        name_label = tk.Label(name_window, text="Enter your name:", bg=bg_color, fg=fg_color, font=(font_family, 14))
        name_label.pack(pady=5)
        name_entry = tk.Entry(name_window, font=(font_family, 12))
        name_entry.pack(pady=5)
        name_entry.focus_set()
        name_entry.bind('<Return>', lambda event: save_name())

        save_button = tk.Button(name_window, text="Save", command=save_name, bg=button_bg_color, fg=button_fg_color, font=button_font)
        save_button.pack(pady=5)

        # Set the popup window to be modal (focus stays on the popup)
        name_window.transient(self.window)
        name_window.geometry(f"+{self.window.winfo_rootx() + 200}+{self.window.winfo_rooty() + 200}")
        name_window.grab_set()

        name_window.wait_window()

    def run(self):
        # Start the application by asking for the user's name and running the main event loop
        self.ask_for_name()
        self.window.mainloop()

def start_arabic_learning_app():
    # Hide the initial start screen, create the ArabicLearningApp instance, and start the learning app
    root.withdraw()

    app = ArabicLearningApp()
    app.run()

# Create the initial start screen window
root = tk.Tk()
root.title("Start Screen")
root.geometry("600x500")
root.resizable(False, False)

# Load GIF animation frames for the start screen
file = "introVid.gif"
frames = Image.open(file)
image_frame_list = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(frames)]

def animation(count, seconds):
    # Function to animate the GIF frames on the start screen
    im = image_frame_list[count]
    gif_label.configure(image=im)
    count += 1
    if count < len(image_frame_list):
        root.after(50, lambda: animation(count, seconds))
    else:
        # Start the Arabic Learning App after animation is complete and hide the start screen
        start_arabic_learning_app()
        hide_start()

# Label to show the GIF animation on the start screen
gif_label = tk.Label(root, image="")
gif_label.pack()

def hide_start():
    # Hide the start screen button
    image_button1.pack_forget()

# Load the image for the start screen button and create the button
image1 = Image.open("start_image.png")
image1 = image1.resize((200, 200))
photo1 = ImageTk.PhotoImage(image1)

image_button1 = tk.Button(root, image=photo1, borderwidth=0, highlightthickness=0, command=lambda: animation(0, 10))
image_button1.pack(pady=(100, 50))

# Start the main event loop for the initial start screen
root.mainloop()
