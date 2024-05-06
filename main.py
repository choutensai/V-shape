#!/usr/bin/python3
import pygame
import sys
import time
import random
import math

WIDTH, HEIGHT = 800, 600
SCREEN_COLOR = (255, 255, 255)
TO_GOAL_WEIGHT = 1
MAX_SPEED = 1.2
l = 40
FORMATION_ANGLE = math.pi/6

#Pygame configuration
pygame.init() 
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("V-formation")
clock = pygame.time.Clock()

class Robot():
    def __init__(self, x, y ,o):
        self.x = x 
        self.y = y
        self.o = o 
        self.vx = 0 
        self.vy = 0
        self.w = 0
        self.size = 20
        self.goal = (x,y)
    def draw(self):

        points = [
        [self.x , self.y],
        [self.x - self.size*math.cos(math.pi*7/6 + self.o) , self.y - self.size*math.sin(math.pi*7/6 + self.o)],
        [self.x - self.size*math.cos(math.pi*5/6 + self.o) , self.y - self.size*math.sin(math.pi*5/6 + self.o)],
        ]
        pygame.draw.polygon(screen, (255, 0, 0), points)

    def update(self): 
        to_goal = self.move_to_goal()
        self.vx = to_goal[0] * TO_GOAL_WEIGHT
        self.vy = to_goal[1] * TO_GOAL_WEIGHT
        self.w = to_goal[2] * TO_GOAL_WEIGHT 
        #self.limit_speed()
        self.x += self.vx
        self.y += self.vy
        self.o += self.w
    
    def move_to_goal(self):
        move_x = -math.cos(self.o)*abs(self.goal[0] -self.x)/50
        move_y = -math.sin(self.o)*abs(self.goal[1] -self.y)/50
        move_o = (math.atan2(-(self.goal[1] -self.y) , -(self.goal[0] -self.x)) - self.o)/10
        if math.atan2(-(self.goal[1] -self.y) , -(self.goal[0] -self.x)) * self.o < 0 and abs(self.o > math.pi/2):
            move_o = (2*math.pi - abs(self.o) -abs(math.atan2(-(self.goal[1] -self.y) , -(self.goal[0] -self.x))))/10
        #print (math.atan2(-(self.goal[1] -self.y) , -(self.goal[0] -self.x))) 
        return move_x, move_y, move_o
    
    def assign_goal(self,followers):
        num = len(followers)
        virtual_points = []
        for i in range (1, num):
            virtual_points.append((self.x - l*i*math.cos(math.pi + FORMATION_ANGLE + self.o) , self.y - l*i*math.sin(math.pi + FORMATION_ANGLE + self.o) ))
            virtual_points.append((self.x - l*i*math.cos(math.pi - FORMATION_ANGLE + self.o) , self.y - l*i*math.sin(math.pi - FORMATION_ANGLE + self.o) ))
        
        for i in range (0, num):
            followers[i].goal = virtual_points[i]

    def limit_speed(self):
        speed = math.sqrt(self.vx**2 + self.vy**2)
        if speed > MAX_SPEED:
            self.x -= self.vx
            self.y -= self.vy 
            self.vx = (self.vx / speed) * MAX_SPEED
            self.vy = (self.vy / speed) * MAX_SPEED
            self.x += self.vx
            self.y += self.vy 
    
    def create_V_shape_followers(self, num):
        followers = []
        for i in range (1, num):
            followers.append(Robot(self.x + l*i*math.cos(math.pi + FORMATION_ANGLE + self.o) , self.y - l*i*math.sin(math.pi + FORMATION_ANGLE + self.o) , self.o))
            followers.append(Robot(self.x + l*i*math.cos(math.pi - FORMATION_ANGLE + self.o) , self.y - l*i*math.sin(math.pi - FORMATION_ANGLE + self.o) , self.o))
        return followers 
    

leader = Robot(400, 400 , 0)
followers = leader.create_V_shape_followers(4)

if __name__=="__main__":
    running = True
    while running:

        #screen color
        screen.fill(SCREEN_COLOR) 
        leader.assign_goal(followers)
        #exit condition
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                leader.goal = (mouse_x, mouse_y)
        leader.update()
        leader.limit_speed()
        for individual in followers:
            individual.update()
            individual.draw()
        leader.draw()


        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


    