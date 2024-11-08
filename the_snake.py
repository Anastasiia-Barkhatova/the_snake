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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Создает базовый класс,
    от которого наследуются
    другие игровые объекты.
    """

    def __init__(self):
        self.position = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)
        self.body_color = (0, 0, 0)

    def draw(self):
        """Определяет, как объект будет
        отрисовываться на экране.
        """
        raise NotImplementedError

    def draw_cell(self, surface, position):
        """Рисует клетку."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Описывает яблоко и действия с ним.
    Отображает яблоко в случайных клетках поля
    с помощью метода def randomize_position(self).
    """

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на поле.
        Задаёт атрибуту position новое значение.
        """
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return (x, y)

    def draw(self, surface):
        """Рисует яблоко на игровой поверхности."""
        self.draw_cell(surface, self.position)


class Snake(GameObject):
    """Описывает змейку и её поведение.
    Управляет её движением, отрисовкой.
    Обрабатывает действия пользователя.
    """

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.reset()
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает первый элемент в списке positions,
        то есть позицию головы змейки.
        """
        return self.positions[0]

    def move(self):
        """Обновляет положение змейки в игре.
        Получает текущую позицию головы змейки.
        Вычисляет новую позицию головы.
        Проверяет на столкновение змейи с собой.
        Обновляет список позиций.
        """
        head_position = self.get_head_position()
        dx = self.direction[0]
        dy = self.direction[1]

        new_head_position = (
            ((head_position[0] + dx * GRID_SIZE) % SCREEN_WIDTH),
            ((head_position[1] + dy * GRID_SIZE) % SCREEN_WIDTH)
        )

        if new_head_position in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_head_position)

        if len(self.positions) > self.length:
            self.last = self.positions[-1]
            self.positions.pop()

    def reset(self):
        """Используется при столкновении змейки с собой.
        Очищает экран методом screen.fill() (заливает его черным цветом).
        При столкновении сбросывает игру,
        возвращает змейку в исходное положение.
        """
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):
        """Рисует змейку на экране.
        Затирает след, удаляя последний сегмент.
        """
        for position in self.positions[:-1]:
            self.draw_cell(surface, position)
        head_position = self.positions[0]
        self.draw_cell(surface, head_position)

        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Создает экземпляры классов Snake и Apple.
    Запускает бескконецный цикл, в котором
    сначала применяется метод clock.tick(speed),
    он замедляет «течение событий» в игре.
    Затем отрисовуваются яблоко и змейка,
    обрабаотываются нажатия клавиш,
    змейка передвагается,
    обновляется её направление движения.
    Проверяется, съела ли змейка яблоко и
    столкновения змейки с собой.
    При столкновении происходит сброс игры.
    """
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        snake.draw(screen)
        apple.draw(screen)
        handle_keys(snake)
        snake.move()
        snake.update_direction()
        if apple.position in snake.positions[1:]:
            apple.position = apple.randomize_position()
        if snake.positions[0] == apple.position:
            apple.position = apple.randomize_position()
            apple.draw(screen)
            snake.length += 1

        if snake.positions[0] in snake.positions[1:]:
            snake.reset()

        pygame.display.update()


if __name__ == '__main__':
    main()
