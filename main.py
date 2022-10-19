import pygame

from menus import MenuManager, Dropdown

pygame.init()

win = pygame.display.set_mode((800, 800), pygame.NOFRAME)
pygame.display.set_caption("Test")

menu = MenuManager()
menu.testing()

activeScrollbar = None


def update():
    win.fill((51, 51, 51))

    for element in menu.elements:
        element.show(win)

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
                for element in menu.elements:
                    # checks if each root element is clicked
                    if element.onClick and element.isClicked(pos):
                        element.onClick()

                    if element.scrollbar:
                        if element.scrollbar.isClicked(pos):
                            activeScrollbar = element.scrollbar

                    # checks if each child element is clicked
                    element.checkChildrenPressed(pos)


        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                activeScrollbar = None

        if activeScrollbar:
            activeScrollbar.onDrag(pos)

    update()
