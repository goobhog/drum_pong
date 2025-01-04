import pygame.mixer

class Drum:
    def __init__(self, sound_file_path):
        self.sound = pygame.mixer.Sound(sound_file_path)

    def play(self, velocity):
        """
        Plays the drum sound with the specified velocity.

        Args:
            velocity: MIDI velocity (0-127).
        """
        gain = velocity / 127.0  # Simple velocity-to-gain mapping
        self.sound.set_volume(gain)
        self.sound.play()
