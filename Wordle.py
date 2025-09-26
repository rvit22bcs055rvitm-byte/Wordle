import pygame
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import random
from collections import deque

# Pygame initialization
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 184)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

image = pygame.image.load("wb.png")
image_rect = image.get_rect()
image_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

inst_image = pygame.image.load("kny.jpeg")
inst_image_rect = inst_image.get_rect()
inst_image_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Fonts
BIG_FONT = pygame.font.Font(None, 36)

class WordleGameInstructions:
    def __init__(self, screen):
        self.screen = screen
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

            self.screen.fill(BLACK)
            self.screen.blit(inst_image, inst_image_rect)
            
            #Instructions - Uses Lists
            instructions_text = [
                "How to Play Wordle:",
                "",
                "Guess a 5-letter word within 6 attempts.",
                "Feedback will be provided after each guess:",
                "Green - Correct letter in the correct position",
                "Yellow - Correct letter in the wrong position",
                "Red - Incorrect letter",
                "",
                "Press ESC to go back",
            ]
            y_offset = 150
            for line in instructions_text:
                text_surface = BIG_FONT.render(line, True, WHITE)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                self.screen.blit(text_surface, text_rect)
                y_offset += 40

            pygame.display.flip()

#Initiallizing the Game Window
class InitialWindow:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Wordle Game")

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_game_button.rect.collidepoint(event.pos):
                        self.start_wordle_game()
                    if how_to_play_button.rect.collidepoint(event.pos):
                        instructions_window = WordleGameInstructions(self.screen)
                        instructions_window.run()

            self.screen.fill(BLACK)
            self.screen.blit(image, image_rect)

            # Draw buttons
            how_to_play_button.draw(self.screen)
            start_game_button.draw(self.screen)

            pygame.display.flip()

        pygame.quit()

    def start_wordle_game(self):
        root = ctk.CTk()
        game_window = WordleGame(root)
        game_window.run()

