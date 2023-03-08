import random
from constants import *
import pygame


class SnakeBlock:
    """Класс блока змейки c координатами левого верхнего угла х и у"""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y


def draw_block(color: tuple[int, int, int], row: int, column: int, screen: pygame.display) -> None:
    """
    Рисует на экране в переданном ряду и колонке блок
    :param screen: экран для отображения блоков
    :param color: цвет заливки блока
    :param row: ряд
    :param column: колонка
    :return: None
    """
    coord_x = SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column + 1)  # Координата X блока
    coord_y = HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row + 1)  # Координата у блока
    pygame.draw.rect(screen, color, [coord_x, coord_y, SIZE_BLOCK, SIZE_BLOCK])


def get_random_block(blocks: list[SnakeBlock]) -> SnakeBlock:
    """
    Функция создает блок по случайным координатам
    :return: Блок класса SnakeBlock
    """
    random_block = SnakeBlock(random.randint(0, SIZE_BLOCK - 1), random.randint(0, SIZE_BLOCK - 1))

    # Цикл если координаты блока совпадают с координатами одного из блоков змейки
    while random_block in blocks:
        random_block.x = random.randint(0, SIZE_BLOCK - 1)
        random_block.y = random.randint(0, SIZE_BLOCK - 1)

    return random_block
