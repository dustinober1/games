import tkinter as tk
from tkinter import messagebox

class SudokuGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sudoku Solver")
        master.geometry("470x570") # Slightly increased window size for padding
        master.resizable(False, False)

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

if __name__ == '__main__':
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
