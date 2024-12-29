import pygame
from pygame.locals import *
from random import randint

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.gridSize = 20
        self.cellSize = 20
        self.width = self.gridSize * self.cellSize
        self.height = self.gridSize * self.cellSize + 40  
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")
        self.BG_COLOR = (0, 0, 0)
        self.SNAKE_COLOR = (0, 255, 0)
        self.FOOD_COLOR = (255, 0, 0)
        self.PANEL_COLOR = (50, 50, 50)
        self.TEXT_COLOR = (255, 255, 255)
        self.font = pygame.font.SysFont("Arial", 20)
        self.large_font = pygame.font.SysFont("Arial", 40)
        self.snake_body = []
        self.food_position = None
        self.snake_direction = "RIGHT"
        self.running = True
        self.startSnake()
        self.placeFood()
        self.timer = 30  # Timer

    def startSnake(self):
        self.snake_body = [[5, 5]]

    def placeFood(self):
        while True:
            food_row = randint(0, self.gridSize - 1)
            food_column = randint(0, self.gridSize - 1)
            if [food_row, food_column] not in self.snake_body:
                self.food_position = [food_row, food_column]
                break

    def moveSnake(self):
        head_row, head_column = self.snake_body[-1]

        if self.snake_direction == "UP":
            new_row, new_column = head_row - 1, head_column
        elif self.snake_direction == "DOWN":
            new_row, new_column = head_row + 1, head_column
        elif self.snake_direction == "LEFT":
            new_row, new_column = head_row, head_column - 1
        elif self.snake_direction == "RIGHT":
            new_row, new_column = head_row, head_column + 1
        else:
            return

        if (
            new_row < 0 or new_row >= self.gridSize or
            new_column < 0 or new_column >= self.gridSize
        ):
            self.running = False
            self.displayEndMessage("You hit the wall!")
            return

        if [new_row, new_column] in self.snake_body:
            self.running = False
            self.displayEndMessage("You ran into yourself!")
            return

        self.snake_body.append([new_row, new_column])

        if [new_row, new_column] == self.food_position:
            self.placeFood()
        else:
            self.snake_body.pop(0)

    def drawGrid(self):
        self.screen.fill(self.BG_COLOR)
        for segment in self.snake_body:
            pygame.draw.rect(
                self.screen,
                self.SNAKE_COLOR,
                pygame.Rect(
                    segment[1] * self.cellSize,
                    segment[0] * self.cellSize,
                    self.cellSize,
                    self.cellSize,
                ),
            )
        pygame.draw.rect(
            self.screen,
            self.FOOD_COLOR,
            pygame.Rect(
                self.food_position[1] * self.cellSize,
                self.food_position[0] * self.cellSize,
                self.cellSize,
                self.cellSize,
            ),
        )

    def drawPanel(self, elapsed_time):
        pygame.draw.rect(
            self.screen,
            self.PANEL_COLOR,
            pygame.Rect(0, self.gridSize * self.cellSize, self.width, 40),
        )
        time_text = self.font.render(f"Time: {elapsed_time:.1f}s", True, self.TEXT_COLOR)
        self.screen.blit(time_text, (10, self.gridSize * self.cellSize + 10))

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_UP and self.snake_direction != "DOWN":
                    self.snake_direction = "UP"
                elif event.key == K_DOWN and self.snake_direction != "UP":
                    self.snake_direction = "DOWN"
                elif event.key == K_LEFT and self.snake_direction != "RIGHT":
                    self.snake_direction = "LEFT"
                elif event.key == K_RIGHT and self.snake_direction != "LEFT":
                    self.snake_direction = "RIGHT"

    def displayEndMessage(self, message):
        self.screen.fill(self.BG_COLOR)
        end_message = self.large_font.render(message, True, self.TEXT_COLOR)
        sub_message = self.font.render("Press any key to exit.", True, self.TEXT_COLOR)
        self.screen.blit(
            end_message,
            (self.width // 2 - end_message.get_width() // 2, self.height // 2 - 50),
        )
        self.screen.blit(
            sub_message,
            (self.width // 2 - sub_message.get_width() // 2, self.height // 2 + 10),
        )
        pygame.display.flip()
        self.waitForExit()

    def waitForExit(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or event.type == KEYDOWN:
                    pygame.quit()
                    return

    def gameLoop(self):
        clock = pygame.time.Clock()
        start_ticks = pygame.time.get_ticks()
        while self.running:
            self.handleEvents()
            self.moveSnake()
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
            if elapsed_time >= self.timer:
                self.running = False
                self.displayEndMessage("You Won!")
                return

            self.drawGrid()
            self.drawPanel(elapsed_time)
            pygame.display.flip()
            clock.tick(5)
        pygame.quit()

if __name__ == "__main__":
    game = SnakeGame()
    game.gameLoop()
