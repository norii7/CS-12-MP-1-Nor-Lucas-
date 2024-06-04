import pyxel
from dataclasses import dataclass
from random import randint, choice

@dataclass
class mainTank:
    x: int
    y: int
    facing: str

@dataclass
class bullet:
    x: int
    y: int
    shooter: str
    direction: str

@dataclass
class enemyTank:
    x: int
    y: int
    facing: str


class App:
    def __init__(self):
        pyxel.init(160, 120)
        self.x = 0
        self.mainTank = mainTank(0, 0, 'n')
        self.bulletList: list[bullet] = []
        self.enemyTanks: list[enemyTank] = []

        for _ in range(3):
            self.enemyTanks.append(enemyTank(randint(15, 145), randint(15, 105), choice(['n', 's', 'e', 'w'])))

        pyxel.run(self.update, self.draw)

    def update(self):
        self.x = (self.x + 1) % pyxel.width
        if pyxel.btn(pyxel.KEY_W) and self.mainTank.y >= 5:
            self.mainTank.facing = 'n'
            self.mainTank.y -= 3
        elif pyxel.btn(pyxel.KEY_A) and self.mainTank.x > 0:
            self.mainTank.facing = 'w'
            self.mainTank.x -= 3
        elif pyxel.btn(pyxel.KEY_S) and self.mainTank.y < 105:
            self.mainTank.facing = 's'
            self.mainTank.y += 3
        elif pyxel.btn(pyxel.KEY_D) and self.mainTank.x < 145:
            self.mainTank.facing = 'e'
            self.mainTank.x += 3

        if pyxel.btnp(pyxel.KEY_SPACE, hold=10, repeat=10):
            self.bulletList.append(bullet(self.mainTank.x, self.mainTank.y, 'mainTank', self.mainTank.facing))
        
        for bul in self.bulletList:
            if bul.direction == 'n' and bul.y > -10:
                bul.y -= 5
            elif bul.direction == 'e' and bul.x < 160:
                bul.x += 5
            elif bul.direction == 's' and bul.y < 120:
                bul.y += 5
            elif bul.direction == 'w' and bul.x > -10:
                bul.x -= 5
            
            for tank in self.enemyTanks:
                if bul.x in range(tank.x-8, tank.x+8) and bul.y in range(tank.y-8, tank.y+8):
                    self.bulletList.remove(bul)
                    self.enemyTanks.remove(tank)


    def draw(self):
        pyxel.cls(0)
        pyxel.load('PYXEL_RESOURCE_FILE.pyxres')
        for bul in self.bulletList:
            self.drawBullet(bul.x, bul.y)
        for tank in self.enemyTanks:
            self.drawEnemyTank(tank.x, tank.y, tank.facing)
        self.drawTank(self.mainTank.x, self.mainTank.y,self.mainTank.facing)


    def drawTank(self, x: int, y: int, facing: str):
        if facing == 'n':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=0,
            v=0,
            w=15,
            h=15,
            colkey=15
        )
        elif facing == 'e':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=48,
            v=0,
            w=15,
            h=15,
            colkey=15
        )
        elif facing == 's':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=16,
            v=0,
            w=15,
            h=15,
            colkey=15
        )
        elif facing == 'w':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=32,
            v=0,
            w=15,
            h=15,
            colkey=15
        )
            
    def drawBullet(self, x:int, y:int):
        pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=0,
            v=32,
            w=15,
            h=15,
            colkey=15
        )

    def drawEnemyTank(self, x: int, y: int, facing: str):
        if facing == 'n':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=0,
            v=16,
            w=15,
            h=15,
            colkey=15
        )
        elif facing == 'e':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=48,
            v=16,
            w=15,
            h=15,
            colkey=15
        )
        elif facing == 's':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=16,
            v=16,
            w=15,
            h=15,
            colkey=15
        )
        elif facing == 'w':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=32,
            v=16,
            w=15,
            h=15,
            colkey=15
        )


App()