import pygame
import sys
import random
import math
from player import Player
from enemy import Enemy
from platform_module import Platform
from gate import Gate

# from db import create_save
# from db import load_player_save
# from db import load_enemies_save
# from db import load_platforms_save

pygame.init()

try:
    pygame.mixer.init()
except pygame.error as e:
    print(f"Error initializing Pygame mixer: {e}")
    sys.exit(1)

# Constants
NORMAL_BACKGROUND_IMAGES = [
    'Product_Library/Source_Code/art/background_1.png',
    'Product_Library/Source_Code/art/background_2.png',
    'Product_Library/Source_Code/art/background_3.png',
    'Product_Library/Source_Code/art/background_4.png',
    'Product_Library/Source_Code/art/background_5.png',
    'Product_Library/Source_Code/art/background_6.png',
    'Product_Library/Source_Code/art/background_7.png',
    'Product_Library/Source_Code/art/background_8.png',
    'Product_Library/Source_Code/art/background_9.png',
    'Product_Library/Source_Code/art/background_10.png'
]
DUNGEON_BACKGROUND_IMAGES = [
    'Product_Library/Source_Code/art/dungeon_background_1.png',
    'Product_Library/Source_Code/art/dungeon_background_2.png',
    'Product_Library/Source_Code/art/dungeon_background_3.png',
    'Product_Library/Source_Code/art/dungeon_background_4.png',
    'Product_Library/Source_Code/art/dungeon_background_5.png'
]

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600

# Fonts
font = pygame.font.Font(None, 50)

# Menu options
options = ["New Game", "Load Game", "Exit"]
buttons = []

# Create buttons as rects
for i, option in enumerate(options):
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 150 + i * 100, 200, 50)
    buttons.append((button_rect, option))


def draw_menu():
    """Draw the menu options."""
    # Load and scale the background image
    original_image = pygame.image.load('Product_Library/Source_Code/art/dungeon_wall.png')
    scaled_image = pygame.transform.scale(original_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    # Draw the background image
    screen.blit(scaled_image, (0, 0))    
    for button, text in buttons:
        # Draw button
        pygame.draw.rect(screen, (210, 180, 140), button)
        # Render text
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=button.center)
        screen.blit(text_surface, text_rect)


def handle_click(pos):
    """Handle mouse click on the menu."""
    for button, text in buttons:
        if button.collidepoint(pos):
            if text == "New Game":
                print("New Game selected!")
                # Add your logic for starting a new game here
                run()
            elif text == "Load Game":
                print("Load Game selected!")
                # Add your logic for loading a game here
                

                run() #! Stubbed, nneds data query added
            elif text == "Exit":
                print("Exiting game...")
                pygame.quit()
                sys.exit()


# Level settings
level_count = 1
used_backgrounds = []

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Function to load a random background, ensuring no repeats until all images are used
def load_random_background(is_dungeon=False):
    global used_backgrounds
    background_list = DUNGEON_BACKGROUND_IMAGES if is_dungeon else NORMAL_BACKGROUND_IMAGES
    if len(used_backgrounds) == len(background_list):
        used_backgrounds = []  # Reset used images when all have been used

    background_image_path = random.choice([bg for bg in background_list if bg not in used_backgrounds])
    used_backgrounds.append(background_image_path)
    try:
        background_image = pygame.image.load(background_image_path)
        return pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except pygame.error as e:
        print(f"Error loading background image: {e}")
        sys.exit(1)

# Function to generate platforms with no overlap
def generate_platforms(num_platforms, exit_rect):
    platforms = pygame.sprite.Group()
    for _ in range(num_platforms):
        attempt = 0
        while attempt < 10:
            width = random.randint(80, 200)
            height = 20
            x = random.randint(0, SCREEN_WIDTH - width)
            y = random.randint(50, SCREEN_HEIGHT - height - 50)
            new_platform = Platform(x, y, width, height)

            if not any(platform.rect.colliderect(new_platform.rect) for platform in platforms) and \
               not new_platform.rect.colliderect(exit_rect):
                platforms.add(new_platform)
                break
            attempt += 1
    return platforms

# Function to generate exit rectangle on top of a platform
def generate_exit(platforms):
    selected_platform = random.choice(list(platforms))
    exit_width, exit_height = 50, 50
    x = selected_platform.rect.centerx - exit_width // 2
    y = selected_platform.rect.top - exit_height
    return Gate(x, y)

# Function to display level transition with fade effect
def level_transition(level):
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 255, 5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        font = pygame.font.Font(None, 60)
        text = font.render(f"Level {level}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(30)

def run():
    # Initial background, platforms, and exit generation
    background_image = load_random_background()
    num_platforms = random.randint(10, 15)
    platforms = generate_platforms(num_platforms, pygame.Rect(0, 0, 50, 50))
    exit_rect = generate_exit(platforms)
    player = Player(10)

    # Level settings
    level_count = 1
    used_backgrounds = []

    # Initial player position on a random platform that is not the same as the exit platform
    platforms_list = list(platforms)
    exit_platform = next((platform for platform in platforms if platform.rect.colliderect(exit_rect)), None)
    available_platforms = [platform for platform in platforms_list if platform != exit_platform]
    random_platform = random.choice(available_platforms) if available_platforms else random.choice(platforms_list)
    player.rect.midbottom = (random_platform.rect.centerx, random_platform.rect.top)

    # Game loop
    while True:
        pygame.event.pump()

        # Frame rate control
        clock.tick(60)  # Limit to 60 frames per second

        # Player input handling
        keys = pygame.key.get_pressed() #! Move player movement logic to Player class
        player.update_entity(keys, platforms, exit_rect, level_count)

        # Level transition on exit collision
        if player.rect.colliderect(exit_rect):
            level_count += 1
            level_transition(level_count)

            # Determine level type and reset assets
            is_dungeon = (level_count % 10 == 0)
            background_image = load_random_background(is_dungeon)
            platforms = generate_platforms(num_platforms, exit_rect)
            exit_rect = generate_exit(platforms)
            exit_platform = next((platform for platform in platforms if platform.rect.colliderect(exit_rect)), None)
            available_platforms = [platform for platform in platforms if platform != exit_platform]
            random_platform = random.choice(available_platforms) if available_platforms else random.choice(list(platforms))
            player.rect.midbottom = (random_platform.rect.centerx, random_platform.rect.top)

        # Exit condition
        if keys[pygame.K_ESCAPE]:
            break

        screen.blit(background_image, (0,0))
        platforms.draw(screen)
        screen.blit(exit_rect.image, exit_rect.rect)  # Draw exit rectangle
        screen.blit(player.image, player.rect)  # Draw player on the screen
        pygame.display.flip()  # Update the display

        clock.tick(60)


def main():
    # Main loop
    running = True
    while running:
        draw_menu()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    handle_click(event.pos)

    pygame.quit()

if __name__ == "__main__":
    main()