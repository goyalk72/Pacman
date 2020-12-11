from graphics import Point, Text

from config import SCALE, VSCALE, TEXT_SIZE, OFFSET, BORDER_COLOR, LENGTH, SCOREOFFSET


def draw_head(window, color, ITEM):
    WIDTH = window.getWidth()
    HEIGHT = window.getHeight()
    CENTERX = WIDTH//2
    CENTERY = HEIGHT//2
    for j in range(len(ITEM)):
        for i in range(len(ITEM[0])):
            t = Text(Point(CENTERX + (i-(len(ITEM[0]))/2)*SCALE/1.3, CENTERY+(j-len(ITEM))*VSCALE/1.3), ITEM[j][i])
            t.setSize(TEXT_SIZE)
            t.setTextColor(color)
            t.draw(window)


def draw_bot(window, color, text):
    WIDTH = window.getWidth()
    HEIGHT = window.getHeight()
    CENTERX = WIDTH//2
    CENTERY = HEIGHT//2 + OFFSET*4

    botText = Text(Point(CENTERX, CENTERY), text)
    botText.setTextColor(color)
    botText.setSize(TEXT_SIZE)
    botText.draw(window)

def draw_middle(window, color, text, offset):
    WIDTH = window.getWidth()
    HEIGHT = window.getHeight()
    CENTERX = WIDTH//2
    CENTERY = HEIGHT//2 + offset*OFFSET*2

    midText = Text(Point(CENTERX, CENTERY), text)
    midText.setTextColor(color)
    midText.setSize(TEXT_SIZE)
    midText.draw(window)

def spawn_score(window):
    x = OFFSET + LENGTH*SCALE + OFFSET + SCOREOFFSET//2
    y = OFFSET *4
    scoreText = Text(Point(x, y), "Current Score")
    scoreText.setSize(TEXT_SIZE)
    scoreText.setTextColor('green')
    scoreText.draw(window)
    y += OFFSET*2
    scoreObj = Text(Point(x, y), "0")
    scoreObj.setSize(TEXT_SIZE)
    scoreObj.setTextColor('green')
    scoreObj.draw(window)
    y += OFFSET*2
    bestText = Text(Point(x, y), "Best Score")
    bestText.setSize(TEXT_SIZE)
    bestText.setTextColor('blue')
    bestText.draw(window)
    y += OFFSET*2
    bestObj = Text(Point(x, y), "0")
    bestObj.setSize(TEXT_SIZE)
    bestObj.setTextColor('blue')
    bestObj.draw(window)
    return scoreObj, bestObj

def update_score(score, scoreOBJ):
    scoreOBJ.setText(str(score))
