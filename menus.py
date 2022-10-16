import time
import pygame


def quitGame():
    pygame.quit()
    quit()


class MenuManager:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 32)

        self.buttons = []
        self.scrollbars = []

    def main_menu(self):
        screenWidth = 800
        screenHeight = 800

        buttonWidth = 200
        buttonHeight = 62
        buttonSpacing = 15

        numberOfButtons = 4

        padding = 10
        accountButtonRadius = 25

        heightOfButtons = (buttonHeight * numberOfButtons) + (buttonSpacing * (numberOfButtons - 1))
        buttonOffsetY = (screenHeight - heightOfButtons) // 2

        playButton = Button(screenWidth // 2 - buttonWidth // 2,
                            buttonOffsetY,
                            buttonWidth, buttonHeight, (160, 160, 160), 2, (0, 0, 0), "Play", self.font)

        leaderboardButton = Button(screenWidth // 2 - buttonWidth // 2,
                                   buttonOffsetY + buttonHeight + buttonSpacing,
                                   buttonWidth, buttonHeight, (160, 160, 160), 2, (0, 0, 0), "Leaderboard", self.font)

        settingsButton = Button(screenWidth // 2 - buttonWidth // 2,
                                buttonOffsetY + (buttonHeight + buttonSpacing) * 2,
                                buttonWidth, buttonHeight, (160, 160, 160), 2, (0, 0, 0), "Settings", self.font)

        quitButton = Button(screenWidth // 2 - buttonWidth // 2,
                            buttonOffsetY + (buttonHeight + buttonSpacing) * 3,
                            buttonWidth, buttonHeight, (160, 160, 160), 2, (0, 0, 0), "Quit", self.font,
                            quitGame)

        accountButton = AccountButton(screenWidth - padding - accountButtonRadius,
                                      padding + accountButtonRadius, accountButtonRadius, (160, 160, 160), 2, (0, 0, 0))

        dropdown = Dropdown(100, 100, 150, 50, (160, 160, 160), 2, (0, 0, 0), "Option 1", self.font)
        dropdown.addButton(100, 150, 150, 40, (100, 100, 100), 2, (0, 0, 0), "Option 1", self.font, parent=dropdown)
        dropdown.addButton(100, 190, 150, 40, (100, 100, 100), 2, (0, 0, 0), "Option 2", self.font, parent=dropdown)
        dropdown.addButton(100, 230, 150, 40, (100, 100, 100), 2, (0, 0, 0), "Option 3", self.font, parent=dropdown)

        scrollbar = Scrollbar(600, 100, 20, 400, (160, 160, 160), 2, (0, 0, 0))

        self.buttons = [playButton, leaderboardButton, settingsButton, quitButton, accountButton, dropdown]
        self.scrollbars = [scrollbar]


class Button:
    def __init__(self, x, y, width, height, colour, borderWidth=None, borderColour=None, text=None, font=None, onCLick=None):
        self.pos = pygame.Vector2(x, y)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.colour = colour
        self.text = text
        self.font = font

        self.borderWidth = borderWidth
        self.borderColour = borderColour
        self.border = None

        self.onClick = onCLick

    def show(self, win):
        if self.borderWidth and self.borderColour:
            self.border = pygame.Rect(self.pos.x - self.borderWidth, self.pos.y - self.borderWidth,
                                      self.width + self.borderWidth * 2, self.height + self.borderWidth * 2)
            pygame.draw.rect(win, self.borderColour, self.border)

        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        pygame.draw.rect(win, self.colour, self.rect)

        if self.text:
            text = self.font.render(self.text, True, (0, 0, 0))
            win.blit(text, (self.pos.x + self.width / 2 - text.get_width() / 2, self.pos.y + self.height / 2 - text.get_height() / 2))

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
        super().__init__(x, y, width, height, colour, borderWidth, borderColour, text, font, lambda: self.toggleDropdown())
        self.isOpen = False
        self.buttons = []

    def addButton(self, x, y, width, height, colour, borderWidth=None, borderColour=None, text=None, font=None, parent=None):
        button = DropdownOption(x, y,
                                width, height,
                                colour,
                                borderWidth, borderColour,
                                text, font,
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
        super().__init__(x, y, width, height, colour, borderWidth, borderColour, text, font, self.selectOption)
        self.parent = parent

    def selectOption(self):
        self.parent.text = self.text
        self.parent.toggleDropdown()


class Scrollbar:
    def __init__(self, x, y, width, height, colour, borderWidth=None, borderColour=None):
        self.pos = pygame.Vector2(x, y)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.colour = colour
        self.altColour = (colour[0] + 20, colour[1] + 20, colour[2] + 20)

        self.containerSize = 500

        self.scrollPos = pygame.Vector2(0, 0)
        self.scrollWidth = width
        self.scrollHeight = 40

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

