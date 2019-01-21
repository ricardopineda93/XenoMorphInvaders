import sys
from time import sleep
import json

import pygame

from bullets import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, stats, screen, sb, ship, aliens, bullets):#moves ship to the right/left when right arrow key pressed, stops when released
    # this is done by using the class method to incite this within the class itself rather than from outside the class
    '''Respond to key presses'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, stats, ship, bullets)
    #allowing the game to start by just pressing 'P'
    elif event.key == pygame.K_p:
        p_to_start(ai_settings, screen, stats, sb, ship, aliens, bullets)
    #allowing the game to restart by pressing 'R'
    elif event.key == pygame.K_r:
        r_to_restart(ai_settings, screen, stats, sb, ship, aliens, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings, screen, stats, ship, bullets):
    # creating new bullet and adding to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

    #Counts the number of times a bullet is fired (since this function only occurs when
    #space bar is hit).
    stats.bullets_fired += 1


def check_keyup_events(event, ship):
    '''Respond to key releases'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    '''Respond to mouse press and keypresses'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, stats, screen, sb, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    '''Start a new game when the player hits PLAY button'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #reset game diffuclty settings
        ai_settings.initialize_dynamic_settings()
        #make the mouse cursor invisible
        pygame.mouse.set_visible(False)
        #reseting game statistics
        stats.reset_stats()
        stats.game_active = True

        #Reset the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        sb.prep_accuracy()

        #empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def p_to_start(ai_settings, screen, stats, sb, ship, aliens, bullets):

    if not stats.game_active:
        #reset game diffuclty settings
        ai_settings.initialize_dynamic_settings()
        #make the mouse cursor invisible
        pygame.mouse.set_visible(False)
        #reseting game statistics
        stats.reset_stats()
        stats.game_active = True

        #Reset the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        sb.prep_accuracy()

        #empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

#Using the 'R' button to restart the game
def r_to_restart(ai_settings, screen, stats, sb, ship, aliens, bullets):

    # reset game diffuclty settings
    ai_settings.initialize_dynamic_settings()
    # make the mouse cursor invisible
    pygame.mouse.set_visible(False)
    # reseting game statistics
    stats.reset_stats()
    stats.game_active = True

    # Reset the scoreboard images
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()
    sb.prep_accuracy()

    # empty the list of aliens and bullets
    aliens.empty()
    bullets.empty()

    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Update position of bullets and gets rid of old bullets'''
    bullets.update()

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


    # getting rid of old bullets that go beyond the top of the screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            sb.prep_accuracy()
    #print(len(bullets)) #- this was to test to see if the bullets were disappearing, would constantly
    # print the number of active bullets in the terminal

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # Check is bullets have hit aliens - and if so get rid of both bullet and alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        '''Since the collisions variable creates a dictionary where each bullet fired is a key and
        the value is the list of all aliens colliding with that bullet, the below operates on
        the values (list of aliens hit) for each bullet key in the collisions dict to multiply our point values by the length of
        the list of aliens hit by the bullet.'''
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            stats.aliens_hit += len(aliens)

            sb.prep_score()
            sb.prep_accuracy()

        check_high_score(stats, sb)

    if len(aliens) == 0:
        #Destroy any bullets remaining on screen
        bullets.empty()
        #speeds up game everytime the entire fleet is destroyed
        ai_settings.increase_speed()
        #Increase level
        stats.level += 1
        sb.prep_level()
        #refill screen with new enemy fleet
        create_fleet(ai_settings, screen, ship, aliens)

def get_number_aliens_x(ai_settings, alien_width):
    #how much space avail in a row given we'd like 1 alien's width between the edges of the screen
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    # how many aliens fit in a row given we'd like 1 alien's width of space between each alien to it's right
    number_aliens_x = int(available_space_x / (2 * alien_width)) # we use in here because we don't want partial numbers of aliens to be created
    #and so by using int() it drops the . and rounds down to the nearest whole number, which in this case is good because we are left
    #with a little extra wiggle space on the screen
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    '''Determine number of rows of aliens that can fit on screen'''
    #We detemine available row space by factoring in that we want 1 aliens height space from the top of the screen and
    #2 aliens heights space from bottom as well as the ship's height from bottom of screen as well
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    #Now that we know how much row space we have, we deduce how many rows of aliens we can fit given 1 alien's height
    #plus the fact that we want one alien's height of space between rows.
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # Create an alien and place it in the row to the group of aliens
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + (2 * alien.rect.height * row_number)
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    '''Creating the alien fleet'''
    #Create an alien and find the number of aliens in a row
    #Spacing between each alien is equal to one alien width
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)


    #Create the first row of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)


def check_fleet_edges(ai_settings, aliens):
    '''Respond appropriately if any aliens have reached an edge'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    '''Drop entire fleet and change fleet's direction'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1 #very clever! This will alternate the direction value for horizontal movement between 1 and
    #-1 every time we hit the edge Very very clever, take note of this kind of thinking.


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Check to see if fleet is at edge of screen'''
    check_fleet_edges(ai_settings, aliens)

    '''Update positions of all aliens in the fleet'''
    aliens.update()

    #Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        print("FUCK OUTTA HERE.")
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Respond to ship being hit by alien'''

    if stats.ships_left > 0:
        #Decrement ships available by 1
        stats.ships_left -= 1

        #Update scoreboard
        sb.prep_ships()

        #Emptying the list of bullets and aliens
        aliens.empty()
        bullets.empty()

        #create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #pause game briefly after being hit
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Check if any aliens have reached the bottom of the screen'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            '''Treats as if aliens hit ship, pauses game and resets'''
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def check_high_score(stats, sb):
    '''Check to see if there is a new high score'''

    high_score_file = 'high_score.txt'

    if stats.score > stats.high_score():

        try:
            with open(high_score_file, 'w') as f_obj:
                json.dump(stats.score, f_obj)
        except:
            pass

        sb.prep_high_score()



def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button): #these are all defined elsewhere but come together in the main code file...clever
    '''Update images on the screen and flip to the new screen'''
    #i.e. redraws the screen during each pass of the loop
    screen.fill(ai_settings.bg_color)

    #redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    #draw the score info
    sb.show_score()

    # Draw play button only if game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    #makes the most recently drawn screen visible
    pygame.display.flip()