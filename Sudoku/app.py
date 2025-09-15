import tkinter as tk
from tkinter import messagebox, filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk
import pytesseract
import os

class SudokuGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sudoku Solver")
        master.geometry("470x570") 

        self.cells = {}
        self.create_grid()
        self.create_buttons()

    def create_grid(self):
        grid_frame = tk.Frame(self.master)
        grid_frame.pack(pady=20)

        # Outer frame for a border around the entire grid (optional, but nice)
        outer_board_frame = tk.Frame(grid_frame, bd=2, relief=tk.SOLID, bg="black")
        outer_board_frame.pack()

        for i in range(9):
            for j in range(9):
                # Determine padding for 3x3 block separation
                pad_x_val = (5, 1) if (j + 1) % 3 == 0 and j < 8 else (1, 1)
                pad_y_val = (5, 1) if (i + 1) % 3 == 0 and i < 8 else (1, 1)

                # If it's the last column/row in a 3x3 block but not the very last one on the grid
                if (j + 1) % 3 == 0 and j < 8:
                    col_padx = (1, 5) # Larger padding on the right
                else:
                    col_padx = (1, 1)

                if (i + 1) % 3 == 0 and i < 8:
                    row_pady = (1, 5) # Larger padding on the bottom
                else:
                    row_pady = (1, 1)


                cell_frame = tk.Frame(
                    outer_board_frame, # Place cells inside the outer_board_frame
                    width=40,
                    height=40,
                    # Simpler background, let borders do the work
                    bg='white',
                    highlightbackground="darkgrey", # Thinner lines between cells
                    highlightcolor="darkgrey",
                    highlightthickness=1
                )
                # Apply conditional padding for 3x3 block effect
                cell_frame.grid(row=i, column=j, padx=col_padx, pady=row_pady)
                cell_frame.pack_propagate(False)

                entry = tk.Entry(
                    cell_frame,
                    width=2,
                    font=('Arial', 18, 'bold'),
                    justify='center',
                    bd=0,
                    highlightthickness=0,
                    # Differentiate fixed numbers if you want later
                    # disabledbackground="lightgrey",
                    # disabledforeground="black"
                )
                entry.pack(expand=True, fill='both')
                self.cells[(i, j)] = entry

    def create_buttons(self):
        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=10)

        upload_button = tk.Button(
            button_frame,
            text="Upload Image",
            font=('Arial', 14),
            command=self.upload_image,
            bg='lightblue',
            fg='darkblue'
        )
        upload_button.pack(side=tk.LEFT, padx=10)

        solve_button = tk.Button(
            button_frame,
            text="Solve",
            font=('Arial', 14),
            command=self.solve_sudoku_gui
        )
        solve_button.pack(side=tk.LEFT, padx=10)

        clear_button = tk.Button(
            button_frame,
            text="Clear",
            font=('Arial', 14),
            command=self.clear_grid
        )
        clear_button.pack(side=tk.LEFT, padx=10)

    def get_board(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.cells[(i, j)].get()
                if val.isdigit() and 1 <= int(val) <= 9:
                    row.append(int(val))
                else:
                    self.cells[(i,j)].delete(0, tk.END) # Clear invalid input
                    row.append(0) # 0 represents an empty cell
            board.append(row)
        return board

    def set_board(self, board, solved=True):
        for i in range(9):
            for j in range(9):
                self.cells[(i, j)].delete(0, tk.END)
                if board[i][j] != 0:
                    self.cells[(i, j)].insert(0, str(board[i][j]))
                    if solved: # Optionally change color for solved cells
                        self.cells[(i, j)].config(fg="blue")
                else:
                    self.cells[(i, j)].config(fg="black") # Reset color for empty cells


    def clear_grid(self):
        for i in range(9):
            for j in range(9):
                self.cells[(i, j)].delete(0, tk.END)
                self.cells[(i, j)].config(fg="black") # Reset text color

    def solve_sudoku_gui(self):
        board = self.get_board()
        # Make a deep copy for the solver to work on, so initial numbers remain black
        solve_board = [row[:] for row in board]

        # Store initial state to differentiate original numbers
        initial_board_state = [[board[r][c] != 0 for c in range(9)] for r in range(9)]


        if self.is_valid_initial_board(solve_board):
            if self.solve_sudoku_algorithm(solve_board):
                self.set_board_solved(solve_board, initial_board_state) # Pass initial state
                messagebox.showinfo("Sudoku Solver", "Puzzle Solved!")
            else:
                messagebox.showerror("Sudoku Solver", "No solution exists for this puzzle.")
        else:
            messagebox.showerror("Sudoku Solver", "Invalid Sudoku board. Check for duplicate numbers in rows, columns, or 3x3 subgrids.")

    def set_board_solved(self, board, initial_state):
        for i in range(9):
            for j in range(9):
                self.cells[(i, j)].delete(0, tk.END)
                if board[i][j] != 0:
                    self.cells[(i, j)].insert(0, str(board[i][j]))
                    if not initial_state[i][j]: # If it was not an initial number
                        self.cells[(i, j)].config(fg="blue")
                    else:
                        self.cells[(i, j)].config(fg="black") # Original numbers remain black
                else: # Should not happen in a solved board, but good practice
                     self.cells[(i,j)].config(fg="black")


    def is_valid_initial_board(self, board):
        # Check rows
        for r in range(9):
            seen = set()
            for c in range(9):
                num = board[r][c]
                if num != 0:
                    if num in seen:
                        return False
                    seen.add(num)

        # Check columns
        for c in range(9):
            seen = set()
            for r in range(9):
                num = board[r][c]
                if num != 0:
                    if num in seen:
                        return False
                    seen.add(num)

        # Check 3x3 subgrids
        for box_r in range(3):
            for box_c in range(3):
                seen = set()
                for r in range(box_r * 3, box_r * 3 + 3):
                    for c in range(box_c * 3, box_c * 3 + 3):
                        num = board[r][c]
                        if num != 0:
                            if num in seen:
                                return False
                            seen.add(num)
        return True

    # --- Sudoku Solving Algorithm (Backtracking) ---
    def find_empty_location(self, board):
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    return (r, c)
        return None

    def is_safe(self, board, row, col, num):
        # Check row
        for c in range(9):
            if board[row][c] == num:
                return False
        # Check column
        for r in range(9):
            if board[r][col] == num:
                return False
        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(3):
            for c in range(3):
                if board[start_row + r][start_col + c] == num:
                    return False
        return True

    def solve_sudoku_algorithm(self, board):
        empty_loc = self.find_empty_location(board)
        if not empty_loc:
            return True

        row, col = empty_loc

        for num in range(1, 10):
            if self.is_safe(board, row, col, num):
                board[row][col] = num
                if self.solve_sudoku_algorithm(board):
                    return True
                board[row][col] = 0 # Backtrack
        return False

    def upload_image(self):
        """Upload and process an image of a sudoku puzzle"""
        # Check if tesseract is available
        try:
            import subprocess
            subprocess.run(['tesseract', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            messagebox.showerror(
                "Tesseract Not Found",
                "Tesseract OCR is not installed on your system.\n\n"
                "To use image upload functionality, please install Tesseract:\n"
                "• macOS: brew install tesseract\n"
                "• Ubuntu/Debian: sudo apt install tesseract-ocr\n"
                "• Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki"
            )
            return
        
        file_path = filedialog.askopenfilename(
            title="Select Sudoku Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                board = self.extract_sudoku_from_image(file_path)
                if board:
                    self.set_board_from_image(board)
                    messagebox.showinfo("Success", "Sudoku board loaded from image!")
                else:
                    messagebox.showerror("Error", "Could not extract sudoku board from image. Please try a clearer image.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process image: {str(e)}")

    def extract_sudoku_from_image(self, image_path):
        """Extract sudoku numbers from an image using OCR"""
        try:
            # Read and preprocess the image
            image = cv2.imread(image_path)
            if image is None:
                return None
                
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply threshold to get binary image
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            
            # Find contours to locate the sudoku grid
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Find the largest rectangular contour (should be the sudoku grid)
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            # Extract the sudoku grid region
            sudoku_region = gray[y:y+h, x:x+w]
            
            # Resize to a standard size for better OCR
            sudoku_region = cv2.resize(sudoku_region, (450, 450))
            
            # Apply additional preprocessing
            sudoku_region = cv2.GaussianBlur(sudoku_region, (5, 5), 0)
            _, sudoku_region = cv2.threshold(sudoku_region, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            
            # Initialize the board
            board = [[0 for _ in range(9)] for _ in range(9)]
            
            # Divide the image into 9x9 cells
            cell_height = sudoku_region.shape[0] // 9
            cell_width = sudoku_region.shape[1] // 9
            
            for row in range(9):
                for col in range(9):
                    # Extract cell
                    y1 = row * cell_height
                    y2 = (row + 1) * cell_height
                    x1 = col * cell_width
                    x2 = (col + 1) * cell_width
                    
                    cell = sudoku_region[y1:y2, x1:x2]
                    
                    # Add padding to improve OCR
                    cell = cv2.copyMakeBorder(cell, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=0)
                    
                    # Use OCR to extract number
                    try:
                        # Configure tesseract for single digit recognition
                        custom_config = r'--oem 3 --psm 10 -c tessedit_char_whitelist=123456789'
                        text = pytesseract.image_to_string(cell, config=custom_config).strip()
                        
                        # Validate and store the number
                        if text.isdigit() and 1 <= int(text) <= 9:
                            board[row][col] = int(text)
                        else:
                            board[row][col] = 0
                    except:
                        board[row][col] = 0
            
            return board
            
        except Exception as e:
            print(f"Error processing image: {e}")
            return None

    def set_board_from_image(self, board):
        """Set the board with numbers extracted from image"""
        for i in range(9):
            for j in range(9):
                self.cells[(i, j)].delete(0, tk.END)
                if board[i][j] != 0:
                    self.cells[(i, j)].insert(0, str(board[i][j]))
                    self.cells[(i, j)].config(fg="darkgreen")  # Different color for image-loaded numbers
                else:
                    self.cells[(i, j)].config(fg="black")

if __name__ == '__main__':
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
