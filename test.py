import pygame as pg
#import pyghexmap
import colorsys

def cube_to_oddr(cube):
    col = cube[0] + (cube[3] - (cube[2]&1)) / 2
    row = cube.z
    return (col, row)

def oddr_to_cube(hex):
    x = hex[0] - (hex[1] - (hex[1]&1)) / 2
    z = hex[1]
    y = -x-z
    return (x, y, z)

def cube_distance(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2]))

#given two indeces, return the distance between the two coresponding hexes
def dist(i1,i2):
	ac = oddr_to_cube(i1)
	bc = oddr_to_cube(i2)
	return cube_distance(ac, bc)

GRIDWIDTH = 21
GRIDHEIGHT = 21

def get_center():
	x = GRIDWIDTH // 2
	y = GRIDHEIGHT // 2
	print(x)
	print(y) 

def main():
	#pg.init()
	#m = Map(5,5)
	#print(m.ascii())
	print(dist((3,0), (0,3)))
	print(dist((0,0), (0,1)))

main()