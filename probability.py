#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 10:59:35 2024

@author: antoine
"""

import copy
import random

class Hat:
    def __init__(self,**kwargs):
        self.contents = []
        for key, value in kwargs.items():
            for v in range(0,value):
                self.contents.append(key)

    def __str__(self):
        return str(self.contents)            
    
    def draw(self,n):
        random.shuffle(self.contents)
        if n > len(self.contents):
            n = len(self.contents)
        return self.contents.pop(random.randrange(n)) 
        #return random.sample(self.contents, n)

def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    m = 0
    n_ball_exp = sum(expected_balls.values())
 
    print(n_ball_exp)
    for exp in range(0,num_experiments):
        print(hat)
        tmp_hat = copy.deepcopy(hat)
        #print("exp " + str(exp))
        contents = tmp_hat.draw(num_balls_drawn)
        
        #print(contents)
        tmp_expected_balls = copy.deepcopy(expected_balls)

        iter = 0
        for ball in contents:
            iter = iter+1
            if ball in expected_balls.keys():
                tmp_expected_balls[ball] -= 1

            if all(value <= 0 for value in tmp_expected_balls.values()) and n_ball_exp<=iter:
                m = m+1
                break
    print(m/num_experiments)     
    return m/num_experiments

hat = Hat(black=6, red=4, green=3)
probability = experiment(hat=hat,
                  expected_balls={"red":2,"green":1},
                  num_balls_drawn=5,
                  num_experiments=2000)
print(probability)

hat = Hat(black=9, red=2)
probability = experiment(hat=hat,
                  expected_balls={"red":0},
                  num_balls_drawn=2,
                  num_experiments=1000)

hat1 = Hat(yellow=3, blue=2, green=6)
hat2 = Hat(red=5, orange=4)
hat3 = Hat(red=5, orange=4, black=1, blue=0, pink=2, striped=9)