import pygame, sys, time, random, json, math
from pygame.locals import *

PLAYERS = 3


pygame.init()
WIDTH, HEIGHT = 800, 500
surface=pygame.display.set_mode((WIDTH, HEIGHT),0,32)
fps=64
ft=pygame.time.Clock()
pygame.display.set_caption("Un Cover")

class Bullet:
    def __init__(self):
        self.length = 30
        self.thickness = 2
        self.top_y = 0

class Gun:
    def __init__(self):
        self.bullets = []
        self.length = 40
        self.top_y = 400
        self.x = -100
        self.width = 10
        self.is_shooting = 0
        self.shooting_duration = 6
    def shoot(self):
        new_bullet = Bullet()
        new_bullet.top_y = self.top_y
        self.bullets.append(new_bullet)
        self.is_shooting = self.shooting_duration

class App:
    def __init__(self, surface):
        self.surface = surface
        self.play = True
        self.mouse=pygame.mouse.get_pos()
        self.click=pygame.mouse.get_pressed()
        self.color = {
            "background": (77, 50, 39),
            "alpha": (205, 119, 0),
            "beta": (235, 201, 153)
        }
        self.guns = []
        self.no_of_guns = PLAYERS
        self.initialize_guns()
        self.cursor = 0
    def initialize_guns(self):
        self.guns = []
        space_each_player_occupies = WIDTH//self.no_of_guns
        offset_for_each_gun = space_each_player_occupies//2
        for index in range(self.no_of_guns):
            x = (index*space_each_player_occupies)+offset_for_each_gun
            new_gun = Gun()
            new_gun.x = x
            self.guns.append(new_gun)
    def render(self):
        for index in range(len(self.guns)):
            gun = self.guns[index]
            x1 = gun.x-(gun.width//4)
            if gun.is_shooting>0:
                pygame.draw.rect(self.surface, self.color["alpha"], (x1, gun.top_y+(gun.length//4), gun.width//2, gun.length//2))
                self.guns[index].is_shooting -= 1
            else:
                pygame.draw.rect(self.surface, self.color["alpha"], (x1, gun.top_y, gun.width//2, gun.length))
            x2 = gun.x-(gun.width//2)
            pygame.draw.rect(self.surface, self.color["alpha"], (x2, gun.top_y+(gun.length//2), gun.width, gun.length//2))
    def shoot(self):
        self.guns[self.cursor].shoot()
    def move_cursor(self, direction):
        self.cursor = (self.cursor+direction)%self.no_of_guns
    def run(self):
        while self.play:
            self.surface.fill(self.color["background"])
            self.mouse=pygame.mouse.get_pos()
            self.click=pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==KEYDOWN:
                    if event.key==K_TAB:
                        self.play=False
                    elif event.key==K_SPACE:
                        self.shoot()
                    elif event.key==K_RIGHT:
                        self.move_cursor(1)
                    elif event.key==K_LEFT:
                        self.move_cursor(-1)
            #--------------------------------------------------------------
            self.render()
            # -------------------------------------------------------------
            pygame.display.update()
            ft.tick(fps)



if  __name__ == "__main__":
    app = App(surface)
    app.run()


