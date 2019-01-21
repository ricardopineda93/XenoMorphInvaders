import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''Building a class to manage bullets fired from ship'''

    def __init__(self, ai_settings, screen, ship):
        '''Creating bullet object at ships current position'''
        super(Bullet, self).__init__()
        self.screen = screen

        #Create a bullet rect(angle) at (0,0) and then set the correct position
        self.rect = pygame.Rect(0,0,ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        #Store the bullets position as a decimal value
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        '''Move bullet up sreen'''
        #updating decimal position of the bullet
        self.y -= self.speed_factor
        #update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        '''Draw bullet on screen'''
        pygame.draw.rect(self.screen, self.color, self.rect)


