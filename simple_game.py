import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Game window
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collect the Coins!")

# Font
font = pygame.font.Font(None, 48)

# Colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Function to reset game
def reset_game():
    player = pygame.Rect(300, 250, 50, 50)
    coin_x = random.randint(20, WIDTH - 20)
    coin_y = random.randint(20, HEIGHT - 20)
    obstacle = pygame.Rect(200, 150, 100, 100)
    return player, coin_x, coin_y, obstacle, 0  # score = 0


# Game loop wrapper
def game_loop():
    player, coin_x, coin_y, obstacle, score = reset_game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            player.x += 5
        if keys[pygame.K_LEFT]:
            player.x -= 5
        if keys[pygame.K_DOWN]:
            player.y += 5
        if keys[pygame.K_UP]:
            player.y -= 5

        # Collision with coin
        distance = ((player.centerx - coin_x) ** 2 + (player.centery - coin_y) ** 2) ** 0.5
        if distance < (player.width // 2 + 15):
            score += 1
            coin_x = random.randint(20, WIDTH - 20)
            coin_y = random.randint(20, HEIGHT - 20)

        # Collision with obstacle
        if player.colliderect(obstacle):
            return "lose", score

        # Win condition
        if score >= 10:
            return "win", score

        # Draw
        screen.fill(BLACK)
        pygame.draw.rect(screen, GREEN, player)
        pygame.draw.circle(screen, YELLOW, (coin_x, coin_y), 15)
        pygame.draw.rect(screen, RED, obstacle)

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        pygame.time.Clock().tick(30)


# End screen with restart option
def end_screen(message):
    waiting = True
    while waiting:
        screen.fill(BLACK)
        text = font.render(message, True, WHITE)
        text2 = font.render("Press R to Restart or Q to Quit", True, WHITE)
        screen.blit(text, (200, 180))
        screen.blit(text2, (80, 250))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # restart
                    waiting = False
                if event.key == pygame.K_q:  # quit
                    pygame.quit()
                    sys.exit()


# Main loop
while True:
    result, score = game_loop()
    if result == "win":
        end_screen("YOU WIN!")
    else:
        end_screen("GAME OVER")
