import pyxel
from dataclasses import dataclass
from random import randint, choice
from operator import xor
from stage import obstacles, levels

#global variables to easily change code when calibrating 
FPS = 30
HEIGHT = 120
WIDTH = 165
TANK_HEIGHT = 12
TANK_WIDTH  = 10
TANK_SPEED = 1
BULLET_SIDE = 2
BULLET_SPEED = 5
MAX_ENEMY_TANKS = 3
OBSTACLE_SIDE = 15
LIVES = 3

global level, stage
level = 1

@dataclass
class Tank:
    x: int
    y: int
    facing: str
    id: str
    height: int = TANK_HEIGHT
    width: int = TANK_WIDTH

@dataclass
class mainTank(Tank):
    global LIVES
    lives: int = LIVES

@dataclass
class bullet:
    x: int
    y: int
    origin: str
    direction: str
    mirrored: bool = False
    side: int = BULLET_SIDE

class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, fps=FPS)
        pyxel.load('PYXEL_RESOURCE_FILE.pyxres')
        self.init_game()
        pyxel.run(self.update, self.draw)

    def init_game(self):
        global level, LIVES
        self.x = 0
        self.mainTank = mainTank(0, 0, 'n', 'main', 0, lives=LIVES) if level != 1 else mainTank(3 * TANK_WIDTH, 0, 'n', 'main', 0, lives=LIVES)
        self.bulletList: list[bullet] = list()
        self.enemyTanks: list[Tank] = list()
        self.gameOver: bool = False
        self.levelWin: bool = False
        self.obstacles: list[obstacles] = levels[level - 1][::]
        self.bgmPlaying: bool = False
        
        for _ in range(MAX_ENEMY_TANKS):
            rand_x = randint(0, WIDTH - TANK_WIDTH)
            rand_y = randint(0, HEIGHT - TANK_HEIGHT)
            rand_tank = Tank(rand_x, rand_y, choice(['n', 's', 'e', 'w']), 'enemy' + str(len(self.enemyTanks)))

            while True in [self.are_overlapping(rand_tank, tank) for tank in self.enemyTanks + [self.mainTank]] or True in [self.are_overlapping(rand_tank, obst) for obst in self.obstacles]:
                rand_x = randint(0, WIDTH - TANK_WIDTH)
                rand_y = randint(0, HEIGHT - TANK_HEIGHT)
                rand_tank = Tank(rand_x, rand_y, choice(['n', 's', 'e', 'w']), 'enemy' + str(len(self.enemyTanks)))
            
            self.enemyTanks.append(rand_tank)

    def update(self):
        global level, LIVES

        self.x = (self.x + 1) % pyxel.width

        if self.mainTank.lives == 0:
            self.gameOver = True
            self.bgmPlaying = False
            level = 1
            pyxel.play(3, 5)

        if not self.bgmPlaying:
            for ch in range(3):
                pyxel.stop(ch)
            if self.gameOver:
                pyxel.playm(1, loop=True)
            else:
                pyxel.playm(0, loop=True)

            self.bgmPlaying = True

        if len(self.enemyTanks) == 0:
            self.levelWin = True

        if self.levelWin:
            if level < len(levels):
                level += 1
                self.init_game()

        if not self.gameOver:
            if pyxel.btn(pyxel.KEY_W):
                self.moveTank('n', self.mainTank)
                pyxel.play(3, 10)
            elif pyxel.btn(pyxel.KEY_A):
                self.moveTank('w', self.mainTank)
                pyxel.play(3, 10)
            elif pyxel.btn(pyxel.KEY_S):
                self.moveTank('s', self.mainTank)
                pyxel.play(3, 10)
            elif pyxel.btn(pyxel.KEY_D):
                self.moveTank('e', self.mainTank)
                pyxel.play(3, 10)

            if pyxel.btnp(pyxel.KEY_SPACE, hold=10, repeat=10):
                if len([bul for bul in self.bulletList if bul.origin == self.mainTank.id]) <= 1:
                    self.bulletList.append(bullet(self.mainTank.x + self.mainTank.width//2 - 1, self.mainTank.y + self.mainTank.height//2 - 1, self.mainTank.id, self.mainTank.facing))
                pyxel.play(3, 6)
        
            for bul in self.bulletList:
                if self.are_overlapping(bul, self.mainTank):
                    if bul.origin != self.mainTank.id:
                        self.bulletList.remove(bul)
                        pyxel.play(3, 5)
                        LIVES -= 1
                        self.mainTank = mainTank(0, 0, 'n', 'main', 0, lives=LIVES) if level != 1 else mainTank(3 * TANK_WIDTH, 0, 'n', 'main', 0, lives=LIVES)
                    elif bul.origin == self.mainTank.id:
                        if bul.mirrored:
                            self.bulletList.remove(bul)
                            self.gameOver = True
                            self.bgmPlaying = False
                            level = 1
                            pyxel.play(3, 5)

                for tank in self.enemyTanks:
                    if self.are_overlapping(bul, tank):
                        if bul.origin == self.mainTank.id:
                            self.bulletList.remove(bul)
                            self.enemyTanks.remove(tank)
                            pyxel.play(3, 5)
                
                for obstacle in self.obstacles:
                    if self.are_overlapping(bul, obstacle) and len(self.bulletList) != 0 and bul in self.bulletList:
                        if obstacle.type == 'stone':
                            self.bulletList.remove(bul)
                        elif obstacle.type == 'brick':
                            self.bulletList.remove(bul)
                            self.obstacles.remove(obstacle)
                            self.obstacles.append(obstacles(obstacle.x, obstacle.y, 'cracked'))
                        elif obstacle.type == 'cracked':
                            self.bulletList.remove(bul)
                            self.obstacles.remove(obstacle)
                            pyxel.play(3, 5)
                        elif obstacle.type == 'mirror_ne':
                            bul.mirrored = True
                            if bul.direction == 'n':
                                bul.direction = 'e'
                            elif bul.direction == 'e':
                                bul.direction = 'n'
                            elif bul.direction == 'w':
                                bul.direction = 's'
                            elif bul.direction == 's':
                                bul.direction = 'w'
                        elif obstacle.type == 'mirror_se':
                            bul.mirrored = True
                            if bul.direction == 'n':
                                bul.direction = 'w'
                            elif bul.direction == 'e':
                                bul.direction = 's'
                            elif bul.direction == 'w':
                                bul.direction = 'n'
                            elif bul.direction == 's':
                                bul.direction = 'e'
                        elif obstacle.type == 'home':
                            self.gameOver = True
                            self.bgmPlaying = False
                            level = 1
                            pyxel.play(3, 5)
                
                for bul2 in [b for b in self.bulletList if b != bul]:
                    if self.are_overlapping(bul, bul2):
                        self.bulletList.remove(bul)
                        self.bulletList.remove(bul2)

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
                self.moveTank(tank.facing, tank)

            if pyxel.frame_count % 15 == 0:
                for tank in self.enemyTanks:
                    dir_choices = ('n', 's', 'e', 'w')
                    tank.facing = choice(dir_choices)

            if pyxel.frame_count % 7 == 0:
                for tank in self.enemyTanks:
                    coin_flip = choice((True, False))
                    if coin_flip == True and len([bul for bul in self.bulletList if bul.origin != self.mainTank.id]) <= MAX_ENEMY_TANKS:
                        self.bulletList.append(bullet(tank.x + tank.width//2 - 1, tank.y + tank.height//2 - 1, tank.id, tank.facing))

        else:
            if pyxel.btn(pyxel.KEY_SPACE):
                LIVES = 3
                self.init_game()

    def line_line_intersection(self, x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, x4: int, y4: int) -> bool:
        uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
        uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))

        if 0 <= uA <= 1 and 0 <= uB <= 1:
            return True
        
        return False
    
    def line_rect_intersection(self, x1: int, y1: int, x2: int, y2: int, rx: int, ry: int, rw: int, rh: int) -> bool:
        left = self.line_line_intersection(x1, y1, x2, y2, rx, ry, rx, ry+rh)
        right = self.line_line_intersection(x1, y1, x2, y2, rx+rw, ry, rx+rw, ry+rh)
        top = self.line_line_intersection(x1, y1, x2, y2, rx, ry, rx+rw, ry)
        bottom = self.line_line_intersection(x1, y1, x2, y2, rx, ry+rh, rx+rw, ry+rh)

        if left or right or top or bottom:
            return True
        
        return False

    def are_overlapping(self, object1: Tank | bullet | obstacles, object2: Tank | bullet | obstacles) -> bool:
        x1, y1 = object1.x, object1.y
        x2, y2 = object2.x, object2.y

        if isinstance(object1, Tank):
            height1 = object1.height
            width1 = object1.width
        else:
            height1 = object1.side
            width1 = object1.side

        if isinstance(object2, Tank):
            height2 = object2.height
            width2 = object2.width
        else:
            height2 = object2.side
            width2 = object2.side

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

        if xor(isinstance(object1, obstacles), isinstance(object2, obstacles)):
            if isinstance(object1, obstacles) and 'mirror' in object1.type:
                mirror_type = object1.type[-2:]

                if mirror_type == 'ne':
                    return self.line_rect_intersection(x1, y1+height1, x1+width1, y1, x2, y2, width2, height2)
                if mirror_type == 'se':
                    return self.line_rect_intersection(x1, y1, x1+width1, y1+height1, x2, y2, width2, height2)
            if isinstance(object2, obstacles) and 'mirror' in object2.type:
                mirror_type = object2.type[-2:]

                if mirror_type == 'ne':
                    return self.line_rect_intersection(x2, y2+height2, x2+width2, y2, x1, y1, width1, height1)
                if mirror_type == 'se':
                    return self.line_rect_intersection(x2, y2, x2+width2, y2+height2, x1, y1, width1, height1)

        # Check if one object is to the left of the other
        if x1 + width1 <= x2 or x2 + width2 <= x1:
            return False
        
        #Check if one object is above the other
        if y1 + height1 <= y2 or y2 + height2 <= y1:
            return False
        
        return True
    
    def moveTank(self, dir: str, tank: Tank) -> None:
        match dir:
            case 'n':
                if tank.y - TANK_SPEED >= 0:
                    dummyTank = Tank(tank.x, tank.y - TANK_SPEED, tank.facing, 'dummy')
                    tank.facing = 'n'

                    if True not in [self.are_overlapping(dummyTank, tnk) for tnk in self.enemyTanks + [self.mainTank] if tnk != tank]:
                        if True not in [self.are_overlapping(dummyTank, obstacle) for obstacle in self.obstacles]:
                            tank.y -= TANK_SPEED
            case 'w':
                if tank.x - TANK_SPEED >= 0:
                    dummyTank = Tank(tank.x - TANK_SPEED, tank.y, tank.facing, 'dummy')
                    tank.facing = 'w'

                    if True not in [self.are_overlapping(dummyTank, tnk) for tnk in self.enemyTanks + [self.mainTank] if tnk != tank]:
                        if True not in [self.are_overlapping(dummyTank, obstacle) for obstacle in self.obstacles]:
                            tank.x -= TANK_SPEED

            case 's':
                if tank.y + TANK_HEIGHT + TANK_SPEED <= HEIGHT:
                    dummyTank = Tank(tank.x, tank.y + TANK_SPEED, tank.facing, 'dummy')
                    tank.facing = 's'

                    if True not in [self.are_overlapping(dummyTank, tnk) for tnk in self.enemyTanks + [self.mainTank] if tnk != tank]:
                        if True not in [self.are_overlapping(dummyTank, obstacle) for obstacle in self.obstacles]:
                            tank.y += TANK_SPEED

            case 'e':
                if tank.x + TANK_WIDTH + TANK_SPEED <= WIDTH:
                    dummyTank = Tank(tank.x + TANK_SPEED, tank.y, tank.facing, 'dummy')
                    tank.facing = 'e' 

                    if True not in [self.are_overlapping(dummyTank, tnk) for tnk in self.enemyTanks + [self.mainTank] if tnk != tank]:
                        if True not in [self.are_overlapping(dummyTank, obstacle) for obstacle in self.obstacles]:
                            tank.x += TANK_SPEED

            case _:
                pass

    def draw(self):
        pyxel.cls(0)

        if not self.gameOver:
            for tank in self.enemyTanks:
                self.drawEnemyTank(tank.x, tank.y, tank.facing)
            for obstacle in self.obstacles:
                if obstacle.type == 'water':
                    self.drawObstacle(obstacle.x, obstacle.y, obstacle.type)
            for bul in self.bulletList:
                self.drawBullet(bul.x, bul.y)
            self.drawTank(self.mainTank.x, self.mainTank.y,self.mainTank.facing)
            for obstacle in self.obstacles:
                if obstacle.type != 'water':
                    self.drawObstacle(obstacle.x, obstacle.y, obstacle.type)
            self.drawHearts(self.mainTank.lives)
        else:
            pyxel.text(WIDTH/2 - 20, HEIGHT/2 - 20, "GAME OVER", 5)
            pyxel.text(WIDTH/2 - 50, HEIGHT/2 - 10, "PRESS SPACE TO PLAY AGAIN", 5)

    def drawTank(self, x: int, y: int, facing: str):
        if facing == 'n':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=3,
            v=1,
            w=TANK_WIDTH,
            h=TANK_HEIGHT,
            colkey=0
        )
            self.mainTank.width = TANK_WIDTH
            self.mainTank.height = TANK_HEIGHT
        elif facing == 'e':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=51,
            v=3,
            w=TANK_HEIGHT,
            h=TANK_WIDTH,
            colkey=0
        )
            self.mainTank.height = TANK_WIDTH
            self.mainTank.width = TANK_HEIGHT
        elif facing == 's':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=19,
            v=3,
            w=TANK_WIDTH,
            h=TANK_HEIGHT,
            colkey=0
        )
            self.mainTank.width = TANK_WIDTH
            self.mainTank.height = TANK_HEIGHT
        elif facing == 'w':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=33,
            v=3,
            w=TANK_HEIGHT,
            h=TANK_WIDTH,
            colkey=0
        )
            self.mainTank.height = TANK_WIDTH
            self.mainTank.width = TANK_HEIGHT
            
    def drawBullet(self, x:int, y:int):
        pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=7,
            v=39,
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
            u=3,
            v=17,
            w=TANK_WIDTH,
            h=TANK_HEIGHT,
            colkey=0
        )
            self.mainTank.width = TANK_WIDTH
            self.mainTank.height = TANK_HEIGHT
        elif facing == 'e':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=51,
            v=19,
            w=TANK_HEIGHT,
            h=TANK_WIDTH,
            colkey=0
        )
            self.mainTank.height = TANK_WIDTH
            self.mainTank.width = TANK_HEIGHT
        elif facing == 's':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=19,
            v=19,
            w=TANK_WIDTH,
            h=TANK_HEIGHT,
            colkey=0
        )
            self.mainTank.width = TANK_WIDTH
            self.mainTank.height = TANK_HEIGHT
        elif facing == 'w':
            pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=33,
            v=19,
            w=TANK_HEIGHT,
            h=TANK_WIDTH,
            colkey=0
        )
            self.mainTank.height = TANK_WIDTH
            self.mainTank.width = TANK_HEIGHT
            
    def drawHearts(self, lives: int) -> None:
        if lives == 3:
            pyxel.blt(
                x=155,
                y=2,
                img=0,
                u=16,
                v=33,
                w=7,
                h=6,
                colkey=0
            )
            pyxel.blt(
                x=146,
                y=2,
                img=0,
                u=16,
                v=33,
                w=7,
                h=6,
                colkey=0
            )
            pyxel.blt(
                x=137,
                y=2,
                img=0,
                u=16,
                v=33,
                w=7,
                h=6,
                colkey=0
            )

        elif lives == 2:
            pyxel.blt(
                x=155,
                y=2,
                img=0,
                u=16,
                v=33,
                w=7,
                h=6,
                colkey=0
            )
            pyxel.blt(
                x=146,
                y=2,
                img=0,
                u=16,
                v=33,
                w=7,
                h=6,
                colkey=0
            )
            pyxel.blt(
                x=137,
                y=2,
                img=0,
                u=32,
                v=33,
                w=7,
                h=6,
                colkey=0
            )

        elif lives == 1:
            pyxel.blt(
                x=155,
                y=2,
                img=0,
                u=16,
                v=33,
                w=7,
                h=6,
                colkey=0
            )
            pyxel.blt(
                x=146,
                y=2,
                img=0,
                u=32,
                v=33,
                w=7,
                h=6,
                colkey=0
            )
            pyxel.blt(
                x=137,
                y=2,
                img=0,
                u=32,
                v=33,
                w=7,
                h=6,
                colkey=0
            )

        elif lives == 0:
            pyxel.blt(
                x=155,
                y=2,
                img=0,
                u=32,
                v=33,
                w=7,
                h=6,
                colkey=0
            )
            pyxel.blt(
                x=146,
                y=2,
                img=0,
                u=32,
                v=33,
                w=7,
                h=6,
                colkey=0
            )
            pyxel.blt(
                x=137,
                y=2,
                img=0,
                u=32,
                v=33,
                w=7,
                h=6,
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

        if type == 'home':
            pyxel.blt(
                x=x*OBSTACLE_SIDE,
                y=y*OBSTACLE_SIDE,
                img=0,
                u=32,
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