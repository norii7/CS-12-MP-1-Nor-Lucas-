#### The project is a direct adaptation of the game "Battle City", a multi-directional shooter video game produced and published in 1985 by Namco. It utilizes the game engine "pyxel" by Takashi Kitao together with the Python programming language to frame its core mechanics.

## Game Mechanics

In the game, you play as a tank that must protect its home by shooting down and eliminating all the enemy tanks. The main tank is controlled by the following commands:

> W - Move up<br>A - Move left<br>S - Move down<br>D - Move right<br>Spacebar - Shoot bullet

There are three maps in the game corresponding to three levels of increasing difficulty from level 1-3. In each of the layout, there are multiple types of obstacles that the player can interact with:

![image](https://github.com/norii7/cs12mp1NorLucas/assets/167980560/bef892b5-9237-4769-8c3c-d0e366c35a50)


> Bricked Wall - The player, enemy tanks and bullets cannot pass through it. If shot, it turns into a Cracked Brick Wall.<br>Cracked Brick Wall - The player, enemy tanks and bullets cannot pass through it. If shot, it disappears and the cell it was originaly in becomes empty where tanks can pass through.<br>Stone - The player, enemy tanks and bullets cannot pass through it. It is indestructible and remains intact when shot.<br>Mirror - The player, enemy tanks and bullets cannot pass through it. If shot, it deflects the bullet to the direction it is facing.<br>Water - The player and enemy tanks cannot pass through it but bullets can.<br>Forest - The player, enemy tanks and bullets are able to pass through it. It obstructs the view of anything passing through it.<br>Home - The player and enemy tanks cannot pass through it. If shot, the game ends regardless of the number of lives left (players start with three lives).

The map data are stored in the `stage.py` file. It contains the dataclass `obstacles` and the 2D list `levels`. Each map is a list of `obstacles` inside `levels`. Each `obstacles` has `x` and `y` fields for coordinates with `x in range(0, 11)` and `y in range(0, 8)` and a `type` field that takes in a string corresponding to the type of obstacle it is from the list above. To add another map, you simply append another list inside `level` with `obstacles` objects that correspond to your desired configuration.

In a map, enemy tanks will spawn periodically. They will move and shoot in random directions in an attemp to eliminate the player and the home cell. Your goal is to prevent this from happening by shooting all of them down. There are two types of tanks:

> Yellow Tank - It behaves just like the player tank in that it moves with the same speed and shoot bullets normally.<br>Blue Tank - They move faster than Yellow Tanks. They shoot bullets normally.

When the player gets hit by a bullet, be it from an enemy tank or themselves, they lose one life out of three and respawn back to their original position. When they go through and finish all levels or when they run out of lives, the game ends. They can restart the game by pressing the Spacebar.

Other game features include a powerup, which when picked up, increases the speed of the player tank—and cheatcodes. To enter cheatcodes, simply press the backtick( &#96; ) key, type in your code and press enter. The following are the available cheatcodes: `["UNOTIME", "MORELIVE", "SIRJBEST", "TANKNICOLONEL"]`. Each code gives the player tank one more life if used.

## Project Details

Highest Phase Accomplished: Phase 3

Contributions:
Lucas = `[collision function, mirror functionality, enemy tank and bullet behavior, game over and replay functionality, bgm and sound effects, cheat codes]`
Nor = `[obstacles and layouts, stage file, sprites and graphics, collision function, life mechanics, powerup, readme]`
