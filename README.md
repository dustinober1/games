# 🎮 Games Collection

A collection of classic games implemented in Python using tkinter for the graphical user interface.

## 🎯 Games Included

### 🔢 Sudoku Solver
- **Location**: `Sudoku/app.py`
- **Description**: A fully functional Sudoku puzzle solver with an intuitive graphical interface
- **Features**:
  - 9x9 grid with proper visual separation of 3x3 blocks
  - Input validation to prevent invalid entries
  - Automatic puzzle solving using backtracking algorithm
  - Visual distinction between original numbers and solved numbers
  - Clear and solve functionality
  - Error detection for invalid puzzle configurations

### ❌⭕ Tic Tac Toe
- **Location**: `TicTacToe/app.py`
- **Description**: Classic 3x3 Tic Tac Toe game for two players
- **Features**:
  - Clean 3x3 grid interface
  - Two-player gameplay (X and O)
  - Win detection for rows, columns, and diagonals
  - Tie game detection
  - New game functionality
  - Visual feedback for current player and game status

## 🚀 How to Run

### Option 1: Game Launcher (Recommended)
Run the main launcher to choose between games:
```bash
python app.py
```

### Option 2: Individual Games
Run games directly:

**Sudoku:**
```bash
python Sudoku/app.py
```

**Tic Tac Toe:**
```bash
python TicTacToe/app.py
```

## 📋 Requirements

- Python 3.x
- tkinter (usually comes with Python installation)

## 🎮 How to Play

### Sudoku
1. Launch the Sudoku game
2. Enter numbers (1-9) in the empty cells
3. Click "Solve" to automatically complete the puzzle
4. Click "Clear" to start over
5. The solver will highlight solved numbers in blue

### Tic Tac Toe
1. Launch the Tic Tac Toe game
2. Players take turns clicking on empty squares
3. First player is X, second player is O
4. Get three in a row (horizontally, vertically, or diagonally) to win
5. Click "New Game" to start over

## 📁 Project Structure

```
games/
├── app.py                 # Main game launcher
├── README.md             # This file
├── Sudoku/
│   └── app.py           # Sudoku solver game
└── TicTacToe/
    └── app.py           # Tic Tac Toe game
```

## 🤝 Contributing

Feel free to add more games to this collection! Follow the existing structure:
1. Create a new folder for your game
2. Add an `app.py` file with your game implementation
3. Update the main launcher to include your game
4. Update this README

## 📝 License

This project is open source and available under the MIT License.