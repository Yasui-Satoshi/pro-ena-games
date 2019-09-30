# This file is algorithm of player3
import pygame as pg  
from pygame.locals import *          
import time
import random as rd
import numpy as np
import os
import sys
import math
class Urashima():
    def __init__(self):
        #print("うらしま社長")
        pass
    def turn(self, P, x, y, direction, wall_cell, wall):
        #print('うらしま Current Coodinate: [ '+ str(x) + ', ' + str(y) + ']')
        #print('うらしま Current Direction: '+ str(direction) )
        next_x    = x + direction[0] 
        next_y    = y + direction[1]
        next_cell = pg.Rect(next_x ,next_y, P,P)
        #print('うらしま Next Coodinate: [ '+ str(next_x) + ', ' + str(next_y) + ']')
        #print('うらしま Next Direction: '+ str(direction) )
    
        if  next_cell.collidelist(wall_cell) != -1 or next_cell.collidelist(wall) != -1:
            if   direction == ( 0,-P): direction = ( P, 0)
            elif direction == ( P, 0): direction = ( 0, P)
            elif direction == ( 0, P): direction = (-P, 0)
            else:                    direction = ( 0,-P)
        return direction