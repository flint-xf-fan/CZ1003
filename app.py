import pygame
import sys
import math
import pandas as pd

from canteen_class import Canteen

##### application configuration #####
FPS = 60
SIZE = (1024, 720)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

LIGHT_RED = (155, 0, 0)
LIGHT_GREEN = (0, 200, 0)

APP_NAME = 'APP NAME TO BE DECIDED'
CANTEENS_PATH = 'assets/canteens.csv'
MAP_PATH = 'assets/NTUCampus_google.png'


# necessary to display text to screen
def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()



##### functionalities #####
def get_user_pos(screen, time):
    """
    Makes the program halt for 'time' seconds or until the user performs the action.
    """
    clock = pygame.time.Clock()
    waiting = True
    print('Now click one point on the map to get your location')
    while waiting:
        dt = clock.tick(30) / 1000  # Takes the time between each loop and convert to seconds.
        time -= dt
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                user_pos = event.pos
                print('Your position is:', user_pos)
                waiting = False
                break

        if time <= 0:
            waiting = False

def distance_a_b(pos_a, pos_b):
    """ computes the absolute distance between pos_a and pos_b
    args:
        pos_a: (x, y) coords of a
        pos_b: (x, y) coords of b
    return:
        distance: absolute distance
    """
    return math.sqrt((pos_b[1] - pos_a[1])**2 + (pos_b[0] - pos_a[0])**2) 

def read_canteens(df):
    """
    args:
        df: canteens_df dataframe
    return:
        canteens_list: a list of canteen objects
    """
    # a list to store canteen objects
    canteens_list = []

    for _, row in df.iterrows():
        canteens_list.append(Canteen(row['name'],
                                     (row['pos_x'], row['pos_y']),
                                     row['review']))

    return canteens_list

def draw_canteens(screen, canteens_list, color=LIGHT_GREEN, radius=15):
    """
    args:
        screen: pygame screen object
        canteens_list: list of canteen objects
        positions: list of canteen positions in (x, y) coords
    """
    for i in range(len(canteens_list)):
        pos = canteens_list[i].pos
        # name = canteens_list[i].name
        pygame.draw.circle(screen, color, pos, radius)

##### main program #####
def main():
    # settings
    pygame.init()
    
    clock = pygame.time.Clock() 


    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption(APP_NAME)
    
    # load database(canteens.csv)
    canteens_df = pd.read_csv(CANTEENS_PATH)
    canteens_list = read_canteens(canteens_df) # a list of canteen objects
    

    map_img = pygame.image.load(MAP_PATH)
    map_x = 100 # maybe move up later
    map_y = 100

    button_x = 50
    button_y = 50
    button_w = 120
    button_h = 50
    button_getUserPos = pygame.Rect(button_x, button_y, button_w, button_h)  # creates a rect object

    # Loop until the user clicks the close button.
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # # obtain mouse position on click
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position

                # checks if mouse position is over the button

                if button_getUserPos.collidepoint(mouse_pos):
                    # ask the user to click a position on the map
                    get_user_pos(screen, 300)
                    
        ##### clean the screen #####
        screen.fill(WHITE)

        ##### app logic #####
        ### test ###
        # print(distance_a_b(canteen_positions[0], canteen_positions[1]))


        ##### drawing code goes here #####
        ### display the map ###
        screen.blit(map_img, (map_x, map_y))
        ### draw canteens on the map ###
        draw_canteens(screen, canteens_list)

        ### get_user_pos button ###
        mouse = pygame.mouse.get_pos()
        if button_x < mouse[0] < button_x+button_w and button_y < mouse[1] < button_y+button_h: # mouse hover the button
            pygame.draw.rect(screen, [255, 0, 0], button_getUserPos)
            button_text = pygame.font.Font("freesansbold.ttf", int(button_h/2.5))
        else:
            pygame.draw.rect(screen, [200, 0, 0], button_getUserPos)  # button
            button_text = pygame.font.Font("freesansbold.ttf", button_h//3)

        textSurf, textRect = text_objects("get_user_pos", button_text)
        textRect.center = (button_x+(button_w//2), button_y+(button_h//2))
        screen.blit(textSurf, textRect)
        

        
        
        pygame.display.update()
        clock.tick(FPS)
        # print('Running test')

    pygame.quit()
    sys.exit

if __name__ == '__main__':
    main()