import tkinter as tk

class Grid:
    """
    Class representing the logical grid of cells
    """
    def __init__(self):
        #: The 2D array of cells
        self.cells = []
        #: The amount of the rows in the grid
        self.rows = 0
        #: The amount of the columns in the grid
        self.columns = 0
    def prepare_empty_grid(self, rows, columns):
        """Prepare an empty grid with the size of rows x columns"""
        self.rows = rows
        self.columns = columns
        for i in range(rows):
            self.cells.append([])
            for j in range(columns):
                self.cells[i].append(Cell(0))
    def set_cell(self, x, y, state):
        """Set a cell at [x][y] to a certain state"""
        self.cells[x][y].state = state
    def make_glider(self, x, y):
        """Create a glider pattern with top left corner at [x][y]"""
        if x<0 or x>self.rows-1-3:
            return
        if y<0 or y>self.columns-1-3:
            return

        self.set_cell(x+0, y+1, 1)
        self.set_cell(x+1, y+2, 1)
        self.set_cell(x+2, y+0, 1)
        self.set_cell(x+2, y+1, 1)
        self.set_cell(x+2, y+2, 1)

    def __str__(self):
        result = ""
        for i in range(self.rows):
            for j in range(self.columns):
                result += f"[{self.cells[i][j].state}]"
            result += "\n"
        return result
    def calculate_next_states(self):
        """Calculate the next state for all cells"""
        for i in range(self.rows):
            for j in range(self.columns):
                self.calculate_next_state(i,j)
    def update_to_next_state(self):
        """Update all cells to their next state"""
        for i in range(self.rows):
            for j in range(self.columns):
                self.cells[i][j].update_to_next_state()
    def calculate_next_state(self, x, y):
        """Calculate the next state for the cell at [x][y]"""
        left = 0
        right = 0
        up = 0
        down = 0
        up_left = 0
        up_right = 0
        down_left = 0
        down_right = 0
        cell = self.cells[x][y]
        if x > 0:
            up = self.cells[x - 1][y].state
        if y > 0:
            left = self.cells[x][y-1].state
        if x < self.columns - 1:
            down = self.cells[x+1][y].state
        if y < self.rows - 1:
            right = self.cells[x][y+1].state
        if x > 0 and y > 0:
            up_left = self.cells[x-1][y-1].state
        if x < self.columns - 1 and y < self.rows - 1:
            down_right = self.cells[x+1][y+1].state
        if x > 0 and y < self.columns - 1:
            up_right = self.cells[x-1][y+1].state
        if x < self.columns - 1 and y>0:
            down_left = self.cells[x+1][y-1].state


        neighbour_sum = left + right + up + down + up_left + down_right + up_right + down_left
        if neighbour_sum < 2:
            cell.next_state = 0
        elif neighbour_sum > 3:
            cell.next_state = 0
        elif neighbour_sum == 3:
            cell.next_state = 1
        elif neighbour_sum == 2 and cell.state == 1:
            cell.next_state = 1
        else:
            cell.next_state = 0


class Cell:
    """
        Class representing the logical cell
    """
    def __init__(self, state):
        #: The current state of the cell
        self.state = state
        #: The next state of the cell
        self.next_state = 0

    def flip_state(self):
        """Flip the current state of the cell"""
        self.state = 1 if self.state == 0 else 0
    def update_to_next_state(self):
        """Set the current state of the cell to the next state"""
        self.state = self.next_state


