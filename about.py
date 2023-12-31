import pygame
import sys

def about():
    # Initialize Pygame and set up display
    from menu import menu
    pygame.init()
    WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Software Developers")
    global answer_sound
    answer_sound=pygame.mixer.Sound("answer.mp3")

    # Constants
    WHITE = (255, 255, 255)
    FONT_SIZE = 48
    TEXT_COLOR = (0, 0, 0)
    BACKGROUND_ALPHA = 100  # Adjust the transparency (0=transparent, 255=opaque)
    def back_button_function():
        answer_sound.play()
        print("Back button pressed")
        menu()
        # Add any additional actions you want to perform here

    # Load images
    background_path = 'Code Arcade.png'  # Replace with your background image path
    back_button_path = 'back_button.png'  # Replace with your back button image path
    developer1_path = 'anuj.png'  # Replace with your first developer image path
    developer2_path = 'akansha.png'  # Replace with your second developer image path

    try:
        background_img = pygame.image.load(background_path).convert_alpha()
        back_button_img = pygame.image.load(back_button_path).convert_alpha()
        developer1_img = pygame.image.load(developer1_path).convert_alpha()
        developer2_img = pygame.image.load(developer2_path).convert_alpha()
    except Exception as e:
        print(f"Error loading images: {e}")
        sys.exit()

    # Resize images
    background_img = pygame.transform.scale(background_img, (2000, 2000))
    back_button_img = pygame.transform.scale(back_button_img, (50, 50))
    developer1_img = pygame.transform.scale(developer1_img, (500, 400))  # Adjust size as needed
    developer2_img = pygame.transform.scale(developer2_img, (200, 400))  # Adjust size as needed
    back_button_rect = back_button_img.get_rect(topleft=(10, 10))

    # Function to draw text
    def draw_text(text, position, font_size=FONT_SIZE):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=position)
        screen.blit(text_surface, text_rect)

    # Apply transparency to the background image
    def apply_transparency(image, alpha):
        transparent_image = pygame.Surface((2000, 2000), pygame.SRCALPHA)
        transparent_image.blit(image, (0, 0))
        transparent_image.set_alpha(alpha)
        return transparent_image

    # Main game loop
    running = True
    while running:
        screen.fill(WHITE)
        transparent_background = apply_transparency(background_img, BACKGROUND_ALPHA)
        screen.blit(transparent_background, (WIDTH // 2 - 1000, HEIGHT // 2 - 1000))
        
        # Title "Developers"
        draw_text("Developers", (WIDTH // 2, 100), font_size=64)

        # Developer images and names
        developer1_pos = (WIDTH // 4, HEIGHT // 2.1)
        developer2_pos = (3 * WIDTH // 4, HEIGHT // 2.25)
        screen.blit(developer1_img, (developer1_pos[0] - 150, developer1_pos[1] - 150))
        screen.blit(developer2_img, (developer2_pos[0] - 150, developer2_pos[1] - 150))
        draw_text("Anuj Swami", (485, developer1_pos[1] + 235))  # Adjust position as needed
        draw_text("Akansha Choudhary", (1100, developer2_pos[1] + 265))  # Adjust position as needed
        draw_text("Code Arcade is a game that teaches coding through interactive puzzles and challenges, making learning fun and engaging for beginners.", (800, 700), font_size=25)

        # Back button
        screen.blit(back_button_img, back_button_rect.topleft)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and back_button_rect.collidepoint(event.pos):
                back_button_function()  # Call the provided back button function

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

# If this script is run standalone, execute the code
if __name__ == "__main__":
    about()
