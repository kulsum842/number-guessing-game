import unittest
from unittest.mock import patch
import tkinter as tk
from number_guessing_game2 import MainApplication, NumberGuessingGame

class TestNumberGuessingGame(unittest.TestCase):
    
    def setUp(self):
        self.root = tk.Tk()
        self.app = MainApplication(self.root)
        
    def tearDown(self):
        self.root.destroy()

    @patch('number_guessing_game.random.randint', return_value=15)
    def test_correct_guess(self, mock_randint):
        self.app.start_game(5, 1, 20)
        game = self.app.number_guessing_game
        
        game.guess_entry.insert(0, '15')
        game.check_guess()
        
        self.assertEqual(game.result_label.cget("text"), "Perfect!")

    @patch('number_guessing_game.random.randint', return_value=15)
    def test_low_guess(self, mock_randint):
        self.app.start_game(5, 1, 20)
        game = self.app.number_guessing_game
        
        game.guess_entry.insert(0, '10')
        game.check_guess()
        
        self.assertEqual(game.result_label.cget("text"), "Low")

    @patch('number_guessing_game.random.randint', return_value=15)
    def test_high_guess(self, mock_randint):
        self.app.start_game(5, 1, 20)
        game = self.app.number_guessing_game
        
        game.guess_entry.insert(0, '20')
        game.check_guess()
        
        self.assertEqual(game.result_label.cget("text"), "High")

    @patch('number_guessing_game.random.randint', return_value=15)
    def test_invalid_input(self, mock_randint):
        self.app.start_game(5, 1, 20)
        game = self.app.number_guessing_game
        
        game.guess_entry.insert(0, 'abc')
        game.check_guess()
        
        self.assertEqual(game.result_label.cget("text"), "Please enter a valid number.")

if __name__ == '__main__':
    unittest.main()
