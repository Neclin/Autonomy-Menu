import pygame


def quitGame():
    pygame.quit()
    quit()


class MenuManager:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 32)

        self.elements = []

    def testing(self):
        testContainer = Container(100, 100, 500, 500,
                                  (160, 160, 160), 2, 20,
                                  padding=10)

        for i in range(5):
            testButton = Button(0, i * 110, 150, 100,
                                (150, 150, 150), 2, (0, 0, 0),
                                "Test Button", (0, 0, 0), self.font,
                                horizontalAlignment="center",
                                onClick=quitGame)

            testContainer.addElement(testButton)

        self.elements = [testContainer]

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
        borderColour = (0, 0, 0)

        heightOfButtons = (buttonHeight * numberOfButtons) + (buttonSpacing * (numberOfButtons - 1))
        buttonOffsetY = (screenHeight - heightOfButtons) // 2

        playButton = Button(screenWidth // 2 - buttonWidth // 2,
                            buttonOffsetY,
                            buttonWidth,
                            buttonHeight,
                            buttonColour,
                            borderWidth,
                            borderColour,
                            "Play",
                            self.font,
                            onClick=self.levelSelect)

        leaderboardButton = Button(screenWidth // 2 - buttonWidth // 2,
                                   buttonOffsetY + buttonHeight + buttonSpacing,
                                   buttonWidth,
                                   buttonHeight,
                                   buttonColour,
                                   borderWidth,
                                   borderColour,
                                   "Leaderboard",
                                   self.font,
                                   onClick=None)

        settingsButton = Button(screenWidth // 2 - buttonWidth // 2,
                                buttonOffsetY + (buttonHeight + buttonSpacing) * 2,
                                buttonWidth,
                                buttonHeight,
                                buttonColour,
                                borderWidth,
                                borderColour,
                                "Settings",
                                self.font)

        quitButton = Button(screenWidth // 2 - buttonWidth // 2,
                            buttonOffsetY + (buttonHeight + buttonSpacing) * 3,
                            buttonWidth,
                            buttonHeight,
                            buttonColour,
                            borderWidth,
                            borderColour,
                            "Quit",
                            self.font,
                            onClick=quitGame)

        accountButton = AccountButton(screenWidth - padding - accountButtonRadius,
                                      padding + accountButtonRadius,
                                      accountButtonRadius,
                                      buttonColour,
                                      borderWidth,
                                      borderColour)

        self.buttons = [playButton, leaderboardButton, settingsButton, quitButton, accountButton]

    def levelSelect(self):
        self.buttons = []
        self.containers = []
        screenWidth = 800
        screenHeight = 800

        # colours
        buttonColour = (160, 160, 160)
        borderColour = (0, 0, 0)
        borderWidth = 2
        containerColour = (160, 160, 160)

        graphContainerMargin = 20
        graphColour = (100, 100, 100)

        levelSelectContainer = Container(0, 100,
                                         screenWidth // 2 + borderWidth // 2,
                                         screenHeight - 100,
                                         containerColour,
                                         borderWidth,
                                         graphContainerMargin,
                                         borderColour)

        graphSelectContainer = Container(screenWidth // 2 - borderWidth // 2, 100,
                                         screenWidth // 2 + borderWidth // 2,
                                         screenHeight - 100,
                                         containerColour,
                                         borderWidth,
                                         graphContainerMargin,
                                         borderColour)

        graphCount = 3
        graphHeight = (graphSelectContainer.displayHeight - graphContainerMargin * 2) // graphCount

        for i in range(graphCount):
            graphSelectContainer.addGraph(0,
                                          0 + i * graphSelectContainer.displayHeight,
                                          graphSelectContainer.displayWidth,
                                          graphSelectContainer.displayHeight,
                                          graphColour,
                                          borderWidth,
                                          borderColour)

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
    #     borderColour = (0, 0, 0)
    #     borderWidth = 2
    #     containerColour = (160, 160, 160)
    #
    #     levelSelectContainer = Container(0, 100,
    #                                      screenWidth//2 + borderWidth//2,
    #                                      screenHeight-100,
    #                                      containerColour,
    #                                      borderWidth,
    #                                      borderColour)
    #     graphSelectContainer = Container(screenWidth//2 - borderWidth//2, 100,
    #                                      screenWidth//2 + borderWidth//2,
    #                                      screenHeight-100,
    #                                      containerColour,
    #                                      borderWidth,
    #                                      borderColour)
    #
    #     self.buttons = []
    #     self.containers = [levelSelectContainer, graphSelectContainer]


