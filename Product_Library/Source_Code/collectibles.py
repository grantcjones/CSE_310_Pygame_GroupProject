import pygame

# Define screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)

# Create a basic collectible class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))

    def apply_effect(self, player):
        pass  # To be overridden in subclasses

# Define specific items: Coin, Health, SpeedBoost, DamageBoost
class Coin(Collectible):
    def apply_effect(self, player):
        player.coins += 1

class Health(Collectible):
    def apply_effect(self, player):
        player.health = min(player.health + 20, player.max_health)

class SpeedBoost(Collectible):
    def apply_effect(self, player):
        player.speed += 2  # Increase speed
        # Set a timer to remove effect after some time

class DamageBoost(Collectible):
    def apply_effect(self, player):
        player.damage += 5  # Increase damage
        # Set a timer to remove effect after some time

# Player class for interaction
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.coins = 0
        self.health = 100
        self.max_health = 100
        self.speed = 5
        self.damage = 10

    def update(self):
        # Player movement code here
        pass

# Initialize game objects
player = Player()
collectibles = pygame.sprite.Group()
collectibles.add(Coin(100, 100, "coin.png"))
collectibles.add(Health(200, 100, "health.png"))
collectibles.add(SpeedBoost(300, 100, "speed_boost.png"))
collectibles.add(DamageBoost(400, 100, "damage_boost.png"))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Collision detection
    for collectible in collectibles:
        if pygame.sprite.collide_rect(player, collectible):
            collectible.apply_effect(player)
            collectible.kill()  # Remove item after collection

    # Update screen and objects
    collectibles.update()
    player.update()
    # Draw code here

pygame.quit()