#Game window
class WordleGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Wordle Game")
        self.master.configure(bg="black")

        # Timer settings
        self.time_limit = 60                # 60 seconds for each attempt
        self.timer_id = None                # To keep track of the timer's after() ID

        # Vibrant color scheme
        self.correct_color = "#66E600"      # Bright green
        self.present_color = "#FFED04"      # Sunny yellow
        self.absent_color = "#EC3500"       # Vibrant red
        self.default_bg = "#121213"
        self.text_color = "black"
        self.button_bg = "#007BFF"          # Bright blue
        self.button_fg = "white"
        self.initialize_game()

    #Initiallizing the Game
    def initialize_game(self):
        self.target_word = self.get_random_word()
        self.attempts = 0
        self.max_attempts = 6
        self.score=0
        self.time_left = self.time_limit
        
        #Hints - Uses Queues and Lists
        self.hints = deque(
            [
                "Start with vowels.",
                "Common letters: E, A, R, I, O, T, N, S",
                "Y sometimes acts as a vowel.",
            ]
        )

        # Cancel previous timer if any
        if self.timer_id is not None:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None

        # Clear the previous game's widgets, if any.
        for widget in self.master.winfo_children():
            widget.destroy()

        self.create_widgets()
        self.update_timer()                 # Start the timer
        pass
    
    def run(self):
        self.master.mainloop()

    def create_keyboard(self):
        self.keyboard_frame = ctk.CTkFrame(self.master, fg_color="#242424")
        self.keyboard_frame.pack(pady=(5, 20))
        
        # Define keyboard layout - Uses Lists
        rows = [
            'QWERTYUIOP',
            'ASDFGHJKL',
            'ZXCVBNM',
            '⌫✓'
        ]

        # Keep track of button widgets in a 'dictionary'
        self.keyboard_buttons = {}
        
        for row_index, row in enumerate(rows):
            frame = ctk.CTkFrame(self.keyboard_frame)
            frame.pack()
            
            for letter in row:
                # Command to be executed on click
                cmd = lambda char=letter: self.on_keyboard_press(char)
                button_text = '⌫' if letter == '⌫' else '✓' if letter == '✓' else letter                    # Adjust button text for special keys
                button = ctk.CTkButton(frame, text=button_text, command=cmd,font=("Comic Sans MS",18,"bold"), width=40, height=40, fg_color=self.default_bg, text_color="white")
                button.pack(side='left', padx=2, pady=2)
                self.keyboard_buttons[letter] = button

    def on_keyboard_press(self, char):
        if char == '⌫':                       # Backspace key
            current_text = self.entry.get()
            # Remove the last character from the entry widget
            self.entry.delete(len(current_text) - 1, tk.END)
        elif char == '✓':                      # Enter key
            guess = self.entry.get().upper()
            if len(guess) != 5 or not guess.isalpha():
                messagebox.showerror("Error", "Please enter a valid 5-letter word.")
                self.entry.delete(0, tk.END)                    # Clear entry box to allow for immediate retry without manual clearing.
                return                                          # Exit the method if the guess is invalid
            self.process_guess(guess)                           # Process the guess if it's valid
            self.reset_timer()                                  # Reset the timer
        else:
            self.entry.insert(tk.END, char)      

    #Fetches a random word from the Wordlist text document using 'random' module
    def get_random_word(self):
        with open("wordlist.txt", "r") as f:
            words = [line.strip().upper() for line in f.readlines() if len(line.strip()) == 5]
        return random.choice(words)

    #Widgits
    def create_widgets(self):
        
        #Score button
        self.score_label = ctk.CTkButton(self.master, text=f"Score: {self.score}", width=20, font=("Comic Sans MS", 20, "bold"), fg_color="transparent", text_color="#5DB8E2", hover_color="#242424", border_width=2, border_color="#5DB8E2")
        self.score_label.pack(side="top",anchor="ne",padx=(10, 10), pady=(10, 10))

        #Letter Box Frame
        self.game_frame = ctk.CTkFrame(self.master, fg_color="#242424")
        self.game_frame.pack(padx=10, pady=10)

        #Creating Boxes
        self.labels = [
            [
                tk.Label(self.game_frame,text="     ",font=("Comic Sans MS", 30),width=2,bg=self.default_bg,fg=self.text_color,borderwidth=2,relief="groove")
               
                for _ in range(5)
            ]
            for _ in range(self.max_attempts)
        ]
        for i, row in enumerate(self.labels):
            for j, label in enumerate(row):
                label.grid(row=i, column=j, padx=2, pady=2)

        #Timer
        self.timer_label = ctk.CTkButton(self.master,text=f"Time left: {self.time_limit}s",font=("Comic Sans MS", 20, "bold"),fg_color="transparent",text_color="#F1D5AD",hover_color="#242424", border_width=2,border_color="#F1D5AD")
        self.timer_label.pack(pady=(5, 10))

        #Text Entry Box
        self.entry = tk.Entry(self.master,font=("Comic Sans MS", 24),width=26,justify="center",bg="#f0f0f0",fg=self.text_color,borderwidth=2)
        self.entry.pack(pady=(5, 10))
        self.entry.bind("<Return>", self.check_guess)

        #New Game Button
        self.new_game_button = ctk.CTkButton(self.master,text="New Game!!!",command=self.initialize_game,width=20,font=("Comic Sans MS", 22,"bold"),fg_color="transparent",text_color="#E6B5F4", border_width=2,border_color="#E6B5F4")
        self.new_game_button.pack(side="bottom",fill="x")

        #Hint Button
        self.hint_button = ctk.CTkButton(self.master,text="💡",command=self.use_hint,width=18,font=("Comic Sans MS", 20,"bold"),fg_color="transparent",text_color="#FFFF00", border_width=2,border_color="#FFFFFF")
        self.hint_button.pack(side="bottom", padx=(1475,1) ,pady=(1, 20))

        #Keyboard
        self.create_keyboard()

    def update_timer(self):
        if self.time_left > 0:
            self.timer_label.configure(text=f"Time left: {self.time_left}s")
            self.time_left -= 1
            # Cancel any existing timer before setting a new one
            if self.timer_id is not None:
                self.master.after_cancel(self.timer_id)
            self.timer_id = self.master.after(1000, self.update_timer)
        else:
            messagebox.showwarning("Time's up!", "Out of time! Moving to the next attempt.")
            self.check_guess(time_up=True)

    def check_guess(self, event=None, time_up=False):
        if not time_up:
            guess = self.entry.get().upper()
            if len(guess) != 5 or not guess.isalpha():
                    messagebox.showerror("Error", "Please enter a valid 5-letter word.")
                    self.entry.delete(0, tk.END)      # Clear entry box to allow for immediate retry without manual clearing.
                    return
            
        else:
            guess = ""                                # Empty guess on time up

        # Cancel the timer when a guess is checked to prevent acceleration issue.
        if self.timer_id is not None:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None

        if self.attempts < self.max_attempts:
            self.process_guess(guess)
            # Reset timer for the next attempt, regardless of time up or user guess.
            self.reset_timer()

    def reset_timer(self):
        self.time_left = self.time_limit
        self.update_timer()                           # Restart the timer with the full time limit

    def process_guess(self, guess):
        guess = self.entry.get()
        guess = guess.upper()
        correct_count = 0
        for i, char in enumerate(guess):
            self.labels[self.attempts][i]["text"] = char if char else "?"
            #Correct Letter, in the right position
            if char and char == self.target_word[i]:
                self.labels[self.attempts][i]["bg"] = self.correct_color
                self.keyboard_buttons[char].configure(fg_color = self.correct_color,text_color="black")
                correct_count += 1
            #Present in the word, but in the wrong position    
            elif char and char in self.target_word:
                self.labels[self.attempts][i]["bg"] = self.present_color
                self.keyboard_buttons[char].configure(fg_color = self.present_color,text_color="black")
            #Not Present in the word  
            else:
                self.labels[self.attempts][i]["bg"] = self.absent_color
                self.keyboard_buttons[char].configure(fg_color = self.absent_color,text_color="black")
        self.attempts += 1
        self.entry.delete(0, tk.END)

        if correct_count == 5:
            # Calculate score based on attempts and time left
            self.score += 1000                                                  # Base score for correct guess
            self.score += (self.max_attempts - self.attempts) * 100             # Bonus for unused attempts
            self.score += self.time_left * 10                                   # Bonus for remaining time
            messagebox.showinfo("Wordle Game", "Correct! Well done.")
            self.score_label.configure(text=f"Score: {self.score}")             # Update the score label
            self.end_game()
        elif self.attempts == self.max_attempts:
            messagebox.showinfo("Wordle Game", f"Game Over! The word was: {self.target_word}")
            self.end_game()

    def use_hint(self):
        if self.hints:
            hint = self.hints.popleft()
            messagebox.showinfo("Hint", hint)
        else:
            messagebox.showinfo("Hint", "No more hints left!")

    def end_game(self):
        self.entry.configure(state="disabled")
        self.new_game_button.focus_set()
        if self.timer_id is not None:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None
        self.timer_label.configure(text="Time's up!")
        
        # Determine medal based on the score
        if self.score >= 1700:
            medal = "Gold Medal 🥇"
        elif self.score >= 1350:
            medal = "Silver Medal 🥈"
        elif self.score >= 1000:
            medal = "Bronze Medal 🥉"
        else:
            medal = "No Medal 👀"
            
        # Display end game message with medal
        end_game_message = f"Game Over! Your score: {self.score}\n{medal}"
        messagebox.showinfo("Wordle Game", end_game_message)

class Button:
    def __init__(self, x, y, width, height, text, bg_color, text_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect)
        text_surface = BIG_FONT.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

# Create buttons
how_to_play_button = Button(225, 325, 350, 50, "How to Play", BLUE, WHITE)
start_game_button = Button(225, 225, 350, 50, "Start Game", BLUE, WHITE)

# Run the initial window
if __name__ == "__main__":
    initial_window = InitialWindow()
    initial_window.run()
