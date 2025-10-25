import pygame

class Physics:
    def __init__(self, obstacles=None):
        # List of pygame.Rect obstacles
        self.obstacles = obstacles if obstacles else []

    def check_collision(self, rect):
        """
        Check if the given rect collides with any obstacles.
        Returns True if there is a collision.
        """
        for obs in self.obstacles:
            if rect.colliderect(obs):
                return True
        return False
