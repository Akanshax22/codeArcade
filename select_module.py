# select_module.py

import pygame
import random

def run_select_module():
    from menu import menu
    from quiz_module import run_quiz_module
    from fill_in_the_blanks import fill_in_the_blanks
    # Initialize pygame
    pygame.init()

    # Create a fullscreen display
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = pygame.display.get_surface().get_size()
    pygame.display.set_caption('Select Module')
    global sound
    sound = pygame.mixer.Sound("Click.mp3")
    global answer_sound
    answer_sound=pygame.mixer.Sound("answer.mp3")

    # Create a clock to manage the frame rate
    clock = pygame.time.Clock()

    # Function to draw text on the screen
    def draw_text(text, size, color, position):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = position
        screen.blit(text_surface, text_rect)

    # Set the background color to white
    WHITE = (255, 255, 255)

    # Define a Button class
    class Button:
        def __init__(self, text, width, height, center_pos, elevation, action=None):
            self.pressed = False
            self.elevation = elevation
            self.dynamic_elevation = elevation
            self.center_pos = center_pos
            self.width = width
            self.height = height
            self.action = action

            self.top_rect = pygame.Rect(0, 0, self.width, self.height)
            self.top_rect.center = self.center_pos
            self.top_color = (71, 95, 119)

            self.bottom_rect = pygame.Rect(0, 0, self.width, self.height)
            self.bottom_rect.center = self.center_pos
            self.bottom_color = (0, 0, 255)

            self.text_surf = pygame.font.Font(None, 36).render(text, True, (255, 255, 255))
            self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

        def draw(self):
            self.top_rect.y = self.center_pos[1] - self.height / 2 - self.dynamic_elevation
            self.text_rect.center = self.top_rect.center

            pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=12)
            pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
            screen.blit(self.text_surf, self.text_rect)

        def check_click(self):
            if self.top_rect.collidepoint(pygame.mouse.get_pos()):
                self.top_color = (0, 191, 255)
                if pygame.mouse.get_pressed()[0]:
                    self.dynamic_elevation = 0
                    self.pressed = True
                    if self.action:
                        self.action()
                else:
                    self.dynamic_elevation = self.elevation
                    if self.pressed:
                        self.pressed = False
            else:
                self.dynamic_elevation = self.elevation
                self.top_color = (71, 95, 119)

    # Action functions for the buttons
    def back_action():
        answer_sound.play()
        print("Back button pressed")
        menu()

    def quiz_action():
        sound.play()
        print("Quiz button pressed")
        run_quiz_module()
    def fill_in_blanks_action():
        sound.play()
        fill_in_the_blanks()
        print("Fill in the Blanks button pressed")

    # Create button instances
    
    button_height = 60
    button_center_y = height // 2

    quiz_button = Button('QUIZ', 250, button_height, (width // 2, button_center_y), 8, action=quiz_action)
    fill_in_blanks_button = Button('FILL IN THE BLANKS', 300, button_height, (width // 2, button_center_y + 80), 8, action=fill_in_blanks_action)
    draw_text("SELECT GAME", 40, (0, 0, 255), (width // 2, button_center_y - 40))

    # Load the back button image
    back_button_img = pygame.image.load('back_button.png')
    back_button_img = pygame.transform.scale(back_button_img, (50, 50))

    # Define a list to hold the cursor trail
    cursor_trail = []

    # Define a function to draw the cursor trail
    def draw_cursor_trail():
        for point in cursor_trail:
            pygame.draw.rect(screen, (0, 0, 255), [point[0], point[1], 5, 5])

    # Main application loop
    app_is_alive = True
    while app_is_alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Exiting... All hail the void!")
                app_is_alive = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print("Exiting... All hail the void!")
                app_is_alive = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if 10 <= mouse_pos[0] <= 60 and 10 <= mouse_pos[1] <= 60:
                        back_action()

        # Set the background color to white
        screen.fill(WHITE)

        # Draw the back button and buttons
        screen.blit(back_button_img, (10, 10))
        
        if quiz_button:
            quiz_button.check_click()
            quiz_button.draw()
        if fill_in_blanks_button:
            fill_in_blanks_button.check_click()
            fill_in_blanks_button.draw()
            
        draw_text("SELECT GAME", 40, (0, 0, 255), (800, 375))


        # Get the current position of the mouse cursor
        mouse_pos = pygame.mouse.get_pos()

        # Append the current cursor position to the cursor trail list
        cursor_trail.append(mouse_pos)

        # Draw the cursor trail with a star pattern
        draw_cursor_trail()

        # If the cursor trail becomes too long, remove the oldest point
        if len(cursor_trail) > 50:
            del cursor_trail[0]
            
        # Update the display
        pygame.display.flip()
        # Set the frame rate
        clock.tick(60)

    

# If this script is run standalone, execute the code
if __name__ == "__main__":
    run_select_module()
