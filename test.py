import pygame as pg
import pyghexmap

def main():
	pg.init()
	m = Map(5,5)
	print(m.ascii())

