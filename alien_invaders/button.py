import pygame.font

class Button():

    def __init__(self, ai_settings, screen, msg):
        '''Initialize button attributes'''
        self.screen = screen
        self.screen_rect = screen.get_rect()

        #setting dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = (25, 150, 0)
        self.text_color = (250, 250, 250)
        self.font = pygame.font.SysFont(None, 48)

        #building button's rect object and centering it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #button message only needs to be prepped one time
        self.prep_msg(msg)

    def prep_msg(self, msg):
        '''Turns msg into a rendered image of the text and centers the text on the button'''
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #draw the blank button and then draw the message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

