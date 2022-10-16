import time
import pygame


def quitGame():
    pygame.quit()
    quit()


class MenuManager:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 32)

        self.buttons = []
        self.containers = []

    def main_menu(self):
        screenWidth = 800
        screenHeight = 800

        buttonWidth = 200
        buttonHeight = 62
        buttonSpacing = 15

        numberOfButtons = 4

        padding = 10
        accountButtonRadius = 25

        # colours
        buttonColour = (160, 160, 160)
        boarderColour = (0, 0, 0)
        dropdownColour = (100, 100, 100)
        containerColour = (100, 100, 100)

        heightOfButtons = (buttonHeight * numberOfButtons) + (buttonSpacing * (numberOfButtons - 1))
        buttonOffsetY = (screenHeight - heightOfButtons) // 2

        playButton = Button(screenWidth // 2 - buttonWidth // 2,
                            buttonOffsetY,
                            buttonWidth, buttonHeight, buttonColour, 2, boarderColour, "Play", self.font)

        leaderboardButton = Button(screenWidth // 2 - buttonWidth // 2,
                                   buttonOffsetY + buttonHeight + buttonSpacing,
                                   buttonWidth, buttonHeight, buttonColour, 2, boarderColour, "Leaderboard", self.font)

        settingsButton = Button(screenWidth // 2 - buttonWidth // 2,
                                buttonOffsetY + (buttonHeight + buttonSpacing) * 2,
                                buttonWidth, buttonHeight, buttonColour, 2, boarderColour, "Settings", self.font)

        quitButton = Button(screenWidth // 2 - buttonWidth // 2,
                            buttonOffsetY + (buttonHeight + buttonSpacing) * 3,
                            buttonWidth, buttonHeight, buttonColour, 2, boarderColour, "Quit", self.font,
                            onCLick=quitGame)

        accountButton = AccountButton(screenWidth - padding - accountButtonRadius,
                                      padding + accountButtonRadius, accountButtonRadius, (160, 160, 160), 2, boarderColour)

        dropdown = Dropdown(100, 100, 150, 50, buttonColour, 2, boarderColour, "Option 1", self.font)
        dropdown.addButton(0, 50, 150, 40, dropdownColour, 2, boarderColour, "Option 1", self.font, parent=dropdown)
        dropdown.addButton(0, 90, 150, 40, dropdownColour, 2, boarderColour, "Option 2", self.font, parent=dropdown)
        dropdown.addButton(0, 130, 150, 40, dropdownColour, 2, boarderColour, "Option 3", self.font, parent=dropdown)

        self.buttons = [playButton, leaderboardButton, settingsButton, quitButton, accountButton, dropdown]

        testContainer = Container(100, 100, 300, 400, 300, 800, containerColour, 2, boarderColour)
        for i in range(21):
            testContainer.addButton(75, i * 50, 150, 40, buttonColour, 2, boarderColour, f"Button {i}", self.font, parent=testContainer)

        coverContainer1 = Button(100, 0, 300, 98, (51, 51, 51), 0)
        coverContainer2 = Button(100, 502, 300, 98, (51, 51, 51), 0)

        self.buttons = [coverContainer1, coverContainer2]
        self.containers = [testContainer]


class Button:
    def __init__(self, x, y, width, height, colour,
                 borderWidth=None, borderColour=None,
                 text=None, font=None, textColour=(0, 0, 0),
                 onCLick=None, parent=None):

        self.pos = pygame.Vector2(x, y)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.colour = colour
        self.text = text
        self.font = font
        self.textColour = textColour

        self.borderWidth = borderWidth
        self.borderColour = borderColour
        self.border = None

        self.onClick = onCLick

        self.parent = parent

    def show(self, win, offset=pygame.Vector2(0, 0)):
        if self.parent is not None:
            pos = self.pos + self.parent.pos
        else:
            pos = self.pos

        if self.borderWidth and self.borderColour:
            self.border = pygame.Rect(pos.x - self.borderWidth + offset.x,
                                      pos.y - self.borderWidth + offset.y,
                                      self.width + self.borderWidth * 2,
                                      self.height + self.borderWidth * 2)
            pygame.draw.rect(win, self.borderColour, self.border)

        self.rect = pygame.Rect(pos.x + offset.x, pos.y + offset.y, self.width, self.height)
        pygame.draw.rect(win, self.colour, self.rect)

        if self.text:
            text = self.font.render(self.text, True, self.textColour)
            win.blit(text, (pos.x + self.width / 2 - text.get_width() / 2 + offset.x,
                            pos.y + self.height / 2 - text.get_height() / 2 + offset.y))

    def isClicked(self, pos):
        return self.rect.collidepoint(pos)


class AccountButton:
    def __init__(self, x, y, radius, colour, borderWidth=None, borderColour=None, onCLick=None):
        self.pos = pygame.Vector2(x, y)
        self.radius = radius
        self.colour = colour

        self.borderWidth = borderWidth
        self.borderColour = borderColour
        self.border = None

        self.onClick = onCLick

        self.sprite = pygame.image.load("assets/account.png")


    def show(self, win):
        if self.borderWidth and self.borderColour:
            pygame.draw.circle(win, self.borderColour, (self.pos.x, self.pos.y), self.radius + self.borderWidth)
        pygame.draw.circle(win, self.colour, (self.pos.x, self.pos.y), self.radius)

    def isClicked(self, pos):
        return self.pos.distance_to(pos) < self.radius


