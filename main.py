import pygame

from menus import MenuManager, Dropdown

pygame.init()

win = pygame.display.set_mode((800, 800), pygame.NOFRAME)
pygame.display.set_caption("Test")

menu = MenuManager()
menu.main_menu()


def update():
    win.fill((51, 51, 51))
    for button in menu.buttons:
        button.show(win)
    pygame.display.update()


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in menu.buttons:
                if button.isClicked(pygame.mouse.get_pos()) and button.onClick:
                    button.onClick()

                if isinstance(button, Dropdown):
                    button.checkButtons(pygame.mouse.get_pos())

    update()
