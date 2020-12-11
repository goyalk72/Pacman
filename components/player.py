import time
import random
from graphics import Text, Point

from components.coins import destroy_coin
from config import PLAYER_SIZE, TOM, TOM_COLOR, JERRY, JERRY_COLOR, SCALE, VSCALE, MAP, LENGTH, HEIGHT, OFFSET

class Player:

    def __init__(self, window, level):
        self.window = window
        self.level = level
        self.tomPos, self.jerryPos = self.generate_spawn()
        self.spawn_tom()
        self.spawn_jerry()
        self.chase_path = []
        self.tunnels = {}
        self.tunnels = self.tunnel_spawn()
        self.create_tunnel()
        

    def tunnel_spawn(self):
        dict = {}
        l = 0
        while l < self.level:
            X1 = random.randint(1, HEIGHT-2)
            Y1 = random.randint(1, LENGTH-2)

            X2 = random.randint(1, HEIGHT-2)
            Y2 = random.randint(1, LENGTH-2)
            if MAP[X1][Y1] != "#" and (X1,Y1) != self.tomPos and (X1,Y1) not in self.jerryPos and MAP[X2][Y2] != "#" and (X2,Y2) != self.tomPos and (X2,Y2) not in self.jerryPos:
                if self.check_dist((X1,Y1),(X2,Y2)):
                    dict[(X1,Y1)] = (X2,Y2)
                    dict[(X2,Y2)] = (X1,Y1)
                    l += 1     
            else:
                continue
        return dict

    def create_tunnel(self):
        for pos in self.tunnels:
            tunnel = Text(Point(OFFSET+pos[1]*SCALE,OFFSET+pos[0]*VSCALE), "\U0001F6AA")
            tunnel.setTextColor("brown")
            tunnel.setSize(15)
            tunnel.draw(self.window)
    
    def check_dist(self,p1,p2):
        return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 >= 150

    def check_distance(self,pos1,pos2,pos3):
        return self.check_dist(pos1,pos2) and self.check_dist(pos2,pos3) and self.check_dist(pos1,pos3)

    def generate_spawn(self):
        jerries = []
        while True:
            tomX = random.randint(1, HEIGHT-2)
            tomY = random.randint(1, LENGTH-2)
            jerryX1 = random.randint(1, HEIGHT-2)
            jerryY1 = random.randint(1, LENGTH-2)
            if self.level == 1:
                if MAP[tomX][tomY] != "#" and MAP[jerryX1][jerryY1] != "#" and self.check_dist((tomX,tomY),(jerryX1,jerryY1)):
                    return (tomX, tomY), [(jerryX1, jerryY1)]
                else:
                    continue
            if self.level == 2:
                jerryX2 = random.randint(1, HEIGHT-2)
                jerryY2 = random.randint(1, LENGTH-2)

                if MAP[tomX][tomY] != "#" and MAP[jerryX1][jerryY1] != "#" and MAP[jerryX2][jerryY2] != "#" and self.check_distance((tomX,tomY),(jerryX1,jerryY1),(jerryX2,jerryY2)):
                    return (tomX, tomY), [(jerryX2, jerryY2),(jerryX1,jerryY1)]
                else:
                    continue
            if self.level == 3:
                jerryX2 = random.randint(1, HEIGHT-2)
                jerryY2 = random.randint(1, LENGTH-2)
                jerryX3 = random.randint(1, HEIGHT-2)
                jerryY3 = random.randint(1, LENGTH-2)

                if MAP[tomX][tomY] != "#" and MAP[jerryX1][jerryY1] != "#" and MAP[jerryX2][jerryY2] != "#" and MAP[jerryX3][jerryY3] != "#" and self.check_distance((tomX,tomY),(jerryX1,jerryY1),(jerryX3,jerryY3)):
                    return (tomX, tomY), [(jerryX1, jerryY1),(jerryX2,jerryY2),(jerryX3, jerryY3)]
                else:
                    continue


    def spawn_tom(self):
        self.Tom = Text(Point(OFFSET+(self.tomPos[1]*SCALE), OFFSET+(self.tomPos[0]*VSCALE)),TOM)
        self.Tom.setSize(PLAYER_SIZE)
        self.Tom.setTextColor(TOM_COLOR)
        self.Tom.draw(self.window)
    
    def spawn_jerry(self):
        self.Jerry = []
        for jp in self.jerryPos:
            j1 = Text(Point(OFFSET+(jp[1]*SCALE), OFFSET+(jp[0]*VSCALE)),JERRY)
            j1.setSize(PLAYER_SIZE)
            j1.setTextColor(JERRY_COLOR)
            j1.draw(self.window)
            self.Jerry.append(j1)

    def move_is_possible(self, pos, dx, dy):
        if MAP[pos[0]+dx][pos[1]+dy] != "+" and MAP[pos[0]+dx][pos[1]+dy] != "-" and MAP[pos[0]+dx][pos[1]+dy] != "|" and MAP[pos[0]+dx][pos[1]+dy] != "#":
            return True
        return False


    def move_tom_object(self, dx, dy):
        self.Tom.move(dy*SCALE,dx*VSCALE)

    def move_jerry_object(self, dx, dy, ind):
        self.Jerry[ind].move(dy*SCALE,dx*VSCALE)

    def move_tom(self, dx, dy):
        ispos = self.move_is_possible(self.tomPos,dx,dy)
        if ispos:
            self.move_tom_object(dx,dy)
            self.tomPos = (self.tomPos[0]+dx,self.tomPos[1]+dy)
            if self.tomPos in self.tunnels:
                dest = self.tunnels[self.tomPos]
                dx,dy = dest[0] - self.tomPos[0] , dest[1] - self.tomPos[1]
                self.move_tom_object(dx,dy)
                self.tomPos = (self.tomPos[0]+dx,self.tomPos[1]+dy)
            return True
        return False 

    def stepping_over(self,pos,dx,dy):
        if (pos[0]+dx,pos[1]+dy) in self.jerryPos:
            return False
        return True

    def move_random(self, ind):
        moves = [(0,1),(1,0),(-1,0),(0,-1)]
        valid_move = []
        for m in moves:
            if self.move_is_possible(self.jerryPos[ind],m[0],m[1]) and self.stepping_over(self.jerryPos[ind],m[0],m[1]):
                valid_move.append(m)
        x = random.randint(0,len(valid_move)-1)
        dx,dy = valid_move[x]
        self.move_jerry_object(dx,dy,ind)
        self.jerryPos[ind] = (self.jerryPos[ind][0] + dx, self.jerryPos[ind][1] + dy)

    def move_bfs(self, ind):
        chase_path = self.bfs(ind)
        if len(chase_path) > 0:
            dx,dy = chase_path.pop(0)
            if self.move_is_possible(self.jerryPos[ind],dx,dy) and self.stepping_over(self.jerryPos[ind],dx,dy):
                self.move_jerry_object(dx,dy,ind)
                self.jerryPos[ind] = (self.jerryPos[ind][0] + dx, self.jerryPos[ind][1] + dy)

    def move_till_obstacle(self, ind):
        moves = [(0,1),(1,0),(0,-1),(-1,0)]
        for m in moves:
            if self.move_is_possible(self.jerryPos[ind],m[0],m[1]) and self.stepping_over(self.jerryPos[ind],m[0],m[1]):
                dx,dy = m[0],m[1]
                self.move_jerry_object(dx,dy,ind)
                self.jerryPos[ind] = (self.jerryPos[ind][0] + dx, self.jerryPos[ind][1] + dy)
                break
            
    def move_jerry(self):
        self.move_bfs(0)
        if self.level >= 2:
            x = random.randint(0,22)
            if x < 10:
                self.move_bfs(1)
            else:
                self.move_random(1)
                
        if self.level == 3:
            x = random.randint(0,2)
            if x < 2:
                self.move_bfs(2)
            else:
                self.move_till_obstacle(2)

    def print_path(self, parent, start, end):
        path = []
        while end != start:
            p = parent[end]
            path = [(end[0]-p[0],end[1] - p[1])]
            end = p
        return path

    def bfs(self, ind):
        start = self.jerryPos[ind]
        end = self.tomPos
        queue = [start]
        visited = {}
        parent = {}
        while queue:
            curr = queue.pop(0)
            if curr in visited:
                continue
            visited[curr] = True

            if curr == end:
                return self.print_path(parent,start,end)
            
            for mov in [(0,1),(1,0),(0,-1),(-1,0)]:
                ispos = self.move_is_possible(curr,mov[0],mov[1])
                if ispos and (curr[0]+mov[0],curr[1]+mov[1]) not in visited:
                    parent[(curr[0]+mov[0],curr[1]+mov[1])] = curr
                    queue.append((curr[0]+mov[0],curr[1]+mov[1]))