class RectangleObject:
    def __init__(self, x, y, width, height,
                 colour,
                 borderWidth=0, borderColour=None,
                 text=None, textColour=None, font=None,
                 margin=0, padding=0,
                 horizontalAlignment="left",
                 onClick=None,
                 parent=None, children=None):

        self.pos = pygame.Vector2(x, y)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

        self.colour = colour

        self.borderWidth = borderWidth
        self.borderColour = borderColour
        self.border = None

        self.text = text
        self.textColour = textColour
        self.font = font

        self.margin = margin
        self.padding = padding

        self.horizontalAlignment = horizontalAlignment

        self.onClick = onClick

        self.parent = parent
        self.children = children

    def checkPadding(self):
        if self.parent:
            self.width = min(self.width, self.parent.width - self.parent.padding * 2)
            self.height = min(self.height, self.parent.height - self.parent.padding * 2)

            self.pos.x = max(self.pos.x, self.parent.padding)
            self.pos.x = min(self.pos.x, self.parent.width - self.parent.padding)

            self.pos.y = max(self.pos.y, self.parent.padding)
            self.pos.y = min(self.pos.y, self.parent.height - self.parent.padding)

    def checkAlignment(self):
        if self.parent:
            if self.horizontalAlignment == "left":
                self.pos.x = 0
            elif self.horizontalAlignment == "right":
                self.pos.x = self.parent.width - self.width
            elif self.horizontalAlignment == "center":
                self.pos.x = self.parent.width // 2 - self.width // 2

    def show(self, win, offset=pygame.Vector2(0, 0)):
        if self.parent:
            pos = self.parent.pos + self.pos
            self.checkAlignment()
            self.checkPadding()
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
            textRect = text.get_rect()
            textRect.center = self.rect.center
            win.blit(text, textRect)

    def isClicked(self, mousePos):
        return self.rect.collidepoint(mousePos)

    def checkChildrenPressed(self, mousePos):
        if self.children:
            for child in self.children:
                if child.onClick and child.isClicked(mousePos):
                    child.onClick()


class Button(RectangleObject):
    def __init__(self, x, y, width, height,
                 colour,
                 borderWidth=0, borderColour=None,
                 text=None, textColour=(0, 0, 0), font=None,
                 margin=0, padding=0,
                 horizontalAlignment="left",
                 onClick=None,
                 parent=None):
        super().__init__(x, y, width, height,
                         colour,
                         borderWidth, borderColour,
                         text, textColour, font,
                         margin, padding,
                         horizontalAlignment,
                         onClick,
                         parent)

    def show(self, win, offset=pygame.Vector2(0, 0)):
        super().show(win, offset)

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


class Container(RectangleObject):
    def __init__(self, x, y, displayWidth, displayHeight,
                 colour,
                 borderWidth=0, borderColour=None,
                 text=None, textColour=None, font=None,
                 margin=0, padding=0,
                 horizontalAlignment="left",
                 onClick=None,
                 parent=None, children=None):

        super().__init__(x, y, displayWidth, displayHeight,
                         colour,
                         borderWidth, borderColour,
                         text, textColour, font,
                         margin, padding,
                         horizontalAlignment,
                         onClick,
                         parent, children)

        self.containerHeight = 0
        self.scrollbar = None
        self.offset = pygame.Vector2(0, 0)

    def addElement(self, element):
        if self.children:
            self.children.append(element)
        else:
            self.children = [element]
        element.parent = self

    def addScrollbar(self):
        scrollbarWidth = 20
        self.width -= scrollbarWidth
        scrollbar = Scrollbar(x=self.pos.x + self.width - self.borderWidth,
                              y=self.pos.y,
                              width=scrollbarWidth + self.borderWidth,
                              height=self.height,
                              container=self,
                              colour=self.colour,
                              borderWidth=2,
                              borderColour=self.borderColour)
        self.scrollbar = scrollbar

        for child in self.children:
            child.width -= scrollbarWidth

    def addButton(self, x, y, width, height, colour,
                  borderWidth=None, borderColour=None, text=None, font=None, parent=None, onClick=None):
        x = max(x, x + self.margin)
        x = min(x, self.displayWidth - self.margin)
        y = max(y, y + self.margin)
        y = min(y, self.displayHeight - self.margin)

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

        x = max(x, self.margin)
        x = min(x, self.displayWidth - self.margin)
        y = max(y, self.margin)
        y = min(y, self.displayHeight - self.margin)

        width = max(width, self.margin * 2)
        width = min(width, self.displayWidth - self.margin * 2)
        height = max(height, self.margin * 2)
        height = min(height, self.displayHeight - self.margin * 2)

        graph = Histogram(x=x,
                          y=y,
                          width=width,
                          height=height,
                          colour=colour,
                          borderWidth=borderWidth,
                          borderColour=borderColour,
                          parent=self)
        self.elements.append(graph)

    def show(self, win, offset=pygame.Vector2(0, 0)):
        super().show(win, offset)

        if self.children:
            self.containerHeight = self.children[-1].pos.y + self.children[-1].height + self.padding

        if self.containerHeight > self.height and not self.scrollbar:
            self.addScrollbar()

        if self.scrollbar:
            self.scrollbar.show(win)

        for child in self.children:
            x = self.pos.x + child.pos.x + self.offset.x
            y = self.pos.y + child.pos.y + self.offset.y
            if self.rect.colliderect((x, y, child.width, child.height)):
                child.show(win, offset=self.offset)


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

        additionalSpace = self.container.containerHeight - self.container.height
        scrollMoveAmount = self.container.height - self.scrollHeight
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
