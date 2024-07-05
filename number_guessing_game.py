import tkinter as tk
from tkinter import messagebox
import random

def setup_window(root):
    # Set the title of the window
    root.title("Number Guessing Game")
    # Set the dimensions of the window
    root.geometry("800x800")

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.lower_bound = 1
        self.upper_bound = 100
        # Generate a random number to guess
        self.number_to_guess = random.randint(self.lower_bound, self.upper_bound)
        self.attempts = 0
        self.max_attempts = 10
        # Create the widgets for the game
        self.create_widgets()

    def create_widgets(self):
        # Add a label to prompt the user to guess the number
        tk.Label(self.root, text="Guess the number between 1 and 100").pack(pady=20)
        # Add an entry widget for the user to enter their guess
        self.guess_entry = tk.Entry(self.root)
        self.guess_entry.pack(pady=10)
        # Add a button to submit the guess
        self.guess_button = tk.Button(self.root, text="Guess", command=self.check_guess)
        self.guess_button.pack(pady=10)
        # Add a label to display the result of the guess
        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack(pady=10)

    def check_guess(self):
        try:
            # Get the guess from the entry widget and convert to an integer
            guess = int(self.guess_entry.get())
        except ValueError:
            # Show an error message if the input is not a valid number
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            return
        
        # Increment the attempts counter
        self.attempts += 1

        if guess < self.number_to_guess:
            # If the guess is too low, update the result label
            self.result_label.config(text="Too low!")
        elif guess > self.number_to_guess:
            # If the guess is too high, update the result label
            self.result_label.config(text="Too high!")
        else:
            # If the guess is correct, update the result label and end the game
            self.result_label.config(text="Congratulations! You guessed the number")
            self.end_game()
            return
        
        if self.attempts >= self.max_attempts:
            # If the user has used all their attempts, update the result label and end the game
            self.result_label.config(text=f"Sorry, you've used all {self.max_attempts} attempts. The number was {self.number_to_guess}")
            self.end_game()

    def end_game(self):
        # Disable the guess button
        self.guess_button.config(state=tk.DISABLED)
        # Ask the user if they want to play again
        play_again = messagebox.askyesno("Play Again", "Do you want to play again?")
        if play_again:
            # If the user wants to play again, reset the game
            self.reset_game()
        else:
            # If the user doesn't want to play again, quit the application
            self.root.quit()

    def reset_game(self):
        # Generate a new random number to guess
        self.number_to_guess = random.randint(self.lower_bound, self.upper_bound)
        # Reset the attempts counter
        self.attempts = 0
        # Clear the entry widget
        self.guess_entry.delete(0, tk.END)
        # Enable the guess button
        self.guess_button.config(state=tk.NORMAL)
        # Clear the result label
        self.result_label.config(text="")

if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    # Set up the window
    setup_window(root)
    # Create the game instance
    game = NumberGuessingGame(root)
    # Start the Tkinter event loop
    root.mainloop()
