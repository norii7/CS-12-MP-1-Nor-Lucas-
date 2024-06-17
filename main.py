import pyxel
from dataclasses import dataclass
from random import randint, choice

FPS = 30
HEIGHT = 120
WIDTH = 165
TANK_SIDE = 12
TANK_SPEED = 1
BULLET_SIDE = 2
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
            obstacles(7, 1, 'mirror_se'),

            #water
            obstacles(0, 7, 'water'),
            obstacles(1, 7, 'water'),
            obstacles(2, 7, 'water'),
            obstacles(0, 6, 'water'),
            obstacles(1, 6, 'water'),
            obstacles(2, 6, 'water'),

            #forest
            obstacles(10, 7, 'forest'),
            obstacles(9, 7, 'forest'),
            obstacles(8, 7, 'forest'),
            obstacles(10, 6, 'forest'),
            obstacles(9, 6, 'forest'),
            obstacles(8, 6, 'forest'),
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

        if pyxel.btn(pyxel.KEY_W) and self.mainTank.y - TANK_SPEED >= 0:
            dummyTank = Tank(self.mainTank.x, self.mainTank.y - TANK_SPEED, self.mainTank.facing)

            if True not in [self.are_overlapping(dummyTank, tank) for tank in self.enemyTanks]:
                if True not in [self.are_overlapping(dummyTank, obstacle) for obstacle in self.obstacles]:
                    self.mainTank.facing = 'n'
                    self.mainTank.y -= TANK_SPEED
        elif pyxel.btn(pyxel.KEY_A) and self.mainTank.x - TANK_SPEED >= 0:
            dummyTank = Tank(self.mainTank.x - TANK_SPEED, self.mainTank.y, self.mainTank.facing)
            
            if True not in [self.are_overlapping(dummyTank, tank) for tank in self.enemyTanks]:
                if True not in [self.are_overlapping(dummyTank, obstacle) for obstacle in self.obstacles]:
                    self.mainTank.facing = 'w'
                    self.mainTank.x -= TANK_SPEED
        elif pyxel.btn(pyxel.KEY_S) and self.mainTank.y + TANK_SIDE + TANK_SPEED <= HEIGHT:
            dummyTank = Tank(self.mainTank.x, self.mainTank.y + TANK_SPEED, self.mainTank.facing)
            
            if True not in [self.are_overlapping(dummyTank, tank) for tank in self.enemyTanks]:
                if True not in [self.are_overlapping(dummyTank, obstacle) for obstacle in self.obstacles]:
                    self.mainTank.facing = 's'
                    self.mainTank.y += TANK_SPEED
        elif pyxel.btn(pyxel.KEY_D) and self.mainTank.x + TANK_SIDE + TANK_SPEED <= WIDTH:
            dummyTank = Tank(self.mainTank.x + TANK_SPEED, self.mainTank.y, self.mainTank.facing)
            
            if True not in [self.are_overlapping(dummyTank, tank) for tank in self.enemyTanks]:
                if True not in [self.are_overlapping(dummyTank, obstacle) for obstacle in self.obstacles]:
                    self.mainTank.facing = 'e'
                    self.mainTank.x += TANK_SPEED

        if pyxel.btnp(pyxel.KEY_SPACE, hold=10, repeat=10):
            if not self.bulletList:
                self.bulletList.append(bullet(self.mainTank.x + 4, self.mainTank.y + 4, 'mainTank', self.mainTank.facing))
        
        for bul in self.bulletList:
        
            for tank in self.enemyTanks:
                if self.are_overlapping(bul, tank):
                    self.bulletList.remove(bul)
                    self.enemyTanks.remove(tank)
            
            for obstacle in self.obstacles:
                if self.are_overlapping(bul, obstacle) and len(self.bulletList) != 0:
                    if obstacle.type == 'stone':
                        self.bulletList.remove(bul)
                    if obstacle.type == 'brick':
                        self.bulletList.remove(bul)
                        self.obstacles.remove(obstacle)
                        self.obstacles.append(obstacles(obstacle.x, obstacle.y, 'cracked'))
                    if obstacle.type == 'cracked':
                        self.bulletList.remove(bul)
                        self.obstacles.remove(obstacle)
            
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


    def are_overlapping(self, object1: Tank | bullet | obstacles, object2: Tank | bullet | obstacles) -> bool:
        x1, y1, side1 = object1.x, object1.y, object1.side
        x2, y2, side2 = object2.x, object2.y, object2.side

        # Convert obstacle coordinates into pixels
        if isinstance(object1, obstacles):
            if object1.type == 'forest':
                return False
            x1 = object1.x * object1.side
            y1 = object1.y * object1.side
        if isinstance(object2, obstacles):
            if object2.type == 'forest':
                return False
            x2 = object2.x * object2.side
            y2 = object2.y * object2.side

        # Check if one object is to the left of the other
        if x1 + side1 <= x2 or x2 + side2 <= x1:
            return False
        
        #Check if one object is above the other
        if y1 + side1 <= y2 or y2 + side2 <= y1:
            return False
        
        return True
    
    def draw(self):
        pyxel.cls(0)
        pyxel.load('PYXEL_RESOURCE_FILE.pyxres')
        for tank in self.enemyTanks:
            self.drawEnemyTank(tank.x, tank.y, tank.facing)
        for bul in self.bulletList:
            self.drawBullet(bul.x, bul.y)
        self.drawTank(self.mainTank.x, self.mainTank.y,self.mainTank.facing)
        for obstacle in self.obstacles:
            self.drawObstacle(obstacle.x, obstacle.y, obstacle.type)

    def drawTank(self, x: int, y: int, facing: str):
        if facing == 'n':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=3,
            v=1,
            w=10,
            h=12,
            colkey=0
        )
        elif facing == 'e':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=51,
            v=3,
            w=12,
            h=10,
            colkey=0
        )
        elif facing == 's':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=19,
            v=3,
            w=10,
            h=12,
            colkey=0
        )
        elif facing == 'w':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=33,
            v=3,
            w=12,
            h=10,
            colkey=0
        )
            
    def drawBullet(self, x:int, y:int):
        pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=7,
            v=39,
            w=2,
            h=2,
            colkey=0
        )

    def drawEnemyTank(self, x: int, y: int, facing: str):
        if facing == 'n':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=3,
            v=17,
            w=10,
            h=12,
            colkey=0
        )
        elif facing == 'e':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=51,
            v=19,
            w=12,
            h=10,
            colkey=0
        )
        elif facing == 's':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=19,
            v=19,
            w=10,
            h=12,
            colkey=0
        )
        elif facing == 'w':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=33,
            v=19,
            w=12,
            h=10,
            colkey=0
        )
            
    def drawObstacle(self, x: int, y: int, type: str) -> None:  # x,y are coordinates in game
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
        if type == 'cracked':
            pyxel.blt(
                x=x*OBSTACLE_SIDE,
                y=y*OBSTACLE_SIDE,
                img=0,
                u=0,
                v=80,
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
        if type == 'water':
            pyxel.blt(
                x=x*OBSTACLE_SIDE,
                y=y*OBSTACLE_SIDE,
                img=0,
                u=48,
                v=80,
                w=OBSTACLE_SIDE,
                h=OBSTACLE_SIDE,
                colkey=0
            )
        if type == 'forest':
            pyxel.blt(
                x=x*OBSTACLE_SIDE,
                y=y*OBSTACLE_SIDE,
                img=0,
                u=16,
                v=80,
                w=OBSTACLE_SIDE,
                h=OBSTACLE_SIDE,
                colkey=0
            )
App()

# Level 1 Layout: (Obstacle Coordinates in 'Grid') *Assuming Grid is 10 x 7

# Bricks = [(1, 0), (1, 1), (1, 2), (5, 0), (5, 1), (5, 2), (9, 0), (9, 1), (9, 2)]
# Stones = [(1, 4), (5, 4), (9, 4)]
# Mirrors = [(3, 1), (7, 1)]
# Water = [(0, 8), (1, 8), (2, 8), (0, 7), (1, 7), (2, 7)]
# Forest = [(11, 8), (10, 8), (9, 8), (11, 7), (10, 7), (9, 7)]