# Datheon Python Programming

A collection of Python projects built during my Datheon Python Programming remote internship. Each project lives in its own folder and runs from the terminal.

| # | Project | What it does |
|---|---------|--------------|
| 1 | [Hangman Word Guessing Game](#1-hangman-word-guessing-game) | Console word game with difficulty levels |
| 2 | [Stock Portfolio Performance Tracker](#2-stock-portfolio-performance-tracker) | Calculates portfolio value and logs results to CSV |
| 3 | [Automated File Organizer & Cleanup Utility](#3-automated-file-organizer--cleanup-utility) | Sorts files into category folders by extension |
| 4 | [Rule-Based Interactive Terminal Assistant](#4-rule-based-interactive-terminal-assistant-chatbot) | FAQ chatbot using keyword and regex matching |

## Requirements

- Python 3.8 or higher
- `yfinance` (only for the Stock Portfolio Tracker)

```bash
pip install yfinance
```

## Repository Structure

```
Datheon_Python_Programming_Git/
├── Hangman_Word_Guessing_Game_Console/
│   ├── hangman.py
│   └── google-10000-english-no-swears.txt
├── Stock_Portfolio_Performance_Tracker/
│   ├── tracker.py
│   ├── constituents.csv
│   └── portfolio_summary.csv
├── Automated_File_Organizer_&_Cleanup_Utility/
│   └── organizer.py
└── Rule_Based_Interactive_Terminal_Assisstant_Chatbot/
    ├── chatbot.py
    └── sample_faq.json
```

> Run each script from inside its own folder. If a folder name contains `&`, wrap the path in quotes in PowerShell, e.g. `cd "Automated_File_Organizer_&_Cleanup_Utility"`.

---

## 1. Hangman Word Guessing Game

A console Hangman game. The secret word is picked at random from a 10,000-word English list.

**Features**
- Three difficulty levels: Easy (3-5 letters), Medium (6-8 letters), Hard (9+ letters)
- 6 attempts with ASCII hangman drawings that update after each mistake
- Input validation: only single English letters are accepted, and repeated guesses are rejected
- Option to play again after each game

**Run**
```bash
cd Hangman_Word_Guessing_Game_Console
py hangman.py
```

---

## 2. Stock Portfolio Performance Tracker

Takes S&P 500 stocks the user holds, fetches the latest prices from Yahoo Finance, and reports how the portfolio is performing.

**Features**
- Validates stock symbols against `constituents.csv` (S&P 500 dataset) and shows the company and sector
- Asks for buy price and number of shares, with input validation
- Prevents adding the same stock twice
- Prints a formatted table with value and profit/loss in dollars and percent for each stock, plus portfolio totals
- Appends every run to `portfolio_summary.csv` with a timestamp and a TOTAL row

**Run**
```bash
cd Stock_Portfolio_Performance_Tracker
pip install yfinance
py tracker.py
```

Enter a stock symbol (for example `AAPL`), then the buy price and number of shares. Type `DONE` to finish and see the summary.

> Prices come from Yahoo Finance and may be delayed. This is not a live trading feed.

---

## 3. Automated File Organizer & Cleanup Utility

Organizes a cluttered folder (the Downloads folder by default) by moving files into category subfolders based on their extension.

**Features**
- Categories: `Documents`, `Images`, `Videos`, `Archives`, `Code`
- Category folders are created only when needed
- Uses `os.scandir()` to inspect files and `shutil.move()` to relocate them
- Naming collisions are handled safely: an existing `report.pdf` is never overwritten, the new file becomes `report (1).pdf`
- `PermissionError` and `FileExistsError` are caught so one problem file does not stop the run
- Files with unknown extensions are left in place
- Prints each move and an execution summary with the total files relocated

**Run**
```bash
cd "Automated_File_Organizer_&_Cleanup_Utility"
py organizer.py
```

The target folder is set by `TARGET_DIR` near the top of `organizer.py`. To add more file types, extend `EXTENSION_MAP`.

---

## 4. Rule-Based Interactive Terminal Assistant (Chatbot)

A rule-based support chatbot that answers questions from a JSON FAQ dataset.

**Features**
- Normalizes user input (lowercase, trimmed, punctuation removed) and extracts keywords with regular expressions
- Matches the input against FAQ questions using a keyword confidence score
- Handles greetings, business hours, and FAQ queries
- Conversation flow: greeting, intent identification, resolution, exit
- Fallback response for unrecognized queries
- Clean exit with `bye`
- Error handling for a missing or invalid JSON file

**Run**
```bash
cd Rule_Based_Interactive_Terminal_Assisstant_Chatbot
py chatbot.py
```

**Example**
```
Bot: Hello! Ask me a question, or type 'bye' to exit.
You: hello
Bot: Hello! How can I help you today?
You: what are your hours
Bot: We operate Monday through Friday from 9:00 AM to 6:00 PM IST.
Bot: Is there anything else I can help with?
You: bye
Bot: Goodbye! Have a great day.
```

To change what the bot knows, edit the `greetings` and `faqs` entries in `sample_faq.json`.