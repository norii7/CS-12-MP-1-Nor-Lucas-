import pyxel
from dataclasses import dataclass
from random import randint, choice

FPS = 30
HEIGHT = 120
WIDTH = 160
TANK_SIDE = 15
TANK_SPEED = 3
BULLET_SIDE = 15
BULLET_SPEED = 5
MAX_ENEMY_TANKS = 3

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

class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, fps=FPS)
        self.x = 0
        self.mainTank = mainTank(0, 0, 'n', 0)
        self.bulletList: list[bullet] = []
        self.enemyTanks: list[Tank] = []

        for _ in range(MAX_ENEMY_TANKS):
            rand_x = randint(0, WIDTH - TANK_SIDE)
            rand_y = randint(0, HEIGHT - TANK_SIDE)
            rand_tank = Tank(rand_x + 4, rand_y + 4, choice(['n', 's', 'e', 'w']))

            while True in [self.are_overlapping(rand_tank, tank) for tank in self.enemyTanks + [self.mainTank]]:
                rand_x = randint(TANK_SIDE, WIDTH - TANK_SIDE)
                rand_y = randint(TANK_SIDE, HEIGHT - TANK_SIDE)
                rand_tank = Tank(rand_x, rand_y, choice(['n', 's', 'e', 'w']))
            
            self.enemyTanks.append(rand_tank)

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

    def are_overlapping(self, object1: Tank | bullet, object2: Tank | bullet) -> bool:
        x1, y1, side1 = object1.x, object1.y, object1.side
        x2, y2, side2 = object2.x, object2.y, object2.side

        if x2 <= x1 + (side1/2) <= x2 + side2 and y2 <= y1 + (side1/2) <= y2 + side2:
            return True
        
        return False
    
    def draw(self):
        pyxel.cls(0)
        pyxel.load('PYXEL_RESOURCE_FILE.pyxres')
        for tank in self.enemyTanks:
            self.drawEnemyTank(tank.x, tank.y, tank.facing)
        for bul in self.bulletList:
            self.drawBullet(bul.x, bul.y)
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

App()