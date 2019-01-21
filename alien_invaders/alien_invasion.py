#import sys -->because this is only being used for the check_events function and we have
#this in another module and imported, we don't need this imported here
import pygame
from pygame.sprite import Group

from settings import Settings
from rocketship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():

    #Initialize game and create a screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))

    pygame.display.set_caption('ALIEN INVASION')

    #Make the play button
    play_button = Button(ai_settings, screen, 'ESKETIT.')

    #creating an instance to store game statistics and create the scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    #Make a ship
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    #creating the alien fleet
    gf.create_fleet(ai_settings, screen, ship, aliens)

    #Start main loop for game.
    while True:

            #Respond to mouse press and keypresses
            gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

            #checks to see if game active flag is still true and runs the following code if so
            #run the active elements of the game. If not, the active elements such as ship positioning,
            #movement, bullets etc. are stopped. However, we still want the 'behind the scenes' elements to still
            #be active at all times like being able to quit the game, choosing to start new game, etc, so we
            #leave those out of this IF block because we always want that to run.
            if stats.game_active:
                #controls the ships movement
                ship.update()

                #controls bullets
                bullets.update()


                #getting rid of old bullets that go beyond the top of the screen
                gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)

                #controls alien movement
                gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)

                #print(ai_settings.ship_limit)

            #redraw the screen through each pass of the loop:
            gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


run_game()

