# 🔢 How to Play Sudoku

## Objective
Fill a 9×9 grid with digits 1-9 so that each column, each row, and each of the nine 3×3 subgrids contains all digits from 1 to 9.

## Game Rules
1. **Grid Structure**: The puzzle consists of a 9×9 grid divided into nine 3×3 subgrids (boxes)
2. **Number Placement**: Each cell can contain only one digit from 1 to 9
3. **Row Rule**: Each row must contain all digits 1-9 with no repetition
4. **Column Rule**: Each column must contain all digits 1-9 with no repetition
5. **Box Rule**: Each 3×3 subgrid must contain all digits 1-9 with no repetition

## How to Use This Sudoku Solver

### Manual Entry
1. **Click on any empty cell** to select it
2. **Type a number (1-9)** to enter it in the cell
3. **Press Tab or click another cell** to move to the next cell
4. **Invalid entries will be automatically cleared**

### Image Upload Feature 🆕
1. **Click "Upload Image"** to load a sudoku puzzle from a photo
2. **Select a clear image** of a sudoku puzzle from your device
3. **The solver will automatically extract** numbers using OCR technology
4. **Numbers loaded from images appear in green**

### Solving Functions
- **Solve Button**: Automatically completes the entire puzzle
- **Clear Button**: Removes all numbers from the grid
- **Solved numbers appear in blue** to distinguish them from your entries

## Sudoku Solving Strategies

### Beginner Techniques
1. **Naked Singles**: If a cell can only contain one possible number
2. **Hidden Singles**: If a number can only go in one cell within a row, column, or box
3. **Scanning**: Look for missing numbers in rows, columns, and boxes

### Intermediate Techniques
1. **Naked Pairs**: Two cells in the same unit can only contain the same two numbers
2. **Pointing Pairs**: When a number in a box can only be in one row/column
3. **Box/Line Reduction**: Eliminate candidates based on box and line interactions

### Advanced Techniques
1. **X-Wing**: Advanced elimination pattern across rows and columns
2. **Swordfish**: Complex pattern involving three rows and three columns
3. **Coloring**: Using alternating patterns to eliminate candidates

## Tips for Success

### Starting Out
- **Begin with easier puzzles** to build confidence
- **Look for cells with the fewest possibilities** first
- **Focus on one number at a time** when scanning

### Problem-Solving Approach
- **Work systematically** through rows, columns, and boxes
- **Use pencil marks** (mental notes) for possible numbers
- **Double-check your work** regularly to avoid errors

### Using the Solver
- **Try solving manually first** to practice your skills
- **Use the solver to check your work** or when you're stuck
- **Study the solved puzzle** to learn new patterns

## Common Mistakes to Avoid

1. **Guessing**: Every number should be logically deduced
2. **Rushing**: Take time to consider all possibilities
3. **Ignoring constraints**: Always check row, column, and box rules
4. **Not double-checking**: Verify each number placement

## Image Upload Tips

For best results when uploading puzzle images:
- **Use good lighting** and avoid shadows
- **Ensure the puzzle is flat** and not skewed
- **Keep the image clear** and in focus
- **Crop closely** around the puzzle grid
- **Use high contrast** between numbers and background

## System Requirements

### Basic Features
- Python 3.x with tkinter (included with most Python installations)

### Image Upload Feature
- **Tesseract OCR engine** must be installed:
  - **macOS**: `brew install tesseract`
  - **Ubuntu/Debian**: `sudo apt install tesseract-ocr`
  - **Windows**: Download from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
- **Additional Python packages** (auto-installed when using image feature):
  - opencv-python-headless
  - pytesseract
  - pillow
  - numpy

## Difficulty Levels

- **Easy**: Many naked singles, minimal advanced techniques needed
- **Medium**: Requires hidden singles and basic elimination techniques
- **Hard**: Needs intermediate techniques like naked pairs and pointing pairs
- **Expert**: Requires advanced techniques and complex logical deduction

Enjoy solving puzzles and improving your logical thinking skills! 🧩