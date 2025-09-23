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
        return self.grid[row][col] == 0
    
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
                x = col * self.cell_size + 11
                y = row * self.cell_size + 11
                w = self.cell_size - 1
                h = self.cell_size - 1
                cell_rect = pygame.Rect(x, y, w, h)

                # קודם כל: צביעת רקע (ככה נשארת הרשת)
                pygame.draw.rect(screen, (30, 30, 30), cell_rect)  # צבע רקע/רשת
                pygame.draw.rect(screen, (50, 50, 50), cell_rect, 1)  # קווי רשת דקים

                cell_value = self.grid[row][col]
                if cell_value == 0:
                    continue

                # צבע עיקרי
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect)

                # מסגרת כהה
                pygame.draw.rect(screen, (40, 40, 40), cell_rect, 3)

                # אפקט תלת־ממדי: קו בהיר למעלה ולשמאל
                pygame.draw.line(screen, (220, 220, 220), (x, y), (x + w, y), 2)
                pygame.draw.line(screen, (220, 220, 220), (x, y), (x, y + h), 2)

                # אפקט תלת־ממדי: קו כהה למטה ולימין
                pygame.draw.line(screen, (60, 60, 60), (x, y + h), (x + w, y + h), 2)
                pygame.draw.line(screen, (60, 60, 60), (x + w, y), (x + w, y + h), 2)

