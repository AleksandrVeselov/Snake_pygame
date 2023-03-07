import pygame

SIZE = [400, 600]  # Размеры окна

screen = pygame.display.set_mode(SIZE)  # создание экрана и присвоение переменной
pygame.display.set_caption('Змейка')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()