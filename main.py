
import pygame, sys, time, random, json, math
from pygame.locals import *

PLAYERS = 4
RANGE = 20, 40


pygame.init()
WIDTH, HEIGHT = 800, 500
surface=pygame.display.set_mode((WIDTH, HEIGHT),0,32)
fps=64
ft=pygame.time.Clock()
pygame.display.set_caption("Un-Cover")

myfont = pygame.font.SysFont('Arial', 73)

class Bullet:
    def __init__(self):
        self.length = 30
        self.thickness = 2
        self.top_y = 0
        self.speed = 10
    def move(self):
        self.top_y -= self.speed
    def is_destroyable(self, destroy_level_y):
        if self.top_y<=destroy_level_y:
            return True
        return False

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
    def destroy_wasted_bullets(self, destroy_level_y):
        no_of_hits = 0
        new_bullet_list = []
        for bullet_index in range(len(self.bullets)):
            if self.bullets[bullet_index].is_destroyable(destroy_level_y):
                no_of_hits += 1
            else:
                new_bullet_list.append(self.bullets[bullet_index])
        self.bullets = new_bullet_list[:]
        return no_of_hits


class App:
    def __init__(self, surface):
        self.surface = surface
        self.play = True
        self.mouse=pygame.mouse.get_pos()
        self.click=pygame.mouse.get_pressed()
        self.color = {
            "background": (77, 50, 39),
            "alpha": (205, 119, 0),
            "beta": (235, 201, 153),
            "shield": (40, 30, 30)
        }
        self.guns = []
        self.no_of_guns = PLAYERS
        self.initialize_guns()
        self.cursor = random.randint(0, PLAYERS-1)
        self.shield_top_y = 50
        self.shield_unit_thickness = 3
        self.shield_height = random.randint(RANGE[0], RANGE[0])*self.shield_unit_thickness
        self.shield_offset = 30
        self.loser = None
        self.last_shot_by = None
        self.pointer_plate_y = 470
        self.pointer_plate_width = 80
        self.pointer_plate_height = 10
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
            # drawing bullets
            for bullet in gun.bullets:
                y1 = bullet.top_y
                y2 = bullet.length + y1
                x = gun.x
                pygame.draw.line(self.surface, self.color["beta"], (x, y1), (x, y2), 1)
            # draw gun
            x1 = gun.x-(gun.width//4)
            if gun.is_shooting>0:
                pygame.draw.rect(self.surface, self.color["alpha"], (x1, gun.top_y+(gun.length//4), gun.width//2, gun.length//2))
                self.guns[index].is_shooting -= 1
            else:
                pygame.draw.rect(self.surface, self.color["alpha"], (x1, gun.top_y, gun.width//2, gun.length))
            x2 = gun.x-(gun.width//2)
            pygame.draw.rect(self.surface, self.color["alpha"], (x2, gun.top_y+(gun.length//2), gun.width, gun.length//2))
        # draw shield
        pygame.draw.rect(self.surface, self.color["shield"], (self.shield_offset, self.shield_top_y, WIDTH-(2*self.shield_offset), self.shield_height))
        # draw cursor
        pygame.draw.rect(self.surface, self.color["alpha"], (self.guns[self.cursor].x-(self.pointer_plate_width//2), self.pointer_plate_y-(self.pointer_plate_height//2), self.pointer_plate_width, self.pointer_plate_height))
    def shoot(self):
        self.guns[self.cursor].shoot()
        self.last_shot_by = self.cursor
    def move_bullets(self):
        total_hits = 0
        for gun_index in range(len(self.guns)):
            for bullet_index in range(len(self.guns[gun_index].bullets)):
                self.guns[gun_index].bullets[bullet_index].move()
            no_of_hits = self.guns[gun_index].destroy_wasted_bullets(self.shield_top_y+self.shield_height)
            total_hits += no_of_hits
        self.shield_height -= (total_hits*self.shield_unit_thickness)
        if self.shield_height<=0:
            self.loser = self.cursor + 1
    def actions(self):
        self.move_bullets()
    def move_cursor(self, direction):
        if self.cursor==self.last_shot_by:
            self.cursor = (self.cursor+direction)%self.no_of_guns
    def show_loser(self):
        message = "LOSER  "+str(self.loser)
        textsurface = myfont.render(message, True, self.color["alpha"])
        self.surface.blit(textsurface,(220,180))
    def reset(self):
        self.shield_height = random.randint(RANGE[0], RANGE[0])*self.shield_unit_thickness
        self.loser = None
    def main(self):
        if self.loser is None:
            self.render()
            self.actions()
        else:
            self.show_loser()
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
                        if self.loser is None:
                            self.shoot()
                        else:
                            self.reset()
                    elif event.key==K_RIGHT:
                        self.move_cursor(1)
                    elif event.key==K_LEFT:
                        pass
            #--------------------------------------------------------------
            self.main()
            # -------------------------------------------------------------
            pygame.display.update()
            ft.tick(fps)



if  __name__ == "__main__":
    app = App(surface)
    app.run()


