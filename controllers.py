import pygame


class Controller:
    """A class to interface with a connected game controller."""
    def __init__(self):
        self.controller = pygame.joystick.Joystick(0) if pygame.joystick.get_count() > 0 else None
        self.deadzone = 0.1
        if self.controller:
            self.controller.init()

    def get_axis(self, axis):
        """Gets values for specified axis with a dead zone threshold."""
        if self.controller:
            axis = self.controller.get_axis(axis)
            return axis if abs(axis) > self.deadzone else 0
        return 0

    def get_button(self, button):
        """Gets state of the specified button."""
        if self.controller:
            return self.controller.get_button(button)
        return False

    def rumble(self, low_frequency=0.3, high_frequency=0.3, duration=100):
        """Triggers a controller rumble with specified frequency and duration."""
        if self.controller:
            self.controller.rumble(low_frequency, high_frequency, duration)
