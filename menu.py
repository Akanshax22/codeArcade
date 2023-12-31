# custom_module.py

import pygame
import random


def menu():
    from select_module import run_select_module
    from content import display_content
    from about import about
    # Initialize the pygame modules
    pygame.init()
    clock = pygame.time.Clock()
    global sound
    sound = pygame.mixer.Sound("Click.mp3")

    # Create a fullscreen display
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = pygame.display.get_surface().get_size()
    pygame.display.set_caption('Window Caption')

    # Function to draw text on the screen
    def draw_text(text, size, color, position):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = position
        screen.blit(text_surface, text_rect)

    # Set the background color to white
    screen.fill((255, 255, 255))

    # Define some commonly used colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Define a Button class for creating interactive buttons
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

            self.text_surf = pygame.font.Font(None, 30).render(text, True, (255, 255, 255))
            self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

        def draw(self):
            self.top_rect.y = self.center_pos[1] - self.height / 2 - self.dynamic_elevation
            self.text_rect.center = self.top_rect.center

            self.bottom_rect.midtop = self.top_rect.midtop
            self.bottom_rect.height = self.height + self.dynamic_elevation

            pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=12)
            pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
            screen.blit(self.text_surf, self.text_rect)

        def check_click(self):
            mouse_pos = pygame.mouse.get_pos()
            if self.top_rect.collidepoint(mouse_pos):
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
    def start_action():
        sound.play()
        print("Start button pressed")
        
        run_select_module()

    def content_action():
        sound.play()
        print("Content button pressed")
        
        display_content()

    def about_action():
        sound.play()
        print("About button pressed")
        about()

    def quit_action():
        global app_is_alive
        print("Quit button pressed, generating quit confirmation box...")
        sound.play()
        confirm = quit_confirmation_box(screen, 'Do you want to quit?')
        
        if confirm:
            sound.play()
            app_is_alive = False

    def quit_confirmation_box(screen, message):
        draw_text(message, 30, BLACK, (width // 2, height // 2))
        draw_text('Press Y for Yes or N for No', 24, BLACK, (width // 2, height // 2 + 50))
        sound.play()
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        return pygame.quit()
                    elif event.key == pygame.K_n:
                        return False

    # Create button instances
    button1 = Button('Start', 200, 40, (width // 2, height // 2 - 150), 5, action=start_action)
    button2 = Button('Content', 200, 40, (width // 2, height // 2 - 50), 5, action=content_action)
    button3 = Button('About', 200, 40, (width // 2, height // 2 + 50), 5, action=about_action)
    button4 = Button('Quit', 200, 40, (width // 2, height // 2 + 150), 5, action=quit_action)

    # Load the airplane images
    airplane_img1 = pygame.image.load('airplane2.png')
    airplane_img2 = pygame.image.load('airplane3.png')
    airplane_rect1 = airplane_img1.get_rect()
    airplane_rect2 = airplane_img2.get_rect()

    # Set initial positions for the airplanes
    airplane_x1 = width
    airplane_y1 = random.randint(0, height - airplane_rect1.height)
    airplane_x2 = 0
    airplane_y2 = random.randint(0, height - airplane_rect2.height)

    # Initialize the application loop
    app_is_alive = True

    # Main application loop
    while app_is_alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Exiting... All hail the void!")
                app_is_alive = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print("Exiting... All hail the void!")
                app_is_alive = False

        button1.check_click()
        button2.check_click()
        button3.check_click()
        button4.check_click()

        button1.draw()
        button2.draw()
        button3.draw()
        button4.draw()

        pygame.display.flip()
        screen.fill('WHITE')

        airplane_x1 -= 1
        airplane_x2 += 1
        if airplane_x1 < -airplane_rect1.width:
            airplane_x1 = width
            airplane_y1 = random.randint(0, height - airplane_rect1.height)
        if airplane_x2 > width:
            airplane_x2 = -airplane_rect2.width
            airplane_y2 = random.randint(0, height - airplane_rect2.height)

        screen.blit(airplane_img1, (airplane_x1, airplane_y1))
        screen.blit(airplane_img2, (airplane_x2, airplane_y2))
        

        clock.tick(60)
        


# If this script is run standalone, execute the code
if __name__ == "__main__":
    menu()
