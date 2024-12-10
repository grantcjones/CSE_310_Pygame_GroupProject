import pygame

class BackgroundMusic:
    def __init__(self, music_files):
        self.music_files = music_files
        self.current_index = 0

    def play_music(self):
        """Play the current song in the playlist."""
        pygame.mixer.music.load(self.music_files[self.current_index])
        pygame.mixer.music.play(-1)  # Loop indefinitely

    def next_song(self):
        """Switch to the next song in the playlist."""
        self.current_index = (self.current_index + 1) % len(self.music_files)
        self.play_music()

    def stop_music(self):
        """Stop playing music."""
        pygame.mixer.music.stop()


