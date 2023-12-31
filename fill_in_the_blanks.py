# fill_in_the_blanks.py

import pygame
import sys

def fill_in_the_blanks():
    from select_module import run_select_module
    def apply_transparency(image, alpha):
        transparent_image = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        transparent_image.blit(image, (0, 0))
        transparent_image.set_alpha(alpha)
        return transparent_image
    global answer_sound
    answer_sound=pygame.mixer.Sound("answer.mp3")
    def back_action():
        answer_sound.play()
        print("Back button pressed")
        run_select_module()
        # Add code to handle the back action

    def apply_glow(surface, image, position, glow_radius=15, glow_intensity=10):
        for i in range(glow_intensity, 0, -1):
            glow_image = apply_transparency(image, 5)
            offset = glow_radius * (1 - (i / glow_intensity))
            surface.blit(glow_image, (position[0] - offset, position[1] - offset))

    pygame.init()
    WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Python Quiz Game")
    clock = pygame.time.Clock()

    WHITE = (255, 255, 255)
    QUESTION_COLOR = (0, 0, 0)
    ANSWER_COLOR = (0, 0, 156)
    WRONG_ANSWER_COLOR = (255, 0, 0)
    INPUT_BOX_COLOR = (128, 218, 235)
    RIGHT_ANSWER = (0, 255, 0)
    FONT_SIZE = 36
    
    questions = [
        "Python was officially made available to the public in _____.","The official Date of Birth for Python is: Feb 20th, _____.",
        "Python is recommended as the first programming language for _____.",
        "The name 'Python' was chosen from the TV show _____.",
        "Python version 1.0 was released in _____.",
        "Python is a popular language for _____ and Data Analysis Applications.",
        "Python is known for its simplicity, making it a _____ language that reads like English statements.",
        "Python is freeware and open source, allowing users to use it without any _____.",
        "Python programs are portable, ensuring that they provide the same results on any _____.",
        "Python is an extensible language, allowing the use of _____ in Python.",
        "Python is embedded, meaning that Python programs can be used _____."
    ]

    answers = [
        "1991",
        "1991",
        "beginners",
        "Monty Python's Flying Circus",
        "1994",
        "Machine Learning",
        "simple and easy to learn",
        "license",
        "platform",
        "other language programs",
        "anywhere"
    ]

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

    font = pygame.font.Font(None, FONT_SIZE)

    current_question_index = 0
    user_input = ""
    feedback = ""
    score = 0
    first_attempt = True

    while current_question_index < len(questions):
        screen.fill(WHITE)
        image_position = (WIDTH // 2 - image_size[0] // 2, HEIGHT // 2 - image_size[1] // 2)
        apply_glow(screen, image, image_position, glow_radius=15, glow_intensity=10)

        question = questions[current_question_index]
        before_blank, after_blank = question.split("_____")
        before_text = font.render(before_blank, True, QUESTION_COLOR)
        after_text = font.render(after_blank, True, QUESTION_COLOR)

        input_box_width = max(100, font.size(user_input)[0] + 10)
        x_pos = (WIDTH - (before_text.get_width() + input_box_width + after_text.get_width())) // 2
        y_pos = (HEIGHT - before_text.get_height()) // 2

        input_box_rect = pygame.Rect(x_pos + before_text.get_width(), y_pos, input_box_width, before_text.get_height())
        pygame.draw.rect(screen, INPUT_BOX_COLOR, input_box_rect)
        input_text = font.render(user_input, True, ANSWER_COLOR)
        screen.blit(input_text, (input_box_rect.x + 5, y_pos))

        screen.blit(before_text, (x_pos, y_pos))
        screen.blit(after_text, (input_box_rect.right, y_pos))

        screen.blit(back_button_img, back_button_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and back_button_rect.collidepoint(event.pos):
                back_action()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_input.lower() == answers[current_question_index].lower():
                        feedback = "Correct Answer!"
                        if first_attempt:
                            score += 1
                        current_question_index += 1
                        first_attempt = True
                    else:
                        feedback = "Wrong Answer! Please try again."
                        first_attempt = False
                    user_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

        feedback_text = font.render(feedback, True, WRONG_ANSWER_COLOR if feedback.startswith("Wrong") else RIGHT_ANSWER)
        feedback_rect = feedback_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        screen.blit(feedback_text, feedback_rect)

        pygame.display.flip()

    screen.fill(WHITE)
    apply_glow(screen, image, image_position, glow_radius=15, glow_intensity=10)
    score_text = font.render(f"Your Final Score: {score}/{len(questions)}", True, QUESTION_COLOR)
    score_text_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(score_text, score_text_rect)
    screen.blit(back_button_img, back_button_rect.topleft)
    pygame.display.update()

    waiting_for_back_button = True
    while waiting_for_back_button:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and back_button_rect.collidepoint(event.pos):
                back_action()

    pygame.display.update()
    clock.tick(30)


# If this script is run standalone, execute the code
if __name__ == "__main__":
    fill_in_the_blanks()
