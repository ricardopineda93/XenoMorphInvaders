class Settings():
    '''THis class stores all settings to the Alien Invaders game'''

    def __init__(self):
        '''Initialize game settings'''
        #Screen Settings:
        self.screen_width = 1000
        self.screen_height = 800
        self.bg_color = (240,150,180)

        #Ship setting as the pertain to the game as a whole
        self.ship_limit = 3


        #Bullet Settings

        self.bullet_width = 10
        self.bullet_height = 15
        self.bullet_color = 60,190,60
        self.bullets_allowed = 8 #limits the number of bullets allowed to be on screen at once

        #Alien settings

        self.fleet_drop_speed = 10

        #how quickly the game speeds up per destroyed fleet
        self.speedup_scale = 1.25
        #how much more points each alien is worth per destroyed fleet cycle
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''Initialize settings that change throughout the game'''
        self.ship_speed_factor = 2.85
        self.bullet_speed_factor = 4.25
        self.alien_speed_factor = 1
        # fleet direction of 1 represents right, -1 represents left
        self.fleet_direction = 1

        #Scoring per alien hit
        self.alien_points = 50

    def increase_speed(self):
        '''Increase speed settings and point values'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)





