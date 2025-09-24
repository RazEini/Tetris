import pygame, sys, os, random
from game import Game
from colors import Colors
from leaderboard import load_leaderboard, add_score
from config import load_config, save_config

pygame.init()

# ---------- Constants & States ----------
WIDTH, HEIGHT = 500, 620
STATE_MENU = "MENU"
STATE_PLAYING = "PLAYING"
STATE_GAME_OVER = "GAME_OVER"
STATE_LEADERBOARD = "LEADERBOARD"
STATE_ENTER_NAME = "ENTER_NAME"

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
prev_state = STATE_MENU
game = None
game_over_buttons = ["Play Again", "Main Menu", "Leaderboard"]
selected_button_index = 0
game_over_button_rects = []
player_name = ""  # For entering name after game over

menu_buttons = ["START GAME", "LEADERBOARD"]
menu_button_rects = []

leaderboard_scroll = 0  # For scrolling the leaderboard

# ---------- Background & Blocks ----------
SHAPES = {
    "I": [(0,0),(1,0),(2,0),(3,0)],
    "O": [(0,0),(0,1),(1,0),(1,1)],
    "T": [(0,1),(1,0),(1,1),(1,2)],
    "S": [(0,1),(0,2),(1,0),(1,1)],
    "Z": [(0,0),(0,1),(1,1),(1,2)],
    "J": [(0,0),(1,0),(2,0),(2,1)],
    "L": [(0,1),(1,1),(2,1),(2,0)]
}
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
    block_surf = pygame.Surface((block_size*4, block_size*4), pygame.SRCALPHA)
    for r, c in shape:
        rect = pygame.Rect(c*block_size, r*block_size, block_size, block_size)
        pygame.draw.rect(block_surf, (*color, alpha), rect)
        pygame.draw.rect(block_surf, (*color, min(alpha+50,255)), rect, 1)
    surface.blit(block_surf, top_left)

def draw_gradient_background_with_tetris_static(surface, top_color, bottom_color):
    height = surface.get_height()
    for y in range(height):
        ratio = y / height
        r = int(top_color[0]*(1-ratio) + bottom_color[0]*ratio)
        g = int(top_color[1]*(1-ratio) + bottom_color[1]*ratio)
        b = int(top_color[2]*(1-ratio) + bottom_color[2]*ratio)
        pygame.draw.line(surface, (r,g,b), (0,y), (surface.get_width(),y))
    for shape, color, pos, block_size in BACKGROUND_BLOCKS:
        draw_tetris_block(surface, shape, color, pos, block_size, alpha=30)

init_background_blocks()

