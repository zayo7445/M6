import pygame


class Audio:
    instance = None

    @staticmethod
    def get_instance():
        if Audio.instance is None:
            Audio.instance = Audio()
        return Audio.instance

    """A class for handling audio."""
    def __init__(self, music_volume=0.5, sfx_volume=0.5):
        pygame.mixer.init()

        pygame.mixer.set_num_channels(32)

        self.music_channel = pygame.mixer.Channel(0)
        self.music_channel.set_volume(music_volume)

        self.music_volume = music_volume
        self.sfx_volume = sfx_volume
        self.sound_effects = {}

        pygame.mixer.music.set_volume(self.music_volume)

    def load_music(self, music_file):
        """Loads a music file for background music."""
        self.music = pygame.mixer.Sound(music_file)

    def play_music(self, loops=-1):
        """Plays the loaded background music. -1 means loop indefinitely."""
        if self.music:
            self.music_channel.play(self.music, loops=loops)

    def stop_music(self):
        """Stops the background music."""
        self.music_channel.stop()

    def pause_music(self):
        """Pauses the background music."""
        self.music_channel.pause()

    def resume_music(self):
        """Unpauses the background music."""
        self.music_channel.unpause()

    def set_music_volume(self, volume):
        """Sets the background music volume (0.0 to 1.0)."""
        self.music_volume = volume
        self.music_channel.set_volume(self.music_volume)

    def load_sfx(self, name, file_path):
        """Loads a sound effect and stores it by name."""
        sound = pygame.mixer.Sound(file_path)
        sound.set_volume(self.sfx_volume)
        self.sound_effects[name] = sound

    def play_sfx(self, name):
        """Plays a sound effect by name, checking for an available channel."""
        channel = pygame.mixer.find_channel()
        if channel:
            channel.play(self.sound_effects[name])

    def set_sfx_volume(self, volume):
        """Sets the volume for sound effects (0.0 to 1.0)."""
        self.sfx_volume = volume
        for sound in self.sound_effects.values():
            sound.set_volume(self.sfx_volume)