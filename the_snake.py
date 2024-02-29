import random
import pygame

# Инициализация Pygame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""
    position = (0, 0)
    body_color = (255, 255, 255)

    def __init__(self, position=position, body_color=body_color):
        """Инициализация объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовка объекта."""
        pass


class Apple(GameObject):
    """Класс, описывающий объект яблока."""
    position = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)
    body_color = APPLE_COLOR

    def __init__(self, position=position, body_color=body_color):
        """Инициализация яблока."""
        super().__init__(position, body_color)

    def randomize_position(self):
        """Рандомизация позиции яблока."""
        x_position = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y_position = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x_position, y_position)

    def draw(self, surface):
        """Отрисовка яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий объект змейки."""
    position = (GRID_WIDTH // 4 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)
    body_color = SNAKE_COLOR

    def __init__(self, position=position, body_color=body_color):
        """Инициализация змейки."""
        super().__init__(position, body_color)
        self.length = 1
        self.positions = [position]
        self.direction = RIGHT

    def update_direction(self, next_direction):
        """Обновление движения """
        self.direction = next_direction

    def move(self):
        """Перемещение змейки."""
        x, y = self.get_head_position()
        dx, dy = self.direction
        new_head = ((x + dx * GRID_SIZE) % SCREEN_WIDTH, (y + dy * GRID_SIZE) %
                    SCREEN_HEIGHT)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """Отрисовка змейки."""
        for position in self.positions:
            rect = pygame.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)
        last_position = self.positions[-1]
        last_rect = pygame.Rect(last_position[0], last_position[1], GRID_SIZE,
                                GRID_SIZE)
        pygame.draw.rect(surface, self.body_color, last_rect)
        pygame.draw.rect(surface, BORDER_COLOR, last_rect, 1)

    def get_head_position(self):
        """Получение позиции головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сброс состояния змейки."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(game_object):
    """Обработка нажатий клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.update_direction(UP)
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.update_direction(DOWN)
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(RIGHT)


def main():
    """Основная функция игры."""
    apple = Apple()

    snake = Snake()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)

        snake.move()

        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.randomize_position()

        if len(snake.positions) != len(set(snake.positions)):
            break

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
