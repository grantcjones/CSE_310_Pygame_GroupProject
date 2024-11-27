import pygame

from player import Player
from platform_module import Platform
from enemy import Enemy

from main import load_random_background
from db import create_save
from db import load_player_save
from db import load_platforms_save
from db import load_enemies_save
from db import delete_save

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600

player = Player(10)

enemy1 = Enemy('Product_Library/Source_Code/art/enemy_frame1_True.png')
enemy2 = Enemy('Product_Library/Source_Code/art/enemy_frame1_True.png')
enemy3 = Enemy('Product_Library/Source_Code/art/enemy_frame1_True.png')

enemies = (enemy1, enemy2, enemy3)

platform1 = Platform(100, 100, 1000, 600)
platform2 = Platform(100, 100, 1000, 600)
platform3 = Platform(100, 100, 1000, 600)

platforms = (platform1, platform2, platform3)

def main():

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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


    try:
        create_save(player)
    except:
        raise "Failed to create save file"
    
    try:
        print(load_player_save())
    except:
        raise FileNotFoundError
    
    try:
        print(load_platforms_save())
    except:
        raise FileNotFoundError

    try:
        print(load_enemies_save())
    except:
        raise FileNotFoundError
    
    try:
        delete_save()
    except:
        raise FileNotFoundError
    
if __name__ == '__main__':
    main()