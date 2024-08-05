import pygame
import os

pygame.init()

WIDTH, HEIGHT = 1900, 1030
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("World's best boxing game hehe")

FPS = 60

PLAYER_WIDTH, PLAYER_HEIGHT = 60, 150

PLAYER1 = pygame.image.load(os.path.join('assets', 'player1.png'))
PLAYER1_RESIZE = pygame.transform.scale(PLAYER1, (PLAYER_WIDTH, PLAYER_HEIGHT))
PLAYER2 = pygame.image.load(os.path.join('assets', 'player2.png'))
PLAYER2_RESIZE = pygame.transform.scale(PLAYER2, (PLAYER_WIDTH, PLAYER_HEIGHT))

RED = (100, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

PLATFORM_WIDTH = WIDTH
PLATFORM_HEIGHT = 20
PLATFORM_Y = HEIGHT - PLATFORM_HEIGHT - 200

GRAVITY = 1
JUMP_STRENGTH = -20

PLAYER_HEALTH = 100

def draw(p1, p2, platform, p1_health, p2_health):
    WIN.fill(RED)
    pygame.draw.rect(WIN, WHITE, platform)
    WIN.blit(PLAYER1_RESIZE, (p1.x, p1.y))
    WIN.blit(PLAYER2_RESIZE, (p2.x, p2.y))

    pygame.draw.rect(WIN, (0, 0, 255), (50, 50, p1_health, 25))
    pygame.draw.rect(WIN, (255, 0, 0), (WIDTH - 150, 50, p2_health, 25))

    pygame.display.update()

def handle_movement(keys, player, is_player1):
    if is_player1:
        if keys[pygame.K_LEFT] and player.x - 5 > 0:
            player.x -= 5
        if keys[pygame.K_RIGHT] and player.x + 5 + PLAYER_WIDTH < WIDTH:
            player.x += 5
    else:
        if keys[pygame.K_a] and player.x - 5 > 0:
            player.x -= 5
        if keys[pygame.K_d] and player.x + 5 + PLAYER_WIDTH < WIDTH:
            player.x += 5

def handle_gravity(player, platform):
    if player.y + player.height < platform.y:
        player.y += GRAVITY
    elif player.y + player.height > platform.y:
        player.y = platform.y - player.height

def handle_jump(keys, player, is_player1, velocity):
    if is_player1:
        if keys[pygame.K_UP] and player.bottom >= PLATFORM_Y:
            velocity = JUMP_STRENGTH
    else:
        if keys[pygame.K_w] and player.bottom >= PLATFORM_Y:
            velocity = JUMP_STRENGTH
    return velocity

def handle_attack(keys, player1, player2, p1_health, p2_health):
    if keys[pygame.K_SPACE]:  
        if player1.colliderect(player2):
            p2_health -= 10
    if keys[pygame.K_RETURN]:  
        if player2.colliderect(player1):
            p1_health -= 10
    return p1_health, p2_health

def display_winner(winner_text):
    WIN.fill(WHITE)
    font = pygame.font.SysFont('comicsans', 100)
    text = font.render(winner_text, True, (255, 0, 0) if winner_text == "Red Wins!" else (0, 0, 255))
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(4000)

def main():
    p1 = pygame.Rect(1800, 500, PLAYER_WIDTH, PLAYER_HEIGHT)
    p2 = pygame.Rect(100, 500, PLAYER_WIDTH, PLAYER_HEIGHT)
    platform = pygame.Rect(0, PLATFORM_Y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    clock = pygame.time.Clock()
    run = True

    p1_health = PLAYER_HEALTH
    p2_health = PLAYER_HEALTH

    p1_velocity = 0
    p2_velocity = 0

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        handle_movement(keys, p1, True)
        handle_movement(keys, p2, False)

        if p1.bottom < PLATFORM_Y:
            p1_velocity += GRAVITY
        else:
            p1_velocity = 0
            p1.y = PLATFORM_Y - PLAYER_HEIGHT

        if p2.bottom < PLATFORM_Y:
            p2_velocity += GRAVITY
        else:
            p2_velocity = 0
            p2.y = PLATFORM_Y - PLAYER_HEIGHT

        p1_velocity = handle_jump(keys, p1, True, p1_velocity)
        p2_velocity = handle_jump(keys, p2, False, p2_velocity)

        p1.y += p1_velocity
        p2.y += p2_velocity

        p1_health, p2_health = handle_attack(keys, p1, p2, p1_health, p2_health)

        if p1_health <= 0:
            display_winner("Red Wins!")
            run = False
        elif p2_health <= 0:
            display_winner("Blue Wins!")
            run = False

        draw(p1, p2, platform, p1_health, p2_health)

    pygame.quit()

if __name__ == "__main__":
    main()