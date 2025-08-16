import pygame
import random
from game_grid import Grid
from blocks import *
from colors import Colors
from position import Position

class Game:
    CELL_SIZE = 30  # גודל תא בפיקסלים

    def __init__(self):
        self.grid = Grid()
        self.blocks = [LBlock(), JBlock(), IBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.next_rect = pygame.Rect(320, 215, 170, 180)

        # מוזיקה
        self.theme = pygame.mixer.Sound("sounds/tetris-theme-korobeiniki-arranged-for-piano-186249.mp3")
        self.theme.play(loops=-1)

    # ================= Score =================
    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        self.score += move_down_points

    # ================= Random Block =================
    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [LBlock(), JBlock(), IBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    # ================= Move =================
    def move_left(self):
        self.current_block.move(0, -1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(-1, 0)
            self.lock_block()

    # ================= Lock Block =================
    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.col] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        self.update_score(rows_cleared, 0)
        if not self.block_fits():
            self.game_over = True
            self.theme.stop()

    # ================= Reset =================
    def reset(self):
        self.grid.reset()
        self.blocks = [LBlock(), JBlock(), IBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0
        self.game_over = False
        self.theme.play(loops=-1)

    # ================= Block Validations =================
    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_empty(tile.row, tile.col):
                return False
        return True

    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_inside(tile.row, tile.col):
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        if not self.block_inside() or not self.block_fits():
            self.current_block.undo_rotation()

    # ================= Ghost Piece =================
    def get_ghost_positions(self):
    # יוצרים רשימה של תאי הבלוק הנוכחי
        ghost_tiles = [Position(t.row, t.col) for t in self.current_block.get_cell_positions()]

    # מפילים את הבלוק עד שלא ניתן לרדת
        while True:
        # בדיקה אם ניתן לרדת
            fits = True
            for t in ghost_tiles:
                if not self.grid.is_inside(t.row + 1, t.col) or not self.grid.is_empty(t.row + 1, t.col):
                    fits = False
                    break
            if not fits:
                break
        # מזיזים את כל התאים שורה אחת למטה
            for t in ghost_tiles:
                t.row += 1
            
        return ghost_tiles

    # ================= Draw =================
    # ================= Draw =================

    # ================= Draw =================
    def draw(self, screen):
        self.grid.draw(screen)

    # Ghost Piece
        ghost_positions = self.get_ghost_positions()
        for tile in ghost_positions:
            rect = pygame.Rect(
                tile.col * self.CELL_SIZE + 11,
                tile.row * self.CELL_SIZE + 11,
                self.CELL_SIZE - 1,
                self.CELL_SIZE - 1
                )
            pygame.draw.rect(screen, (150, 150, 150), rect)  
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)

    # Current Block
        self.current_block.draw(screen, 0, 0, self.CELL_SIZE)

        # Next Block – מרכז בתוך next_rect
        next_area_x, next_area_y = self.next_rect.x, self.next_rect.y
        next_area_width, next_area_height = self.next_rect.width, self.next_rect.height

        tiles = self.next_block.get_cell_positions()
        min_col = min(t.col for t in tiles)
        max_col = max(t.col for t in tiles)
        min_row = min(t.row for t in tiles)
        max_row = max(t.row for t in tiles)

        block_width = (max_col - min_col + 1) * self.CELL_SIZE
        block_height = (max_row - min_row + 1) * self.CELL_SIZE

        offset_x = next_area_x + (next_area_width - block_width) // 2 - min_col * self.CELL_SIZE -10
        offset_y = next_area_y + (next_area_height - block_height) // 2 - min_row * self.CELL_SIZE

        self.next_block.draw(screen, offset_x, offset_y, self.CELL_SIZE)

    

