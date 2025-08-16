import pygame, sys, os
from game import Game
from colors import Colors
import random

pygame.init()

# ---------- Constants & States ----------
WIDTH, HEIGHT = 500, 620
STATE_MENU = "MENU"
STATE_PLAYING = "PLAYING"
STATE_GAME_OVER = "GAME_OVER"

DIFFICULTIES = [("Easy", 600), ("Medium", 400), ("Hard", 250)]
difficulty_index = 1  # default: Medium

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Tetris")
clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.Font(None, 64)
small_font = pygame.font.Font(None, 32)

score_title_surface = small_font.render("Score", True, Colors.white)
next_title_surface = small_font.render("Next", True, Colors.white)
score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)

# ---------- High Score ----------
HIGHSCORE_FILE = "highscore.txt"

def load_high_score(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return int(f.read().strip() or "0")
    return 0

def save_high_score(path, score):
    with open(path, "w", encoding="utf-8") as f:
        f.write(str(score))

high_score = load_high_score(HIGHSCORE_FILE)

# ---------- Block Drop Event ----------
GAME_UPDATE = pygame.USEREVENT
def set_drop_timer(ms):
    pygame.time.set_timer(GAME_UPDATE, ms)

# ---------- Game State ----------
state = STATE_MENU
game = None
game_over_buttons = ["Play Again", "Main Menu"]
selected_button_index = 0
game_over_button_rects = []

# ---------- Start Button ----------
start_button_rect = None
start_button_color = Colors.dark_blue
start_button_hover_color = Colors.light_blue

def draw_start_button(center):
    global start_button_rect
    text_surf = small_font.render("START GAME", True, Colors.white)
    padding_x, padding_y = 20, 10
    rect_width = text_surf.get_width() + padding_x*2
    rect_height = text_surf.get_height() + padding_y*2
    rect = pygame.Rect(center[0]-rect_width//2, center[1]-rect_height//2, rect_width, rect_height)
    
    # hover effect
    mouse_pos = pygame.mouse.get_pos()
    color = start_button_hover_color if rect.collidepoint(mouse_pos) else start_button_color
    
    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, Colors.white, rect, width=2, border_radius=10)
    screen.blit(text_surf, text_surf.get_rect(center=center))
    
    start_button_rect = rect

# ---------- Game Functions ----------
def start_game():
    global game, state, selected_button_index
    game = Game()
    set_drop_timer(DIFFICULTIES[difficulty_index][1])
    state = STATE_PLAYING
    selected_button_index = 0

def go_to_menu():
    global state, selected_button_index
    set_drop_timer(0)
    state = STATE_MENU
    selected_button_index = 0

def handle_game_over():
    global high_score, state, selected_button_index
    if game.score > high_score:
        high_score = game.score
        save_high_score(HIGHSCORE_FILE, high_score)
    try:
        if hasattr(game, "theme"):
            game.theme.stop()
        else:
            pygame.mixer.music.stop()
    except:
        pass
    state = STATE_GAME_OVER
    selected_button_index = 0

# ---------- Drawing Functions ----------
def draw_gradient_background(surface, top_color, bottom_color):
    height = surface.get_height()
    for y in range(height):
        ratio = y / height
        r = int(top_color[0]*(1-ratio) + bottom_color[0]*ratio)
        g = int(top_color[1]*(1-ratio) + bottom_color[1]*ratio)
        b = int(top_color[2]*(1-ratio) + bottom_color[2]*ratio)
        pygame.draw.line(surface, (r,g,b), (0,y), (surface.get_width(),y))

# Tetris shapes relative coordinates
SHAPES = {
    "I": [(0,0),(1,0),(2,0),(3,0)],
    "O": [(0,0),(0,1),(1,0),(1,1)],
    "T": [(0,1),(1,0),(1,1),(1,2)],
    "S": [(0,1),(0,2),(1,0),(1,1)],
    "Z": [(0,0),(0,1),(1,1),(1,2)],
    "J": [(0,0),(1,0),(2,0),(2,1)],
    "L": [(0,1),(1,1),(2,1),(2,0)]
}

# ליצירת בלוקים ברקע קבועים
BACKGROUND_BLOCKS = []

def init_background_blocks():
    shapes = list(SHAPES.values())
    colors = [Colors.red, Colors.green, Colors.blue, Colors.yellow, Colors.cyan, Colors.white, Colors.orange]
    block_size = 20
    for i in range(0, WIDTH, 100):
        for j in range(0, HEIGHT, 100):
            shape = random.choice(shapes)
            color = random.choice(colors)
            BACKGROUND_BLOCKS.append((shape, color, (i,j), block_size))

def draw_tetris_block(surface, shape, color, top_left, block_size=20, alpha=30):
    """Draw a tetris shape on the surface as a watermark."""
    block_surf = pygame.Surface((block_size*4, block_size*4), pygame.SRCALPHA)
    for r, c in shape:
        rect = pygame.Rect(c*block_size, r*block_size, block_size, block_size)
        pygame.draw.rect(block_surf, (*color, alpha), rect)
        pygame.draw.rect(block_surf, (*color, min(alpha+50,255)), rect, 1)  # border
    surface.blit(block_surf, top_left)

def draw_gradient_background_with_tetris_static(surface, top_color, bottom_color):
    # Gradient background
    height = surface.get_height()
    for y in range(height):
        ratio = y / height
        r = int(top_color[0]*(1-ratio) + bottom_color[0]*ratio)
        g = int(top_color[1]*(1-ratio) + bottom_color[1]*ratio)
        b = int(top_color[2]*(1-ratio) + bottom_color[2]*ratio)
        pygame.draw.line(surface, (r,g,b), (0,y), (surface.get_width(),y))

    # Draw pre-defined Tetris shapes
    for shape, color, pos, block_size in BACKGROUND_BLOCKS:
        draw_tetris_block(surface, shape, color, pos, block_size, alpha=30)

init_background_blocks()

def draw_menu():
    # Background with gradient + static Tetris shapes
    draw_gradient_background_with_tetris_static(screen, (20,20,60), (60,0,80))
    
    # Title
    title = title_font.render("TETRIS", True, Colors.white)
    outline = title_font.render("TETRIS", True, Colors.red)
    screen.blit(outline, title.get_rect(center=(WIDTH//2+3,143)))
    screen.blit(title, title.get_rect(center=(WIDTH//2,140)))

    # Short instruction text above difficulty buttons
    instr_font = pygame.font.Font(None, 20)  # small font
    instr_surf = instr_font.render("Use LEFT/RIGHT arrows", True, Colors.white)
    screen.blit(instr_surf, instr_surf.get_rect(center=(WIDTH//2, 210)))

    # Difficulty buttons with hover effect
    mouse_pos = pygame.mouse.get_pos()
    for i, (name, ms) in enumerate(DIFFICULTIES):
        # צבע הרקע
        if i == difficulty_index:
            rect_color = Colors.white        # המסומן – לבן
            text_color = Colors.dark_blue    # טקסט כהה כדי שיהיה קריא
        else:
            rect_color = Colors.light_blue   # לא מסומן – כחול
            text_color = Colors.white

        # אפקט hover
        rect = pygame.Rect(WIDTH//2 + (i-1)*120 - 50, 250, 100, 40)  # רוחב/גובה קבועים
        if rect.collidepoint(mouse_pos):
            rect_color = Colors.yellow      # צבע משתנה כשעכבר מעל הכפתור

        pygame.draw.rect(screen, rect_color, rect, border_radius=10)
        pygame.draw.rect(screen, Colors.white, rect, width=2, border_radius=10)

        # טקסט הכפתור במרכז
        text_surf = small_font.render(name, True, text_color)
        screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    # Start button
    draw_start_button((WIDTH//2,340))

    # High Score
    hs_surf = small_font.render(f"High Score: {high_score}", True, Colors.yellow)
    screen.blit(hs_surf, hs_surf.get_rect(center=(WIDTH//2,400)))

def draw_game_over_buttons():
    global game_over_button_rects
    game_over_button_rects = []
    y = HEIGHT//2 + 40
    spacing = 180
    mouse_pos = pygame.mouse.get_pos()
    for i, text in enumerate(game_over_buttons):
        center_x = WIDTH//2 + (i - 0.5) * spacing
        active = (i==selected_button_index)
        rect_color = (100,50,50) if active else (50,50,50)
        text_surf = small_font.render(text, True, Colors.white)
        rect = text_surf.get_rect(center=(center_x,y)).inflate(40,20)
        if rect.collidepoint(mouse_pos):
            rect_color = Colors.light_blue
        pygame.draw.rect(screen, rect_color, rect, border_radius=8)
        pygame.draw.rect(screen, Colors.white, rect, width=2, border_radius=8)
        screen.blit(text_surf, text_surf.get_rect(center=(center_x,y)))
        game_over_button_rects.append(rect)

def draw_game_over():
    overlay = pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
    overlay.fill((0,0,0,180))
    screen.blit(overlay,(0,0))
    title = title_font.render("GAME OVER", True, Colors.red)
    outline = title_font.render("GAME OVER", True, Colors.white)
    screen.blit(outline, title.get_rect(center=(WIDTH//2+2, HEIGHT//2-58)))
    screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2-60)))
    draw_game_over_buttons()

# ---------- Main Loop ----------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        # --------- Menu ---------
        if state==STATE_MENU:
            if event.type==pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    difficulty_index = (difficulty_index-1) % len(DIFFICULTIES)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    difficulty_index = (difficulty_index+1) % len(DIFFICULTIES)
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    start_game()
                elif event.key==pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
            elif event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                if start_button_rect and start_button_rect.collidepoint(event.pos):
                    start_game()

        # --------- Playing ---------
        elif state==STATE_PLAYING:
            if event.type==pygame.KEYDOWN:
                if not game.game_over:
                    if event.key==pygame.K_LEFT:
                        game.move_left()
                    elif event.key==pygame.K_RIGHT:
                        game.move_right()
                    elif event.key==pygame.K_DOWN:
                        game.move_down()
                        game.update_score(0,1)
                    elif event.key==pygame.K_UP:
                        game.rotate()
            if event.type==GAME_UPDATE and not game.game_over:
                game.move_down()
            if state==STATE_PLAYING and game.game_over:
                handle_game_over()

        # --------- Game Over ---------
        elif state==STATE_GAME_OVER:
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    selected_button_index = (selected_button_index-1) % len(game_over_buttons)
                elif event.key==pygame.K_RIGHT:
                    selected_button_index = (selected_button_index+1) % len(game_over_buttons)
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if game_over_buttons[selected_button_index]=="Play Again":
                        start_game()
                    elif game_over_buttons[selected_button_index]=="Main Menu":
                        go_to_menu()
            elif event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                for i, rect in enumerate(game_over_button_rects):
                    if rect.collidepoint(event.pos):
                        if game_over_buttons[i]=="Play Again":
                            start_game()
                        elif game_over_buttons[i]=="Main Menu":
                            go_to_menu()

    # ---------- Drawing ----------
    if state==STATE_MENU:
        draw_menu()
    elif state==STATE_PLAYING:
        screen.fill(Colors.dark_blue)
        screen.blit(score_title_surface,(365,20,50,50))
        screen.blit(next_title_surface,(375,180,50,50))
        pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
        pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
        score_value_surface = title_font.render(str(game.score), True, Colors.white)
        screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx, centery=score_rect.centery))
        hs_label = small_font.render(f"High Score: {high_score}", True, Colors.white)
        screen.blit(hs_label, (next_rect.x+next_rect.width//2 - hs_label.get_width()//2, next_rect.y + next_rect.height + 25))
        game.draw(screen)
    elif state==STATE_GAME_OVER:
        screen.fill(Colors.dark_blue)
        screen.blit(score_title_surface,(365,20,50,50))
        screen.blit(next_title_surface,(375,180,50,50))
        pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
        pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
        score_value_surface = title_font.render(str(game.score), True, Colors.white)
        screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx, centery=score_rect.centery))
        hs_label = small_font.render(f"High Score: {high_score}", True, Colors.white)
        screen.blit(hs_label, (next_rect.x+next_rect.width//2 - hs_label.get_width()//2, next_rect.y + next_rect.height + 25))
        game.draw(screen)
        draw_game_over()

    pygame.display.update()
    clock.tick(60)
