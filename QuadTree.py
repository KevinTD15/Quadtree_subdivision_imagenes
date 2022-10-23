from ctypes.wintypes import RGB
from turtle import color
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

from operator import add
from functools import reduce



def split4(image):
    half_split = np.array_split(image, 2)
    res = map(lambda x: np.array_split(x, 2, axis=1), half_split)
    return reduce(add, res)

def calculate_mean(img):
    return np.mean(img, axis=(0, 1))

def concatenate4(north_west, north_east, south_west, south_east):
    top = np.concatenate((north_west, north_east), axis=1)
    bottom = np.concatenate((south_west, south_east), axis=1)
    return np.concatenate((top, bottom), axis=0)

def check_equal(myList):
    first=myList[0]
    return all((x==first).all() for x in myList)

class QuadTree:
    
    def insert(self, img, level = 0, count = 0):
        self.level = level
        self.mean = calculate_mean(img).astype(int)
        self.resolution = (img.shape[0], img.shape[1])
        self.final = True
        
        if not check_equal(img):
            split_img = split4(img)
            
            self.final = False
            self.north_west = QuadTree().insert(split_img[0], level + 1)
            self.north_east = QuadTree().insert(split_img[1], level + 1)
            self.south_west = QuadTree().insert(split_img[2], level + 1)
            self.south_east = QuadTree().insert(split_img[3], level + 1)
        
        return self
    
    def get_image(self, level):
        if(self.final or self.level == level):
            return np.tile(self.mean, (self.resolution[0], self.resolution[1], 1))
        return concatenate4(
            self.north_west.get_image(level), 
            self.north_east.get_image(level),
            self.south_west.get_image(level),
            self.south_east.get_image(level))
    

    def get_border(self, level):
        if(self.final or self.level == level):
            return cv2.copyMakeBorder((
            np.tile(self.mean, (self.resolution[0], self.resolution[1], 1))[1:self.resolution[0]-1,1:self.resolution[1]-1]),
            1, 1, 1, 1, cv2.BORDER_CONSTANT, value=[0, 0, 255])
        
        return concatenate4(
            self.north_west.get_border(level), 
            self.north_east.get_border(level),
            self.south_west.get_border(level),
            self.south_east.get_border(level))        

    def get_cluster(self, level):
        cluster = np.zeros((self.resolution[0], self.resolution[1]))
        img = self.get_image(level)
        for i in range(self.resolution[0]):
            for j in range(self.resolution[1]):
                if(len(img[i][j]) == 3):
                    cluster[i, j] = (img[i][j][0] + img[i][j][1] + img[i][j][2]) / 765
                else:
                    cluster[i, j] = (img[i][j][0]) / 255
        return cluster
