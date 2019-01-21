import json


class GameStats():
    '''Track statistics for game'''

    def __init__(self, ai_settings):
        '''initialize settings'''

        self.ai_settings = ai_settings
        #Calculating in-game accuracy

        self.reset_stats()

        #start the game in an inactive state so the player has to press "play' to begin
        self.game_active = False

        #Highscore should never be reset
        self.high_score()


    def reset_stats(self):
        '''initialize statistics that can be changed during the game'''
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

        '''Stats needed to calculate accuracy % in-game'''
        self.bullets_fired = 0
        self.aliens_hit = 0



    def high_score(self):

        high_score_file = 'high_score.txt'


        try:
            with open(high_score_file, 'r') as f_obj:
                return int(json.load(f_obj))
        except:
                return 0

