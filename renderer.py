import pygame

def draw_game(screen, player, platforms, score, game_over):
    screen.fill("white")

    for platform in platforms:
        pygame.draw.rect(screen, "green", platform)

    pygame.draw.rect(screen, "blue", player)

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, "black")
    screen.blit(score_text, (10, 10))

    if game_over:
        message = font.render("GAME OVER", True, "red")
        restart = font.render("Press R to restart", True, "black")

        screen.blit(
            message,
            message.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 20))
        )
        screen.blit(
            restart,
            restart.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 20))
        )