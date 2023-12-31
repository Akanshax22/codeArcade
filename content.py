import pygame
from pygame.locals import *
from PIL import Image



def display_content():
    from menu import menu
    def read_file_content(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.readlines()
    global answer_sound
    answer_sound=pygame.mixer.Sound("answer.mp3")
    def back_button_action():
        answer_sound.play()
        print("Back button pressed")
        menu()

    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Content Display")

    clock = pygame.time.Clock()

    file_path = 'content.txt'  # Replace with your file's name
    back_button_image_path = 'back_button.png'  # Replace with your image file path

    # Resize the back button image
    original_image = Image.open(back_button_image_path)
    resized_image = original_image.resize((50, 50))  # Customize the size (width, height)

    # Convert PIL image to Pygame surface
    back_button_image = pygame.image.fromstring(resized_image.tobytes(), resized_image.size, resized_image.mode)

    font = pygame.font.Font(None, 36)
    content_lines = read_file_content(file_path)

    scroll_x, scroll_y = 0, 0
    scroll_speed = 5

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN and event.button == 4:  # Scroll up
                scroll_y += scroll_speed
            elif event.type == MOUSEBUTTONDOWN and event.button == 5:  # Scroll down
                scroll_y -= scroll_speed
            elif event.type == MOUSEMOTION:
                if event.buttons[0]:  # Left mouse button pressed
                    scroll_x += event.rel[0]  # Update scroll_x based on mouse motion
            elif event.type == MOUSEBUTTONDOWN and back_button_rect.collidepoint(event.pos):
                back_button_action()

        screen.fill((255, 255, 255))

        # Draw text content
        text_y = scroll_y
        for line in content_lines:
            text_surface = font.render(line.strip(), True, (0, 0, 0))
            screen.blit(text_surface, (10 + scroll_x, text_y))
            text_y += text_surface.get_height()

        # Draw back button after text
        back_button_rect = screen.blit(back_button_image, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    display_content()
