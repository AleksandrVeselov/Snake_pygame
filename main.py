import pygame

SIZE = [500, 600]  # Размеры окна
SIZE_BLOCK = 20  # Размер одного блока
COUNT_BLOCKS = 20  # Количество блоков по горизонтали и вертикали

# Цвета игры
FRAME_COLOR = (0, 255, 204)  # Цвет рамки
WHITE = (255, 255, 255)
BLUE = (204, 255, 255)

MARGIN = 1  # Отступ блоков друг от друга

screen = pygame.display.set_mode(SIZE)  # создание экрана и присвоение переменной
pygame.display.set_caption('Змейка')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill(FRAME_COLOR)  # Заливка экрана цветом

    # Отрисовка игрового поля
    for row in range(COUNT_BLOCKS):
        for column in range(COUNT_BLOCKS):
            if (row + column) % 2 == 0:
                color = BLUE
            else:
                color = WHITE
            coord_x = 10 + column * SIZE_BLOCK + MARGIN * (column + 1)  # Координата X блока
            coord_y = 20 + row * SIZE_BLOCK + MARGIN * (row + 1)  # Координата у блока
            pygame.draw.rect(screen, color, [coord_x, coord_y, SIZE_BLOCK, SIZE_BLOCK])
    pygame.display.flip()  # Обновление экрана