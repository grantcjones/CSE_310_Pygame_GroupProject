import pygame
import random
from entity import Entity
from platform_module import Platform
from gate import Gate
from typing import List
# from main import SCREEN_WIDTH
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600

class Player(Entity):
    def __init__(self, health: int):
        # Initialize the parent class
        super().__init__(health)
        self.id = 'player'

        # Load player sprite
        self.image = pygame.image.load("art/player_frame1_True.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (500, 500)

        self.half_jump_height = 18
        self.is_jumping = False
        self.jumps_left = 2

        # Initialize player-specific attributes
        self.level = 0  # Start the player at level 1
        self.animation_True = [
            "art/player_frame1_True.png",
            "art/player_frame2_True.png"
        ]
        self.animation_False = [
            "art/player_frame1_False.png",
            "art/player_frame2_False.png"
        ]

    def get_level(self) -> int:
        return self.level

    def set_level(self, level: int) -> None:
        self.level = level

    def move(self):
        keys = pygame.key.get_pressed() #! Move player movement logic to Player class

        # Movement
        if keys[pygame.K_a] and self.rect.left > 0:
            self.flip_False()
            self.update_frame()
            self.rect.x -= self.move_speed
        if keys[pygame.K_d] and self.rect.right < SCREEN_WIDTH:
            self.flip_True()
            self.update_frame()
            self.rect.x += self.move_speed

         # Jumping logic with double jump
        if keys[pygame.K_SPACE]:
            if self.jumps_left > 0 and not self.is_jumping:
                self.velocity_y = -self.half_jump_height if self.jumps_left == 2 else -self.half_jump_height
                self.jumps_left -= 1
                self.is_jumping = True

    def platform_collision(self, keys, platforms: pygame.sprite.Group, exit_rect: Gate, level_count):
        on_platform = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.is_jumping = False
                    self.jumps_left = 2
                    break

        if not on_platform and self.rect.bottom < SCREEN_HEIGHT:
            self.velocity_y += self.gravity

        # Level transition on exit collision
        if self.rect.colliderect(exit_rect):
            self.level += 1

                    # Check if the player has fallen past the bottom of the screen
        if self.rect.top >= SCREEN_HEIGHT:
            # Convert platforms group to a list and respawn player on a new platform
            platforms_list = list(platforms)
            random_platform = random.choice(platforms_list) if platforms_list else None  # Check if there are platforms
            if random_platform:
                # Respawn the self on the selected platform
                self.rect.midbottom = (random_platform.rect.centerx, random_platform.rect.top)
                # Reset vertical velocity to prevent immediate falling
                self.velocity_y = 0
                self.is_jumping = False

    def update_entity(self, keys, platforms: pygame.sprite.Group, exit_rect: Gate, level_count):
        keys = pygame.key.get_pressed()

        # Movement
        if keys[pygame.K_a] and self.rect.left > 0:
            self.flip_False()
            self.update_frame()
            self.rect.x -= self.move_speed
        if keys[pygame.K_d] and self.rect.right < SCREEN_WIDTH:
            self.flip_True()
            self.update_frame()
            self.rect.x += self.move_speed

        self.move()
        self.platform_collision(keys, platforms, exit_rect, level_count)

        # Apply gravity
        self.rect.y += self.velocity_y
        if self.velocity_y < 0:
            self.is_jumping = True
        elif self.velocity_y > 0:
            self.is_jumping = False

                

            