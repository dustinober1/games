import tkinter as tk
from tkinter import messagebox, filedialog
import random
import time
import json
import os


class MinesweeperGUI:
    def __init__(self, master, rows=9, cols=9, mines=10):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.first_click = True
        self.start_time = None
        self.timer_id = None
        self.difficulty = 'Beginner'

        master.title("Minesweeper")
        master.resizable(False, False)

        # Visual style variables
        self.cell_bg = '#d9d9d9'
        self.revealed_bg = '#ffffff'
        self.mine_bg = '#ffcccb'
        self.flag_bg = '#ffd700'
        self.font = ('Segoe UI', 11, 'bold')

        self.cells = {}  # button widgets
        self.model = [[{'mine': False, 'revealed': False, 'flagged': False, 'count': 0} for _ in range(cols)] for _ in range(rows)]
        self.undo_stack = []  # store actions for undo
        self.images = {}  # keep references to PhotoImage
        # attempt to load optional icons (flag.png, mine.png) from same dir
        self.load_optional_images()

        self.create_header()
        self.create_grid()
        self.create_footer()

    def create_header(self):
        header = tk.Frame(self.master)
        header.pack(pady=8)
        # Difficulty selector
        diff_frame = tk.Frame(header)
        diff_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(diff_frame, text="Difficulty:", font=('Arial', 10)).pack(side=tk.LEFT)
        self.diff_var = tk.StringVar(value='Beginner')
        diff_menu = tk.OptionMenu(diff_frame, self.diff_var, 'Beginner', 'Intermediate', 'Expert', command=self.change_difficulty)
        diff_menu.config(width=12)
        diff_menu.pack(side=tk.LEFT)

        self.mines_label = tk.Label(header, text=f"Mines: {self.mines}", font=('Arial', 12))
        self.mines_label.pack(side=tk.LEFT, padx=10)

        self.timer_label = tk.Label(header, text="Time: 0", font=('Arial', 12))
        self.timer_label.pack(side=tk.LEFT, padx=10)

        new_btn = tk.Button(header, text="New Game", command=self.new_game)
        new_btn.pack(side=tk.LEFT, padx=10)
        # Highscores panel (small)
        hs_frame = tk.Frame(header)
        hs_frame.pack(side=tk.RIGHT, padx=10)
        tk.Label(hs_frame, text='Best Times', font=('Arial', 9, 'bold')).pack()
        self.hs_text = tk.StringVar()
        self.hs_text.set('Beginner: —\nIntermediate: —\nExpert: —')
        tk.Label(hs_frame, textvariable=self.hs_text, justify='right', font=('Arial', 9)).pack()
        self.refresh_highscores()

    def change_difficulty(self, val):
        """Called when the difficulty OptionMenu changes; restart game with selected preset."""
        try:
            self.difficulty = val
            # apply new difficulty by starting a new game
            self.new_game()
        except Exception:
            pass

    def create_grid(self):
        grid = tk.Frame(self.master)
        grid.pack(pady=8)

        for r in range(self.rows):
            for c in range(self.cols):
                b = tk.Button(grid, width=3, height=1, font=self.font, bg=self.cell_bg)
                b.grid(row=r, column=c)
                b.bind('<Button-1>', lambda e, rr=r, cc=c: self.on_left_click(rr, cc))
                # Right click; on macOS users may use Control-Click
                b.bind('<Button-3>', lambda e, rr=r, cc=c: self.on_right_click(rr, cc))
                b.bind('<Control-Button-1>', lambda e, rr=r, cc=c: self.on_right_click(rr, cc))
                self.cells[(r, c)] = b

    def create_footer(self):
        footer = tk.Frame(self.master)
        footer.pack(pady=8)

        self.status_label = tk.Label(footer, text="Good luck!", font=('Arial', 12))
        self.status_label.pack()

        # Undo, Save, Load, Highscores
        ctrl_frame = tk.Frame(self.master)
        ctrl_frame.pack(pady=6)

        undo_btn = tk.Button(ctrl_frame, text='Undo', command=self.undo_action)
        undo_btn.pack(side=tk.LEFT, padx=6)

        save_btn = tk.Button(ctrl_frame, text='Save Board', command=self.save_board)
        save_btn.pack(side=tk.LEFT, padx=6)

        load_btn = tk.Button(ctrl_frame, text='Load Board', command=self.load_board)
        load_btn.pack(side=tk.LEFT, padx=6)

        hs_btn = tk.Button(ctrl_frame, text='Highscores', command=self.show_highscores)
        hs_btn.pack(side=tk.LEFT, padx=6)

        # ensure highscores file exists
        self.highscores_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'highscores.json')
        if not os.path.exists(self.highscores_path):
            try:
                with open(self.highscores_path, 'w') as f:
                    json.dump({}, f)
            except Exception:
                pass

    def place_mines(self, safe_r, safe_c):
        # avoid placing mines on the safe cell and its neighbors
        forbidden = set()
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = safe_r + dr, safe_c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    forbidden.add((nr, nc))

        coords = [(r, c) for r in range(self.rows) for c in range(self.cols) if (r, c) not in forbidden]
        mines_coords = random.sample(coords, self.mines)
        for (r, c) in mines_coords:
            self.model[r][c]['mine'] = True

        # calculate neighbor counts
        for r in range(self.rows):
            for c in range(self.cols):
                if self.model[r][c]['mine']:
                    continue
                count = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.model[nr][nc]['mine']:
                                count += 1
                self.model[r][c]['count'] = count

    def on_left_click(self, r, c):
        if self.model[r][c]['flagged'] or self.model[r][c]['revealed']:
            return

        if self.first_click:
            self.place_mines(r, c)
            self.first_click = False
            self.start_timer()

        if self.model[r][c]['mine']:
            self.reveal_all_mines()
            self.cells[(r, c)].config(bg='red')
            self.game_over(False)
            return

        self.reveal_cell(r, c)
        if self.check_win():
            self.game_over(True)

    def on_right_click(self, r, c):
        if self.model[r][c]['revealed']:
            return
        flagged = self.model[r][c]['flagged']
        self.model[r][c]['flagged'] = not flagged
        # record action for undo
        self.undo_stack.append(('flag', (r, c)))
        # Use emoji for flag or optional icon
        if 'flag' in self.images:
            self.cells[(r, c)].config(image=self.images['flag'], compound='center')
        else:
            self.cells[(r, c)].config(text='🚩' if not flagged else '')
        mines_left = self.mines - sum(1 for rr in range(self.rows) for cc in range(self.cols) if self.model[rr][cc]['flagged'])
        self.mines_label.config(text=f"Mines: {mines_left}")

    def reveal_cell(self, r, c):
        # Iterative flood-fill reveal to avoid recursion depth issues
        stack = [(r, c)]
        while stack:
            cr, cc = stack.pop()
            if self.model[cr][cc]['revealed'] or self.model[cr][cc]['flagged']:
                continue
            # record reveal for undo
            self.undo_stack.append(('reveal', (cr, cc)))
            self.model[cr][cc]['revealed'] = True
            btn = self.cells[(cr, cc)]
            btn.config(relief=tk.SUNKEN, state='disabled', bg=self.revealed_bg)
            count = self.model[cr][cc]['count']
            if count > 0:
                btn.config(text=str(count), disabledforeground=self.number_color(count))
            else:
                # add neighbors to stack
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if not self.model[nr][nc]['revealed'] and not self.model[nr][nc]['flagged']:
                                stack.append((nr, nc))

    def load_optional_images(self):
        base = os.path.dirname(os.path.abspath(__file__))
        try:
            flag_path = os.path.join(base, 'flag.png')
            mine_path = os.path.join(base, 'mine.png')
            if os.path.exists(flag_path):
                self.images['flag'] = tk.PhotoImage(file=flag_path)
            if os.path.exists(mine_path):
                self.images['mine'] = tk.PhotoImage(file=mine_path)
        except Exception:
            # ignore image load errors
            self.images = {}

    def undo_action(self):
        if not self.undo_stack:
            messagebox.showinfo('Undo', 'No actions to undo')
            return
        action, pos = self.undo_stack.pop()
        r, c = pos
        if action == 'flag':
            # toggle flag back
            self.model[r][c]['flagged'] = not self.model[r][c]['flagged']
            if 'flag' in self.images and self.model[r][c]['flagged']:
                self.cells[(r, c)].config(image=self.images['flag'], compound='center', text='')
            else:
                self.cells[(r, c)].config(image='', text='🚩' if self.model[r][c]['flagged'] else '')
        elif action == 'reveal':
            # hide the revealed cell
            self.model[r][c]['revealed'] = False
            btn = self.cells[(r, c)]
            btn.config(relief=tk.RAISED, state='normal', text='')
        # update mines label
        mines_left = self.mines - sum(1 for rr in range(self.rows) for cc in range(self.cols) if self.model[rr][cc]['flagged'])
        self.mines_label.config(text=f"Mines: {mines_left}")

    def save_board(self):
        try:
            path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON','*.json')])
            if not path:
                return
            data = {
                'rows': self.rows,
                'cols': self.cols,
                'mines': self.mines,
                'model': self.model
            }
            with open(path, 'w') as f:
                json.dump(data, f)
            messagebox.showinfo('Save Board', f'Board saved to {path}')
        except Exception as e:
            messagebox.showerror('Save Board', f'Failed to save board: {e}')

    def load_board(self):
        try:
            path = filedialog.askopenfilename(filetypes=[('JSON','*.json')])
            if not path:
                return
            with open(path, 'r') as f:
                data = json.load(f)
            self.rows = data.get('rows', self.rows)
            self.cols = data.get('cols', self.cols)
            self.mines = data.get('mines', self.mines)
            self.model = data.get('model', self.model)
            # rebuild grid to match loaded size
            for widget in list(self.master.pack_slaves()):
                widget.destroy()
            self.cells = {}
            self.create_header()
            self.create_grid()
            self.create_footer()
            # apply model state to UI
            for r in range(self.rows):
                for c in range(self.cols):
                    cell = self.model[r][c]
                    btn = self.cells[(r, c)]
                    if cell.get('flagged'):
                        if 'flag' in self.images:
                            btn.config(image=self.images['flag'], compound='center')
                        else:
                            btn.config(text='🚩')
                    if cell.get('revealed'):
                        btn.config(relief=tk.SUNKEN, state='disabled')
                        if cell.get('mine'):
                            btn.config(text='💣', bg='yellow')
                        else:
                            cnt = cell.get('count', 0)
                            if cnt > 0:
                                btn.config(text=str(cnt), disabledforeground=self.number_color(cnt))
            self.mines_label.config(text=f"Mines: {self.mines}")
            self.timer_label.config(text='Time: 0')
            messagebox.showinfo('Load Board', f'Board loaded from {path}')
        except Exception as e:
            messagebox.showerror('Load Board', f'Failed to load board: {e}')

    def show_highscores(self):
        try:
            with open(self.highscores_path, 'r') as f:
                data = json.load(f)
        except Exception:
            data = {}
        lines = []
        for diff in ('Beginner', 'Intermediate', 'Expert'):
            v = data.get(diff)
            lines.append(f"{diff}: {v if v is not None else '—'}")
        messagebox.showinfo('Highscores', '\n'.join(lines))

    def refresh_highscores(self):
        try:
            with open(self.highscores_path, 'r') as f:
                data = json.load(f)
        except Exception:
            data = {}
        lines = []
        for diff in ('Beginner', 'Intermediate', 'Expert'):
            v = data.get(diff)
            lines.append(f"{diff}: {v if v is not None else '—'}")
        if hasattr(self, 'hs_text'):
            self.hs_text.set('\n'.join(lines))

    def number_color(self, n):
        # Common Minesweeper color scheme
        colors = {
            1: '#0000FF',
            2: '#007A00',
            3: '#FF0000',
            4: '#000080',
            5: '#800000',
            6: '#008080',
            7: '#000000',
            8: '#808080'
        }
        return colors.get(n, 'black')

    def reveal_all_mines(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.model[r][c]['mine']:
                    btn = self.cells[(r, c)]
                    if 'mine' in self.images:
                        btn.config(image=self.images['mine'], compound='center', bg=self.mine_bg)
                    else:
                        btn.config(text='💣', bg=self.mine_bg)

    def check_win(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if not self.model[r][c]['mine'] and not self.model[r][c]['revealed']:
                    return False
        return True

    def game_over(self, won):
        self.stop_timer()
        if won:
            self.status_label.config(text='You Win!')
            elapsed = int(time.time() - self.start_time) if self.start_time else 0
            messagebox.showinfo('Minesweeper', f'Congratulations, you won! Time: {elapsed}s')
            self.save_highscore(elapsed)
        else:
            self.status_label.config(text='You Lost!')
            messagebox.showinfo('Minesweeper', 'Boom! You hit a mine.')
        # disable all buttons
        for b in self.cells.values():
            b.config(state='disabled')

    def new_game(self):
        # apply difficulty settings
        diff = self.diff_var.get() if hasattr(self, 'diff_var') else 'Beginner'
        if diff == 'Beginner':
            self.rows, self.cols, self.mines = 9, 9, 10
        elif diff == 'Intermediate':
            self.rows, self.cols, self.mines = 16, 16, 40
        elif diff == 'Expert':
            self.rows, self.cols, self.mines = 16, 30, 99

        self.first_click = True
        self.start_time = None
        self.stop_timer()
        # rebuild model and grid if size changed
        self.model = [[{'mine': False, 'revealed': False, 'flagged': False, 'count': 0} for _ in range(self.cols)] for _ in range(self.rows)]
        # destroy and recreate grid
        for widget in list(self.master.pack_slaves()):
            widget.destroy()
        self.cells = {}
        self.create_header()
        self.create_grid()
        self.create_footer()
        for r in range(self.rows):
            for c in range(self.cols):
                # model already initialized above
                b = self.cells[(r, c)]
                b.config(text='', state='normal', bg='SystemButtonFace', relief=tk.RAISED)
        self.mines_label.config(text=f"Mines: {self.mines}")
        self.timer_label.config(text="Time: 0")
        self.status_label.config(text='Good luck!')

    def save_highscore(self, elapsed):
        try:
            with open(self.highscores_path, 'r') as f:
                data = json.load(f)
        except Exception:
            data = {}
        diff = self.diff_var.get() if hasattr(self, 'diff_var') else 'Beginner'
        best = data.get(diff)
        if best is None or elapsed < best:
            data[diff] = elapsed
            try:
                with open(self.highscores_path, 'w') as f:
                    json.dump(data, f)
                messagebox.showinfo('Highscore', f'New best time for {diff}: {elapsed}s')
            except Exception:
                pass

    def start_timer(self):
        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        if self.start_time is None:
            return
        elapsed = int(time.time() - self.start_time)
        self.timer_label.config(text=f"Time: {elapsed}")
        self.timer_id = self.master.after(1000, self.update_timer)

    def stop_timer(self):
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None


if __name__ == '__main__':
    root = tk.Tk()
    app = MinesweeperGUI(root)
    root.mainloop()
