from colors import Colors
import pygame
from position import Position

class Block:
    def __init__(self, id):
        self.id = id
        self.cells = {}
        self.cell_size = 30
        self.rowoffset = 0
        self.coloffset = 0
        self.rotation_state = 0
        self.colors = Colors.get_cell_colors()

    def move(self, rows, cols):
        self.rowoffset += rows
        self.coloffset += cols

    def get_cell_positions(self):
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            position = Position(position.row + self.rowoffset, position.col + self.coloffset)
            moved_tiles.append(position)
        return moved_tiles
    
    def rotate(self):
        self.rotation_state += 1
        if self.rotation_state == len(self.cells):
            self.rotation_state = 0

    def undo_rotation(self):
        self.rotation_state -= 1
        if self.rotation_state < 0:  # תיקנתי כאן באג קטן שהיה
            self.rotation_state = len(self.cells) - 1

    def draw(self, screen, offset_x, offset_y, cell_size=None):
        if cell_size is None:
            cell_size = self.cell_size

        tiles = self.get_cell_positions()
        for tile in tiles:
            x = offset_x + tile.col * cell_size + 11
            y = offset_y + tile.row * cell_size + 11
            w = cell_size - 1
            h = cell_size - 1
            tile_rect = pygame.Rect(x, y, w, h)
            # צבע עיקרי
            pygame.draw.rect(screen, self.colors[self.id], tile_rect)
            # מסגרת כהה
            pygame.draw.rect(screen, (40, 40, 40), tile_rect, 3)
            # אפקט תלת־ממדי: קו בהיר למעלה ולשמאל
            pygame.draw.line(screen, (220, 220, 220), (x, y), (x + w, y), 2)
            pygame.draw.line(screen, (220, 220, 220), (x, y), (x, y + h), 2)
            # אפקט תלת־ממדי: קו כהה למטה ולימין
            pygame.draw.line(screen, (60, 60, 60), (x, y + h), (x + w, y + h), 2)
            pygame.draw.line(screen, (60, 60, 60), (x + w, y), (x + w, y + h), 2)
