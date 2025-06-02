from time import sleep


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

    def update_to_next_state(self):
        self.state = self.next_state

def main():
    grid = Grid()
    grid.prepare_empty_grid(10,10)
    grid.make_glider(0,0)
    print(grid)
    for i in range(30):
        grid.calculate_next_states()
        grid.update_to_next_state()
        print(grid)
        sleep(1)

    return

if __name__ == '__main__':
    main()

