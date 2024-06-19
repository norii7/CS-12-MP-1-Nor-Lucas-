from dataclasses import dataclass

OBSTACLE_SIDE = 15

@dataclass(frozen=True)
class obstacles:
    x: int
    y: int
    type: str
    side: int = OBSTACLE_SIDE

# Grid  is assumed to be 11 x 8

levels: list[list[obstacles]] = [
        
        # LEVEL 1
        [
            #home
            obstacles(0, 0, 'home'),
            obstacles(1, 0, 'brick'),
            obstacles(0, 1, 'brick'),
            obstacles(1, 1, 'brick'),

            obstacles(5, 3, 'stone'),
            obstacles(5, 1, 'brick'),
            obstacles(5, 5, 'brick'),
            obstacles(3, 3, 'brick'),
            obstacles(7, 3, 'brick'),

            obstacles(4, 2, 'forest'),
            obstacles(6, 2, 'forest'),
            obstacles(4, 4, 'forest'),
            obstacles(6, 4, 'forest'),
            
            obstacles(0, 3, 'stone'),
            obstacles(1, 3, 'brick'),
            obstacles(1, 5, 'stone'),
            obstacles(1, 6, 'brick'),
            obstacles(2, 6, 'forest'),
            obstacles(3, 6, 'brick'),

            obstacles(7, 1, 'stone'),
            obstacles(8, 1, 'forest'),

            obstacles(5, 7, 'water'),
            obstacles(6, 7, 'water'),
            obstacles(7, 7, 'water'),
            obstacles(8, 7, 'water'),
            obstacles(9, 7, 'water'),
            obstacles(10, 7, 'water'),
            obstacles(7, 6, 'water'),
            obstacles(8, 6, 'water'),
            obstacles(9, 6, 'water'),
            obstacles(10, 6, 'water'),

            
        ],
            
        # LEVEL 2
        [
            #home
            obstacles(5, 7, 'home'),
            obstacles(4, 7, 'brick'),
            obstacles(6, 7, 'brick'),
            obstacles(4, 6, 'brick'),
            obstacles(5, 6, 'brick'),
            obstacles(6, 6, 'brick'),

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

            #forest
            obstacles(10, 7, 'forest'),
            obstacles(9, 7, 'forest'),
            obstacles(8, 7, 'forest'),
            obstacles(10, 6, 'forest'),
            obstacles(9, 6, 'forest')
        ],

        # LEVEL 3
        [
            obstacles(1, 2, 'home'),

            obstacles(0, 7, 'water'),
            obstacles(1, 7, 'water'),
            obstacles(1, 6, 'water'),
            obstacles(1, 5, 'water'),
            obstacles(2, 5, 'water'),
            obstacles(2, 6, 'water'),
            obstacles(3, 4, 'water'),
            obstacles(4, 4, 'water'),
            obstacles(3, 5, 'water'),
            obstacles(4, 5, 'water'),

            obstacles(7, 2, 'mirror_se'),
            obstacles(7, 1, 'brick'),
            obstacles(7, 3, 'brick'),
            obstacles(6, 2, 'brick'),
            obstacles(8, 2, 'brick'),
            obstacles(6, 1, 'forest'),
            obstacles(8, 1, 'forest'),
            obstacles(6, 3, 'forest'),
            obstacles(8, 3, 'forest'),

            obstacles(2, 0, 'forest'),
            obstacles(3, 0, 'forest'),
            obstacles(4, 0, 'forest'),
            obstacles(5, 0, 'forest'),
            obstacles(3, 1, 'forest'),
            obstacles(4, 1, 'forest'),
            obstacles(3, 2, 'brick'),
            obstacles(4, 2, 'brick'),

            obstacles(5, 7, 'mirror_se'),

            obstacles(7, 5, 'brick'),
            obstacles(6, 5, 'brick'),
            obstacles(8, 5, 'brick'),

        ]
]