import pygame
import random
import math

class Entity(pygame.sprite.Sprite):
    def __init__(self, health: int):
        self.health = health
        self.direction = True
        
        self.animation_True = []
        self.animation_False = []

        self.move_speed = 5
        
        self.gravity = 2
        self.velocity_y = 0        

        self.current_frame = 0
        self.frame_counter = 0
        self.last_update_time = pygame.time.get_ticks()
        self.frame_interval = 500  # Milliseconds for switching frames

    def flip_True(self):
        """Faces the player sprite to the right."""

        if not self.direction:
            self.frame_counter = 0  # Reset frame counter when switching direction
            self.direction = True
            self.update_frame()
            self.image = pygame.image.load(self.animation_True[self.frame_counter])

    def flip_False(self):
        """Faces the player sprite to the left."""
        if self.direction:
            self.frame_counter = 0  # Reset frame counter when switching direction
            self.direction = False
            self.update_frame()
            self.image = pygame.image.load(self.animation_False[self.frame_counter])

    def update_frame(self):
        """Ensures the frame change is managed consistently, whether the player is facing True or False."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.frame_interval:
            self.last_update_time = current_time
            self.frame_counter = (self.frame_counter + 1) % 2

    def update_entity(self):
        raise NotImplementedError("Subclass must implement 'update_entity' method.")
    
    def move():
        raise NotImplementedError("Subclass must implement 'move' method.")