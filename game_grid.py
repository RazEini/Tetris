import pygame

from colors import Colors

class Grid:
    def __init__(self):
        self.number_of_rows = 20
        self.number_of_columns = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.number_of_columns)] for i in range(self.number_of_rows)]
        self.colors = Colors.get_cell_colors()

    def print_grid(self):
        for row in range(self.number_of_rows):
            for col in range(self.number_of_columns):
                print(self.grid[row][col], end=' ')
            print()

    def is_inside(self, row, col):
        if row >= 0 and row < self.number_of_rows and col >= 0 and col < self.number_of_columns:
            return True
        return False
    
    def is_empty(self, row, col):
        if self.grid[row][col] == 0:
            return True
        return False
    
    def is_row_full(self, row):
        for col in range(self.number_of_columns):
            if self.grid[row][col] == 0:
                return False
        return True
    
    def clear_row(self, row):
        for col in range(self.number_of_columns):
            self.grid[row][col] = 0

    def move_row_down(self, row, number_of_rows):
        for col in range(self.number_of_columns):
            self.grid[row + number_of_rows][col] = self.grid[row][col]
            self.grid[row][col] = 0

    def clear_full_rows(self):
        completed = 0
        for row in range(self.number_of_rows-1, 0, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed
    
    def reset(self):
        for row in range(self.number_of_rows):
            for col in range(self.number_of_columns):
                self.grid[row][col] = 0
    
    def draw(self, screen):
        for row in range(self.number_of_rows):
            for col in range(self.number_of_columns):
                cell_value = self.grid[row][col]
                cell_rect = pygame.Rect(col * self.cell_size + 11, row * self.cell_size + 11, self.cell_size -1, self.cell_size -1)
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect)