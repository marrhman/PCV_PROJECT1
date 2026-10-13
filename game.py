import pygame
import random

def draw_world(screen):
    screen.fill((100, 150, 190))

    # Area migrasi Tuna
    pygame.draw.rect(screen,(170, 150, 110),(0, 200, 900, 100))
    pygame.draw.rect(screen,(170, 150, 130),(0, 400, 900, 100))

    pygame.draw.line(screen,(255, 255, 255),(0, 80),(900, 80),2) # Garis spawn Nemo
    pygame.draw.line(screen,(255, 255, 255),(0, 620),(900, 620),2) # Garis tujuan migrasi

#pygame setup
pygame.init()
screen = pygame.display.set_mode((900, 700)) #640x480 di opencv
clock = pygame.time.Clock()
running = True
font = pygame.font.Font(None, 28)

#Nemo setup
nemo_x = 450
nemo_y = 80
nemo_speed = 2
score = 0

#Tuna setup
tunas = [[0, 240, 3, 1],[180, 240, 2, 1],[470, 240, 4, 1],[720, 440, 2, -1]] #[x, y, speed, direction]
last_spawn = pygame.time.get_ticks()
spawn_delay = random.randint(500, 1500)

while running:
    # 1. Event
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Update
    #update nemo
    nemo_y += nemo_speed
    if nemo_y >= 620:
        score += 1
        nemo_y = 80
    #update tuna
    now = pygame.time.get_ticks() #spawn tuna dengan jeda acak
    if now - last_spawn >= spawn_delay:
        if random.random() < 0.5:
            tunas.append([-70, 240, random.randint(2, 4), 1])
        else:
            tunas.append([900, 440, random.randint(2, 4), -1])
        last_spawn = now
        spawn_delay = random.randint(450,1600)
    for tuna in tunas: #update posisi tuna
        tuna[0] += tuna[2] * tuna[3]
    tunas = [tuna for tuna in tunas if -70 < tuna[0] < 900] #hapus yang ga keliatan

    # 3. Draw
    # fill the screen with a color to wipe away anything from last frame
    draw_world(screen)
    pygame.draw.circle(screen,(255, 130, 50),(nemo_x, nemo_y),12)
    for x, y, speed, direction in tunas:
        color = (70, 90, 110)
        if direction == 1:
            tail = [(x + 7, y + 15),(x - 9, y + 5),(x - 9, y + 25),]
        else:
            tail = [(x + 63, y + 15),(x + 79, y + 5),(x + 79, y + 25),]
        pygame.draw.polygon(screen, color, tail) #penanda arah
        pygame.draw.ellipse(screen, color, (x, y, 70, 30))
    #taruh teks
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))
    screen.blit(fps_text, (20, 50))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()