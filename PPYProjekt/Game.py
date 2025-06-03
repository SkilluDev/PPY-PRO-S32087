import tkinter as tk

class Grid:
    def __init__(self):
        self.cells = []
        self.rows = 0
        self.columns = 0
    def prepare_empty_grid(self, rows, columns):
        self.rows = rows
        self.columns = columns
        for i in range(rows):
            self.cells.append([])
            for j in range(columns):
                self.cells[i].append(Cell(0))
    def set_cell(self, x, y, state):
        self.cells[x][y].state = state
    def make_glider(self, x, y):
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
        for i in range(self.rows):
            for j in range(self.columns):
                self.calculate_next_state(i,j)

    def update_to_next_state(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self.cells[i][j].update_to_next_state()

    def calculate_next_state(self, x, y):
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
    def __init__(self, state):
        self.state = state
        self.next_state = 0

    def flip_state(self):
        self.state = 1 if self.state == 0 else 0
    def update_to_next_state(self):
        self.state = self.next_state



class GameUI:
    def __init__(self, root, grid, width=400, height=400):
        self.width = width
        self.height = height
        self.cell_width = width/grid.columns
        self.cell_height = height/grid.rows
        self.root = root
        self.grid = grid
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()

        self.button = tk.Button(self.root, text="Start", command=self.start_game)
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
        self.speed = self.speed_slider.get()*1000

    def update_grid(self, event):
        j = int(event.x // self.cell_width)
        i = int(event.y // self.cell_height)
        self.grid.cells[i][j].flip_state()
        self.draw_grid()

    def draw_grid(self):
        for i in range(self.grid.rows):
            for j in range(self.grid.columns):
                color = "black" if self.grid.cells[i][j].state == 1 else "white"
                x = j * self.cell_width
                y = i * self.cell_height
                self.canvas.create_rectangle(x, y, x+self.cell_width, y+self.cell_height, fill=color)

    def start_game(self):
        self.button.destroy()
        self.update_game()

    def update_game(self):
        self.grid.calculate_next_states()
        self.grid.update_to_next_state()
        self.draw_grid()
        self.root.after(int(self.speed), self.update_game)


def main():
    grid = Grid()
    grid.prepare_empty_grid(10,10)
    grid.make_glider(0,0)
    print(grid)
    root = tk.Tk()
    root.title("Game of Life")
    GameUI(root, grid, 200, 200)
    root.mainloop()
    return


if __name__ == '__main__':
    main()

