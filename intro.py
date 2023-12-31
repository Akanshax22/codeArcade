import pygame
import time
import random
from pygame import mixer

pygame.mixer.init()
mixer.music.load("Introsound.mp3")
mixer.music.play()

def intro():
    # Initialize pygame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("CodeArcade")

    # Set the background to white
    background_color = (255, 255, 255)
    screen.fill(background_color)

    # Define the code rain
    code_rain = pygame.image.load('Rain Background.png')

    # Load the game icon
    game_icon = pygame.image.load('Code Arcade.png')
    icon_rect = game_icon.get_rect()

    # Adjust the size of the game icon
    icon_width, icon_height = icon_rect.size
    icon_width = int(icon_width * 0.5)
    icon_height = int(icon_height * 0.5)
    game_icon = pygame.transform.scale(game_icon, (icon_width, icon_height))
    icon_rect = game_icon.get_rect(center=screen.get_rect().center)

    # Set initial transparency for fade-in effect
    alpha_value = 0

    # Rain effect
    for i in range(100):
        x = random.randrange(0, screen.get_width())
        y = random.randrange(0, screen.get_height())
        screen.blit(code_rain, (x, y))
        pygame.display.flip()
        pygame.time.delay(25)
        screen.fill(background_color)

    # Fade in effect for the game icon
    while alpha_value < 255:
        game_icon.set_alpha(alpha_value)
        screen.fill(background_color)
        screen.blit(game_icon, icon_rect)
        pygame.display.flip()
        pygame.time.delay(3)  # Adjust delay for a smoother effect
        alpha_value += 3

    # Display for 3 seconds
    start_time = time.time()
    while time.time() - start_time < 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    # Fade out effect for the game icon
    while alpha_value > 0:
        game_icon.set_alpha(alpha_value)
        screen.fill(background_color)
        screen.blit(game_icon, icon_rect)
        pygame.display.flip()
        pygame.time.delay(5)  # Adjust delay for a smoother effect
        alpha_value -= 1

    # Quit the program

# If this script is run standalone, execute the code
if __name__ == "__main__":
    intro()
