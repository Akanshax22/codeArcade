# quiz_module.py

import pygame
import sys

def run_quiz_module():
    from select_module import run_select_module
    # Initialize Pygame and set up display
    pygame.init()
    WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Python Quiz Game")
    clock = pygame.time.Clock()
    width, height = WIDTH, HEIGHT

    # Constants
    WHITE = (255, 255, 255)
    FONT_SIZE = 30
    BUTTON_FONT_SIZE = 20
    BUTTON_HEIGHT = 40
    BUTTON_PADDING = 20
    global answer_sound
    answer_sound=pygame.mixer.Sound("answer.mp3")

    # Load and set up images
    image_path = 'Code Arcade.png'
    back_button_path = 'back_button.png'
    try:
        original_image = pygame.image.load(image_path).convert_alpha()
        back_button_img = pygame.transform.scale(pygame.image.load(back_button_path).convert_alpha(), (50, 50))
    except Exception as e:
        print(f"Error loading images: {e}")
        sys.exit()
    back_button_rect = back_button_img.get_rect(topleft=(10, 10))
    image_size = (2000, 2000)
    image = pygame.transform.scale(original_image, image_size)

    # Function to apply dynamic transparency to the entire image
    def apply_transparency(image, alpha):
        transparent_image = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        transparent_image.blit(image, (0, 0))
        transparent_image.set_alpha(alpha)
        return transparent_image

    # Function to create a glow effect
    def apply_glow(surface, image, position, glow_radius=15, glow_intensity=10):
        for i in range(glow_intensity, 0, -1):
            glow_image = apply_transparency(image, 5)
            offset = glow_radius * (1 - (i / glow_intensity))
            surface.blit(glow_image, (position[0] - offset, position[1] - offset))

    # Function to handle the back button action
    def back_action():
        answer_sound.play()
        print("Back button pressed")
        run_select_module()

    # Function to draw text
    def draw_text(text, size, color, position):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=position)
        screen.blit(text_surface, text_rect)

    # Define the Button class
    class Button:
        def __init__(self, text, center_pos, elevation, action=None):
            self.pressed = False
            self.elevation = elevation
            self.dynamic_elevation = elevation
            self.center_pos = center_pos
            self.action = action

            self.font = pygame.font.Font(None, BUTTON_FONT_SIZE)
            self.text_surf = self.font.render(text, True, (255, 255, 255))
            self.width = self.text_surf.get_width() + BUTTON_PADDING
            self.height = BUTTON_HEIGHT

            self.top_rect = pygame.Rect(0, 0, self.width, self.height)
            self.top_rect.center = center_pos
            self.top_color = (71, 95, 119)

            self.bottom_rect = pygame.Rect(0, 0, self.width, self.height)
            self.bottom_rect.center = center_pos
            self.bottom_color = (0, 0, 255)

            self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

        def draw(self):
            self.top_rect.y = self.center_pos[1] - self.height / 2 - self.dynamic_elevation
            self.text_rect.center = self.top_rect.center

            pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=12)
            pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
            screen.blit(self.text_surf, self.text_rect)

        def check_click(self, event):
            mouse_pos = pygame.mouse.get_pos()
            if self.top_rect.collidepoint(mouse_pos):
                self.top_color = (0, 191, 255)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.dynamic_elevation = 0
                    if self.action:
                        self.action()
                        answer_sound.play()
            else:
                self.dynamic_elevation = self.elevation
                self.top_color = (71, 95, 119)

    # Function to create option buttons with dynamic width
    def create_option_buttons(options, y_start):
        buttons = []
        for i, option in enumerate(options):
            button_y = y_start + i * 50
            new_button = Button(option, (width // 2, button_y), 5, action=lambda option=option: check_answer(option))
            
            buttons.append(new_button)
        return buttons

    # Quiz questions and options
    questions = [{
        "question": "Who is the creator of Python?",
        "options": ["Alan Turing", "Guido van Rossum", "Dennis Ritchie", "Linus Torvalds"],
        "answer": "Guido van Rossum"
    },
    {
        "question": "When was Python officially made available to the public?",
        "options": ["1989", "1991", "1995", "2000"],
        "answer": "1991"
    },
    {
        "question": "What is the official Date of Birth for Python?",
        "options": ["Jan 1st, 1990", "Feb 20th, 1991", "Mar 15th, 1992", "Apr 5th, 1993"],
        "answer": "Feb 20th, 1991"
    },
    {
        "question": "Why was the name 'Python' chosen for the programming language?",
        "options": ["It is named after a species of snake", "Inspired by a famous mathematician", "From a TV show, 'Monty Python's Flying Circus'", "Guido van Rossum's favorite animal"],
        "answer": "From a TV show, 'Monty Python's Flying Circus'"
    },
    {
        "question": "From which TV show was the name 'Python' inspired?",
        "options": ["Friends", "The Simpsons", "Monty Python's Flying Circus", "Breaking Bad"],
        "answer": "Monty Python's Flying Circus"
    },
    {
        "question": "Which programming features did Guido van Rossum incorporate into Python from different languages?",
        "options": ["Only features from C", "Features from C++ and Perl", "Features from C, C++, Perl, and Modula-3", "Features from Java and Shell Script"],
        "answer": "Features from C, C++, Perl, and Modula-3"
    },
    {
        "question": "Why is Python recommended as the first programming language for beginners?",
        "options": ["It has a simple syntax", "It is the oldest programming language", "It is the most powerful programming language", "It is the only language supported by all operating systems"],
        "answer": "It has a simple syntax"
    },
    {
        "question": "Where did Guido van Rossum work when he conceived the idea of Python?",
        "options": ["NASA", "National Research Institute (NRI) at Netherlands", "Microsoft", "Google"],
        "answer": "National Research Institute (NRI) at Netherlands"
    },
    {
        "question": "Which programming paradigm did Guido van Rossum incorporate into Python from C?",
        "options": ["Imperative Programming", "Object-Oriented Programming", "Functional Programming", "Procedural Programming"],
        "answer": "Functional Programming"
    },
    {
        "question": "Which language's syntax heavily influenced Python?",
        "options": ["Java", "C++", "ABC", "Perl"],
        "answer": "ABC"
    },
    {
        "question": "What makes Python a simple programming language?",
        "options": ["Complex syntax", "Few available keywords", "Extensive libraries", "Complicated memory management"],
        "answer": "Few available keywords"
    },
    {
        "question": "Why is Python considered a high-level programming language?",
        "options": ["It requires low-level activities like memory management", "It is platform-independent", "Programmers do not need to focus on low-level activities", "It supports both procedure-oriented and object-oriented features"],
        "answer": "Programmers do not need to focus on low-level activities"
    },
    {
        "question": "What is the significance of Python being an interpreted language?",
        "options": ["Programs need to be compiled explicitly", "Python uses a Python Virtual Machine for compilation", "Compilation errors are handled by the interpreter", "It can only run on a specific platform"],
        "answer": "Compilation errors are handled by the interpreter"
    },
    {
        "question": "How does Python handle variable types?",
        "options": ["Variables must be declared with a type", "Type is allocated automatically based on the value", "Type is allocated at runtime", "Variables can only have a numeric type"],
        "answer": "Type is allocated automatically based on the value"
    },
    {
        "question": "What is the main advantage of Python's portability?",
        "options": ["It supports only one platform", "Programs provide different results on different platforms", "Python programs are not portable", "Python programs will provide the same results on any platform"],
        "answer": "Python programs will provide the same results on any platform"
    },
    {
        "question": "What is the role of PVM (Python Virtual Machine) in Python?",
        "options": ["Compilation of Python programs", "Execution of Python programs", "Memory management", "Type allocation"],
        "answer": "Execution of Python programs"
    },
    {
        "question": "Why is Python considered an extensible language?",
        "options": ["It can only use Python code", "It can use other language programs", "It cannot integrate with legacy code", "It is limited to a specific platform"],
        "answer": "It can use other language programs"
    },
    {
        "question": "What does 'Embedded' mean in the context of Python?",
        "options": ["Python cannot be used in other language programs", "Python can only be used as a standalone language", "Python programs can be embedded anywhere", "Python does not support integration"],
        "answer": "Python programs can be embedded anywhere"
    },
    {
        "question": "What does Python's rich inbuilt library contribute to?",
        "options": ["Increased productivity", "Decreased flexibility", "Complexity of syntax", "Limited functionality"],
        "answer": "Increased productivity"
    },
    {
        "question": "How does Python contribute to increased productivity?",
        "options": ["By having a complex syntax", "Through powerful libraries and simple syntax", "By being a low-level language", "By requiring explicit type declaration"],
        "answer": "Through powerful libraries and simple syntax"
    },

    {"question": "What is Python primarily used for?", "options": ["Web Development", "Game Development", "Data Analysis", "All of the above"], "answer": "All of the above"},
    {"question": "Which is not a data type in Python?", "options": ["String", "Integer", "Float", "Perform"], "answer": "Perform"},
    {"question": "What does the `break` statement do in a loop?", "options": ["Pauses the loop", "Stops the loop", "Skips one iteration", "None of the above"], "answer": "Stops the loop"},
    {"question": "How do you define a function in Python?", "options": ["function myFunc():", "def myFunc():", "create myFunc():", "newFunction myFunc():"], "answer": "def myFunc():"},
    {"question": "How do you read a line of input from the user?", "options": ["input()", "getInput()", "readLine()", "scan()"], "answer": "input()"},    # ... More questions ...
    ]


    # Global variables for the quiz
    quiz_over = False
    score = 0
    feedback = ""
    feedback_color = (0, 0, 0)
    feedback_display_time = 2
    last_feedback_time = 0
    first_attempt = True

    # Function to check the answer
    def check_answer(selected_option):
        nonlocal current_question_index, option_buttons, quiz_over, score, feedback, feedback_color, last_feedback_time, first_attempt
        correct = selected_option == questions[current_question_index]['answer']
        if correct:
            feedback = "Correct!"
            feedback_color = (0, 255, 0)
            if first_attempt:
                score += 1
            first_attempt = True
            current_question_index += 1
            if current_question_index < len(questions):
                option_buttons = create_option_buttons(questions[current_question_index]["options"], height // 2 - 50)
            else:
                quiz_over = True
        else:
            feedback = "Wrong! Try again."
            feedback_color = (255, 0, 0)
            first_attempt = False
        last_feedback_time = pygame.time.get_ticks()

    # Initialize the first set of option buttons and the current question index
    current_question_index = 0
    option_buttons = create_option_buttons(questions[current_question_index]["options"], height // 2 - 50)

    # Main application loop
    app_is_alive = True
    while app_is_alive:
        screen.fill(WHITE)
        apply_glow(screen, image, (width // 2 - image_size[0] // 2, height // 2 - image_size[1] // 2), 15, 10)

        current_time = pygame.time.get_ticks()
        if not quiz_over:
            if current_question_index < len(questions):
                current_question = questions[current_question_index]
                question_text = current_question["question"]
                draw_text(question_text, FONT_SIZE, (0, 0, 0), (width // 2, height // 2 - 150))
                for button in option_buttons:
                    button.draw()
                if (current_time - last_feedback_time) // 1000 < feedback_display_time:
                    draw_text(feedback, FONT_SIZE, feedback_color, (width // 2, height - 50))
            else:
                final_score_text = f"Final Score: {score} / {len(questions)}"
                draw_text(final_score_text, FONT_SIZE, (0, 0, 250), (width // 2, height // 2))
        else:
            final_score_text = f"Final Score: {score} / {len(questions)}"
            draw_text(final_score_text, FONT_SIZE, (0, 0, 250), (width // 2, height // 2))

        screen.blit(back_button_img, (10, 10))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                app_is_alive = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    back_action()
            for button in option_buttons:
                button.check_click(event)

        pygame.display.update()
        clock.tick(60)

    # Exit Pygame

# If this script is run standalone, execute the code
if __name__ == "__main__":
    run_quiz_module()