class Dropdown(Button):
    def __init__(self, x, y, width, height, colour, borderWidth=None, borderColour=None, text=None, font=None):
        super().__init__(x=x, y=y,
                         width=width,
                         height=height,
                         colour=colour,
                         borderWidth=borderWidth,
                         borderColour=borderColour,
                         text=text,
                         font=font,
                         onCLick=self.toggleDropdown)
        self.isOpen = False
        self.buttons = []

    def addButton(self, x, y, width, height, colour, borderWidth=None, borderColour=None, text=None, font=None, parent=None):
        button = DropdownOption(x=x, y=y,
                                width=width,
                                height=height,
                                colour=colour,
                                borderWidth=borderWidth,
                                borderColour=borderColour,
                                text=text,
                                font=font,
                                parent=parent)
        self.buttons.append(button)

    def show(self, win):
        super().show(win)
        if self.isOpen:
            for button in self.buttons:
                button.show(win)

    def isClicked(self, pos):
        return self.rect.collidepoint(pos)

    def checkButtons(self, pos):
        for button in self.buttons:
            if button.isClicked(pos) and button.onClick:
                button.onClick()

    def toggleDropdown(self):
        self.isOpen = not self.isOpen


class DropdownOption(Button):
    def __init__(self, x, y, width, height, colour, borderWidth=None, borderColour=None, text=None, font=None, parent=None):
        super().__init__(x=x, y=y,
                         width=width,
                         height=height,
                         colour=colour,
                         borderWidth=borderWidth,
                         borderColour=borderColour,
                         text=text,
                         font=font,
                         onCLick=self.selectOption,
                         parent=parent)

    def selectOption(self):
        self.parent.text = self.text
        self.parent.toggleDropdown()


class Container:
    def __init__(self, x, y, displayWidth, displayHeight, containerWidth, containerHeight, colour, borderWidth=None, borderColour=None):
        self.pos = pygame.Vector2(x, y)
        self.displayWidth = displayWidth
        self.displayHeight = displayHeight
        self.containerWidth = containerWidth
        self.containerHeight = containerHeight
        self.rect = pygame.Rect(x, y, displayWidth, displayHeight)
        self.colour = colour

        self.borderWidth = borderWidth
        self.borderColour = borderColour
        self.border = None

        self.scrollbar = None
        self.elements = []
        self.offset = pygame.Vector2(0, 0)


    def addScrollbar(self):
        scrollbarWidth = 20
        scrollbar = Scrollbar(x=self.pos.x + self.displayWidth,
                              y=self.pos.y,
                              width=scrollbarWidth,
                              height=self.displayHeight,
                              container=self,
                              colour=self.colour,
                              borderWidth=2,
                              borderColour=self.borderColour)
        self.scrollbar = scrollbar

    def addButton(self, x, y, width, height, colour, borderWidth=None, borderColour=None, text=None, font=None, parent=None):
        button = Button(x=x,
                        y=y,
                        width=width,
                        height=height,
                        colour=colour,
                        borderWidth=borderWidth,
                        borderColour=borderColour,
                        text=text,
                        font=font,
                        parent=parent)
        self.elements.append(button)

    def show(self, win):

        self.containerHeight = self.elements[-1].pos.y + self.elements[-1].height

        if self.containerHeight > self.displayHeight and not self.scrollbar:
            self.addScrollbar()

        if self.borderWidth and self.borderColour:
            self.border = pygame.Rect(self.pos.x - self.borderWidth, self.pos.y - self.borderWidth,
                                      self.displayWidth + self.borderWidth * 2, self.displayHeight + self.borderWidth * 2)
            pygame.draw.rect(win, self.borderColour, self.border)

        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.displayWidth, self.displayHeight)
        pygame.draw.rect(win, self.colour, self.rect)

        if self.scrollbar:
            self.scrollbar.show(win)

        for element in self.elements:
            x = self.pos.x + element.pos.x + self.offset.x
            y = self.pos.y + element.pos.y + self.offset.y
            if self.rect.colliderect((x, y, element.width, element.height)):
                element.show(win, offset=self.offset)


class Scrollbar:
    def __init__(self, x, y, width, height, container, colour, borderWidth=None, borderColour=None):
        self.pos = pygame.Vector2(x, y)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.colour = colour
        self.altColour = (colour[0] + 20, colour[1] + 20, colour[2] + 20)

        self.container = container

        self.scrollPos = pygame.Vector2(0, 0)
        self.scrollWidth = width
        self.scrollHeight = (self.height / self.container.containerHeight) * self.height

        self.borderWidth = borderWidth
        self.borderColour = borderColour
        self.border = None

        self.onDrag = self.moveScroll

    def show(self, win):
        if self.borderWidth and self.borderColour:
            self.border = pygame.Rect(self.pos.x - self.borderWidth, self.pos.y - self.borderWidth,
                                      self.width + self.borderWidth * 2, self.height + self.borderWidth * 2)
            pygame.draw.rect(win, self.borderColour, self.border)

        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        pygame.draw.rect(win, self.colour, self.rect)

        pygame.draw.rect(win, self.altColour, (self.pos.x, self.pos.y + self.scrollPos.y, self.scrollWidth, self.scrollHeight))

    def isClicked(self, pos):
        return self.rect.collidepoint(pos)

    def moveScroll(self, pos):
        self.scrollPos = pos - self.pos - pygame.Vector2(0, self.scrollHeight / 2)
        self.scrollPos.y = max(0, min(self.scrollPos.y, self.height - self.scrollHeight))

        additionalSpace = self.container.containerHeight - self.container.displayHeight
        scrollMoveAmount = self.container.displayHeight - self.scrollHeight
        if scrollMoveAmount > 0:
            self.container.offset.y = -additionalSpace / scrollMoveAmount * self.scrollPos.y
        else:
            self.container.offset.y = self.container.containerHeight
