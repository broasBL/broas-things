import pygame
import sys
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 640))
clock = pygame.time.Clock()
running = True
pygame.mixer.init()
pygame.display.set_caption("JOUGO DA CROBA")

# Load images
background_img = pygame.image.load("fundo.png").convert()
options_img = pygame.image.load("options(1).png").convert()
cobra_img = pygame.image.load("cobra.png").convert_alpha()
cobra_jogo_img = pygame.image.load("croba_game.png").convert_alpha()
apple_img = pygame.image.load("bitcoin.png").convert_alpha()

# Load background music
pygame.mixer.music.load("background.mp3")

# Colors
WHITE = (255, 255, 255)
YELLOW = (218, 165, 32)
DARK_YELLOW = (184, 134, 11)
LIGHT_BLUE = (135, 206, 235)  # Light Blue
STRONG_BLUE = (0, 0, 139)  # Strong Blue (dark blue)
GREEN = (143, 188, 143)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_GREEN = (144, 238, 144)  # Light Green
DARK_GREEN = (173, 255, 47)  # Dark Green
BLUE = (70, 130, 180)
PURPLE = (138, 43, 226)

# Fonts
smallfont = pygame.font.SysFont('Corbel', 35)
largefont = pygame.font.SysFont('Corbel', 50)
text_quit = smallfont.render('Quit', True, WHITE)
text_play = smallfont.render('Play', True, WHITE)
text_pause = smallfont.render('Pause', True, WHITE)
text_resume = smallfont.render('Resume', True, WHITE)
text_option1 = smallfont.render('English', True, WHITE)
text_option2 = smallfont.render('Spanish', True, WHITE)
text_back = smallfont.render('Back', True, WHITE)

# Define music functions
def play_background_music():
    pygame.mixer.music.play(-1)

def stop_background_music():
    pygame.mixer.music.stop()

# Define game parameters
speed = 1
cell_size = 20

