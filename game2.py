import pygame
import random
import cv2
from vision import get_controls

# Setup
pygame.init()
screen = pygame.display.set_mode((500, 700))
pygame.display.set_caption("Doodle Jump")
clock = pygame.time.Clock()

WIDTH, HEIGHT = screen.get_size()
running = True
dt = 0

# Hand detection setup
cv2.namedWindow("Threshold Configuration")

cv2.createTrackbar("H Min", "Threshold Configuration", 7, 179, lambda x: None)
cv2.createTrackbar("H Max", "Threshold Configuration", 22, 179, lambda x: None)
cv2.createTrackbar("S Min", "Threshold Configuration", 45, 255, lambda x: None)
cv2.createTrackbar("S Max", "Threshold Configuration", 160, 255, lambda x: None)
cv2.createTrackbar("V Min", "Threshold Configuration", 80, 255, lambda x: None)
cv2.createTrackbar("V Max", "Threshold Configuration", 220, 255, lambda x: None)

video_cam = cv2.VideoCapture(0)

# Player
player = pygame.Rect(WIDTH // 2 - 15, HEIGHT - 120, 30, 30)
player_vy = 0
gravity = 900
jump_strength = -600
move_speed = 300

# Platforms
platforms = [
    pygame.Rect(WIDTH // 2 - 50, HEIGHT - 70, 100, 15)
]

for i in range(6):
    x = random.randint(0, WIDTH - 100)
    y = HEIGHT - 170 - i * 100
    platforms.append(pygame.Rect(x, y, 100, 15))

# Game state
score = 0
game_over = False
font = pygame.font.Font(None, 36)


def reset_game():
    global player_vy, score, game_over

    player.x = WIDTH // 2 - player.width // 2
    player.y = HEIGHT - 120
    player_vy = 0
    score = 0
    game_over = False

    platforms.clear()
    platforms.append(
        pygame.Rect(WIDTH // 2 - 50, HEIGHT - 70, 100, 15)
    )

    for i in range(6):
        x = random.randint(0, WIDTH - 100)
        y = HEIGHT - 170 - i * 100
        platforms.append(pygame.Rect(x, y, 100, 15))


while running:
    dt = clock.tick(60) / 1000

    # Read camera
    success, frame = video_cam.read()

    if not success:
        running = False
        continue

    frame = cv2.flip(frame, 1)

    # Read HSV thresholds
    h_min = cv2.getTrackbarPos("H Min", "Threshold Configuration")
    h_max = cv2.getTrackbarPos("H Max", "Threshold Configuration")
    s_min = cv2.getTrackbarPos("S Min", "Threshold Configuration")
    s_max = cv2.getTrackbarPos("S Max", "Threshold Configuration")
    v_min = cv2.getTrackbarPos("V Min", "Threshold Configuration")
    v_max = cv2.getTrackbarPos("V Max", "Threshold Configuration")

    # Detect hand controls
    active_controls, commands, mask, detected_objects, *_ = get_controls(
        frame, h_min, s_min, v_min, h_max, s_max, v_max
    )

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                reset_game()

    keys = pygame.key.get_pressed()

    if not game_over:
        # Horizontal movement
        # Key controls
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.x -= move_speed * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.x += move_speed * dt

        # Hand controls
        if 1 in active_controls or 3 in active_controls:
            player.x -= move_speed * dt
        if 2 in active_controls or 4 in active_controls:
            player.x += move_speed * dt

        # Wrap around screen
        if player.right < 0:
            player.left = WIDTH
        elif player.left > WIDTH:
            player.right = 0

        # Gravity
        previous_bottom = player.bottom
        player_vy += gravity * dt
        player.y += player_vy * dt

        # Landing: only when falling
        if player_vy > 0:
            for platform in platforms:
                if (
                    previous_bottom <= platform.top
                    and player.bottom >= platform.top
                    and player.right > platform.left
                    and player.left < platform.right
                ):
                    player.bottom = platform.top
                    player_vy = jump_strength
                    break

        # Camera scrolling
        if player.y < HEIGHT * 0.4:
            scroll = int(HEIGHT * 0.4 - player.y)
            player.y += scroll

            for platform in platforms:
                platform.y += scroll

            score += scroll

        # Generate new platforms above the screen
        while min(p.y for p in platforms) > 0:
            highest_y = min(p.y for p in platforms)
            x = random.randint(0, WIDTH - 100)
            platforms.append(
                pygame.Rect(x, highest_y - 100, 100, 15)
            )

        # Remove platforms below the screen
        platforms = [p for p in platforms if p.top < HEIGHT]

        # Game over
        if player.top > HEIGHT:
            game_over = True

    # Drawing
    screen.fill("white")

    for platform in platforms:
        pygame.draw.rect(screen, "green", platform)

    pygame.draw.rect(screen, "blue", player)

    score_text = font.render(f"Score: {score}", True, "black")
    screen.blit(score_text, (10, 10))

    if game_over:
        message = font.render("GAME OVER", True, "red")
        restart = font.render("Press R to restart", True, "black")

        screen.blit(
            message,
            message.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        )
        screen.blit(
            restart,
            restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        )

    cv2.imshow("Camera", frame)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        running = False

    pygame.display.flip()

video_cam.release()
cv2.destroyAllWindows()
pygame.quit()
