import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
FPS = 60
TANK_SIZE = 40
BULLET_SIZE = 10
TANK_SPEED = 3
BULLET_SPEED = 7
PLAYER_SHOOT_DELAY = 1000  # Время перезарядки (в миллисекундах)
ENEMY_SHOOT_DELAY = 2000  # Время перезарядки для противников

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Глобальные переменные
player_color = GREEN
game_speed = 1
difficulty = 3  # Количество противников
last_player_shot_time = 0
enemies = []
bullets = []

# Настройка экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tanks 1990")
clock = pygame.time.Clock()


class Tank:
    def __init__(self, x, y, color, is_player=False):
        self.x = x
        self.y = y
        self.color = color
        self.is_player = is_player
        self.direction = "up"
        self.last_shot_time = 0

    def draw(self):
        # Рисуем корпус танка
        pygame.draw.rect(screen, self.color, (self.x, self.y, TANK_SIZE, TANK_SIZE))
        # Рисуем пушку
        if self.direction == "up":
            pygame.draw.rect(screen, self.color, (self.x + TANK_SIZE // 2 - 2, self.y - 10, 4, 10))
        elif self.direction == "down":
            pygame.draw.rect(screen, self.color, (self.x + TANK_SIZE // 2 - 2, self.y + TANK_SIZE, 4, 10))
        elif self.direction == "left":
            pygame.draw.rect(screen, self.color, (self.x - 10, self.y + TANK_SIZE // 2 - 2, 10, 4))
        elif self.direction == "right":
            pygame.draw.rect(screen, self.color, (self.x + TANK_SIZE, self.y + TANK_SIZE // 2 - 2, 10, 4))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.x = max(0, min(self.x, SCREEN_WIDTH - TANK_SIZE))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - TANK_SIZE))

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > (PLAYER_SHOOT_DELAY if self.is_player else ENEMY_SHOOT_DELAY):
            bullet_x, bullet_y = self.x + TANK_SIZE // 2 - BULLET_SIZE // 2, self.y + TANK_SIZE // 2 - BULLET_SIZE // 2
            if self.direction == "up":
                bullets.append(Bullet(bullet_x, bullet_y, 0, -BULLET_SPEED, self.is_player))
            elif self.direction == "down":
                bullets.append(Bullet(bullet_x, bullet_y, 0, BULLET_SPEED, self.is_player))
            elif self.direction == "left":
                bullets.append(Bullet(bullet_x, bullet_y, -BULLET_SPEED, 0, self.is_player))
            elif self.direction == "right":
                bullets.append(Bullet(bullet_x, bullet_y, BULLET_SPEED, 0, self.is_player))
            self.last_shot_time = current_time


class Bullet:
    def __init__(self, x, y, dx, dy, is_player_bullet):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.is_player_bullet = is_player_bullet

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        pygame.draw.rect(screen, RED if self.is_player_bullet else BLUE, (self.x, self.y, BULLET_SIZE, BULLET_SIZE))


def draw_menu():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    title = font.render("Tanks 1990", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

    button_font = pygame.font.Font(None, 50)
    start_button = button_font.render("Start Game", True, WHITE)
    settings_button = button_font.render("Settings", True, WHITE)

    start_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 300, 300, 50)
    settings_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 400, 300, 50)

    pygame.draw.rect(screen, GREEN, start_rect)
    pygame.draw.rect(screen, YELLOW, settings_rect)

    screen.blit(start_button, (start_rect.x + 10, start_rect.y + 10))
    screen.blit(settings_button, (settings_rect.x + 10, settings_rect.y + 10))

    return start_rect, settings_rect


def draw_settings():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 50)
    title = font.render("Settings", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

    color_text = font.render("Tank Color:", True, WHITE)
    speed_text = font.render("Game Speed:", True, WHITE)
    difficulty_text = font.render("Difficulty:", True, WHITE)

    screen.blit(color_text, (100, 200))
    screen.blit(speed_text, (100, 300))
    screen.blit(difficulty_text, (100, 400))

    color_options = ["Green", "Red", "Blue"]
    speed_options = ["Slow", "Normal", "Fast"]
    difficulty_options = ["Easy", "Medium", "Hard"]

    return draw_option_buttons(color_options, 200), draw_option_buttons(speed_options, 300), draw_option_buttons(difficulty_options, 400)


def draw_option_buttons(options, y):
    button_font = pygame.font.Font(None, 40)
    rects = []
    for i, option in enumerate(options):
        rect = pygame.Rect(300 + i * 120, y, 100, 50)
        pygame.draw.rect(screen, WHITE, rect)
        text = button_font.render(option, True, BLACK)
        screen.blit(text, (rect.x + 10, rect.y + 10))
        rects.append(rect)
    return rects


def main():
    global player_color, game_speed, difficulty, enemies, bullets

    running = True
    in_menu = True
    in_settings = False

    while running:
        if in_menu:
            start_rect, settings_rect = draw_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_rect.collidepoint(event.pos):
                        in_menu = False
                        initialize_game()
                    elif settings_rect.collidepoint(event.pos):
                        in_menu = False
                        in_settings = True

        elif in_settings:
            color_buttons, speed_buttons, difficulty_buttons = draw_settings()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, rect in enumerate(color_buttons):
                        if rect.collidepoint(event.pos):
                            player_color = [GREEN, RED, BLUE][i]
                    for i, rect in enumerate(speed_buttons):
                        if rect.collidepoint(event.pos):
                            game_speed = [0.5, 1, 2][i]
                    for i, rect in enumerate(difficulty_buttons):
                        if rect.collidepoint(event.pos):
                            difficulty = [1, 3, 5][i]
                    in_settings = False
                    in_menu = True

        else:
            screen.fill(BLACK)

            # Управление игроком
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                player.move(0, -TANK_SPEED)
                player.direction = "up"
            if keys[pygame.K_DOWN]:
                player.move(0, TANK_SPEED)
                player.direction = "down"
            if keys[pygame.K_LEFT]:
                player.move(-TANK_SPEED, 0)
                player.direction = "left"
            if keys[pygame.K_RIGHT]:
                player.move(TANK_SPEED, 0)
                player.direction = "right"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    player.shoot()

            # Движение и стрельба противников
            for enemy in enemies:
                if random.randint(1, 100) < 2:
                    enemy.shoot()
                if random.randint(1, 100) < 5:
                    enemy.direction = random.choice(["up", "down", "left", "right"])
                if enemy.direction == "up":
                    enemy.move(0, -TANK_SPEED)
                elif enemy.direction == "down":
                    enemy.move(0, TANK_SPEED)
                elif enemy.direction == "left":
                    enemy.move(-TANK_SPEED, 0)
                elif enemy.direction == "right":
                    enemy.move(TANK_SPEED, 0)

            # Обновление позиций пуль
            for bullet in bullets[:]:
                bullet.move()
                if not (0 <= bullet.x <= SCREEN_WIDTH) or not (0 <= bullet.y <= SCREEN_HEIGHT):
                    bullets.remove(bullet)

            # Проверка столкновений
            for bullet in bullets[:]:
                if bullet.is_player_bullet:
                    for enemy in enemies[:]:
                        if (
                            enemy.x < bullet.x < enemy.x + TANK_SIZE and
                            enemy.y < bullet.y < enemy.y + TANK_SIZE
                        ):
                            enemies.remove(enemy)
                            bullets.remove(bullet)
                else:
                    if (
                        player.x < bullet.x < player.x + TANK_SIZE and
                        player.y < bullet.y < player.y + TANK_SIZE
                    ):
                        print("Game Over!")
                        running = False

            # Отрисовка
            player.draw()
            for enemy in enemies:
                enemy.draw()
            for bullet in bullets:
                bullet.draw()

        pygame.display.flip()
        clock.tick(FPS * game_speed)

    pygame.quit()
    sys.exit()


def initialize_game():
    global player, enemies, bullets
    player = Tank(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, player_color, is_player=True)
    enemies.clear()
    bullets.clear()
    for _ in range(difficulty):
        x, y = random.randint(0, SCREEN_WIDTH - TANK_SIZE), random.randint(0, SCREEN_HEIGHT // 2)
        enemies.append(Tank(x, y, RED))


if __name__ == "__main__":
    main()