import pygame
import sys
import random
import math
from player import Player
from enemy import Enemy
from platform_module import Platform
from gate import Gate
from backgroundmusic import BackgroundMusic
import itertools

from db import create_save, load_player_save, load_enemies_save, load_platforms_save, delete_save

pygame.init()

try:
    pygame.mixer.init()
except pygame.error as e:
    print(f"Error initializing Pygame mixer: {e}")
    sys.exit(1)

# Constants
NORMAL_BACKGROUND_IMAGES = [
    'art/background_1.png',
    'art/background_2.png',
    'art/background_3.png',
    'art/background_4.png',
    'art/background_5.png',
    'art/background_6.png',
    'art/background_7.png',
    'art/background_8.png',
    'art/background_9.png',
    'art/background_10.png'
]
DUNGEON_BACKGROUND_IMAGES = [
    'art/dungeon_background_1.png',
    'art/dungeon_background_2.png',
    'art/dungeon_background_3.png',
    'art/dungeon_background_4.png',
    'art/dungeon_background_5.png'
]

MUSIC_FILES = [
    "music/song1.mp3",
    "music/song2.mp3",
    "music/song3.mp3",
    "music/song4.mp3",
    "music/song5.mp3",
    "music/song6.mp3",
]

music = BackgroundMusic(MUSIC_FILES)


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




def interpolate_color(color1, color2, t):
    """Interpolate between two colors based on t (0 to 1)."""
    return tuple(
        int(color1[i] * (1 - t) + color2[i] * t)
        for i in range(3)
    )

def start_menu():
    """Draw the start-menu options with a pulsating, color-changing title."""
    # Load and scale the background image
    original_image = pygame.image.load('art/dungeon_wall.png')
    scaled_image = pygame.transform.scale(original_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    # Draw the background image
    screen.blit(scaled_image, (0, 0))

    # Create a larger font for the title
    title_font = pygame.font.Font(None, 100)  # Adjust size as needed
    title_text = "JUMP QUEST"
    
    # Define the colors for pulsating
    colors = [
        (255, 215, 0),   # Gold
        (178, 34, 34),   # Deep Red
        (0, 255, 128),   # Glowing Green
        (0, 191, 255)    # Icy Blue
    ]

    # Get elapsed time and create a sine wave effect
    elapsed_time = pygame.time.get_ticks() / 1000  # Convert to seconds
    sine_value = (math.sin(elapsed_time * 2 * math.pi / 2) + 1) / 2  # Oscillates between 0 and 1 over 2 seconds
    
    # Cycle through the colors and interpolate
    color_index = int(elapsed_time) % len(colors)
    next_color_index = (color_index + 1) % len(colors)
    current_color = interpolate_color(colors[color_index], colors[next_color_index], sine_value)

    # Render the title with the interpolated color
    title_surface = title_font.render(title_text, True, current_color)
    
    # Add a shadow for depth
    shadow_surface = title_font.render(title_text, True, (50, 50, 50))  # Dark gray for shadow
    shadow_rect = shadow_surface.get_rect(center=(SCREEN_WIDTH // 2 + 5, SCREEN_HEIGHT // 6 + 5))
    screen.blit(shadow_surface, shadow_rect)

    # Render the main title slightly above the shadow
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))
    screen.blit(title_surface, title_rect)

    # Draw the buttons
    for button, text in buttons:
        # Draw button
        pygame.draw.rect(screen, (210, 180, 140), button)
        # Render text
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=button.center)
        screen.blit(text_surface, text_rect)




def start_handle_click(pos):
    """Handle mouse click on the start-menu."""
    for button, text in buttons:
        if button.collidepoint(pos):
            if text == "New Game":
                print("New Game selected!")
                # Add your logic for starting a new game here
                num_platforms = random.randint(10, 15)
                platforms = generate_platforms(num_platforms, pygame.Rect(0, 0, 50, 50))
                exit_rect = generate_exit(platforms)
                enemies = (Enemy(), Enemy(), Enemy())
                player = Player(10)

                run(player, enemies, platforms, exit_rect)
            elif text == "Load Game":
                print("Load Game selected!")
                # Add your logic for loading a game here
                
                platforms = load_platforms_save()
                exit_rect = generate_exit(platforms)
                run(load_player_save(), load_enemies_save(), platforms, exit_rect) #! Stubbed, nneds data query added
            elif text == "Exit":
                print("Exiting game...")
                pygame.quit()
                sys.exit()


