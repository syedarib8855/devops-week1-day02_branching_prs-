import pygame
import random
from collections import deque


# =====================
# Snake Game (Pygame)
# =====================

CELL_SIZE = 20
GRID_W, GRID_H = 30, 20  # 600x400 window
WIDTH, HEIGHT = GRID_W * CELL_SIZE, GRID_H * CELL_SIZE
FPS = 12

BG_COLOR = (18, 18, 18)
GRID_COLOR = (28, 28, 28)
SNAKE_HEAD_COLOR = (0, 200, 90)
SNAKE_BODY_COLOR = (0, 150, 70)
FOOD_COLOR = (220, 70, 70)
TEXT_COLOR = (235, 235, 235)


def draw_grid(screen):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y), 1)


def draw_cell(screen, pos, color):
    x, y = pos
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)
    # subtle border
    pygame.draw.rect(screen, (0, 0, 0), rect, 2)


def random_free_cell(occupied):
    all_cells = [(x, y) for x in range(GRID_W) for y in range(GRID_H)]
    free = [c for c in all_cells if c not in occupied]
    return random.choice(free) if free else None


def main():
    pygame.init()
    pygame.display.set_caption("Snake Game")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    def reset_game():
        # Start in the middle with length 3
        start_x, start_y = GRID_W // 2, GRID_H // 2
        snake = deque([(start_x - 1, start_y), (start_x, start_y), (start_x + 1, start_y)])
        direction = (1, 0)  # moving right
        pending_direction = direction
        score = 0

        food = random_free_cell(set(snake))
        return snake, direction, pending_direction, score, food

    snake, direction, pending_direction, score, food = reset_game()
    game_over = False

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

                if not game_over:
                    # Prevent instant reverse
                    dx, dy = direction
                    if event.key in (pygame.K_UP, pygame.K_w):
                        if dy == 0:  # currently horizontal
                            pending_direction = (0, -1)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        if dy == 0:
                            pending_direction = (0, 1)
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        if dx == 0:
                            pending_direction = (-1, 0)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        if dx == 0:
                            pending_direction = (1, 0)
                else:
                    if event.key == pygame.K_r:
                        snake, direction, pending_direction, score, food = reset_game()
                        game_over = False

        if not game_over:
            direction = pending_direction
            head_x, head_y = snake[-1]
            dx, dy = direction
            new_head = (head_x + dx, head_y + dy)

            # Wall collision
            if not (0 <= new_head[0] < GRID_W and 0 <= new_head[1] < GRID_H):
                game_over = True
            else:
                # Self collision: allow moving into the last tail cell only if we are not growing
                occupied = set(snake)
                tail = snake[0]

                growing = (food is not None and new_head == food)

                if new_head in occupied and not (new_head == tail and not growing):
                    game_over = True
                else:
                    snake.append(new_head)
                    if growing:
                        score += 1
                        food = random_free_cell(set(snake))
                        # If no free cells, you win
                        if food is None:
                            game_over = True
                    else:
                        snake.popleft()

        # --------- Render ---------
        screen.fill(BG_COLOR)
        draw_grid(screen)

        # Food
        if food is not None:
            draw_cell(screen, food, FOOD_COLOR)

        # Snake
        for i, cell in enumerate(snake):
            color = SNAKE_HEAD_COLOR if i == len(snake) - 1 else SNAKE_BODY_COLOR
            draw_cell(screen, cell, color)

        # HUD
        score_surf = font.render(f"Score: {score}", True, TEXT_COLOR)
        screen.blit(score_surf, (10, 10))

        if game_over:
            msg = "You Win!" if food is None else "Game Over"
            over_surf = font.render(msg, True, TEXT_COLOR)
            hint_surf = font.render("Press R to Restart | ESC to Quit", True, TEXT_COLOR)

            # Center
            over_rect = over_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 10))
            hint_rect = hint_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
            screen.blit(over_surf, over_rect)
            screen.blit(hint_surf, hint_rect)

        pygame.display.flip()


if __name__ == "__main__":
    main()

