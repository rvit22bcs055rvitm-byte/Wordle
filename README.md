# 🟩 Wordle Game (Python)

A feature-rich Wordle clone built using **Python**, **Pygame**, and **CustomTkinter**.  
This project combines a **Pygame main menu** with a **CustomTkinter game interface**, offering a fun and interactive experience.

---

## 🎮 Features

- ✅ **Wordle Gameplay** – Guess a 5-letter word in 6 attempts  
- ⌛ **Countdown Timer** – 60 seconds per attempt, resets automatically after each guess  
- 🟩 **Color Feedback**  
  - Green: Correct letter & position  
  - Yellow: Correct letter, wrong position  
  - Red: Incorrect letter  
- 🖥️ **Virtual On-Screen Keyboard** with Enter (✓) and Backspace (⌫) support  
- 🧩 **Hints System** – Get limited hints to help guess the word  
- 🏆 **Scoring System**  
  - Base score for winning  
  - Bonus for unused attempts  
  - Bonus for remaining time  
- 🎨 **Custom UI Styling** with **CustomTkinter**  
- 📜 **Instructions Screen** in the Pygame menu  

---

## 🛠️ Tech Stack

- **Python 3.x**
- [Pygame](https://www.pygame.org/) – for menu & instruction screen  
- [Tkinter](https://docs.python.org/3/library/tkinter.html) – for GUI window  
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) – modern Tkinter styling  

---

## 📂 Project Structure

├── wordle_game.py # Main game file
├── wordlist.txt # Word bank (list of valid 5-letter words)
├── initial.png # Background for main menu
├── bg.png # Background for instructions screen
└── README.md # Project documentation

yaml
Copy code

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/wordle-game.git
cd wordle-game
2. Install dependencies
bash
Copy code
pip install pygame customtkinter
3. Run the game
bash
Copy code
python wordle_game.py
🎯 How to Play
Start the game from the Pygame main menu.

Guess the 5-letter word within 6 attempts.

Use either:

Your physical keyboard

The on-screen virtual keyboard (with ✓ for Enter and ⌫ for Backspace).

Keep an eye on the 60s timer for each attempt.

Win points based on attempts left & remaining time.

🖼️ Screenshots
(Add screenshots of your menu, game, and results here)

✨ Future Improvements
 Add difficulty levels (Easy, Medium, Hard)

 Save high scores

 Daily challenge mode

 Multiplayer (vs mode)
