import pygame
import random

class Combat:
    def __init__(self, obstacles, bullet_speed=10, bullet_radius=5, max_ammo=10):
        self.obstacles = obstacles
        self.bullet_speed = bullet_speed
        self.bullet_radius = bullet_radius
        self.bullets = []
        self.max_ammo = max_ammo
        self.ammo = max_ammo

    def shoot(self, x, y, dx, dy, owner):
        if self.ammo <= 0:
            return
        self.ammo -= 1

        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            factor = (self.bullet_speed / ((dx**2 + dy**2)**0.5))
            dx *= factor
            dy *= factor

        self.bullets.append({
            'x': x, 'y': y, 'dx': dx, 'dy': dy, 'owner': owner
        })

    def reload(self):
        self.ammo = self.max_ammo

    def update_bullets(self, players, width, height):
        for bullet in self.bullets[:]:
            bullet['x'] += bullet['dx']
            bullet['y'] += bullet['dy']

            # Remove off-screen
            if bullet['x'] < 0 or bullet['x'] > width or bullet['y'] < 0 or bullet['y'] > height:
                self.bullets.remove(bullet)
                continue

            bullet_rect = pygame.Rect(
                bullet['x'] - self.bullet_radius,
                bullet['y'] - self.bullet_radius,
                self.bullet_radius * 2,
                self.bullet_radius * 2
            )

            # Player collisions
            for sid, pdata in players.items():
                if pdata['name'] != bullet['owner']:
                    hitbox = pygame.Rect(pdata['x'], pdata['y'], 40, 40)
                    if bullet_rect.colliderect(hitbox):
                        pdata['health'] = max(0, pdata.get('health', 100) - 10)
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                        break

            # Obstacle collisions
            for obs in self.obstacles:
                if bullet_rect.colliderect(obs):
                    if random.random() < 0.5:
                        # Bounce
                        if abs(bullet_rect.centerx - obs.left) < 5 or abs(bullet_rect.centerx - obs.right) < 5:
                            bullet['dx'] *= -1
                        else:
                            bullet['dy'] *= -1
                    else:
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                    break

    def draw_bullets(self, screen, color=(255, 255, 0)):
        for bullet in self.bullets:
            pygame.draw.circle(screen, color, (int(bullet['x']), int(bullet['y'])), self.bullet_radius)

    def draw_hud(self, screen, players, player_name, height):
        font = pygame.font.Font(None, 30)
        hud_y = height - 100  # position below bottom wall
        hud_x = 40

        # Background strip
        pygame.draw.rect(screen, (20, 20, 20), (20, hud_y - 30, 800, 100))

        for sid, pdata in players.items():
            # Health bar
            health_ratio = pdata.get('health', 100) / 100
            bar_width = 150
            bar_height = 12
            bar_x = hud_x
            bar_y = hud_y

            pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))

            # Player name
            name_text = font.render(pdata['name'], True, (255, 255, 255))
            screen.blit(name_text, (bar_x, bar_y - 25))

            # Ammo (only for yourself)
            if pdata['name'] == player_name:
                ammo_text = font.render(f"Ammo: {self.ammo}/{self.max_ammo}", True, (255, 255, 0))
                screen.blit(ammo_text, (bar_x + 200, bar_y - 5))

            hud_x += 300  # space between players
