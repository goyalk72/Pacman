import random
from graphics import Point, Circle, color_rgb

from config import TEXT_SIZE, MAP, SCALE, VSCALE, OFFSET, HEIGHT, LENGTH, GOLD_COIN, SILVER_COIN, GOLD_SIZE, SILVER_SIZE


def draw_coins(window, tomStart, jerryStart, tunnels):
    total = 0
    coinObjects = [[(None, 0) for i in range(LENGTH)] for j in range(HEIGHT)]
    for coin in generate_coins():
        x = coin[0]
        y = coin[1]
        if (x,y) == tomStart or (x,y) in jerryStart or (x,y) in tunnels:
            continue
        score = 2 if random.randint(0,20) == 0 else 1
        total += score
        coinObjects[x][y] = (draw_coin(window, x, y, score), score)
    return coinObjects, total

def generate_coins():
    coins = set()
    for j in range(1,HEIGHT-1):
        for i in range(1,LENGTH-1):
            if MAP[j][i] != "#":
                if random.randint(0,3) == 0:
                    coins.add((j,i))
    return coins

def draw_coin(window, x, y, score):
    coinCoord = Point(OFFSET+y*SCALE,OFFSET+x*VSCALE)
    if score == 2:
        coin = Circle(coinCoord, GOLD_SIZE)
        coin.setFill(GOLD_COIN)
    else:
        coin = Circle(coinCoord, SILVER_SIZE)
        coin.setFill(SILVER_COIN)
    coin.draw(window)
    return coin

def destroy_coin(coin):
    coin.undraw()