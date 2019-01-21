import pygame
from pygame.sprite import Sprite

#remember, ask yourself when thinking about defining classes... are things a HAS A relationship
#or IS A relationship when thinking about including class attributes
#i.e a car IS A machine vs. a car HAS A battery - a battery should be it's own class because is isn't
#necesarily a unique attribute of a car.


class Ship(Sprite):

    '''Everything pertaining to the ship in the game'''

    def __init__(self, ai_settings,screen):
        '''Initialize the ship and set it's starting position'''
        super(Ship, self).__init__()

        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image and get its rect
        self.image = pygame.image.load('images/rocketShip.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #Start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #stores decimal value for the ship's center
        self.center = float(self.rect.centerx)

        #Movement Flag - allows for continuous movement of the ship since we set this to be True as long as
        #a directional key is pressed and returns to false when the key is release (see game_functions)
        self.moving_right = False
        self.moving_left = False



    def update(self):
        '''Update the ship's position based on the movement flag, in conjunction with the
        game_function method for movement allows for continuous movement'''
        #Update the ship's center value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        #Update the rect object from self.center
        self.rect.centerx = self.center

    def blitme(self):
        '''Draw the ship at its current location'''
        self.screen.blit(self.image,self.rect)


    def center_ship(self):
        '''Center the ship on the screen'''
        self.center = self.screen_rect.centerx
