import pygame as pg
import sys
import csv
import time
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH+SIDEBAR, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        args = sys.argv
        timestr = time.strftime("%Y%m%d-%H%M%S")
        if len(args) < 2:
            self.filename = timestr + ".csv"
            self.grid = [[0 for x in range(GRIDWIDTH)] for y in range(GRIDHEIGHT)]
            self.grid[0][0] = 1
            self.grid[0][GRIDHEIGHT-1] = 2
            self.grid[GRIDWIDTH-1][0] = 3
            self.grid[GRIDWIDTH-1][GRIDHEIGHT-1] = 4
        else:
            self.grid = []
            self.filename = args[1]
            with open(self.filename,'r') as my_csv:
                csvReader = csv.reader(my_csv,delimiter=',')
                for row in csvReader:
                    self.grid.append(list(map(int,row)))
            print(self.grid)
            print("+++++++++++++++++++")

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.cells  = pg.sprite.Group()
        self.player = Player(self, 10, 10)
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                if self.grid[x][y] == 1:
                    print("GREEN")
                    Wall(self, x, y,GREEN)
                elif self.grid[x][y] == 2:
                    Wall(self, x, y, BLUE)
                elif self.grid[x][y] == 3:
                    Wall(self, x, y, RED)
                elif self.grid[x][y] == 4:
                    Wall(self, x, y, YELLOW)
            

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        with open(self.filename,'w') as my_csv:
            csvWriter = csv.writer(my_csv,delimiter=',')
            csvWriter.writerows(self.grid)
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()

    def cube_to_oddr(self, cube):
        col = cube[0] + (cube[3] - (cube[2]&1)) / 2
        row = cube.z
        return (col, row)

    def oddr_to_cube(self, hex):
        x = hex[0] - (hex[1] - (hex[1]&1)) / 2
        z = hex[1]
        y = -x-z
        return (x, y, z)

    def cube_distance(self, a, b):
        return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2]))

    #given two indeces, return the distance between the two coresponding hexes
    def dist(self,i1,i2):
        ac = self.oddr_to_cube(i1)
        bc = self.oddr_to_cube(i2)
        return self.cube_distance(ac, bc)

    def find_center(self):
        x = (GRIDWIDTH // 2)
        y = (GRIDHEIGHT // 2)
        return (x, y)

    def draw_grid(self):
        #for x in range(0, WIDTH+1, TILESIZE):
            #pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        center = self.find_center()

        for y in range (0, GRIDHEIGHT, 2):
            for x in range(0, GRIDWIDTH):
                if self.dist(center, (x,y)) <= BOARDRADIUS:
                    CellBorder(self,x,y)
                    Cell(self,x,y,x+y)
        for y in range (1, GRIDHEIGHT, 2):
            for x in range(0, GRIDWIDTH):
                if self.dist(center, (x,y)) <= BOARDRADIUS:
                    CellBorder(self,x+0.5,y)
                    Cell(self,x+0.5,y,x+y)
        #for y in range(0, HEIGHT, TILESIZE):
            #pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
        pg.draw.line(self.screen, LIGHTGREY, (WIDTH, 0), (WIDTH, HEIGHT))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def get_grid_pos():
        pos = pg.mouse.get_pos()
        y = pos[1] // (TILESIZE)
        if y%2 == 0:
            pass
        else:
            x = pos[0] // (TILESIZE)

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                 # User clicks the mouse. Get the position
                pos = pg.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                x = pos[0] // (TILESIZE)
                y = pos[1] // (TILESIZE)
                # Set that location to one
                #grid[row][column] = 1

                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_1:
                    Wall(self, x, y,GREEN)
                    self.grid[y][x] = 1
                if event.key == pg.K_2:
                    Wall(self, x, y, BLUE)
                    self.grid[y][x] = 2
                if event.key == pg.K_3:
                    Wall(self, x, y, RED)
                    self.grid[y][x] = 3
                if event.key == pg.K_4:
                    Wall(self, x, y, YELLOW)
                    self.grid[y][x] = 4

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()