import sys
import pygame_menu
from utils import *

pygame.init()

screen = pygame.display.set_mode(SIZE)  # создание экрана и присвоение переменной
pygame.display.set_caption('Змейка')
timer = pygame.time.Clock()  # создание объекта "Таймер" для задания количества кадров в секунду
courier = pygame.font.SysFont('courier', 36)  # Создание шрифта


def start_the_game():
    snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9)]  # Список блоков змейки
    food = get_random_block(snake_blocks)  # Блок еды для змейки
    total = 0  # Количество блоков змейки
    speed = 1  # Начальная скорость змейки

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
            break

        # Отрисовка еды
        if food == head:
            snake_blocks.append(food)
            total += 1
            speed = total // 5 + 1
            food = get_random_block(snake_blocks)
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


# Создание меню для игры
menu = pygame_menu.Menu('Welcome', 400, 300,
                        theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Имя :', default='Игрок 1')
menu.add.button('Играть', start_the_game)
menu.add.button('Выход', pygame_menu.events.EXIT)

# Главный цикл
while True:
    screen.fill(FRAME_COLOR)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()

