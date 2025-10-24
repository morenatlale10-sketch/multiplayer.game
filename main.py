import pygame
from network import Network

pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2-Player Multiplayer Game")
clock = pygame.time.Clock()

# --- Player setup ---
player_name = input("Enter your name: ")
network = Network()
network.join_game(player_name)

player_x, player_y = 100, 100
player_speed = 5

running = True
while running:
    clock.tick(60)
    screen.fill((30, 30, 30))

    # --- Handle input ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Send position to server
    network.send_action(player_x, player_y)

    # --- Draw all players ---
    font = pygame.font.Font(None, 24)
    for sid, pdata in network.players.items():
        color = (0, 255, 0) if pdata['name'] == player_name else (255, 0, 0)
        pygame.draw.rect(screen, color, (pdata['x'], pdata['y'], 30, 30))
        name_text = font.render(pdata['name'], True, (255, 255, 255))
        screen.blit(name_text, (pdata['x'], pdata['y'] - 20))

    pygame.display.flip()

    # --- Event handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
