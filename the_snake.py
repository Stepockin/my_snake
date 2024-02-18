from random import choice, randint

import pygame

# Инициализация PyGame:
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
    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        pass


class Apple(GameObject):
    def __init__(self, position, body_color=(255, 0, 0)):
        super().__init__(position, body_color)

    def randomize_position(self):
        self.position = (randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT))

    def draw(self, surface):
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    def __init__(self, position, body_color=(0, 255, 0)):
        super().__init__(position, body_color)
        self.length = 1
        self.positions = [position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        self.last = self.positions[-1]  # Сохраняем последнюю позицию перед движением
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % SCREEN_WIDTH, (head_y + dy) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        for position in self.positions:
            x, y = position
            rect = pygame.Rect(x + GRID_SIZE // 2, y + GRID_SIZE // 2, GRID_SIZE // 2, GRID_SIZE // 2)
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Затирание последнего сегмента
        if self.last:
            x, y = self.last
            rect = pygame.Rect(x + GRID_SIZE // 2, y + GRID_SIZE // 2, GRID_SIZE // 2, GRID_SIZE // 2)
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect)


    def get_head_position(self):
        return self.positions[0]

def handle_keys(self):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != DOWN:
                self.next_direction = UP
            elif event.key == pygame.K_DOWN and self.direction != UP:
                self.next_direction = DOWN
            elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                self.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                self.next_direction = RIGHT


def main():
    """Функция реализации логики игры"""
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        # Прорисовка Snake и Apple
        snake.draw(screen)
        apple.draw(screen)

        # Установка скорости движения Snake
        clock.tick(SPEED)

        # Опрос клавиатуры на определение команды изменения направления
        

        # Изменение направление при наличии команды
        snake.update_direction()

        # Изменение набора позиций тела Snake
        # в зависимости от текущего направления движения
        snake.move()

        # Проверка совпадения головы Snake и apple
        # В случае совпадения, генерация нового яблока
        if snake.positions[0] == apple.position:
            apple.new_position_apple(snake.position)
            snake.flag = True

        # Проверка ввыхода за пределы поля
        if (
            snake.positions[0][0] < 0 or snake.positions[0][0] > 620
            or snake.positions[0][1] < 0 or snake.positions[0][1] > 460
        ):
            print('Игра окончена. Вы столкнулись со стеной')
            break
        pygame.display.update()


if __name__ == '__main__':
    main()