import time
from graphics import GraphWin, update, Text, Point

from components.map import draw_borders, draw_obstacles
from components.coins import draw_coins, destroy_coin
from components.player import Player
from components.draw import draw_head, draw_bot, update_score, spawn_score, draw_middle

from config import GOLD_COIN, SILVER_COIN, HEIGHT, LENGTH, OFFSET, SCALE, VSCALE, TITLE, START, END, SCOREOFFSET, JERRY_WEIGHT_EASY, JERRY_WEIGHT_MEDIUM, JERRY_WEIGHT_HARD, PLAYER_SPEED, WIN

WindowHeight = OFFSET + HEIGHT*VSCALE + OFFSET
WindowLength = OFFSET + LENGTH*SCALE + OFFSET + SCOREOFFSET

PauseY = OFFSET*12
PauseX = OFFSET + LENGTH*SCALE + OFFSET + SCOREOFFSET//2

class Game:

    def __init__(self):
        self.window = GraphWin(TITLE, WindowLength, WindowHeight, autoflush = False)
        self.window.setBackground('black')
        self.Players = None
        self.score = 0
        self.coins = []
        self.best = 0
        self.PauseObj = Text(Point(PauseX, PauseY), "Press p to pause!")
        self.PauseObj.setTextColor('red')

    def generate_coins(self):
        tomStart, jerryStart = self.Players.tomPos, self.Players.jerryPos
        self.coins, self.total = draw_coins(self.window, tomStart, jerryStart, self.Players.tunnels)
    
    def initiate_score(self):
        self.scoreObj, self.bestObj = spawn_score(self.window)

    def update_score_and_coins(self):
        obj,sc = self.coins[self.Players.tomPos[0]][self.Players.tomPos[1]]
        if obj:
            self.score += sc
            update_score(self.score, self.scoreObj)
            self.coins[self.Players.tomPos[0]][self.Players.tomPos[1]] = (None,0)
            destroy_coin(obj)

    def draw_map(self):
        draw_borders(self.window)
        self.obstacles = draw_obstacles(self.window)
    
    def clear(self):
        self.window.autoflush = False
        for item in self.window.items[:]:
            item.undraw()
        update()
        self.window.autoflush = True
    
    def check_win_loss(self):
        if self.Players.tomPos in self.Players.jerryPos:
            self.game_over()
            return True
        if self.score == self.total:
            self.game_win()
            return True
    
    def pause(self):
        self.PauseObj.setText("Game Paused!")
        while(self.window.checkKey() != "p"):
            continue
        self.PauseObj.setText("Press p to pause.")
    
    def gameLoop(self, weight):
        i = 0
        while not self.check_win_loss():
            key = self.window.checkKey()
            if key == "w":
                if self.Players.move_tom(-1,0):
                    self.update_score_and_coins()
            elif key == "s":
                if self.Players.move_tom(1,0):
                    self.update_score_and_coins()
            elif key == "a":
                if self.Players.move_tom(0,-1):
                    self.update_score_and_coins()
            elif key == "d":
                if self.Players.move_tom(0,1):
                    self.update_score_and_coins()
            elif key == "p":
                self.pause()
            elif key == "e":
                self.game_over()
                break
            if i == weight:
                i = 0
            if i == 0:
                self.Players.move_jerry()
            i += 1
            update(PLAYER_SPEED)
    
    def choose_difficulty(self):
        self.clear()
        key = None
        draw_bot(gameInstance.window, 'green', "Press 1 for difficulty level easy!\n\nPress 2 for difficulty level medium!\n\nPress 3 for difficulty level hard")
        while not key:
            key = self.window.checkKey()
        if key == "1":
            self.start_easy()
        elif key == "2":
            self.start_medium()
        elif key == "3":
            self.start_hard()
        else:
            self.start_medium()
    
    def start_easy(self):
        self.clear()
        self.scoreObj, self.bestObj = spawn_score(self.window)
        update_score(self.best, self.bestObj)
        self.PauseObj.draw(self.window)
        self.Players = Player(self.window, 1)
        self.draw_map()
        self.generate_coins()
        self.gameLoop(JERRY_WEIGHT_EASY)
    
    def start_medium(self):
        self.clear()
        self.scoreObj, self.bestObj = spawn_score(self.window)
        update_score(self.best, self.bestObj)
        self.PauseObj.draw(self.window)
        self.Players = Player(self.window, 2)
        self.draw_map()
        self.generate_coins()
        self.gameLoop(JERRY_WEIGHT_MEDIUM)

    def start_hard(self):
        self.clear()
        self.scoreObj, self.bestObj = spawn_score(self.window)
        update_score(self.best, self.bestObj)
        self.PauseObj.draw(self.window)
        self.Players = Player(self.window, 3)
        self.draw_map()
        self.generate_coins()
        self.gameLoop(JERRY_WEIGHT_HARD)
    
    def show_help(self):
        self.clear()
        draw_middle(self.window, 'blue', "'E' is the player who has to collect all coins.", -2)
        draw_middle(self.window, 'red', "'J' is the bot who will chase you to catch you.", -1)
        draw_middle(self.window, GOLD_COIN, "Golden coin is worth 2 points", 0)
        draw_middle(self.window, SILVER_COIN, "Silver coin is worth 1 points", 1)
        draw_middle(self.window, 'brown', "'\U0001F6AA' represents tunnel through which you can teleport to a corresponding tunnel", 2)
        draw_middle(self.window, 'green', "'#' represents obstacles which player or bot cannot pass", 3)
        draw_middle(self.window, 'green', "Press any key to continue!", 5)
        
        key = None
        while not key:
            key = self.window.checkKey()
        
        self.play()

    def play(self):
        key = None
        self.clear()
        draw_head(self.window, 'green', START)
        draw_bot(gameInstance.window, 'green', "Press h for help.\n\nPress any other key to start!")
        
        while not key:
            key = self.window.checkKey()
        
        if key == "h":
            self.show_help()
        else:
            self.choose_difficulty()
    
    def game_over(self):
        self.clear()
        key = None
        if self.score > self.best:
            self.best = self.score
        self.score = 0
        draw_head(gameInstance.window, 'red', END)
        draw_bot(gameInstance.window, 'white', "Your Final Score: "+str(self.best)+"\n\n Press e to exit."+ "\n\n Press any other key to play again!")
        while not key:
            key = gameInstance.window.checkKey()
        if key != "e":
            self.play()

    
    def game_win(self):
        self.clear()
        key = None
        if self.score > self.best:
            self.best = self.score
        self.score = 0
        draw_head(gameInstance.window, 'green', WIN)
        draw_bot(gameInstance.window, 'white', "Your Final Score: "+str(self.best)+"\n\n Press e to exit."+ "\n\n Press any other key to play again!")
        while not key:
            key = gameInstance.window.checkKey()
        if key != "e":
            self.play()
    
    def exit(self):
        self.window.close()
    


gameInstance = Game()
gameInstance.play()
gameInstance.exit()
