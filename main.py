import pygame

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


snake_blocks = [SnakeBlock(9, 9)]  # Список блоков змейки
d_row = 0
d_col = 1

while True:

    # Обработка событий нажатия клавиш
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

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

    # Отрисовка змейки
    for block in snake_blocks:
        draw_block(SNAKE_COLOR, block.x, block.y)
        block.x += d_row
        block.y += d_col

    pygame.display.flip()  # Обновление экрана
    timer.tick(2)  # число кадров в секунду
