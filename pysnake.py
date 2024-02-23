import pygame
import time
import random
from pygame.display import get_surface
from enum import Enum

class Dir(Enum):
    UP=0,
    DOWN=1,
    LEFT=2,
    RIGHT=3,
    NONE=4

config = {
    "background_color" : "lightgoldenrodyellow",
    "ui_color" : "darkseagreen4",
    "snake_color" : "seagreen3",
    "apple_color" : "salmon2",
    "block_padding" : 2,
    "window_width": 400,
    "window_height": 500,
    "field_width": 400,
    "field_height": 400,
    "fps_cap": 60,
    "grid_rows" : 14,
    "grid_cols" : 14,
    "game_speed": 2.5,
    "speed_modifier": 0.5,
    "score" : 0,
    "snake_length" : 1,
    "snake_head" : [],
    "snake_tail" : [],
    "snake_dir" : Dir.UP,
    }

def grid_screen_y(row_num: int, total_rows: int, height: int) -> float:
    return (row_num/total_rows * height)

def grid_screen_x(col_num: int, total_cols: int, width: int) -> float:
    return (col_num/total_cols * width)

#This draws a 'block' for every list item that equals 1
def drawSnakeBlocks(grid: list[list], surface: pygame.Surface):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            val = grid[row][col]
            if (val == 1):
                padding = config['block_padding']
                snake_rect = pygame.Rect(
                        padding + grid_screen_x(col, config['grid_cols'], config['field_width']) + config['window_width'] - config['field_width'],
                        padding + grid_screen_y(row, config['grid_rows'], config['field_height']) + config['window_height'] - config['field_height'],
                         config['field_width']/config['grid_cols'] - padding,
                         config['field_height']/config['grid_rows'] - padding)

                pygame.draw.rect(surface, config['snake_color'], snake_rect)
            elif (val == 2):
                padding = config['block_padding']
                apple_rect = pygame.Rect(
                        padding + grid_screen_x(col, config['grid_cols'], config['field_width']) + config['window_width'] - config['field_width'],
                        padding + grid_screen_y(row, config['grid_rows'], config['field_height']) + config['window_height'] - config['field_height'],
                         config['field_width']/config['grid_cols'] - padding,
                         config['field_height']/config['grid_rows'] - padding)

                pygame.draw.rect(surface, config['apple_color'], apple_rect)

def checkForFood(grid: list[list], pos: list) -> bool:
    if grid[pos[0]][pos[1]] == 2:
        config["score"] += 1
        config["game_speed"] += config["speed_modifier"]
        addFood(grid, pos[1], pos[0])
        return True
    return False

def addFood(grid: list[list], excludeX: int, excludeY: int):
    xVal = random.randrange(len(grid[0]))
    yVal = random.randrange(len(grid))

    while grid[yVal][xVal] != 0 and (xVal == excludeX or yVal == excludeY):
        xVal = random.randrange(len(grid[0]))
        yVal = random.randrange(len(grid))

    grid[yVal][xVal] = 2

def updateSnakePosition(grid: list[list]):
    snake_head = config["snake_head"]
    snake_tail = config["snake_tail"]
    snake_length = config["snake_length"]
    snake_dir = config["snake_dir"]
    if snake_dir == Dir.UP:
        if (snake_head[1] - 1 < 0):
            config["snake_dir"] = Dir.NONE
            print("snake dead :(")
        else:
            checkForFood(grid, [snake_head[0]-1, snake_head[1]])

            grid[snake_head[0]-1][snake_head[1]] = 1
            grid[snake_head[0]][snake_head[1]] = 0
            snake_head[0] -= 1
    elif snake_dir == Dir.DOWN:
        if (snake_head[1] + 1 >= len(grid)):
            config["snake_dir"] = Dir.NONE
            print("snake dead :(")
        else:
            checkForFood(grid, [snake_head[0]+1, snake_head[1]])
            grid[snake_head[0]+1][snake_head[1]] = 1
            grid[snake_head[0]][snake_head[1]] = 0
            snake_head[0] += 1
    elif snake_dir == Dir.LEFT:
        if (snake_head[0] - 1 < 0):
            config["snake_dir"] = Dir.NONE
            print("snake dead :(")
        else:
            checkForFood(grid, [snake_head[0], snake_head[1]-1])
            grid[snake_head[0]][snake_head[1]-1] = 1
            grid[snake_head[0]][snake_head[1]] = 0
            snake_head[1] -= 1
    elif snake_dir == Dir.RIGHT:
        if (snake_head[1] + 1 >= len(grid)):
            config["snake_dir"] = Dir.NONE
            print("snake dead :(")
        else:
            checkForFood(grid, [snake_head[0], snake_head[1]+1])
            grid[snake_head[0]][snake_head[1]+1] = 1
            grid[snake_head[0]][snake_head[1]] = 0
            snake_head[1] += 1
    elif snake_dir == Dir.NONE:
            pass

    config["snake_head"] = snake_head


def main():
    #pygame setup
    pygame.init()

    screen = pygame.display.set_mode((config["window_width"], config["window_height"]))
    clock = pygame.time.Clock()
    running = True

    grid_rows = config["grid_rows"]
    grid_cols = config["grid_cols"]

    grid = [[0 for x in range(grid_cols)] for y in range(grid_rows)]
    grid[int(grid_rows/2)][int(grid_cols/2)] = 1
    config["snake_head"] = [int(grid_rows/2), int(grid_cols/2)]
    config["snake_tail"] = [int(grid_rows/2), int(grid_cols/2)]
    addFood(grid, int(grid_cols/2), int(grid_rows/2))

    font = pygame.font.Font('freesansbold.ttf', 22)

    lastMs = time.time() * 1000

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and config['snake_dir'] is not Dir.NONE:
                currdir = config["snake_dir"]
                if (event.key == pygame.K_w or event.key == pygame.K_UP) and currdir is not Dir.DOWN:

                    config['snake_dir'] = Dir.UP
                elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and currdir is not Dir.RIGHT:
                    config['snake_dir'] = Dir.LEFT
                elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and currdir is not Dir.UP:
                    config['snake_dir'] = Dir.DOWN
                elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and currdir is not Dir.LEFT:
                    config['snake_dir'] = Dir.RIGHT

        #fill screen with a color to wipe anything from last frame
        screen.fill(config["background_color"])

        # RUN UPDATES
        if((time.time()*1000)-lastMs >= 1000/config["game_speed"]):
            lastMs = time.time() * 1000
            updateSnakePosition(grid)

        # RENDER GAME HERE

        line_x1 = 0
        line_x2 = config['window_width']
        line_y1 = config['window_height'] - config['field_height']
        line_y2 = config['window_height'] - config['field_height']
        pygame.draw.line(get_surface(), config['ui_color'], (line_x1, line_y1), (line_x2, line_y2))

        score_text = font.render("Score: " + str(config['score']), True, config['ui_color'], config['background_color'])
        text_rect = score_text.get_rect()
        get_surface().blit(score_text, text_rect)

        drawSnakeBlocks(grid, get_surface())

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(config["fps_cap"])

    pygame.quit()

if __name__ == "__main__":
    main()
