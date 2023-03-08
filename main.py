import pygame
import sys
import random
pygame.init()
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
BLACK = (0, 0, 0)
HEADER_COLOR = (0, 204, 153)  # Цвет заголовка
SNAKE_COLOR = (0, 102, 0)

screen = pygame.display.set_mode(SIZE)  # создание экрана и присвоение переменной
pygame.display.set_caption('Змейка')
timer = pygame.time.Clock()  # создание объекта "Таймер" для задания количества кадров в секунду
courier = pygame.font.SysFont('courier', 36)  # Создание шрифта
speed = 1


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
total = 0  # Количество блоков змейки

# Задание первоначального движения змейки по оси Х
d_row = buf_row = 0  # buf_row - буферное значение ряда
d_col = buf_col = 1  # buf_col - буферное значение колонки

while True:

    # Обработка событий нажатия клавиш
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            # Движение змейки вверх
            if event.key == pygame.K_UP and d_col != 0:
                buf_row -= 1
                buf_col = 0
            # Движение змейки вниз
            elif event.key == pygame.K_DOWN and d_col != 0:
                buf_row = 1
                buf_col = 0
            # Движение змейки влево
            elif event.key == pygame.K_LEFT and d_row != 0:
                buf_row = 0
                buf_col -= 1
            # Движение змейки вправо
            elif event.key == pygame.K_RIGHT and d_row != 0:
                buf_row = 0
                buf_col = 1

    screen.fill(FRAME_COLOR)  # Заливка экрана цветом
    pygame.draw.rect(screen, HEADER_COLOR, [0, 0, SIZE[0], HEADER_MARGIN])

    text_total = courier.render(f'Total: {total}', 0, WHITE)  # Создание текста
    speed_total = courier.render(f'Speed: {speed}', 0, WHITE)  # Создание текста
    screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))  # обновление экрана
    screen.blit(speed_total, (SIZE_BLOCK + 230, SIZE_BLOCK))  # обновление экрана

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
        snake_blocks.append(food)
        total += 1
        speed = total // 5 + 1
        food = get_random_block()
    draw_block(RED, food.x, food.y)

    # Отрисовка змейки
    for i in range(len(snake_blocks)):

        # отрисовка головы (последнего значение в списке snake_blocks) черным цветом
        if i == len(snake_blocks) - 1:
            draw_block(BLACK, snake_blocks[i].x, snake_blocks[i].y)

        else:
            draw_block(SNAKE_COLOR, snake_blocks[i].x, snake_blocks[i].y)

    pygame.display.flip()  # Обновление экрана

    # присвоение буферного значения
    d_row = buf_row
    d_col = buf_col

    new_head = SnakeBlock(head.x + d_row, head.y + d_col)  # Новая голова по ходу движения
    if new_head in snake_blocks:
        pygame.quit()
        sys.exit()

    snake_blocks.append(new_head)  # Добавление новой головы в список блоков змейки
    snake_blocks.pop(0)

    timer.tick(2 + speed)  # число кадров в секунду
