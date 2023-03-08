import pygame
import sys
import random

SIZE_BLOCK = 20  # Размер одного блока
COUNT_BLOCKS = 20  # Количество блоков по горизонтали и вертикали
HEADER_MARGIN = 70  # Отступ от верха окна
MARGIN = 1  # Отступ блоков друг от друга
SIZE = [SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS,
        SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS + HEADER_MARGIN]  # Размеры окна

# Цвета игры
FRAME_COLOR = (0, 255, 204)  # Цвет рамки
WHITE = (255, 255, 255)
BLUE = (204, 255, 255)
RED = (224, 0, 0)
HEADER_COLOR = (0, 204, 153)  # Цвет заголовка
SNAKE_COLOR = (0, 102, 0)

screen = pygame.display.set_mode(SIZE)  # создание экрана и присвоение переменной
pygame.display.set_caption('Змейка')
timer = pygame.time.Clock()  # создание объекта "Таймер" для задания количества кадров в секунду


class SnakeBlock:
    """Класс блока змейки c координатами левого верхнего угла х и у"""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y


def draw_block(color: tuple[int, int, int], row: int, column: int) -> None:
    """
    Рисует на экране в переданном ряду и колонке блок
    :param color: цвет заливки блока
    :param row: ряд
    :param column: колонка
    :return: None
    """
    coord_x = SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column + 1)  # Координата X блока
    coord_y = HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row + 1)  # Координата у блока
    pygame.draw.rect(screen, color, [coord_x, coord_y, SIZE_BLOCK, SIZE_BLOCK])


def get_random_block() -> SnakeBlock:
    """
    Функция создает блок по случайным координатам
    :return: Блок класса SnakeBlock
    """
    random_block = SnakeBlock(random.randint(0, SIZE_BLOCK - 1), random.randint(0, SIZE_BLOCK - 1))

    # Цикл если координаты блока совпадают с координатами одного из блоков змейки
    while random_block in snake_blocks:
        random_block.x = random.randint(0, SIZE_BLOCK - 1)
        random_block.y = random.randint(0, SIZE_BLOCK - 1)

    return random_block


snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9)]  # Список блоков змейки
food = get_random_block()  # Блок еды для змейки

# Задание первоначального движения змейки по оси Х
d_row = 0
d_col = 1

while True:

    # Обработка событий нажатия клавиш
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            # Движение змейки вверх
            if event.key == pygame.K_UP and d_col != 0:
                d_row -= 1
                d_col = 0
            # Движение змейки вниз
            elif event.key == pygame.K_DOWN and d_col != 0:
                d_row = 1
                d_col = 0
            # Движение змейки влево
            elif event.key == pygame.K_LEFT and d_row != 0:
                d_row = 0
                d_col -= 1
            # Движение змейки вправо
            elif event.key == pygame.K_RIGHT and d_row != 0:
                d_row = 0
                d_col = 1

    screen.fill(FRAME_COLOR)  # Заливка экрана цветом
    pygame.draw.rect(screen, HEADER_COLOR, [0, 0, SIZE[0], HEADER_MARGIN])

    # Отрисовка игрового поля
    for row in range(COUNT_BLOCKS):
        for column in range(COUNT_BLOCKS):
            if (row + column) % 2 == 0:
                color = BLUE
            else:
                color = WHITE
            draw_block(color, row, column)

    head = snake_blocks[-1]  # голова змейки

    # проверка на расположение змейки в пределах игрового поля
    if not head.is_inside():
        pygame.quit()
        sys.exit()

    # Отрисовка еды
    if food == head:
        food = get_random_block()
    draw_block(RED, food.x, food.y)

    # Отрисовка змейки
    for block in snake_blocks:
        draw_block(SNAKE_COLOR, block.x, block.y)
    new_head = SnakeBlock(head.x + d_row, head.y + d_col)  # Новая голова по ходу движения
    snake_blocks.append(new_head)  # Добавление новой головы в список блоков змейки
    snake_blocks.pop(0)

    pygame.display.flip()  # Обновление экрана
    timer.tick(3)  # число кадров в секунду
