import pygame.font
from pygame.sprite import Group


from rocketship import Ship

class Scoreboard():
    '''A class to report all scoring information'''

    def __init__(self, ai_settings, screen, stats):
        '''Initialize  scoreboard attributes'''
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        #Font settings for scoreboard
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 28)

        #Prepping the inital score image
        self.prep_score()

        #Prepping High Score image
        self.prep_high_score()

        #Prepping current level image
        self.prep_level()

        #prep images of ships to display as lives
        self.prep_ships()

        #prep accuracy %
        self.prep_accuracy()

    def prep_score(self):
        '''Turns the score into a rendered image'''

        #rounds score to nearest 10
        rounded_score = round(self.stats.score, -1)
        #below will convert the number into a string and format
        #such that there is a 0 between significant 0s, i.e. 1,000 .. 1,000,00
        score_str = "SCORE: " + "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        #Displaying the scoreboard on the top right of screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = self.score_rect.top


    def prep_high_score(self):
        '''Turning the high score into a rendered image'''
        high_score = round(self.stats.high_score(), -1)
        high_score_str = "HI SCORE: " + "{:,}".format(high_score)

        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)

        #Having the high score on the far right of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.high_score_rect.top

    def prep_level(self):
        '''Turn level into rendered image'''
        level_str = "LEVEL " + str(self.stats.level)

        self.level_image = self.font.render(level_str, True, self.text_color, self.ai_settings.bg_color)

        #Position level at center of screen
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom

    def prep_ships(self):
        '''Show how many ships are left'''
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 0
            self.ships.add(ship)

    def prep_accuracy(self):
        '''Display accuracy % of player'''
        try:
            accuracy = round(self.stats.aliens_hit/self.stats.bullets_fired * 100, 2)
        except ZeroDivisionError:
            accuracy = 0.00

        accuracy_str = "{}%".format(accuracy)

        self.accuracy_image = self.font.render(accuracy_str, True, self.text_color, self.ai_settings.bg_color)

        # Position level at center of screen
        self.accuracy_rect = self.accuracy_image.get_rect()
        self.accuracy_rect.left = self.accuracy_rect.left + 10
        self.accuracy_rect.top = self.level_rect.bottom


    def show_score(self):
        '''Draw score to the screen'''
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.accuracy_image, self.accuracy_rect)

        self.ships.draw(self.screen)
