import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''A class to represent a single alien in the fleet'''

    def __init__(self, ai_settings, screen):
        '''Initialize alien and set it's starting position'''
        super(Alien,self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #Load alien image and set it's rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        #start each alien near top left of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #store alien's exact position
        self.x = float(self.rect.x)


    def check_edges(self):
        '''return TRUE is alien is at the edge of screen'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True


    def update(self):
        '''Move alien to the right'''
        self.x += (self.ai_settings.alien_speed_factor *
            self.ai_settings.fleet_direction)

        self.rect.x = self.x


    def blitme(self):
        '''Draw alien at it's current location'''
        self.screen.blit(self.image, self.rect)