# Function to randomly place the apple on the screen
def random_apple_position():
    return pygame.Vector2((random.randint(1, (780 // cell_size) - 2) * cell_size,
                           random.randint(3, (600 // cell_size) - 2) * cell_size))

# Main game function
def game():
    # Position the snake in the center of the screen
    x, y = 400 // cell_size * cell_size, 320 // cell_size * cell_size
    snake = [pygame.Vector2(x, y)]
    direction = 'RIGHT'
    apple_position = random_apple_position()
    score = 0
    paused = False  # Flag to track if the game is paused

    global running
    in_game = True
    play_background_music()  # Start the background music
    while in_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                in_game = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    in_game = False
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    direction = 'RIGHT'
                elif event.key == pygame.K_UP and direction != 'DOWN':
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    direction = 'DOWN'
                elif event.key == pygame.K_SPACE:
                    paused = not paused  # Toggle pause state

        if not paused:
            # Update the snake's position
            if direction == 'LEFT':
                x -= cell_size
            elif direction == 'RIGHT':
                x += cell_size
            elif direction == 'UP':
                y -= cell_size
            elif direction == 'DOWN':
                y += cell_size

            snake.insert(0, pygame.Vector2(x, y))

            # Check for collisions with the apple
            if snake[0] == apple_position:
                score += 1
                apple_position = random_apple_position()
            else:
                snake.pop()

            # Check for collisions with boundaries or itself
            if (x < cell_size or x >= 775 - cell_size or y < 3 * cell_size or y >= 615 - cell_size or snake[0] in snake[1:]):
                in_game = False

        # Draw everything
        screen.fill(BLACK)

        # Draw the chessboard pattern with green gradient
        for i in range(1, 39):
            for j in range(3, 32):
                color = LIGHT_GREEN if (i + j) % 2 == 0 else DARK_GREEN
                pygame.draw.rect(screen, color, (i * cell_size, j * cell_size, cell_size, cell_size))

        # Draw the border and score background
        pygame.draw.rect(screen, BLUE, (0, 0, 800, cell_size * 3))  # Top border and score background
        pygame.draw.rect(screen, BLUE, (0, 0, cell_size, 640))  # Left border
        pygame.draw.rect(screen, BLUE, (800 - cell_size, 0, cell_size, 640))  # Right border
        pygame.draw.rect(screen, BLUE, (0, 640 - cell_size, 800, cell_size))  # Bottom border

        # Draw the score
        score_text = smallfont.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (23, 25))

        # Draw the snake and apple
        for segment in snake:
            pygame.draw.rect(screen, PURPLE, (segment.x, segment.y, cell_size, cell_size))
        screen.blit(apple_img, apple_position)

        # Draw pause/resume button
        if paused:
            pygame.draw.rect(screen, BLUE, (50,700 , 80, 40))  # Pause button background
            screen.blit(text_resume, (675, 25))
        else:
            pygame.draw.rect(screen, BLUE, (50, 700, 80, 40))  # Pause button background
            screen.blit(text_pause, (675, 25))

        pygame.display.flip()
        clock.tick(12.5)

    stop_background_music()  # Stop the background music when the game ends

# Draw buttons on the main menu
def draw_buttons():
    mouse = pygame.mouse.get_pos()
    if 400 <= mouse[0] <= 600 and 475 <= mouse[1] <= 515:
        pygame.draw.rect(screen, YELLOW, [400, 475, 200, 40])
    else:
        pygame.draw.rect(screen, DARK_YELLOW, [400, 475, 200, 40])
    screen.blit(text_quit, (475, 480))

    if 400 <= mouse[0] <= 600 and 425 <= mouse[1] <= 465:
        pygame.draw.rect(screen, LIGHT_BLUE, [400, 425, 200, 40])
    else:
        pygame.draw.rect(screen, STRONG_BLUE, [400, 425, 200, 40])
    screen.blit(text_play, (475, 430))

# Draw buttons on the options menu
def draw_options_buttons():
    mouse = pygame.mouse.get_pos()
    if 300 <= mouse[0] <= 500 and 300 <= mouse[1] <= 340:
        pygame.draw.rect(screen, YELLOW, [300, 300, 200, 40])
    else:
        pygame.draw.rect(screen, DARK_YELLOW, [300, 300, 200, 40])
    screen.blit(text_option1, (350, 305))

    if 300 <= mouse[0] <= 500 and 350 <= mouse[1] <= 390:
        pygame.draw.rect(screen, LIGHT_BLUE, [300, 350, 200, 40])
    else:
        pygame.draw.rect(screen, STRONG_BLUE, [300, 350, 200, 40])
    screen.blit(text_option2, (350, 355))

# Main menu function
def main_menu():
    global running
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 400 <= mouse[0] <= 600 and 475 <= mouse[1] <= 515:
                    running = False
                elif 400 <= mouse[0] <= 600 and 425 <= mouse[1] <= 465:
                    game()
                elif 750 <= mouse[0] <= 750 + options_img.get_width() and 10 <= mouse[1] <= 10 + options_img.get_height():
                    options_menu()

        screen.blit(background_img, (0, 0))
        screen.blit(options_img, (750, 10))
        screen.blit(cobra_img, (75, 375))
        screen.blit(cobra_jogo_img, (90, 45))
        draw_buttons()
        pygame.display.flip()
        clock.tick(60)

# Options menu function
def options_menu():
    global running
    in_options = True
    while in_options:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                in_options = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 300 <= mouse[0] <= 500 and 300 <= mouse[1] <= 340:
                    in_options = False  # Go back to the main menu
                elif 300 <= mouse[0] <= 500 and 350 <= mouse[1] <= 390:
                    in_options = False  # Go back to the main menu

        screen.blit(background_img, (0, 0))
        draw_options_buttons()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()
    pygame.quit()
    sys.exit()
