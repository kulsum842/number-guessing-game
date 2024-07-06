import tkinter as tk
from tkinter import messagebox
import random

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        self.root.title("Number Guessing Game")
        self.root.geometry("600x400")
        self.root.configure(bg='orange')
        self.root.resizable(False, False)

    def create_widgets(self):
        self.clear_window()

        game_name_label = tk.Label(self.root, text="NUMBER GUESSING GAME", font=("Rubber Stamp", 18), bg='orange')
        game_name_label.pack(pady=10)

        button_frame = tk.Frame(self.root, bg='orange')
        button_frame.pack(expand=True)

        play_icon = tk.Canvas(button_frame, width=70, height=70, bg='orange', highlightthickness=0)
        play_icon.create_polygon([20, 60, 20, 20, 60, 40], fill='green')
        play_icon.grid(row=0, column=0, padx=10)

        play_button = tk.Button(button_frame, text="PLAY", font=("Rubber Stamp", 14), command=self.open_difficulty_selection, bg='orange', fg='black', bd=0, relief=tk.FLAT)
        play_button.grid(row=1, column=0, padx=10, pady=(0, 10))

        exit_icon = tk.Canvas(button_frame, width=70, height=70, bg='orange', highlightthickness=0)
        exit_icon.create_line(60, 20, 20, 60, fill='red', width=4)
        exit_icon.create_line(20, 20, 60, 60, fill='red', width=4)
        exit_icon.grid(row=0, column=1, padx=10)

        exit_button = tk.Button(button_frame, text="EXIT", font=("Rubber Stamp", 14), command=self.root.quit, bg='orange', fg='black', bd=0, relief=tk.FLAT)
        exit_button.grid(row=1, column=1, padx=10, pady=(0, 10))

        self.root.bind('<Return>', lambda event=None: play_button.invoke())

    def open_difficulty_selection(self):
        self.clear_window()
        self.root.configure(bg='orange')

        difficulty_label = tk.Label(self.root, text="SELECT DIFFICULTY LEVEL", font=("Helvetica", 16), bg='orange', fg='black')
        difficulty_label.pack(pady=20)

        button_frame = tk.Frame(self.root, bg='orange')
        button_frame.pack(expand=True)

        easy_button = tk.Button(button_frame, text="➤ EASY", font=("Helvetica", 14), command=lambda: self.start_game(10, 1, 20), bg='orange', fg='black', bd=0, relief=tk.FLAT, anchor='w')
        easy_button.grid(row=0, column=0, pady=10, sticky='w')

        medium_button = tk.Button(button_frame, text="➤ MEDIUM", font=("Helvetica", 14), command=lambda: self.start_game(7, 1, 50), bg='orange', fg='black', bd=0, relief=tk.FLAT, anchor='w')
        medium_button.grid(row=1, column=0, pady=10, sticky='w')

        hard_button = tk.Button(button_frame, text="➤ HARD", font=("Helvetica", 14), command=lambda: self.start_game(5, 1, 100), bg='orange', fg='black', bd=0, relief=tk.FLAT, anchor='w')
        hard_button.grid(row=2, column=0, pady=10, sticky='w')

        go_back_button = tk.Button(self.root, text="GO BACK", font=("Helvetica", 12), command=self.create_widgets, bg='orange', fg='black', bd=0, relief=tk.FLAT)
        go_back_button.pack(side=tk.LEFT, padx=10, pady=20, anchor='sw')

    def start_game(self, max_attempts, lower_bound, upper_bound):
        self.clear_window()
        self.number_guessing_game = NumberGuessingGame(self.root, self, max_attempts, lower_bound, upper_bound)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class NumberGuessingGame:
    def __init__(self, root, main_app, max_attempts, lower_bound, upper_bound):
        self.root = root
        self.main_app = main_app
        self.max_attempts = max_attempts
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.number_to_guess = random.randint(self.lower_bound, self.upper_bound)
        self.attempts = 0
        self.paused = False
        self.create_widgets()

    def create_widgets(self):
        self.top_frame = tk.Frame(self.root, bg='orange')
        self.top_frame.pack(fill=tk.X)

        # Pause button on the first line, right aligned
        self.pause_button = tk.Button(self.top_frame, text="||", font=("Helvetica", 14), command=self.pause_game, bg='orange', fg='black', bd=0)
        self.pause_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Guess range message on the next line
        range_text = f"GUESS A NUMBER BETWEEN {self.lower_bound} AND {self.upper_bound}"
        self.range_label = tk.Label(self.root, text=range_text, font=("Helvetica", 16, "bold"), bg='orange', fg='black')
        self.range_label.pack(pady=10)

        # Input frame, result label, and other widgets
        self.input_frame = tk.Frame(self.root, bg='orange')
        self.input_frame.pack(pady=10)
        
        self.guess_entry = tk.Entry(self.input_frame, font=("Helvetica", 14))
        self.guess_entry.pack(side=tk.LEFT, padx=5)
        self.guess_entry.focus_set()
        self.guess_entry.bind('<Return>', lambda event=None: self.check_guess())

        self.confirm_button = tk.Button(self.input_frame, text="OK", font=("Helvetica", 14), command=self.check_guess)
        self.confirm_button.pack(side=tk.LEFT, padx=5)

        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 12), bg='orange', fg='black', wraplength=500)  # Adjust wrap length as needed
        self.result_label.pack(pady=10)

        # Hint button and OK button
        self.hint_button = tk.Button(self.root, text="HINT", font=("Helvetica", 12), command=self.show_hint_with_ok, bg='orange', fg='black', bd=0)
        self.hint_button.pack(pady=10)

        self.hint_label = tk.Label(self.root, text="", font=("Helvetica", 12), bg='orange', fg='black', wraplength=500)
        self.ok_button = tk.Button(self.root, text="✓", font=("Helvetica", 12), command=self.dismiss_hint, bg='orange', fg='black', bd=0)
    
    def give_hint(self):
        if self.number_to_guess % 2 == 0:
            hint = "The number is even."
        else:
            hint = "The number is odd."
        
        self.hint_label.config(text=hint)
        self.ok_button.pack_forget()
        self.hint_label.pack(pady=10)
        self.ok_button.pack(pady=10)

    def show_hint_with_ok(self):
        self.give_hint()

    def give_hint(self):
        if self.number_to_guess % 2 == 0:
            hint = "The number is even."
        else:
            hint = "The number is odd."
        
        self.hint_label.config(text=hint)
        self.hint_label.pack(pady=10)  # Add padding below the hint label
        self.ok_button.pack(pady=10)  # Add padding between the hint label and tick mark button

    def dismiss_hint(self):
        self.hint_label.pack_forget()
        self.ok_button.pack_forget()




    def check_guess(self):
        if self.paused:
            return

        try:
            guess = int(self.guess_entry.get())
            if guess < self.lower_bound or guess > self.upper_bound:
                raise ValueError("Out of range")
        except ValueError:
            messagebox.showerror("Invalid Input", f"Please enter a valid number between {self.lower_bound} and {self.upper_bound}.")
            return
        
        self.attempts += 1

        if guess == self.number_to_guess:
            self.show_result("Perfect!")
        else:
            feedback = self.get_feedback(guess)
            self.result_label.config(text=feedback)
            if self.attempts >= self.max_attempts:
                self.show_result(f"Oops! You used up all the attempts.\nThe number was {self.number_to_guess}")

    def get_feedback(self, guess):
        if guess < self.number_to_guess:
            return "Low"
        else:
            return "High"

    def show_result(self, message):
        self.clear_widgets()

        result_label = tk.Label(self.root, text=message, font=("Helvetica", 20), bg='orange')
        result_label.pack(pady=20)

        button_frame = tk.Frame(self.root, bg='orange')
        button_frame.pack(expand=True)

        play_icon = tk.Canvas(button_frame, width=70, height=70, bg='orange', highlightthickness=0)
        play_icon.create_polygon([20, 60, 20, 20, 60, 40], fill='green')
        play_icon.grid(row=0, column=0, padx=10)

        play_again_button = tk.Button(button_frame, text="PLAY AGAIN", font=("Rubber Stamp", 14), command=self.main_app.create_widgets, bg='orange', fg='black', bd=0, relief=tk.FLAT)
        play_again_button.grid(row=1, column=0, padx=10, pady=(0, 10))

        exit_icon = tk.Canvas(button_frame, width=70, height=70, bg='orange', highlightthickness=0)
        exit_icon.create_line(60, 20, 20, 60, fill='red', width=4)
        exit_icon.create_line(20, 20, 60, 60, fill='red', width=4)
        exit_icon.grid(row=0, column=1, padx=10)

        exit_button = tk.Button(button_frame, text="EXIT", font=("Rubber Stamp", 14), command=self.root.quit, bg='orange', fg='black', bd=0, relief=tk.FLAT)
        exit_button.grid(row=1, column=1, padx=10, pady=(0, 10))

    def pause_game(self):
        self.paused = True
        self.clear_widgets()

        button_frame = tk.Frame(self.root, bg='orange')
        button_frame.pack(expand=True)

        resume_icon = tk.Canvas(button_frame, width=70, height=70, bg='orange', highlightthickness=0)
        resume_icon.create_polygon([20, 60, 20, 20, 60, 40], fill='green')
        resume_icon.grid(row=0, column=0, padx=10)

        resume_button = tk.Button(button_frame, text="RESUME", font=("Rubber Stamp", 14), command=self.resume_game, bg='orange', fg='black', bd=0, relief=tk.FLAT)
        resume_button.grid(row=1, column=0, padx=10, pady=(0, 10))

        exit_icon = tk.Canvas(button_frame, width=70, height=70, bg='orange', highlightthickness=0)
        exit_icon.create_line(60, 20, 20, 60, fill='red', width=4)
        exit_icon.create_line(20, 20, 60, 60, fill='red', width=4)
        exit_icon.grid(row=0, column=1, padx=10)

        exit_button = tk.Button(button_frame, text="EXIT", font=("Rubber Stamp", 14), command=self.root.quit, bg='orange', fg='black', bd=0, relief=tk.FLAT)
        exit_button.grid(row=1, column=1, padx=10, pady=(0, 10))

        how_to_play_icon = tk.Canvas(self.root, width=70, height=70, bg='orange', highlightthickness=0)
        how_to_play_icon.create_text(35, 35, text="?", font=("Helvetica", 30), fill='blue')
        how_to_play_icon.pack(side=tk.RIGHT, padx=10, pady=10)

        how_to_play_button = tk.Button(self.root, text="HOW TO PLAY", font=("Rubber Stamp", 14), command=self.show_how_to_play, bg='orange', fg='black', bd=0, relief=tk.FLAT)
        how_to_play_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def resume_game(self):
        self.paused = False
        self.clear_widgets()
        self.create_widgets()

    def show_how_to_play(self):
        messagebox.showinfo("How to Play", "Guess the number within the specified range. You have a limited number of attempts to guess the correct number. Use the hints to guide your guesses.")

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
