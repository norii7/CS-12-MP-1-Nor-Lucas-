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
BULLET_SIDE = 2
BULLET_SPEED = 5
MAX_ENEMY_TANKS = {1: 4, 2: 4, 3: 6}
ENEMY_SPAWNS = {1: (105, 75), 2: (150, 60), 3: (136, 30)}
MAX_POWERUPS = 1
OBSTACLE_SIDE = 15
MAX_LIVES = 3
CHEAT_CODES = ["UNOTIME", "MORELIVE", "SIRJBEST", "TANKNICOLONEL"]

global level
level = 1

@dataclass
class Tank:
    x: int
    y: int
    facing: str
    id: str
    type: str
    speed: int
    lives: int = 0
    height: int = TANK_HEIGHT
    width: int = TANK_WIDTH

@dataclass
class bullet:
    x: int
    y: int
    origin: str
    direction: str
    mirrored: bool = False
    side: int = BULLET_SIDE

@dataclass
class powerUp:
    x: int
    y: int
    type: str
    side: int = OBSTACLE_SIDE

class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, fps=FPS)
        pyxel.load('PYXEL_RESOURCE_FILE.pyxres')
        self.init_game()
        pyxel.run(self.update, self.draw)

    def init_game(self):
        global level
        self.x = 0
        if level != 1:
            self.mainTank = Tank(0, 0, 'n', self.mainTank.id, self.mainTank.type, self.mainTank.speed, lives = self.mainTank.lives)
        else: 
            self.mainTank = Tank(3 * TANK_WIDTH, 0, 'n', 'main', 'main', 1, lives = MAX_LIVES)
        self.bulletList: list[bullet] = list()
        self.enemyTanksToSpawn: list[Tank] = list()
        self.enemyTanks: list[Tank] = list()
        self.enterCheatCode: bool = False
        self.input_str: str = ""
        self.isPaused: bool = False
        self.gameOver: bool = False
        self.levelWin: bool = False
        self.gameWin: bool = False
        self.obstacles: list[obstacles] = levels[level - 1][::]
        self.bgmPlaying: bool = False
        self.powerUPs: list[powerUp] = list()
        
        for _ in range(MAX_ENEMY_TANKS[level]):
            x = ENEMY_SPAWNS[level][0]
            y = ENEMY_SPAWNS[level][1]
            rand_type = choice(('enemyA', 'enemyB'))
            rand_dir = choice(('n', 's', 'e', 'w', 'n', 'w'))
            rand_tank = Tank(x, y, rand_dir, 'enemy' + str(len(self.enemyTanks)), rand_type, 2 if rand_type == 'enemyA' else 1)
            
            self.enemyTanksToSpawn.append(rand_tank)

        self.enemyTanks.append(self.enemyTanksToSpawn.pop())

        for _ in range(MAX_POWERUPS):
            rand_x = randint(0, WIDTH - OBSTACLE_SIDE)
            rand_y = randint(0, HEIGHT - OBSTACLE_SIDE)
            rand_powerup = powerUp(rand_x, rand_y, 'speedUp')

            while True in [self.are_overlapping(rand_powerup, tank) for tank in self.enemyTanks + [self.mainTank]] or True in [self.are_overlapping(rand_powerup, obst) for obst in self.obstacles]:
                rand_x = randint(0, WIDTH - OBSTACLE_SIDE)
                rand_y = randint(0, HEIGHT - OBSTACLE_SIDE)
                rand_powerup = powerUp(rand_x, rand_y, 'speedUp')
            
            self.powerUPs.append(rand_powerup)

    def update(self):
        global level

        self.x = (self.x + 1) % pyxel.width

        if not self.bgmPlaying:
            self.bgmPlaying = True
            for ch in range(3):
                pyxel.stop(ch)
            if self.gameOver:
                pyxel.playm(1, loop=True)
            else:
                pyxel.playm(0, loop=True)

        if len(self.enemyTanks) == 0 and len(self.enemyTanksToSpawn) == 0:
            self.levelWin = True

        if self.levelWin:
            if level < len(levels):
                level += 1
                self.init_game()
            else:
                self.gameWin = True

        if not self.gameOver:
            if self.gameWin:
                if pyxel.btnp(pyxel.KEY_SPACE):
                    level = 1
                    self.init_game()
            else:
                if pyxel.btnp(pyxel.KEY_P):
                    self.isPaused = not self.isPaused
                if pyxel.btn(pyxel.KEY_LCTRL) and pyxel.btnp(pyxel.KEY_R):
                    level = 1
                    self.init_game()
                if pyxel.btnp(pyxel.KEY_BACKQUOTE):
                    self.isPaused = True
                    self.enterCheatCode = True
                if self.enterCheatCode:
                    for k in pyxel.__dict__.keys():
                        if k.startswith('KEY_'):
                            if pyxel.btnp(getattr(pyxel, k)) and k not in ["KEY_RETURN", "KEY_BACKSPACE", "KEY_BACKQUOTE"]:
                                char = k[-1]
                                self.input_str += char

                    if pyxel.btnp(pyxel.KEY_RETURN):
                        self.isPaused = False
                        self.enterCheatCode = False

                        if self.input_str in CHEAT_CODES and self.mainTank.lives < MAX_LIVES:
                            self.mainTank.lives += 1

                        self.input_str = ""
                    elif pyxel.btnp(pyxel.KEY_P):
                        self.isPaused = False
                        self.enterCheatCode = False
                        self.input_str = ""
                    elif pyxel.btnp(pyxel.KEY_BACKSPACE):
                        self.input_str = self.input_str[:-1]

                if not self.isPaused:
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
                        if len([bul for bul in self.bulletList if bul.origin == self.mainTank.id]) < 1:
                            self.bulletList.append(bullet(self.mainTank.x + self.mainTank.width//2 - 1, self.mainTank.y + self.mainTank.height//2 - 1, self.mainTank.id, self.mainTank.facing))
                        pyxel.play(3, 6)

                    for powerup in self.powerUPs:
                        if self.are_overlapping(powerup, self.mainTank):
                            self.powerUPs.remove(powerup)
                            if powerup.type == 'speedUp':
                                self.mainTank.speed += 1

                    for bul in self.bulletList:
                        if self.are_overlapping(bul, self.mainTank):
                            if bul.origin != self.mainTank.id:
                                self.bulletList.remove(bul)
                                pyxel.play(3, 5)
                                self.mainTank.lives -= 1
                                if self.mainTank.lives == 0:
                                    self.gameOver = True
                                    self.bgmPlaying = False
                                    self.gameOver = True
                                else:
                                    if level != 1:
                                        self.mainTank = Tank(0, 0, 'n', self.mainTank.id, self.mainTank.type, self.mainTank.speed, lives = self.mainTank.lives)  
                                    else:
                                        self.mainTank = Tank(3 * TANK_WIDTH, 0, 'n', self.mainTank.id, self.mainTank.type, self.mainTank.speed, lives = self.mainTank.lives)
                            elif bul.origin == self.mainTank.id:
                                if bul.mirrored:
                                    self.bulletList.remove(bul)
                                    pyxel.play(3, 5)
                                    self.mainTank.lives -= 1
                                    if self.mainTank.lives == 0:
                                        self.gameOver = True
                                        self.bgmPlaying = False
                                        self.gameOver = True
                                    else:
                                        if level != 1:
                                            self.mainTank = Tank(0, 0, 'n', self.mainTank.id, self.mainTank.type, self.mainTank.speed, lives = self.mainTank.lives)  
                                        else:
                                            self.mainTank = Tank(3 * TANK_WIDTH, 0, 'n', self.mainTank.id, self.mainTank.type, self.mainTank.speed, lives = self.mainTank.lives)

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
                                    self.bulletList.remove(bul)
                                    self.obstacles.remove(obstacle)
                                    self.bgmPlaying = False
                                    self.gameOver = True
                                    pyxel.play(3, 5)
                        
                        for bul2 in [b for b in self.bulletList if b != bul]:
                            if self.are_overlapping(bul, bul2) and bul in self.bulletList and bul2 in self.bulletList:
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
                            if bul in self.bulletList:
                                self.bulletList.remove(bul)

                    for tank in self.enemyTanks:
                        self.moveTank(tank.facing, tank)

                    if pyxel.frame_count % 65 == 0 or len(self.enemyTanks) == 0:
                        try:
                            enemy = self.enemyTanksToSpawn.pop()
                            if True in [self.are_overlapping(enemy, tank) for tank in self.enemyTanks + [self.mainTank]]:
                                self.enemyTanksToSpawn.append(enemy)
                            else:
                                self.enemyTanks.append(enemy)
                        except:
                            pass 

                    if pyxel.frame_count % 20 == 0:
                        for tank in self.enemyTanks:
                            dir_choices = ('n', 's', 'e', 'w', 'n', 'w')
                            tank.facing = choice(dir_choices)

                    if pyxel.frame_count % 7 == 0:
                        for tank in self.enemyTanks:
                            if tank.type == 'enemyA' and pyxel.frame_count % 2 == 0:
                                coin_flip = choice((True, False))
                                if coin_flip == True and len([bul for bul in self.bulletList if bul.origin != self.mainTank.id]) <= MAX_ENEMY_TANKS[level] * 2:
                                    self.bulletList.append(bullet(tank.x + tank.width//2 - 1, tank.y + tank.height//2 - 1, tank.id, tank.facing))
                            elif tank.type == 'enemyB' and pyxel.frame_count % 4 == 0:
                                for _ in range(randint(2, 3)):
                                    coin_flip = choice((True, False))
                                    if coin_flip == True and len([bul for bul in self.bulletList if bul.origin != self.mainTank.id]) <= MAX_ENEMY_TANKS[level] * 2:
                                        self.bulletList.append(bullet(tank.x + tank.width//2 - 1, tank.y + tank.height//2 - 1, tank.id, tank.facing))
        else:
            if pyxel.btn(pyxel.KEY_SPACE):
                level = 1
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

    def are_overlapping(self, object1: Tank | bullet | obstacles | powerUp, object2: Tank | bullet | obstacles | powerUp) -> bool:
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
                if tank.y - tank.speed >= 0:
                    dummyTank = Tank(tank.x, tank.y - tank.speed, tank.facing, 'dummy', 'dummy', tank.speed)
                    tank.facing = 'n'

                    if True not in [self.are_overlapping(dummyTank, tnk) for tnk in self.enemyTanks + [self.mainTank] if tnk != tank]:
                        if True not in [self.are_overlapping(dummyTank, obstacle) for obstacle in self.obstacles]:
                            tank.y -= tank.speed
            case 'w':
                if tank.x - tank.speed >= 0:
                    dummyTank = Tank(tank.x - tank.speed, tank.y, tank.facing, 'dummy', 'dummy', tank.speed)
                    tank.facing = 'w'

                    if True not in [self.are_overlapping(dummyTank, tnk) for tnk in self.enemyTanks + [self.mainTank] if tnk != tank]:
                        if True not in [self.are_overlapping(dummyTank, obstacle) for obstacle in self.obstacles]:
                            tank.x -= tank.speed

            case 's':
                if tank.y + TANK_HEIGHT + tank.speed <= HEIGHT:
                    dummyTank = Tank(tank.x, tank.y + tank.speed, tank.facing, 'dummy', 'dummy', tank.speed)
                    tank.facing = 's'

                    if True not in [self.are_overlapping(dummyTank, tnk) for tnk in self.enemyTanks + [self.mainTank] if tnk != tank]:
                        if True not in [self.are_overlapping(dummyTank, obstacle) for obstacle in self.obstacles]:
                            tank.y += tank.speed

            case 'e':
                if tank.x + TANK_WIDTH + tank.speed <= WIDTH:
                    dummyTank = Tank(tank.x + tank.speed, tank.y, tank.facing, 'dummy', 'dummy', tank.speed)
                    tank.facing = 'e' 

                    if True not in [self.are_overlapping(dummyTank, tnk) for tnk in self.enemyTanks + [self.mainTank] if tnk != tank]:
                        if True not in [self.are_overlapping(dummyTank, obstacle) for obstacle in self.obstacles]:
                            tank.x += tank.speed

            case _:
                pass

    def draw(self):
        pyxel.cls(0)

        if not self.gameOver:
            if self.gameWin:
                pyxel.text(WIDTH/2 - 20, HEIGHT/2 - 20, "YOU WIN!!!", 5)
                pyxel.text(WIDTH/2 - 50, HEIGHT/2 - 10, "PRESS SPACE TO PLAY AGAIN", 5)

            else:
                pyxel.dither(1)
                for obstacle in self.obstacles:
                    if obstacle.type == 'water':
                        self.drawObstacle(obstacle.x, obstacle.y, obstacle.type)
                for bul in self.bulletList:
                    self.drawBullet(bul.x, bul.y)
                for tank in self.enemyTanks:
                    self.drawTank(tank.x, tank.y, tank.facing, tank.type)
                self.drawTank(self.mainTank.x, self.mainTank.y,self.mainTank.facing, self.mainTank.type)
                for obstacle in self.obstacles:
                    if obstacle.type != 'water':
                        self.drawObstacle(obstacle.x, obstacle.y, obstacle.type)
                for powerup in self.powerUPs:
                    self.drawPowerUp(powerup.x, powerup.y, powerup.type)
                self.drawHearts(self.mainTank.lives)

                if self.isPaused:
                    if self.enterCheatCode:
                        pyxel.dither(0.15)
                        pyxel.rect(0, 0, WIDTH, HEIGHT, 13)
                        pyxel.dither(1)
                        pyxel.rect(WIDTH//2-32, HEIGHT//2-17, 63, 10, 7)
                        pyxel.rect(WIDTH//2-32, HEIGHT//2-7, 63, 10, 7)
                        pyxel.text(WIDTH//2-30, HEIGHT//2-15, "ENTER CHEATCODE", 8)
                        pyxel.text(WIDTH//2-30, HEIGHT//2-5, f"{self.input_str}", 8)
                    else:
                        pyxel.dither(0.15)
                        pyxel.rect(0, 0, WIDTH, HEIGHT, 13)
                        pyxel.dither(1)
                        pyxel.rect(WIDTH//2-32, HEIGHT//2-12, 60, 10, 7)
                        pyxel.text(WIDTH//2-30, HEIGHT//2-10, "GAME IS PAUSED", 8)
        else:
            pyxel.text(WIDTH/2 - 20, HEIGHT/2 - 20, "GAME OVER", 5)
            pyxel.text(WIDTH/2 - 50, HEIGHT/2 - 10, "PRESS SPACE TO PLAY AGAIN", 5)

    def drawTank(self, x: int, y: int, facing: str, type: str):
        main_facing = {'n': (3, 1), 's': (19, 3), 'e': (51, 3), 'w': (33, 3)}
        enemyA_facing = {'n': (3, 17), 's': (19, 19), 'e': (51, 19), 'w': (33, 19)}
        enemyB_facing = {'n': (3, 49), 's': (19, 51), 'e': (51, 51), 'w': (33, 51)}
        sprite_coords = {'main': main_facing, 'enemyA': enemyA_facing, 'enemyB': enemyB_facing}
        u = sprite_coords[type][facing][0]
        v = sprite_coords[type][facing][1]

        pyxel.blt(
            x=x,
            y=y,
            img=0,
            u=u,
            v=v,
            w=TANK_WIDTH,
            h=TANK_HEIGHT,
            colkey=0
        )
            
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

    def drawHearts(self, lives: int) -> None:
        sprite_coords = {'live': (16, 33), 'dead': (32, 33)}
        hearts = lives * ['live'] + (3-lives) * ['dead']
        heart_x = [155, 146, 137]

        for i in range(len(hearts)):
            pyxel.blt(
                x=heart_x[i],
                y=2,
                img=0,
                u=sprite_coords[hearts[i]][0],
                v=sprite_coords[hearts[i]][1],
                w=7,
                h=6,
                colkey=0
            )

    def drawPowerUp(self, x: int, y: int, type: str) -> None:
        if type == 'speedUp':
            pyxel.blt(
                    x=x,
                    y=y,
                    img=0,
                    u=17,
                    v=113,
                    w=14,
                    h=14,
                    colkey=0
            )

    def drawObstacle(self, x: int, y: int, type: str) -> None:  # x,y are coordinates in game
        sprite_coords = {'brick': (0, 64), 'cracked': (0, 80), 'stone': (16, 64), 'mirror_ne': (32, 64), 'mirror_se': (48, 64), 'water': (48, 80), 'forest': (16, 80), 'home': (32, 80)}
        u = sprite_coords[type][0]
        v = sprite_coords[type][1]

        pyxel.blt(
            x=x*OBSTACLE_SIDE,
            y=y*OBSTACLE_SIDE,
            img=0,
            u=u,
            v=v,
            w=OBSTACLE_SIDE,
            h=OBSTACLE_SIDE,
            colkey=0
        )
        
App()