import pygame


def quitGame():
    pygame.quit()
    quit()


class MenuManager:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 32)

        self.buttons = []
        self.containers = []

    def mainMenu(self):
        self.buttons = []
        self.containers = []
        screenWidth = 800
        screenHeight = 800

        buttonWidth = 200
        buttonHeight = 62
        buttonSpacing = 15

        numberOfButtons = 4

        padding = 10
        accountButtonRadius = 25

        borderWidth = 2

        # colours
        buttonColour = (160, 160, 160)
        boarderColour = (0, 0, 0)

        heightOfButtons = (buttonHeight * numberOfButtons) + (buttonSpacing * (numberOfButtons - 1))
        buttonOffsetY = (screenHeight - heightOfButtons) // 2

        playButton = Button(screenWidth // 2 - buttonWidth // 2,
                            buttonOffsetY,
                            buttonWidth,
                            buttonHeight,
                            buttonColour,
                            borderWidth,
                            boarderColour,
                            "Play",
                            self.font,
                            onClick=self.levelSelect)

        leaderboardButton = Button(screenWidth // 2 - buttonWidth // 2,
                                   buttonOffsetY + buttonHeight + buttonSpacing,
                                   buttonWidth,
                                   buttonHeight,
                                   buttonColour,
                                   borderWidth,
                                   boarderColour,
                                   "Leaderboard",
                                   self.font,
                                   onClick=None)

        settingsButton = Button(screenWidth // 2 - buttonWidth // 2,
                                buttonOffsetY + (buttonHeight + buttonSpacing) * 2,
                                buttonWidth,
                                buttonHeight,
                                buttonColour,
                                borderWidth,
                                boarderColour,
                                "Settings",
                                self.font)

        quitButton = Button(screenWidth // 2 - buttonWidth // 2,
                            buttonOffsetY + (buttonHeight + buttonSpacing) * 3,
                            buttonWidth,
                            buttonHeight,
                            buttonColour,
                            borderWidth,
                            boarderColour,
                            "Quit",
                            self.font,
                            onClick=quitGame)

        accountButton = AccountButton(screenWidth - padding - accountButtonRadius,
                                      padding + accountButtonRadius,
                                      accountButtonRadius,
                                      buttonColour,
                                      borderWidth,
                                      boarderColour)

        self.buttons = [playButton, leaderboardButton, settingsButton, quitButton, accountButton]

    def levelSelect(self):
        self.buttons = []
        self.containers = []
        screenWidth = 800
        screenHeight = 800

        # colours
        buttonColour = (160, 160, 160)
        boarderColour = (0, 0, 0)
        borderWidth = 2
        containerColour = (160, 160, 160)

        graphContainerMargin = 20
        graphColour = (100, 100, 100)

        levelSelectContainer = Container(0, 100,
                                         screenWidth // 2 + borderWidth // 2,
                                         screenHeight - 100,
                                         containerColour,
                                         borderWidth,
                                         boarderColour)

        graphSelectContainer = Container(screenWidth // 2 - borderWidth // 2, 100,
                                         screenWidth // 2 + borderWidth // 2,
                                         screenHeight - 100,
                                         containerColour,
                                         borderWidth,
                                         boarderColour)

        graphCount = 5
        graphHeight = (graphSelectContainer.displayHeight - graphContainerMargin * 2) // 3

        for i in range(graphCount):
            graphSelectContainer.addGraph(graphContainerMargin,
                                          graphContainerMargin + i * (graphHeight + graphContainerMargin//4),
                                          graphSelectContainer.displayWidth - graphContainerMargin * 2,
                                          graphHeight - graphContainerMargin//2,
                                          graphColour,
                                          borderWidth,
                                          boarderColour)

        graphSelectContainer.elements[0].loadData([10, 15, 10, 20, 32, 10, 21, 2, 10])

        self.buttons = []
        self.containers = [levelSelectContainer, graphSelectContainer]

    # def leaderboard(self):
    #     self.buttons = []
    #     self.containers = []
    #     screenWidth = 800
    #     screenHeight = 800
    #
    #     # colours
    #     buttonColour = (160, 160, 160)
    #     boarderColour = (0, 0, 0)
    #     borderWidth = 2
    #     containerColour = (160, 160, 160)
    #
    #     levelSelectContainer = Container(0, 100,
    #                                      screenWidth//2 + borderWidth//2,
    #                                      screenHeight-100,
    #                                      containerColour,
    #                                      borderWidth,
    #                                      boarderColour)
    #     graphSelectContainer = Container(screenWidth//2 - borderWidth//2, 100,
    #                                      screenWidth//2 + borderWidth//2,
    #                                      screenHeight-100,
    #                                      containerColour,
    #                                      borderWidth,
    #                                      boarderColour)
    #
    #     self.buttons = []
    #     self.containers = [levelSelectContainer, graphSelectContainer]


class Button:
    def __init__(self, x, y, width, height, colour,
                 borderWidth=0, borderColour=None,
                 text=None, font=None, textColour=(0, 0, 0),
                 onClick=None, parent=None):

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

        self.onClick = onClick

        self.parent = parent

    def show(self, win, offset=pygame.Vector2(0, 0)):
        if self.parent is not None:
            pos = self.pos + self.parent.pos
        else:
            pos = self.pos

        if self.borderColour:
            self.border = pygame.Rect(pos.x + offset.x,
                                      pos.y + offset.y,
                                      self.width,
                                      self.height)
            pygame.draw.rect(win, self.borderColour, self.border)

        self.rect = pygame.Rect(pos.x + self.borderWidth + offset.x,
                                pos.y + self.borderWidth + offset.y,
                                self.width - self.borderWidth * 2,
                                self.height - self.borderWidth * 2)
        pygame.draw.rect(win, self.colour, self.rect)

        if self.text:
            text = self.font.render(self.text, True, self.textColour)
            win.blit(text, (pos.x + self.width / 2 - text.get_width() / 2 + offset.x,
                            pos.y + self.height / 2 - text.get_height() / 2 + offset.y))

    def isClicked(self, pos):
        return self.rect.collidepoint(pos)


class AccountButton:
    def __init__(self, x, y, radius, colour, borderWidth=0, borderColour=None, onClick=None):
        self.pos = pygame.Vector2(x, y)
        self.radius = radius
        self.colour = colour

        self.borderWidth = borderWidth
        self.borderColour = borderColour
        self.border = None

        self.onClick = onClick

        self.sprite = pygame.image.load("assets/account.png")

    def show(self, win):
        if self.borderWidth and self.borderColour:
            pygame.draw.circle(win, self.borderColour, (self.pos.x, self.pos.y), self.radius + self.borderWidth)
        pygame.draw.circle(win, self.colour, (self.pos.x, self.pos.y), self.radius)

    def isClicked(self, pos):
        return self.pos.distance_to(pos) < self.radius


class Dropdown(Button):
    def __init__(self, x, y, width, height, colour, borderWidth=0, borderColour=None, text=None, font=None):
        super().__init__(x=x, y=y,
                         width=width,
                         height=height,
                         colour=colour,
                         borderWidth=borderWidth,
                         borderColour=borderColour,
                         text=text,
                         font=font,
                         onClick=self.toggleDropdown)
        self.isOpen = False
        self.buttons = []

    def addButton(self, x, y, width, height, colour,
                  borderWidth=0, borderColour=None, text=None, font=None, parent=None):
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

    def show(self, win, offset=pygame.Vector2(0, 0)):
        super().show(win, offset)
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
    def __init__(self, x, y, width, height, colour,
                 borderWidth=0, borderColour=None, text=None, font=None, parent=None):
        super().__init__(x=x, y=y,
                         width=width,
                         height=height,
                         colour=colour,
                         borderWidth=borderWidth,
                         borderColour=borderColour,
                         text=text,
                         font=font,
                         onClick=self.selectOption,
                         parent=parent)

    def selectOption(self):
        self.parent.text = self.text
        self.parent.toggleDropdown()


class Container:
    def __init__(self, x, y, displayWidth, displayHeight, colour, borderWidth=0, borderColour=None):
        self.pos = pygame.Vector2(x, y)
        self.displayWidth = displayWidth
        self.displayHeight = displayHeight
        self.containerHeight = displayHeight
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
        self.displayWidth -= scrollbarWidth
        scrollbar = Scrollbar(x=self.pos.x + self.displayWidth - self.borderWidth,
                              y=self.pos.y,
                              width=scrollbarWidth + self.borderWidth,
                              height=self.displayHeight,
                              container=self,
                              colour=self.colour,
                              borderWidth=2,
                              borderColour=self.borderColour)
        self.scrollbar = scrollbar

        for element in self.elements:
            element.width -= scrollbarWidth

    def addButton(self, x, y, width, height, colour,
                  borderWidth=None, borderColour=None, text=None, font=None, parent=None, onClick=None):
        button = Button(x=x,
                        y=y,
                        width=width,
                        height=height,
                        colour=colour,
                        borderWidth=borderWidth,
                        borderColour=borderColour,
                        text=text,
                        font=font,
                        onClick=onClick,
                        parent=parent)
        self.elements.append(button)

    def addGraph(self, x, y, width, height, colour, borderWidth=None, borderColour=None):
        graph = Histogram(x=x,
                          y=y,
                          width=width,
                          height=height,
                          colour=colour,
                          borderWidth=borderWidth,
                          borderColour=borderColour,
                          parent=self)
        self.elements.append(graph)

    def show(self, win):

        if self.elements:
            self.containerHeight = self.elements[-1].pos.y + self.elements[-1].height

        if self.containerHeight > self.displayHeight and not self.scrollbar:
            self.addScrollbar()

        if self.borderColour:
            self.border = pygame.Rect(self.pos.x,
                                      self.pos.y,
                                      self.displayWidth,
                                      self.displayHeight)
            pygame.draw.rect(win, self.borderColour, self.border)

        self.rect = pygame.Rect(self.pos.x + self.borderWidth,
                                self.pos.y + self.borderWidth,
                                self.displayWidth - self.borderWidth * 2,
                                self.displayHeight - self.borderWidth * 2)
        pygame.draw.rect(win, self.colour, self.rect)

        if self.scrollbar:
            self.scrollbar.show(win)

        for element in self.elements:
            x = self.pos.x + element.pos.x + self.offset.x
            y = self.pos.y + element.pos.y + self.offset.y
            if self.rect.colliderect((x, y, element.width, element.height)):
                element.show(win, offset=self.offset)


class Scrollbar:
    def __init__(self, x, y, width, height, container, colour, borderWidth=0, borderColour=None):
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
        if self.borderColour:
            self.border = pygame.Rect(self.pos.x,
                                      self.pos.y,
                                      self.width,
                                      self.height)
            pygame.draw.rect(win, self.borderColour, self.border)

        self.rect = pygame.Rect(self.pos.x + self.borderWidth,
                                self.pos.y + self.borderWidth,
                                self.width - self.borderWidth * 2,
                                self.height - self.borderWidth * 2)
        pygame.draw.rect(win, self.colour, self.rect)

        scrollRect = pygame.Rect(self.pos.x + self.borderWidth,
                                 self.pos.y + self.scrollPos.y + self.borderWidth,
                                 self.scrollWidth - self.borderWidth * 2,
                                 self.scrollHeight - self.borderWidth * 2)
        pygame.draw.rect(win, self.altColour, scrollRect)

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


class Histogram:
    def __init__(self, x, y, width, height, colour, borderWidth=0, borderColour=None, parent=None):
        self.pos = pygame.Vector2(x, y)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.colour = colour

        self.borderWidth = borderWidth
        self.borderColour = borderColour
        self.border = None

        self.data = []
        self.maxValue = 0
        self.barWidth = 0
        self.barHeight = 0
        self.barSpacing = 0

        self.parent = parent

        self.onClick = None

    def loadData(self, data):
        self.data = data
        self.maxValue = max(self.data)
        self.barWidth = (self.width - self.borderWidth * 2) / len(self.data)
        self.barHeight = (self.height - self.borderWidth * 2) / self.maxValue
        self.barSpacing = self.barWidth / 10

    def show(self, win, offset=pygame.Vector2(0, 0)):
        if self.parent:
            pos = self.parent.pos + self.pos
        else:
            pos = self.pos

        if self.borderColour:
            self.border = pygame.Rect(pos.x + offset.x,
                                      pos.y + offset.y,
                                      self.width,
                                      self.height)
            pygame.draw.rect(win, self.borderColour, self.border)

        self.rect = pygame.Rect(pos.x + self.borderWidth + offset.x,
                                pos.y + self.borderWidth + offset.y,
                                self.width - self.borderWidth * 2,
                                self.height - self.borderWidth * 2)
        pygame.draw.rect(win, self.colour, self.rect)

        for i, value in enumerate(self.data):
            barRect = pygame.Rect(pos.x + self.borderWidth + i * self.barWidth + self.barSpacing + offset.x,
                                  pos.y + self.borderWidth + self.height - value * self.barHeight + offset.y,
                                  self.barWidth - self.barSpacing * 2,
                                  value * self.barHeight)
            pygame.draw.rect(win, (self.colour[0] - 20, self.colour[1] - 20, self.colour[2] - 20), barRect)

    def isClicked(self, pos):
        return self.rect.collidepoint(pos)
