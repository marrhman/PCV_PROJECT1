import pygame

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
tunas = [[0, 240, 3],[180,240,2],[470,240,4],[720,440,2]] #[x, y, speed]

while running:
    # 1. Event
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Update
    nemo_y += nemo_speed
    for tuna in tunas:
        tuna[0] += tuna[2]
        if tuna[0] >= 900:
            tuna[0] = -70
    if nemo_y >= 620:
        score += 1
        nemo_y = 80

    # 3. Draw
    # fill the screen with a color to wipe away anything from last frame
    draw_world(screen)
    pygame.draw.circle(screen,(255, 130, 50),(nemo_x, nemo_y),12)
    for tuna in tunas:
        pygame.draw.ellipse(screen,(70, 90, 110),(tuna[0], tuna[1], 70, 30))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))
    screen.blit(fps_text, (20, 50))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()