#!/usr/bin/env python3

import colorsys
import math
from random import random
import time
from unicornhatmini import UnicornHATMini
from gpiozero import Button
from signal import pause


class Screen():
    def __init__(self, width, height, randomvals = True):
        self.matrix = [[0 for i in range(width)] for i in range(height)]
        self.width = width
        self.height = height
        if randomvals:
            for y, row in enumerate(self.matrix):
                for x, val in enumerate(row):
                    if random() >= 0.5:
                        self.matrix[y][x] = 1

    def draw(self):
        for y, row in enumerate(self.matrix):
            for x, val in enumerate(row):
                color = (255, 255, 255)
                if val == 0:
                    color = (0,0,0)
                if val == 2:
                    color = (0, 255,0)
                unicornhatmini.set_pixel(x, y, *color)
        unicornhatmini.show()

    def update(self):
        newmatrix = [[self.matrix[y][x] for x in range(self.width)] for y in range(self.height)]
        for y, row in enumerate(self.matrix):
            for x, val in enumerate(row):
                neigh = self.neighbours(x,y)
                val = self.matrix[y][x]
                #Any live cell with fewer than two live neighbours dies, as if by underpopulation.
                #Any live cell with two or three live neighbours lives on to the next generation.
                #Any live cell with more than three live neighbours dies, as if by overpopulation.
                #Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
                if (val > 0) and (neigh < 2):
                    newmatrix[y][x] = 0
                    continue
                if (val > 0) and ( 2 <= neigh <= 3):
                    newmatrix[y][x] = 1
                    continue
                if (val > 0) and (neigh > 3):
                    newmatrix[y][x] = 0
                    continue
                if (val == 0) and (neigh == 3):
                    newmatrix[y][x] = 2
                    continue
        self.matrix = newmatrix

    def neighbours(self,x,y) -> int:
        n = 0
        possiblecoords = [(x+i,y+j) for i in range(-1,2) for j in range(-1,2)]
        coords = []
        for coord in possiblecoords:
            xv, yv = coord[0], coord[1]
            #if 0 <= yv < self.height:
            #    if 0 <= xv < self.width:
            if (xv != x) or (yv != y):
                coords.append((coord[0]%self.width,coord[1]%self.height))
        for coord in coords:
            if self.matrix[coord[1]][coord[0]]:
                n += 1
        return n

def pressed(button):
    global screen
    button_name = button_map[button.pin.number]
    screen = Screen(u_width, u_height, randomvals=True)

button_map = {5: "A", 6: "B", 16: "X", 24: "Y"}
unicornhatmini = UnicornHATMini()
unicornhatmini.set_brightness(0.1)
unicornhatmini.set_rotation(0)
u_width, u_height = unicornhatmini.get_shape()
t_start = time.time()
screen = Screen(u_width, u_height, randomvals=True)

def main():
    global screen
    
    button_a = Button(5)
    button_b = Button(6)
    button_x = Button(16)
    button_y = Button(24)

    button_a.when_pressed = pressed
    button_b.when_pressed = pressed
    button_x.when_pressed = pressed
    button_y.when_pressed = pressed

    #vals = [(4,5),(3,4),(4,3)]
    #for val in vals:
    #    screen.matrix[val[1]][val[0]] = True
    while True:
        #for y in range(u_height):
        #    for x in range(u_width):
        #         unicornhatmini.set_pixel(x, y, 255, 255, 255)
        # unicornhatmini.show()
        screen.draw()
        screen.update()
        time.sleep(20.0 / 60.0)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
