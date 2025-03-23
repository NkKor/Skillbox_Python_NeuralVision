import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Размеры экрана
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 40

# Настройки по умолчанию
DEFAULT_SPEED = 10
DEFAULT_TRAPS = 5

# Загрузка спрайтов
snake_head_img = pygame.image.load(r"S:\code\vscode\Skillbox_Python_NeuralVision\PythonForInginiers\RawProjects\Snake\head.png")  # Спрайт головы змейки
snake_body_img = pygame.image.load(r"S:\code\vscode\Skillbox_Python_NeuralVision\PythonForInginiers\RawProjects\Snake\body.png")  # Спрайт тела змейки
food_img = pygame.image.load(r"S:\code\vscode\Skillbox_Python_NeuralVision\PythonForInginiers\RawProjects\Snake\meat.png")              # Спрайт еды
trap_img = pygame.image.load(r"S:\code\vscode\Skillbox_Python_NeuralVision\PythonForInginiers\RawProjects\Snake\trap.png")              # Спрайт ловушки
background_img = pygame.image.load(r"S:\code\vscode\Skillbox_Python_NeuralVision\PythonForInginiers\RawProjects\Snake\wall.png")  # Фоновое изображение

# Масштабирование спрайтов под размер блока
snake_head_img = pygame.transform.scale(snake_head_img, (BLOCK_SIZE, BLOCK_SIZE))
snake_body_img = pygame.transform.scale(snake_body_img, (BLOCK_SIZE, BLOCK_SIZE))
food_img = pygame.transform.scale(food_img, (BLOCK_SIZE, BLOCK_SIZE))
trap_img = pygame.transform.scale(trap_img, (BLOCK_SIZE, BLOCK_SIZE))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Экран
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка с красивой графикой")

# Часы для контроля скорости
clock = pygame.time.Clock()

# Шрифты
font_style = pygame.font.SysFont("bahnschrift", 35)

# Отображение текста
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Основной игровой цикл
def game_loop(speed, traps):
    game_over = False
    game_close = False

    # Начальные координаты змейки
    x, y = WIDTH // 2, HEIGHT // 2
    dx, dy = 0, 0

    snake_list = []
    snake_length = 1

    # Генерация случайной еды
    food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    # Генерация случайных ловушек
    trap_positions = []
    for _ in range(traps):
        trap_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        trap_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        trap_positions.append((trap_x, trap_y))

    while not game_over:
        while game_close:
            screen.fill(BLACK)
            draw_text("Вы проиграли! Нажмите Q-Выход или C-Играть снова", WHITE, screen, WIDTH // 6, HEIGHT // 3)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop(speed, traps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -BLOCK_SIZE, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = BLOCK_SIZE, 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -BLOCK_SIZE
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, BLOCK_SIZE

        # Проверка выхода за границы экрана
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        # Обновление координат змейки
        x += dx
        y += dy

        # Отрисовка фона
        screen.blit(background_img, (0, 0))

        # Отрисовка еды
        screen.blit(food_img, (food_x, food_y))

        # Отрисовка ловушек
        for trap in trap_positions:
            screen.blit(trap_img, (trap[0], trap[1]))

        # Добавление новой части змейки
        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Проверка столкновения с самой собой
        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        # Проверка столкновения с ловушкой
        if (x, y) in trap_positions:
            game_close = True

        # Отрисовка змейки
        for i, block in enumerate(snake_list):
            if i == len(snake_list) - 1:  # Голова змейки
                screen.blit(snake_head_img, (block[0], block[1]))
            else:  # Тело змейки
                screen.blit(snake_body_img, (block[0], block[1]))

        pygame.display.update()

        # Проверка поедания еды
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            snake_length += 1

        clock.tick(speed)

    pygame.quit()
    quit()

# Главное меню
def main_menu():
    while True:
        screen.fill(BLACK)
        draw_text("Змейка", font_style, WHITE, screen, WIDTH // 2 - 100, HEIGHT // 4)
        draw_text("Нажмите SPACE для начала игры", font_style, WHITE, screen, WIDTH // 2 - 200, HEIGHT // 2)
        draw_text("Нажмите N для настроек", font_style, WHITE, screen, WIDTH // 2 - 200, HEIGHT // 2 + 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return DEFAULT_SPEED, DEFAULT_TRAPS
                if event.key == pygame.K_n:
                    return settings_menu()

        pygame.display.update()

# Меню настроек
def settings_menu():
    speed = DEFAULT_SPEED
    traps = DEFAULT_TRAPS

    while True:
        screen.fill(BLACK)
        draw_text("Настройки", font_style, WHITE, screen, WIDTH // 2 - 100, HEIGHT // 4)
        draw_text(f"Скорость: {speed}", font_style, WHITE, screen, WIDTH // 2 - 200, HEIGHT // 2)
        draw_text(f"Количество ловушек: {traps}", font_style, WHITE, screen, WIDTH // 2 - 200, HEIGHT // 2 + 50)
        draw_text("Используйте стрелки ВВЕРХ/ВНИЗ для изменения", font_style, WHITE, screen, WIDTH // 2 - 300, HEIGHT // 2 + 100)
        draw_text("Нажмите ENTER для сохранения", font_style, WHITE, screen, WIDTH // 2 - 200, HEIGHT // 2 + 150)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if event.mod & pygame.KMOD_SHIFT:
                        traps += 1
                    else:
                        speed += 1
                if event.key == pygame.K_DOWN:
                    if event.mod & pygame.KMOD_SHIFT:
                        traps = max(1, traps - 1)
                    else:
                        speed = max(5, speed - 1)
                if event.key == pygame.K_RETURN:
                    return speed, traps

        pygame.display.update()

# Запуск игры
if __name__ == "__main__":
    speed, traps = main_menu()
    game_loop(speed, traps)