def pause_menu():
    """Draw the pause menu options."""
    # Load and scale the background image
    original_image = pygame.image.load('art/scroll.png')
    scaled_image = pygame.transform.scale(original_image, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200))
    
    # Calculate position for centered background
    bg_x = (SCREEN_WIDTH - scaled_image.get_width()) // 2
    bg_y = (SCREEN_HEIGHT - scaled_image.get_height()) // 2
    screen.blit(scaled_image, (bg_x, bg_y))

    # Pause menu options
    pause_options = ["Resume", "Save & Exit", "Exit"]
    pause_buttons = []

    # Calculate positions for buttons on the scroll background
    for i, option in enumerate(pause_options):
        button_width, button_height = 200, 50
        button_x = bg_x + (scaled_image.get_width() - button_width) // 2
        button_y = bg_y + 150 + i * 100  # Adjust vertical spacing between buttons

        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, (210, 180, 140), button_rect)  # Draw button

        # Render text and center it in the button
        text_surface = font.render(option, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

        # Append button and its text for handling
        pause_buttons.append((button_rect, option))

    return pause_buttons

def pause_handle_click(pos, pause_buttons):
    """Handle mouse clicks on the pause menu."""
    for button, text in pause_buttons:
        if button.collidepoint(pos):
            if text == "Resume":
                return "resume"
            elif text == "Save & Exit":
                return "save_exit"
            elif text == "Exit":
                return "exit"

# Level settings
#level_count = 0
used_backgrounds = []
# paused = False

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Function to load a random background, ensuring no repeats until all images are used
def load_random_background(is_dungeon=False):
    global used_backgrounds
    background_list = DUNGEON_BACKGROUND_IMAGES if is_dungeon else NORMAL_BACKGROUND_IMAGES
    
    # Reset used backgrounds if transitioning to a new dungeon level
    if len(used_backgrounds) == len(background_list):
        used_backgrounds = []
    
    available_backgrounds = [bg for bg in background_list if bg not in used_backgrounds]
    background_image_path = random.choice(available_backgrounds)
    used_backgrounds.append(background_image_path)

    try:
        background_image = pygame.image.load(background_image_path)
        return pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except pygame.error as e:
        print(f"Error loading background image: {e}")
        sys.exit(1)


# Constants for minimum and maximum gaps between platforms
MIN_GAP_X = 100  # minimum gap in the x direction
MAX_GAP_X = 400  # maximum gap in the x direction
MIN_GAP_Y = 80   # minimum gap in the y direction
MAX_GAP_Y = 300  # maximum gap in the y direction

# Modified generate_platforms function to ensure gaps between platforms
def generate_platforms(num_platforms, exit_rect):
    platforms = pygame.sprite.Group()
    last_platform_rect = None

    for _ in range(num_platforms):
        attempt = 0
        while attempt < 10:
            width = random.randint(80, 200)
            height = 20
            if last_platform_rect:
                # Set x and y based on the last platform to maintain gaps
                x = last_platform_rect.right + random.randint(MIN_GAP_X, MAX_GAP_X)
                y = last_platform_rect.top + random.randint(-MAX_GAP_Y, MAX_GAP_Y)
                # Ensure new platform doesn't go off-screen
                if x + width > SCREEN_WIDTH:
                    x = random.randint(0, SCREEN_WIDTH - width)
                if y < 50 or y > SCREEN_HEIGHT - height - 50:
                    y = random.randint(50, SCREEN_HEIGHT - height - 50)
            else:
                # Position first platform randomly within screen bounds
                x = random.randint(0, SCREEN_WIDTH - width)
                y = random.randint(50, SCREEN_HEIGHT - height - 50)

            new_platform = Platform(x, y, width, height)

            # Ensure no overlap with existing platforms and no collision with exit
            if not any(platform.rect.colliderect(new_platform.rect) for platform in platforms) and \
               not new_platform.rect.colliderect(exit_rect):
                platforms.add(new_platform)
                last_platform_rect = new_platform.rect  # Update last platform position
                break
            attempt += 1
    return platforms

# Function to generate exit rectangle exactly on top of a platform
def generate_exit(platforms):
    selected_platform = random.choice(list(platforms))  # Select a random platform
    exit_width, exit_height = 50, 50  # Dimensions of the gate
    x = selected_platform.rect.centerx - exit_width // 2  # Center the gate horizontally on the platform
    y = selected_platform.rect.top - exit_height  # Position the gate so its bottom aligns with the platform's top
    return Gate(x, y + exit_height, exit_width, exit_height)



# Function to display level transition with fade effect
def level_transition(player: Player):
    player.level += 1

    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 255, 5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        font = pygame.font.Font(None, 60)
        text = font.render(f"Level {player.level}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(30)


def run():
    global used_backgrounds  # Declare global to access the global variable


    # Initial background, platforms, and exit generation
    background_image = load_random_background()
    num_platforms = random.randint(20, 30) #range number of platforms
    platforms = generate_platforms(num_platforms, pygame.Rect(0, 0, 50, 50))
    exit_rect = generate_exit(platforms)
    enemies = (Enemy('art/enemy_frame1_True.png'), Enemy('art/enemy_frame1_True.png'), Enemy('art/enemy_frame1_True.png'))
    player = Player(10)

    # Level settings
    level_count = 0
    used_backgrounds = []
    paused = False
    stop_running = False

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

        if keys[pygame.K_ESCAPE]:
            paused = True

        if paused:
            # Draw the pause menu and retrieve the buttons
            pause_buttons = pause_menu()
            pygame.display.flip()

            # Handle events specific to the pause menu
            while paused:  # Enter a loop that freezes the game
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left mouse button
                            action = pause_handle_click(event.pos, pause_buttons)
                            if action == "resume":
                                paused = False  # Resume the game
                            elif action == "save_exit":
                                # Save the game and exit
                                delete_save()
                                create_save(player, enemies, platforms)
                                sys.exit()
                            elif action == "exit":
                                # Exit the game without saving
                                sys.exit()

        # Prevent updates to the game while paused
        pygame.display.flip()  # Keep the pause menu visible

        if stop_running:
            break

        # Level transition on exit collision
        if player.rect.colliderect(exit_rect):
            level_count += 1
            level_transition(level_count)

            # Change background music
            music.next_song()

            # Determine level type and reset assets
            current_level = player.level
            is_dungeon = (current_level % 10 == 0)
            background_image = load_random_background(is_dungeon)
            platforms = generate_platforms(len(platforms), exit_rect)
            exit_rect = generate_exit(platforms)
            exit_platform = next((platform for platform in platforms if platform.rect.colliderect(exit_rect)), None)
            available_platforms = [platform for platform in platforms if platform != exit_platform]
            random_platform = random.choice(available_platforms) if available_platforms else random.choice(list(platforms))
            player.rect.midbottom = (random_platform.rect.centerx, random_platform.rect.top)

        # Exit condition
        # if keys[pygame.K_ESCAPE]:
        #     break

        level_count = font.render(f"Player Level: {player.level}", True, (255, 0 , 0))

        screen.blit(background_image, (0,0))
        platforms.draw(screen)
        screen.blit(exit_rect.image, exit_rect.rect)  # Draw exit rectangle
        screen.blit(player.image, player.rect)  # Draw player on the screen
        screen.blit(level_count, (10, 20))
        pygame.display.flip()  # Update the display

        clock.tick(60)


def main():
    # Main loop
    running = True
    while running:
        start_menu()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    start_handle_click(event.pos)

    pygame.quit()

if __name__ == "__main__":
    main()