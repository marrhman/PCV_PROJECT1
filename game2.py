import pygame
import random


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.gravity = 900
        self.jump_strength = -600
        self.move_speed = 300

        self.reset()

    def reset(self):
        self.player = pygame.Rect(
            self.width // 2 - 15,
            self.height - 120,
            30, 30
        )

        self.player_vy = 0
        self.score = 0
        self.game_over = False

        self.platforms = [
            pygame.Rect(
                self.width // 2 - 50,
                self.height - 70,
                100, 15
            )
        ]

        for i in range(6):
            x = random.randint(0, self.width - 100)
            y = self.height - 170 - i * 100

            self.platforms.append(
                pygame.Rect(x, y, 100, 15)
            )

    def update(self, direction, dt):
        if self.game_over:
            return

        # Horizontal movement
        self.player.x += direction * self.move_speed * dt

        # Wrap around screen
        if self.player.right < 0:
            self.player.left = self.width
        elif self.player.left > self.width:
            self.player.right = 0

        # Gravity
        previous_bottom = self.player.bottom
        self.player_vy += self.gravity * dt
        self.player.y += self.player_vy * dt

        # Landing and automatic jump
        if self.player_vy > 0:
            for platform in self.platforms:
                if (
                    previous_bottom <= platform.top
                    and self.player.bottom >= platform.top
                    and self.player.right > platform.left
                    and self.player.left < platform.right
                ):
                    self.player.bottom = platform.top
                    self.player_vy = self.jump_strength
                    break

        # Camera scrolling
        if self.player.y < self.height * 0.4:
            scroll = int(self.height * 0.4 - self.player.y)

            self.player.y += scroll

            for platform in self.platforms:
                platform.y += scroll

            self.score += scroll

        # Generate platforms above the screen
        while min(p.y for p in self.platforms) > 0:
            highest_y = min(p.y for p in self.platforms)

            x = random.randint(0, self.width - 100)

            self.platforms.append(
                pygame.Rect(x, highest_y - 100, 100, 15)
            )

        # Remove platforms below the screen
        self.platforms = [
            p for p in self.platforms
            if p.top < self.height
        ]

        # Game over
        if self.player.top > self.height:
            self.game_over = True