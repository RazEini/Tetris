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
        
        # Next Block (שומרים על ה־offset שלה באזור הצדדי)
        if self.next_block.id == 3:
            self.next_block.draw(screen, 255, 290, self.CELL_SIZE)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 255, 280, self.CELL_SIZE)
        else:
            self.next_block.draw(screen, 270, 270, self.CELL_SIZE)