# ---------- Menu ----------
def draw_menu():
    draw_gradient_background_with_tetris_static(screen, (20,20,60), (60,0,80))
    title = title_font.render("TETRIS", True, Colors.white)
    outline = title_font.render("TETRIS", True, Colors.red)
    screen.blit(outline, title.get_rect(center=(WIDTH//2+3,143)))
    screen.blit(title, title.get_rect(center=(WIDTH//2,140)))
    
    mouse_pos = pygame.mouse.get_pos()
    for i, (name, ms) in enumerate(DIFFICULTIES):
        rect_color = Colors.white if i==difficulty_index else Colors.light_blue
        text_color = Colors.dark_blue if i==difficulty_index else Colors.white
        rect = pygame.Rect(WIDTH//2 + (i-1)*120 - 50, 250, 100, 40)
        if rect.collidepoint(mouse_pos): rect_color = Colors.yellow
        pygame.draw.rect(screen, rect_color, rect, border_radius=10)
        pygame.draw.rect(screen, Colors.white, rect, width=2, border_radius=10)
        text_surf = small_font.render(name, True, text_color)
        screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    menu_button_rects.clear()
    start_y = 340
    spacing = 60
    for i, text in enumerate(menu_buttons):
        center = (WIDTH//2, start_y + i*spacing)
        rect_color = Colors.dark_blue
        rect = pygame.Rect(center[0]-100, center[1]-20, 200, 40)
        if rect.collidepoint(mouse_pos): rect_color = Colors.light_blue
        pygame.draw.rect(screen, rect_color, rect, border_radius=10)
        pygame.draw.rect(screen, Colors.white, rect, 2, border_radius=10)
        text_surf = small_font.render(text, True, Colors.white)
        screen.blit(text_surf, text_surf.get_rect(center=center))
        menu_button_rects.append(rect)

    hs_surf = small_font.render(f"High Score: {high_score}", True, Colors.yellow)
    screen.blit(hs_surf, hs_surf.get_rect(center=(WIDTH//2, 500)))

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
    global high_score, state, selected_button_index, player_name
    if game.score > high_score:
        high_score = game.score
        save_high_score(HIGHSCORE_FILE, high_score)
    try:
        if hasattr(game, "theme"): game.theme.stop()
        else: pygame.mixer.music.stop()
    except: pass
    state = STATE_ENTER_NAME
    player_name = ""
    selected_button_index = 0

# ---------- Game Over ----------
def draw_game_over_buttons():
    global game_over_button_rects
    game_over_button_rects = []
    start_y = HEIGHT//2 - 50
    spacing = 60
    mouse_pos = pygame.mouse.get_pos()
    for i, text in enumerate(game_over_buttons):
        center = (WIDTH//2, start_y + i*spacing)
        rect_color = (100,50,50) if i==selected_button_index else (50,50,50)
        text_surf = small_font.render(text, True, Colors.white)
        rect = text_surf.get_rect(center=center).inflate(40,20)
        if rect.collidepoint(mouse_pos): rect_color = Colors.light_blue
        pygame.draw.rect(screen, rect_color, rect, border_radius=8)
        pygame.draw.rect(screen, Colors.white, rect, width=2, border_radius=8)
        screen.blit(text_surf, text_surf.get_rect(center=center))
        game_over_button_rects.append(rect)

def draw_game_over():
    overlay = pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
    overlay.fill((0,0,0,180))
    screen.blit(overlay,(0,0))
    title = title_font.render("GAME OVER", True, Colors.red)
    outline = title_font.render("GAME OVER", True, Colors.white)
    screen.blit(outline, title.get_rect(center=(WIDTH//2+2, HEIGHT//2-108)))  # מעל קצת יותר
    screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2-110)))
    draw_game_over_buttons()

# ---------- Enter Name ----------
def draw_enter_name():
    draw_gradient_background_with_tetris_static(screen, (20,20,60), (60,0,80))  # רקע עם בלוקים
    
    prompt = small_font.render("Enter your name:", True, Colors.white)
    screen.blit(prompt, prompt.get_rect(center=(WIDTH//2, HEIGHT//2-80)))
    
    rect_width, rect_height = 300, 50
    rect = pygame.Rect(WIDTH//2-rect_width//2, HEIGHT//2-25, rect_width, rect_height)
    pygame.draw.rect(screen, Colors.light_blue, rect, border_radius=8)
    pygame.draw.rect(screen, Colors.white, rect, 2, border_radius=8)
    
    # Cursor / קו קופץ
    cursor = "|" if pygame.time.get_ticks() % 1000 < 500 else ""
    name_surf = small_font.render(player_name + cursor, True, Colors.yellow)
    screen.blit(name_surf, name_surf.get_rect(center=rect.center))
    
    # כפתור Enter
    submit_rect = pygame.Rect(WIDTH//2-70, HEIGHT//2 + 50, 140, 40)
    mouse_pos = pygame.mouse.get_pos()
    color = Colors.light_blue if submit_rect.collidepoint(mouse_pos) else Colors.dark_blue
    pygame.draw.rect(screen, color, submit_rect, border_radius=10)
    pygame.draw.rect(screen, Colors.white, submit_rect, width=2, border_radius=10)
    submit_surf = small_font.render("Submit", True, Colors.white)
    screen.blit(submit_surf, submit_surf.get_rect(center=submit_rect.center))
    
    return rect, submit_rect  # נחזיר את ה־rects בשביל טיפול בלחיצה

# ---------- Leaderboard ----------
ROW_HEIGHT = 50
BUTTON_HEIGHT = 40
BUTTON_MARGIN = 20
TOP_MARGIN = 150
LEADERBOARD_MAX_DISPLAY = (HEIGHT - (BUTTON_HEIGHT + BUTTON_MARGIN) - TOP_MARGIN) // ROW_HEIGHT


def draw_text_with_outline(text, font, text_color, outline_color, pos, surface):
    """מצייר טקסט עם outline לבן סביבו"""
    base = font.render(text, True, text_color)
    outline = font.render(text, True, outline_color)
    x, y = pos
    # צל לבן מכל הכיוונים
    for dx in [-2, -1, 1, 2]:
        for dy in [-2, -1, 1, 2]:
            surface.blit(outline, (x+dx, y+dy))
    surface.blit(base, (x, y))


# טעינת המדליות פעם אחת (מחוץ לפונקציה)
trophy_gold   = pygame.image.load("images/medal-gold.png").convert_alpha()
trophy_silver = pygame.image.load("images/medal-silver.png").convert_alpha()
trophy_bronze = pygame.image.load("images/medal-bronze.png").convert_alpha()

trophy_gold   = pygame.transform.scale(trophy_gold, (24,24))
trophy_silver = pygame.transform.scale(trophy_silver, (24,24))
trophy_bronze = pygame.transform.scale(trophy_bronze, (24,24))


def draw_leaderboard():
    global leaderboard_scroll
    draw_gradient_background_with_tetris_static(screen, (20,20,60), (60,0,80))

    # overlay שקוף
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0,0,0,120))
    screen.blit(overlay, (0,0))

    # כותרת
    draw_text_with_outline("LEADERBOARD", title_font, Colors.yellow, Colors.white,
                           (WIDTH//2 - 160, 70), screen)

    entries = load_leaderboard()
    max_display = LEADERBOARD_MAX_DISPLAY

    # הגבלת גלילה
    max_scroll = max(0, len(entries) - max_display)
    leaderboard_scroll = max(0, min(leaderboard_scroll, max_scroll))

    # אזור רשימה
    list_height = max_display * ROW_HEIGHT
    list_rect = pygame.Rect(50, TOP_MARGIN, WIDTH-100, list_height)
    list_surface = pygame.Surface((list_rect.width, ROW_HEIGHT*len(entries)), pygame.SRCALPHA)

    # ציור שורות
    for i, entry in enumerate(entries):
        rank = i + 1
        if rank == 1: bg_color = (255,215,0)
        elif rank == 2: bg_color = (192,192,192)
        elif rank == 3: bg_color = (205,127,50)
        else: bg_color = (40,40,70)

        rect = pygame.Rect(0, i*ROW_HEIGHT, list_rect.width, ROW_HEIGHT-5)
        pygame.draw.rect(list_surface, bg_color, rect, border_radius=12)
        pygame.draw.rect(list_surface, Colors.white, rect, 2, border_radius=12)

        # טקסט
        name_text = f"{rank}. {entry['name']}"
        score_text = f"{entry['score']}"
        draw_text_with_outline(name_text, small_font, Colors.white, Colors.black, (10, rect.y+10), list_surface)
        draw_text_with_outline(score_text, small_font, Colors.yellow, Colors.black, (rect.width-100, rect.y+10), list_surface)

        # אייקון מדליה
        if rank == 1: list_surface.blit(trophy_gold, (rect.width-40, rect.y+8))
        elif rank == 2: list_surface.blit(trophy_silver, (rect.width-40, rect.y+8))
        elif rank == 3: list_surface.blit(trophy_bronze, (rect.width-40, rect.y+8))

    # הצגת ה־Viewport
    screen.blit(list_surface, (list_rect.x, list_rect.y),
                area=pygame.Rect(0, leaderboard_scroll*ROW_HEIGHT, list_rect.width, list_rect.height))

    # Back button בתחתית
    back_rect = pygame.Rect(WIDTH//2-70, HEIGHT-(BUTTON_HEIGHT+BUTTON_MARGIN), 140, BUTTON_HEIGHT)
    mouse_pos = pygame.mouse.get_pos()
    color = Colors.light_blue if back_rect.collidepoint(mouse_pos) else Colors.dark_blue
    pygame.draw.rect(screen, color, back_rect, border_radius=10)
    pygame.draw.rect(screen, Colors.white, back_rect, 2, border_radius=10)
    back_surf = small_font.render("Back", True, Colors.white)
    screen.blit(back_surf, back_surf.get_rect(center=back_rect.center))

    return back_rect


# ---------- Main Loop ----------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        # --- Menu ---
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
                for i, rect in enumerate(menu_button_rects):
                    if rect.collidepoint(event.pos):
                        if menu_buttons[i]=="START GAME": start_game()
                        elif menu_buttons[i]=="LEADERBOARD":
                            prev_state = STATE_MENU
                            state = STATE_LEADERBOARD

        # --- Playing ---
        elif state==STATE_PLAYING:
            if event.type==pygame.KEYDOWN:
                if not game.game_over:
                    if event.key==pygame.K_LEFT: game.move_left()
                    elif event.key==pygame.K_RIGHT: game.move_right()
                    elif event.key==pygame.K_DOWN:
                        game.move_down()
                        game.update_score(0,1)
                    elif event.key==pygame.K_UP: game.rotate()
            if event.type==GAME_UPDATE and not game.game_over:
                game.move_down()
            if state==STATE_PLAYING and game.game_over:
                handle_game_over()

        # --- Game Over ---
        elif state==STATE_GAME_OVER:
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    selected_button_index = (selected_button_index-1) % len(game_over_buttons)
                elif event.key==pygame.K_RIGHT:
                    selected_button_index = (selected_button_index+1) % len(game_over_buttons)
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    sel = game_over_buttons[selected_button_index]
                    if sel=="Play Again": start_game()
                    elif sel=="Main Menu": go_to_menu()
                    elif sel=="Leaderboard":
                        prev_state = STATE_GAME_OVER
                        state = STATE_LEADERBOARD
            elif event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                for i, rect in enumerate(game_over_button_rects):
                    if rect.collidepoint(event.pos):
                        sel = game_over_buttons[i]
                        if sel=="Play Again": start_game()
                        elif sel=="Main Menu": go_to_menu()
                        elif sel=="Leaderboard":
                            prev_state = STATE_GAME_OVER
                            state = STATE_LEADERBOARD

        # --- Leaderboard ---
        elif state == STATE_LEADERBOARD:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    leaderboard_scroll = max(0, leaderboard_scroll-1)
                elif event.key == pygame.K_DOWN:
                    entries = load_leaderboard()
                    max_scroll = max(0, len(entries)-LEADERBOARD_MAX_DISPLAY)
                    leaderboard_scroll = min(leaderboard_scroll+1, max_scroll)
            elif event.type == pygame.MOUSEWHEEL:
                entries = load_leaderboard()
                max_scroll = max(0, len(entries)-LEADERBOARD_MAX_DISPLAY)
                leaderboard_scroll -= event.y
                leaderboard_scroll = max(0, min(leaderboard_scroll, max_scroll))
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                back_rect = draw_leaderboard()
                if back_rect.collidepoint(event.pos):
                    state = prev_state
                    

        # --- Enter Name ---
        elif state==STATE_ENTER_NAME:
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    if player_name.strip():
                        add_score(player_name.strip(), game.score)
                        state = STATE_GAME_OVER
                elif event.key==pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    if len(player_name)<10:
                        player_name += event.unicode
            elif event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                input_rect, submit_rect = draw_enter_name()  # נקבל את ה־rect של הכפתור
                if submit_rect.collidepoint(event.pos) and player_name.strip():
                    add_score(player_name.strip(), game.score)
                    state = STATE_GAME_OVER

    # --- Drawing ---
    if state==STATE_MENU: draw_menu()
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
    elif state==STATE_LEADERBOARD:
        draw_leaderboard()
    elif state==STATE_ENTER_NAME:
        draw_enter_name()

    pygame.display.update()
    clock.tick(60)
    