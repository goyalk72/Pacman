from graphics import Text, Point, Circle, color_rgb
from config import HEIGHT, LENGTH, SCALE, VSCALE, OFFSET, TEXT_SIZE, BORDER_COLOR, MAP

def draw_borders(window):

    for i in range(1, LENGTH-1):
        borderTop = Text(Point(OFFSET+i*SCALE, OFFSET), "-")
        borderTop.setTextColor(BORDER_COLOR)
        borderTop.setSize(TEXT_SIZE)
        borderTop.draw(window)
        borderBot = Text(Point(OFFSET+i*SCALE, OFFSET+(HEIGHT-1)*VSCALE), "-")
        borderBot.setTextColor(BORDER_COLOR)
        borderBot.setSize(TEXT_SIZE)
        borderBot.draw(window)

    for i in range(1, HEIGHT-1):
        borderLeft = Text(Point(OFFSET, OFFSET+i*VSCALE), "|")
        borderLeft.setTextColor(BORDER_COLOR)
        borderLeft.setSize(TEXT_SIZE)
        borderLeft.draw(window)
        borderRight = Text(Point(OFFSET+(LENGTH-1)*SCALE, OFFSET+i*VSCALE), "|")
        borderRight.setTextColor(BORDER_COLOR)
        borderRight.setSize(TEXT_SIZE)
        borderRight.draw(window)
    
    topLeft = Text(Point(OFFSET, OFFSET), "+")
    topLeft.setTextColor(BORDER_COLOR)
    topLeft.setSize(TEXT_SIZE)
    topLeft.draw(window)

    topRight = Text(Point(OFFSET+(LENGTH-1)*SCALE, OFFSET), "+")
    topRight.setTextColor(BORDER_COLOR)
    topRight.setSize(TEXT_SIZE)
    topRight.draw(window)

    botLeft = Text(Point(OFFSET, OFFSET+(HEIGHT-1)*VSCALE), "+")
    botLeft.setTextColor(BORDER_COLOR)
    botLeft.setSize(TEXT_SIZE)
    botLeft.draw(window)

    botRight = Text(Point(OFFSET+(LENGTH-1)*SCALE, OFFSET+(HEIGHT-1)*VSCALE), "+")
    botRight.setTextColor(BORDER_COLOR)
    botRight.setSize(TEXT_SIZE)
    botRight.draw(window)


def draw_obstacles(window):
    obstacles = set()
    for j in range(HEIGHT):
        for i in range(LENGTH):
            if MAP[j][i] == "#":
                obstacles.add((i,j))
                obstacle = Text(Point(OFFSET+i*SCALE,OFFSET+j*VSCALE), "#")
                obstacle.setTextColor(BORDER_COLOR)
                obstacle.setSize(TEXT_SIZE)
                obstacle.draw(window)
    return obstacles

