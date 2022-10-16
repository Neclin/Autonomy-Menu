import pygame

from menus import MenuManager, Dropdown

pygame.init()

win = pygame.display.set_mode((800, 800), pygame.NOFRAME)
pygame.display.set_caption("Test")

menu = MenuManager()
menu.main_menu()

activeScrollbar = None

def update():
    win.fill((51, 51, 51))

    for button in menu.buttons:
        button.show(win)
    for scrollbar in menu.scrollbars:
        scrollbar.show(win)

    pygame.display.update()


run = True
while run:
    pos = pygame.mouse.get_pos()
    pos = pygame.Vector2(pos[0], pos[1])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in menu.buttons:
                    if button.isClicked(pos) and button.onClick:
                        button.onClick()

                    if isinstance(button, Dropdown):
                        button.checkButtons(pos)
                for scrollbar in menu.scrollbars:
                    if scrollbar.isClicked(pos):
                        activeScrollbar = scrollbar

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                activeScrollbar = None

        if activeScrollbar:
            activeScrollbar.onDrag(pos)


    update()
