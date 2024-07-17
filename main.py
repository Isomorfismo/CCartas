import pygame
import random
import sys

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Card Counting Trainer")
font = pygame.font.Font(None, 36)

# Variables globales
speed = 1
num_cards = 52
input_active = False
user_text = ''

# Cargar imágenes de cartas (suponiendo que tienes las imágenes en la carpeta 'images/cards/')
suits = ['clubs', 'diamonds', 'hearts', 'spades']
card_files = [f'images/cards/{rank}_of_{suit}.png' for suit in suits for rank in
              list(range(2, 11)) + ['jack', 'queen', 'king', 'ace']]
cards = [pygame.transform.scale(pygame.image.load(card_file), (200, 250)) for card_file in
         card_files]  # Redimensionar cartas
card_names = [card_file for card_file in card_files]


class CardCounter:
    def __init__(self):
        self.running_count = 0

    def update_count(self, card_name):
        if any(rank in card_name for rank in ['2', '3', '4', '5', '6']):
            self.running_count += 1
        elif any(rank in card_name for rank in ['10', 'jack', 'queen', 'king', 'ace']):
            self.running_count -= 1

    def get_running_count(self):
        return self.running_count


def draw_menu():
    #Crear el menú principal con las opciones de configuración y su color (RGB)
    screen.fill((0, 0, 0))
    title = font.render("Card Counting Trainer", True, (201, 52, 52))
    speed_label = font.render(f"Speed (u/d arrows): {speed}", True, (66, 166, 252))
    num_cards_label = font.render(f"Number of Cards (l/r arrows): {num_cards}", True, (66, 166, 252))
    cards_rand = font.render("For random num. of cards (between 10 and 52) choose 0", True, (255, 255, 255))
    speed_rand = font.render("For random speed (between 1 and 7) choose 0", True, (255, 255, 255))
    remember = font.render("Remember: +1 if 2 to 6  ~  +0 if 7 to 9  ~  -1 if 10 to A", True, (201, 186, 52))
    play_button = font.render("Play", True, (0, 255, 0))
    #Agregar el texto al menú y su posición (horizontal, vertical)
    screen.blit(title, (250, 100))
    screen.blit(speed_label, (200, 200))
    screen.blit(num_cards_label, (200, 250))
    screen.blit(speed_rand, (100, 300))
    screen.blit(cards_rand, (100, 350))
    screen.blit(remember, (100, 400))
    screen.blit(play_button, (350, 500))

    pygame.display.flip()


def menu():
    """Display the main menu and handle user inputs to set the game configuration."""
    global speed, num_cards
    clock = pygame.time.Clock()

    while True:
        draw_menu()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            speed += 1
        if keys[pygame.K_DOWN]:
            speed = max(0, speed - 1)
        if keys[pygame.K_RIGHT]:
            if num_cards < 52:
                num_cards += 1
            else:
                num_cards += 0
        if keys[pygame.K_LEFT]:
            num_cards = max(0, num_cards - 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    play_game()

        clock.tick(10)  #Controlar la velocidad de actualización de la pantalla


def play_game():
    global input_active, user_text, speed, num_cards
    if num_cards == 0:
        num_cards = random.randint(10, 52)
    card_counter = CardCounter()
    dealt_cards = random.sample(list(zip(cards, card_names)), num_cards)

    for card, card_name in dealt_cards:
        screen.fill((0, 0, 0))
        screen.blit(card, (300, 100))
        pygame.display.flip()
        card_counter.update_count(card_name)
        if speed == 0:
            speed = random.randint(1, 7)
        pygame.time.wait(2000 // speed)

    input_active = True
    user_text = ''
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                    if int(user_text) == card_counter.get_running_count():
                        result_text = "Correct!"
                    else:
                        result_text = f"Incorrect. The correct count was: {card_counter.get_running_count()}"
                    display_result(result_text)
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

        screen.fill((0, 0, 0))
        input_box = pygame.Rect(300, 500, 200, 32)
        txt_surface = font.render(user_text, True, (255, 255, 255))
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
        pygame.display.flip()


def display_result(result_text):
    result_active = True
    while result_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    result_active = False
                    menu()

        screen.fill((0, 0, 0))
        result_surface = font.render(result_text, True, (255, 255, 255))
        screen.blit(result_surface, (150, 300))
        pygame.display.flip()


if __name__ == "__main__":
    menu()
