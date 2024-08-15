import pygame
import random
import sys

pygame.init()

width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("bird attack")

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

try:
    dog_img = pygame.image.load("dog.png")
    bone_img = pygame.image.load("bone.png")
    obstacle_img = pygame.image.load("obstacle.png")
    dog_img = pygame.transform.scale(dog_img, (50, 50))
    bone_img = pygame.transform.scale(bone_img, (30, 30))
    obstacle_img = pygame.transform.scale(obstacle_img, (50, 50))
except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    sys.exit()

def reset_game():
    global dog_pos, bone_pos, obstacle_positions, obstacle_velocities, game_over, score
    global dog_speed
    dog_pos = [width // 2, height // 2]
    bone_pos = [random.randint(0, width - 30), random.randint(0, height - 30)]
    obstacle_positions = [[random.randint(0, width - 50), random.randint(0, height - 50)] for _ in range(num_obstacles)]
    obstacle_velocities = [[random.choice([-obstacle_speed, obstacle_speed]), random.choice([-obstacle_speed, obstacle_speed])] for _ in range(num_obstacles)]
    game_over = False
    score = 0

num_obstacles = 2
dog_speed = 5
obstacle_speed = 3
reset_game()

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            dog_pos[0] -= dog_speed
        if keys[pygame.K_RIGHT]:
            dog_pos[0] += dog_speed
        if keys[pygame.K_UP]:
            dog_pos[1] -= dog_speed
        if keys[pygame.K_DOWN]:
            dog_pos[1] += dog_speed

        for i in range(num_obstacles):
            obstacle_positions[i][0] += obstacle_velocities[i][0]
            obstacle_positions[i][1] += obstacle_velocities[i][1]
            if obstacle_positions[i][0] <= 0 or obstacle_positions[i][0] >= width - 50:
                obstacle_velocities[i][0] = -obstacle_velocities[i][0]
            if obstacle_positions[i][1] <= 0 or obstacle_positions[i][1] >= height - 50:
                obstacle_velocities[i][1] = -obstacle_velocities[i][1]

        dog_rect = pygame.Rect(dog_pos[0], dog_pos[1], 50, 50)
        bone_rect = pygame.Rect(bone_pos[0], bone_pos[1], 30, 30)
        if dog_rect.colliderect(bone_rect):
            score += 1
            bone_pos = [random.randint(0, width - 30), random.randint(0, height - 30)]

        for pos in obstacle_positions:
            obstacle_rect = pygame.Rect(pos[0], pos[1], 50, 50)
            if dog_rect.colliderect(obstacle_rect):
                game_over = True

    screen.fill(black)
    screen.blit(dog_img, (int(dog_pos[0]), int(dog_pos[1])))
    screen.blit(bone_img, (int(bone_pos[0]), int(bone_pos[1])))
    for pos in obstacle_positions:
        screen.blit(obstacle_img, (int(pos[0]), int(pos[1])))
    
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (width - 120, 20))

    if game_over:
        game_over_text = font.render("Game Over", True, red)
        screen.blit(game_over_text, (width // 2 - 100, height // 2))
        retry_text = font.render("Press R to Retry", True, white)
        screen.blit(retry_text, (width // 2 - 120, height // 2 + 40))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r] and game_over:
        reset_game()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
