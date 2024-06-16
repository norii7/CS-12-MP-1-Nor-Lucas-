import pyxel
from dataclasses import dataclass
from random import randint, choice

FPS = 30
HEIGHT = 120
WIDTH = 165
TANK_SIDE = 15
TANK_SPEED = 3
BULLET_SIDE = 15
BULLET_SPEED = 5
MAX_ENEMY_TANKS = 3
OBSTACLE_SIDE = 15

@dataclass
class Tank:
    x: int
    y: int
    facing: str
    side: int = TANK_SIDE

@dataclass
class mainTank(Tank):
    score: int = 0

@dataclass
class bullet:
    x: int
    y: int
    shooter: str
    direction: str
    side: int = BULLET_SIDE

@dataclass
class obstacles:
    x: int
    y: int
    type: str
    side: int = OBSTACLE_SIDE

class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, fps=FPS)
        self.x = 0
        self.mainTank = mainTank(0, 0, 'n', 0)
        self.bulletList: list[bullet] = []
        self.enemyTanks: list[Tank] = []
        
        level1_obstacles: list[obstacles] = [
            #bricks
            obstacles(1, 0, 'brick'),
            obstacles(1, 1, 'brick'),
            obstacles(1, 2, 'brick'),
            obstacles(5, 0, 'brick'),
            obstacles(5, 1, 'brick'),
            obstacles(5, 2, 'brick'),
            obstacles(9, 0, 'brick'),
            obstacles(9, 1, 'brick'),
            obstacles(9, 2, 'brick'),

            #stones
            obstacles(1, 4, 'stone'),
            obstacles(5, 4, 'stone'),
            obstacles(9, 4, 'stone'),

            #mirrors
            obstacles(3, 1, 'mirror_ne'),
            obstacles(7, 1, 'mirror_se')
            ]
        
        self.obstacles: list[obstacles] = level1_obstacles

        '''
        for _ in range(MAX_ENEMY_TANKS):
            rand_x = randint(0, WIDTH - TANK_SIDE)
            rand_y = randint(0, HEIGHT - TANK_SIDE)
            rand_tank = Tank(rand_x + 4, rand_y + 4, choice(['n', 's', 'e', 'w']))

            while True in [self.are_overlapping(rand_tank, tank) for tank in self.enemyTanks + [self.mainTank]]:
                rand_x = randint(TANK_SIDE, WIDTH - TANK_SIDE)
                rand_y = randint(TANK_SIDE, HEIGHT - TANK_SIDE)
                rand_tank = Tank(rand_x, rand_y, choice(['n', 's', 'e', 'w']))
            
            self.enemyTanks.append(rand_tank)
        '''

        pyxel.run(self.update, self.draw)

    def update(self):
        self.x = (self.x + 1) % pyxel.width

        overlap_allowance = 4
        if pyxel.btn(pyxel.KEY_W) and self.mainTank.y - TANK_SPEED >= 0:
            dummyTank = Tank(self.mainTank.x, self.mainTank.y - TANK_SPEED - overlap_allowance, self.mainTank.facing)

            if True not in [self.are_overlapping(dummyTank, tank) for tank in self.enemyTanks]:
                self.mainTank.facing = 'n'
                self.mainTank.y -= TANK_SPEED
        elif pyxel.btn(pyxel.KEY_A) and self.mainTank.x - TANK_SPEED >= 0:
            dummyTank = Tank(self.mainTank.x - TANK_SPEED - overlap_allowance, self.mainTank.y, self.mainTank.facing)
            
            if True not in [self.are_overlapping(dummyTank, tank) for tank in self.enemyTanks]:
                self.mainTank.facing = 'w'
                self.mainTank.x -= TANK_SPEED
        elif pyxel.btn(pyxel.KEY_S) and self.mainTank.y + TANK_SIDE + TANK_SPEED <= HEIGHT:
            dummyTank = Tank(self.mainTank.x, self.mainTank.y + TANK_SPEED + overlap_allowance, self.mainTank.facing)
            
            if True not in [self.are_overlapping(dummyTank, tank) for tank in self.enemyTanks]:
                self.mainTank.facing = 's'
                self.mainTank.y += TANK_SPEED
        elif pyxel.btn(pyxel.KEY_D) and self.mainTank.x + TANK_SIDE + TANK_SPEED <= WIDTH:
            dummyTank = Tank(self.mainTank.x + TANK_SPEED + overlap_allowance, self.mainTank.y, self.mainTank.facing)
            
            if True not in [self.are_overlapping(dummyTank, tank) for tank in self.enemyTanks]:
                self.mainTank.facing = 'e'
                self.mainTank.x += TANK_SPEED

        if pyxel.btnp(pyxel.KEY_SPACE, hold=10, repeat=10):
            self.bulletList.append(bullet(self.mainTank.x, self.mainTank.y, 'mainTank', self.mainTank.facing))
        
        for bul in self.bulletList:
            if bul.direction == 'n' and bul.y + BULLET_SIDE - BULLET_SPEED >= 0:
                bul.y -= BULLET_SPEED
            elif bul.direction == 'e' and bul.x + BULLET_SPEED <= WIDTH:
                bul.x +=  BULLET_SPEED
            elif bul.direction == 's' and bul.y + BULLET_SPEED <= HEIGHT:
                bul.y += BULLET_SPEED
            elif bul.direction == 'w' and bul.x + BULLET_SIDE - BULLET_SPEED >= 0:
                bul.x -= BULLET_SPEED
            else:
                self.bulletList.remove(bul)

            for tank in self.enemyTanks:
                if self.are_overlapping(bul, tank):
                    self.bulletList.remove(bul)
                    self.enemyTanks.remove(tank)


    def are_overlapping(self, object1: Tank | bullet | obstacles, object2: Tank | bullet | obstacles) -> bool:
        x1, y1, side1 = object1.x, object1.y, object1.side
        x2, y2, side2 = object2.x, object2.y, object2.side

        if x2 <= x1 + (side1/2) <= x2 + side2 and y2 <= y1 + (side1/2) <= y2 + side2:
            return True
        
        return False
    
    def draw(self):
        pyxel.cls(0)
        pyxel.load('PYXEL_RESOURCE_FILE.pyxres')
        #for tank in self.enemyTanks:
        #    self.drawEnemyTank(tank.x, tank.y, tank.facing)
        for bul in self.bulletList:
            self.drawBullet(bul.x, bul.y)
        for obstacle in self.obstacles:
            self.drawObsatacle(obstacle.x, obstacle.y, obstacle.type)
        self.drawTank(self.mainTank.x, self.mainTank.y,self.mainTank.facing)

    def drawTank(self, x: int, y: int, facing: str):
        if facing == 'n':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=0,
            v=0,
            w=TANK_SIDE,
            h=TANK_SIDE,
            colkey=0
        )
        elif facing == 'e':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=48,
            v=0,
            w=TANK_SIDE,
            h=TANK_SIDE,
            colkey=0
        )
        elif facing == 's':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=16,
            v=0,
            w=TANK_SIDE,
            h=TANK_SIDE,
            colkey=0
        )
        elif facing == 'w':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=32,
            v=0,
            w=TANK_SIDE,
            h=TANK_SIDE,
            colkey=0
        )
            
    def drawBullet(self, x:int, y:int):
        pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=0,
            v=32,
            w=BULLET_SIDE,
            h=BULLET_SIDE,
            colkey=0
        )

    def drawEnemyTank(self, x: int, y: int, facing: str):
        if facing == 'n':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=0,
            v=16,
            w=BULLET_SIDE,
            h=BULLET_SIDE,
            colkey=0
        )
        elif facing == 'e':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=48,
            v=16,
            w=BULLET_SIDE,
            h=BULLET_SIDE,
            colkey=0
        )
        elif facing == 's':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=16,
            v=16,
            w=BULLET_SIDE,
            h=BULLET_SIDE,
            colkey=0
        )
        elif facing == 'w':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=32,
            v=16,
            w=BULLET_SIDE,
            h=BULLET_SIDE,
            colkey=0
        )
            
    def drawObsatacle(self, x: int, y: int, type: str) -> None:  # x,y are coordinates in game
        if type == 'brick':
            pyxel.blt(
                x=x*OBSTACLE_SIDE,
                y=y*OBSTACLE_SIDE,
                img=0,
                u=0,
                v=64,
                w=OBSTACLE_SIDE,
                h=OBSTACLE_SIDE,
                colkey=0
            )
        if type == 'stone':
            pyxel.blt(
                x=x*OBSTACLE_SIDE,
                y=y*OBSTACLE_SIDE,
                img=0,
                u=16,
                v=64,
                w=OBSTACLE_SIDE,
                h=OBSTACLE_SIDE,
                colkey=0
            )
        if type == 'mirror_ne':
            pyxel.blt(
                x=x*OBSTACLE_SIDE,
                y=y*OBSTACLE_SIDE,
                img=0,
                u=32,
                v=64,
                w=OBSTACLE_SIDE,
                h=OBSTACLE_SIDE,
                colkey=0
            )
        if type == 'mirror_se':
            pyxel.blt(
                x=x*OBSTACLE_SIDE,
                y=y*OBSTACLE_SIDE,
                img=0,
                u=48,
                v=64,
                w=OBSTACLE_SIDE,
                h=OBSTACLE_SIDE,
                colkey=0
            )
App()

# Level 1 Layout: (Obstacle Coordinates in 'Grid') *Assuming Grid is 11 x 8

#Bricks = [(1, 0), (1, 1), (1, 2), (5, 0), (5, 1), (5, 2), (9, 0), (9, 1), (9, 2)]
#Stones = [(1, 4), (5, 4), (9, 4)]
#Mirrors = [(3, 1), (7, 1)]