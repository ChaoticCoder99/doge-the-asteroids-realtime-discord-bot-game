from random import random, randint

class dogeTheAsteroids:
    def __init__(self):
        self.ROWS     = 50
        self.COLUMNS  = 5
        self.ROCKET   = ")==>"
        self.ASTEROID = "#"
        self.ASTSPNCH = 1/4
        self.score    = 0
        self.col      = int(self.COLUMNS / 2)
        self.run      = False
        self.player   = None
        self.dir      = 0 
        self.grid     = [[" " for _ in range(self.ROWS)] for _ in range(self.COLUMNS)]
        self.astroids = []

    def get_screen(self):
        screen = ""
        for i in self.grid:
            screen += "I"+"".join(i)
            screen += "I\n"
        return screen

    def spawn_asteroid(self):
        if random() < self.ASTSPNCH:
            tmp = [randint(0, self.COLUMNS-1), self.ROWS-1]
            self.astroids.append(tmp)

    def move_asteroid(self):
        t = []

        for i in range(len(self.astroids)):
            j = self.astroids[i]
            j[1] -= 1
            if j[1] < 0:
                t.append(i)
        
        for i in t:
            self.astroids.pop(i)

    def collision_check(self):
        for i in self.astroids:
            if i[0] == self.col:
                for j in range(1,4):
                    if i[1] == j:
                        return True
            continue
        return False

    def update_screen(self):
        # Reset grid
        self.grid = [[" " for _ in range(self.ROWS)] for _ in range(self.COLUMNS)]

        # Asteroid stuff
        self.spawn_asteroid()
        self.move_asteroid()

        # Make sure the ship doesn't move to fast vertically
        if   self.dir > 1: self.dir = 1
        elif self.dir <-1: self.dir = -1

        # Move the ship in a vertical direction
        self.col += self.dir

        # Move the ship back into the screen and reset the direction        
        t1 = self.COLUMNS-1
        if self.col < 0:
            self.col = 0
            self.dir = 0
        elif self.col > t1:
            self.col = t1
            self.dir = 0
        
        # Draw Ship
        for i in range(len(self.ROCKET)):
            self.grid[self.col][i] = self.ROCKET[i]
        
        # Draw asteroids
        for i in range(len(self.astroids)):
            j = self.astroids[i]
            self.grid[j[0]][j[1]] = self.ASTEROID