class SettingsUI:
    """
        UI element for configuration of the game
    """
    def __init__(self, root, on_generate):
        self.root = root
        #: The method to call when you press the generate button
        self.on_generate = on_generate
        self.frame = tk.Frame(root)
        self.frame.pack()

        tk.Label(self.frame, text="Rows:").grid(row=0, column=0)
        self.rows_entry = tk.Entry(self.frame)
        self.rows_entry.insert(0, "10")
        self.rows_entry.grid(row=0, column=1)

        tk.Label(self.frame, text="Columns:").grid(row=1, column=0)
        self.columns_entry = tk.Entry(self.frame)
        self.columns_entry.insert(0, "10")
        self.columns_entry.grid(row=1, column=1)

        tk.Label(self.frame, text="Cell size:").grid(row=2, column=0)
        self.cell_size_entry = tk.Entry(self.frame)
        self.cell_size_entry.insert(0, "20")
        self.cell_size_entry.grid(row=2, column=1)

        self.button = tk.Button(self.frame, text="Generate", command=self.generate)
        self.button.grid(row=3, column=1)

    def generate(self):
        """Set the configuration of the game and run on_generate() with the config"""
        rows = int(self.rows_entry.get())
        columns = int(self.columns_entry.get())
        cell_size = int(self.cell_size_entry.get())
        self.frame.destroy()
        self.on_generate(self.root, rows, columns, cell_size)



class GameUI:
    """
        UI element for the main game
    """
    def __init__(self, root, grid, width=400, height=400):
        self.after_id = -1
        self.is_running = False
        #: Width of the window
        self.width = width
        #: Height of the window
        self.height = height
        self.cell_width = width/grid.columns
        self.cell_height = height/grid.rows
        self.root = root
        #: The Grid() for logic operations
        self.grid = grid
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()

        self.button = tk.Button(self.root, text="Start", command=self.toggle_game)
        self.button.pack()

        self.speed = 1000

        self.speed_slider = tk.Scale(self.root, from_=0.2, to=5, resolution=0.1,
                                     orient=tk.HORIZONTAL, label="Update time")
        self.speed_slider.set(self.speed/1000)
        self.speed_slider.pack()

        self.canvas.bind("<ButtonRelease-1>", self.update_grid)
        self.speed_slider.bind("<ButtonRelease-1>", self.update_speed)

        self.draw_grid()

    def update_speed(self, event):
        """Update the speed of the in-game tick"""
        self.speed = self.speed_slider.get()*1000

    def update_grid(self, event):
        """Handle the click event - Flip the cell state when it's pressed - Update the UI"""
        if self.is_running: return
        j = int(event.x // self.cell_width)
        i = int(event.y // self.cell_height)
        self.grid.cells[i][j].flip_state()
        self.draw_grid()

    def draw_grid(self):
        """Update the UI grid of the game"""
        self.canvas.delete("all")
        for i in range(self.grid.rows):
            for j in range(self.grid.columns):
                color = "black" if self.grid.cells[i][j].state == 1 else "white"
                x = j * self.cell_width
                y = i * self.cell_height
                self.canvas.create_rectangle(x, y, x+self.cell_width, y+self.cell_height, fill=color)

    def toggle_game(self):
        """Toggle the game on and off"""
        self.is_running = not self.is_running
        if self.is_running:
            self.button.config(text="Stop")
            self.update_game()
        else:
            self.button.config(text="Start")
            self.stop_game()

    def update_game(self):
        """Calculate the logic for next tick and update the UI in a loop"""
        self.grid.calculate_next_states()
        self.grid.update_to_next_state()
        self.draw_grid()
        self.after_id = self.root.after(int(self.speed), self.update_game)

    def stop_game(self):
        """Cancel the main game loop"""
        self.root.after_cancel(self.after_id)

def start_game(root, rows, columns, cell_size):
    """Start a new game with the config (rows, columns, cell_size)"""
    grid = Grid()
    grid.prepare_empty_grid(rows, columns)
    grid.make_glider(0, 0)
    GameUI(root, grid, cell_size*columns, cell_size*rows)

def main():
    """Run the program - Start with settings"""
    grid = Grid()
    grid.prepare_empty_grid(10,10)
    grid.make_glider(0,0)
    #print(grid)
    root = tk.Tk()
    root.title("Game of Life")
    SettingsUI(root, start_game)
    root.mainloop()
    return



if __name__ == '__main__':
    main()

