import sys, random, pygame
pygame.init()

# Set the parameters of this game
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = SCREEN_WIDTH // GRID_SIZE, SCREEN_HEIGHT // GRID_SIZE
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
SNAKE_COLOR = (100,100, 100)
FOOD_COLOR = (225, 225, 225)
GRID_COLOR = (115, 20, 190)
FPS = 10

# Draw the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("hungry snake")

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, SNAKE_COLOR, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_food(food):
    pygame.draw.rect(screen, FOOD_COLOR, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_grid():
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

# Get a random location for the food
def get_random_location(snake):
    while True:
        location = (random.randint(3, GRID_WIDTH - 3), random.randint(3, GRID_HEIGHT - 3))
        if location not in snake:  # Ensure food does not overlap with the snake
            return location

# Main function
def main():
    snake_direction = RIGHT
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    food = get_random_location(snake)
    paused = False
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != DOWN:
                    snake_direction = UP
                elif event.key == pygame.K_DOWN and snake_direction != UP:
                    snake_direction = DOWN
                elif event.key == pygame.K_RIGHT and snake_direction != LEFT:
                    snake_direction = RIGHT
                elif event.key == pygame.K_LEFT and snake_direction != RIGHT:
                    snake_direction = LEFT
                elif event.key == pygame.K_SPACE:
                    paused = not paused

        if not paused:
            head_x, head_y = snake[0]
            new_head = (head_x + snake_direction[0], head_y + snake_direction[1])
            snake.insert(0, new_head)

            # Check game over conditions
            if (
                new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
                new_head in snake[1:]  # Avoid self-collision with the second segment
            ):
                pygame.quit()
                sys.exit()

            # Check if food is eaten
            if new_head == food:
                food = get_random_location(snake)
            else:
                snake.pop()

        # Draw game interface
        screen.fill((0, 0, 0))
        draw_grid()
        draw_snake(snake)
        draw_food(food)

        # Display pause message
        if paused:
            font = pygame.font.Font(None, 36)
            text = font.render("Paused - Press SPACE to Resume", True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
