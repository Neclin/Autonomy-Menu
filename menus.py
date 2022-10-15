import time
import pygame


def quitGame():
    pygame.quit()
    quit()


class MenuManager:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 32)

        self.buttons = []

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
                            lambda: quitGame())

        accountButton = AccountButton(screenWidth - padding - accountButtonRadius,
                                      padding + accountButtonRadius, accountButtonRadius, (160, 160, 160), 2, (0, 0, 0))

        self.buttons = [playButton, leaderboardButton, settingsButton, quitButton, accountButton]


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

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class AccountButton():
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

    def is_clicked(self, pos):
        return self.pos.distance_to(pos) < self.radius
