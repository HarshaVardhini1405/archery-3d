import pygame
import sys
from pytmx.util_pygame import load_pygame

# Initialize
pygame.init()
pygame.mixer.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🏹 Archery Game")
clock = pygame.time.Clock()

# Load assets
tmx_data = load_pygame("tile map archery.tmx")

archer_img = pygame.image.load("archery5.png").convert_alpha()
archer_img = pygame.transform.scale(archer_img, (100, 100))

arrow_img = pygame.image.load("arrow.png").convert_alpha()
arrow_img = pygame.transform.scale(arrow_img, (60, 20))

target_img = pygame.image.load("target.png").convert_alpha()
target_img = pygame.transform.scale(target_img, (100, 100))
target_rect = target_img.get_rect()
target_rect.x = WIDTH - 200
target_rect.y = HEIGHT // 2 - 50

# Fonts
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

# Sounds
pygame.mixer.music.load("bg_music.mp3")
pygame.mixer.music.set_volume(0.5)
shoot_sound = pygame.mixer.Sound("shoot.wav")

# Game variables
archer_x, archer_y = 100, HEIGHT // 2 - 50
arrow_x, arrow_y = archer_x + 50, archer_y + 40
arrow_speed = 15
arrow_fired = False

score = 0
chances = 5
game_over = False
game_started = False

target_speed_y = 3
target_direction = 1

# Utility functions
def draw_tile_map():
    for layer in tmx_data.visible_layers:
        if hasattr(layer, 'tiles'):
            for x, y, tile in layer.tiles():
                if tile:
                    screen.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

def show_score():
    text = font.render(f"Score: {score}   Chances Left: {chances}", True, (0, 0, 0))
    screen.blit(text, (20, 20))

def show_game_over():
    text = big_font.render("Game Over!", True, (255, 0, 0))
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, rect)

def draw_archer(x, y):
    screen.blit(archer_img, (x, y))

def draw_start_screen():
    screen.fill((200, 230, 255))
    title = big_font.render("🏹 Archery Game", True, (0, 100, 0))
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title, title_rect)

    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 60)
    pygame.draw.rect(screen, (0, 150, 0), button_rect, border_radius=10)
    button_text = font.render("Start Game", True, (255, 255, 255))
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

    pygame.display.update()
    return button_rect

# Show start menu
start_button_rect = draw_start_screen()
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button_rect.collidepoint(event.pos):
                game_started = True
                waiting = False
                pygame.mixer.music.play(-1)

# Main game loop
running = True
while running:
    screen.fill((255, 255, 255))
    draw_tile_map()
    screen.blit(target_img, target_rect)
    draw_archer(archer_x, archer_y)
    screen.blit(arrow_img, (arrow_x, arrow_y))
    show_score()
    if game_over:
        show_game_over()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not arrow_fired and not game_over:
            if event.key == pygame.K_SPACE:
                arrow_fired = True
                shoot_sound.play()

    # Archer movement
    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_UP] and archer_y > 0:
            archer_y -= 5
        if keys[pygame.K_DOWN] and archer_y < HEIGHT - 100:
            archer_y += 5
        if not arrow_fired:
            arrow_y = archer_y + 40

    # Move target
    if not game_over:
        target_rect.y += target_speed_y * target_direction
        if target_rect.y <= 0 or target_rect.y >= HEIGHT - target_rect.height:
            target_direction *= -1

    # Move arrow
    if arrow_fired and not game_over:
        arrow_x += arrow_speed
        arrow_rect = pygame.Rect(arrow_x, arrow_y, 60, 20)
        bullseye = pygame.Rect(target_rect.x + 35, target_rect.y + 35, 30, 30)
        inner_ring = pygame.Rect(target_rect.x + 20, target_rect.y + 20, 60, 60)
        outer_ring = target_rect

        if arrow_rect.colliderect(bullseye):
            score += 100
            arrow_fired = False
        elif arrow_rect.colliderect(inner_ring):
            score += 75
            arrow_fired = False
        elif arrow_rect.colliderect(outer_ring):
            score += 50
            arrow_fired = False
        elif arrow_x > WIDTH:
            chances -= 1
            arrow_fired = False
            if chances == 0:
                game_over = True

        if not arrow_fired:
            arrow_x = archer_x + 50
            arrow_y = archer_y + 40

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
