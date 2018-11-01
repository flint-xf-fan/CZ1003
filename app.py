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

# # to be discarded
# def text_objects(text, font):
#     textSurface = font.render(text, True, BLACK)
#     return textSurface, textSurface.get_rect()
            # button_text = pygame.font.Font("freesansbold.ttf", button_h//3)
        # textSurf, textRect = text_objects("Where am I?", button_text) ## maybe wrap those as a function
        # textRect.center = (button_x+(button_w//2), button_y+(button_h//2))
        # screen.blit(textSurf, textRect)

def draw_text(screen, pos, text, size=5, color=BLACK):
    # text_surface = pygame.font.Font(font, size).render(text, True, color)
    text_surface = pygame.font.SysFont("arial", size).render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = pos
    screen.blit(text_surface, text_rect)


##### functionalities #####
def get_user_pos(screen, time):
    """
    Makes the program halt for 'time' seconds or until the user performs the action.
    """
    clock = pygame.time.Clock()
    waiting = True
    print('Now click one point on the map to get your location')
    while waiting:
        dt = clock.tick(FPS) / 1000  # Takes the time between each loop and convert to seconds.
        time -= dt
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                user_pos = event.pos
                print('Your position is:', user_pos)
                #
                return user_pos
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
        canteens_list.append(Canteen(row['id'],
                                     row['name'],
                                     (row['pos_x'], row['pos_y']),
                                     row['food_type'],
                                     row['review']))

    return canteens_list

def draw_canteens(screen, canteens_list, color=LIGHT_GREEN, radius=15):
    """ draw circles to represent the canteens. 
    
    right now only draw the canteen id on top of it. because name can be too lengthy
    we may implement it an interactive button. So after the user clicks on it, we display the corresponding information
    
    args:
        screen: pygame screen object
        canteens_list: list of canteen objects
        positions: list of canteen positions in (x, y) coords

    returns:
        canteenButton_list: list of pygame.rect objects
    """
    canteenButton_list = []

    for i in range(len(canteens_list)):
        pos = canteens_list[i].pos
        name = canteens_list[i].name
        canteen_id = str(canteens_list[i].id)

        canteenButton_list.append(pygame.Rect(pos[0]-radius, pos[1]-radius, radius*2, radius*2))
        pygame.draw.circle(screen, color, pos, radius)
        draw_text(screen, pos, canteen_id, 10)    

    return canteenButton_list



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


    button_getUserPos_x = 50
    button_getUserPos_y = 50
    button_getUserPos_w = 120
    button_getUserPos_h = 50
    button_getUserPos = pygame.Rect(button_getUserPos_x, button_getUserPos_y, button_getUserPos_w, button_getUserPos_h)  # creates a rect object

    button_getNearestCanteen_x = 200
    button_getNearestCanteen_y = 50
    button_getNearestCanteen_w = 220
    button_getNearestCanteen_h = 50
    button_getNearesrCanteen = pygame.Rect(button_getNearestCanteen_x, button_getNearestCanteen_y, button_getNearestCanteen_w, button_getNearestCanteen_h)  # creates a rect object

    # Loop until the user clicks the close button.
    done = False
    dt = pygame.time.Clock().tick(FPS) / 1000
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # obtain mouse position on click
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position

                # check if mouse position is over the get_user_pos button
                if button_getUserPos.collidepoint(mouse_pos):
                    # ask the user to click a position on the map and store it for later use
                    user_pos = get_user_pos(screen, 10)
            
                # check if mouse position is over one of the canteen buttons(circle)
                if 'canteen_buttons' in locals():
                    for i, canteen_button in enumerate(canteen_buttons):
                        if canteen_button.collidepoint(mouse_pos):
                            # canteen_name_temp = canteens_list[i].name
                            # canteen_pos_temp = canteens_list[i].pos
                            # draw the information about the cateen near it
                            canteen_pressed_id = i
                            canteen_pressed_time = 5
                            print(canteens_list[i].name)
                            # draw_text(screen, (canteen_pos_temp[0]+20, canteen_pos_temp[1]), canteen_name_temp, 10, BLACK)


        ##### clean the screen #####
        screen.fill(WHITE)

        ##### app logic #####
        ### test ###
        # check if user_pos has been entered
        if 'user_pos' in locals():
            print(user_pos)


        ##### drawing code goes here #####
        ### display the map ###
        screen.blit(map_img, (map_x, map_y))
        ### draw canteens on the map ###
        canteen_buttons = draw_canteens(screen, canteens_list)
        ### show canteens information after user clicked the button/circle
        if 'canteen_pressed_id' in locals():
            
            
            id_temp = canteen_pressed_id
            canteen_name_temp = canteens_list[id_temp].name
            canteen_food_temp = canteens_list[id_temp].food_type
            canteen_review_temp = "Review: " + str(canteens_list[id_temp].review)
            canteen_pos_temp = canteens_list[id_temp].pos
            draw_text(screen, (canteen_pos_temp[0]+60, canteen_pos_temp[1]), canteen_name_temp, 10, BLACK)
            draw_text(screen, (canteen_pos_temp[0]+60, canteen_pos_temp[1]+10), canteen_food_temp, 10, BLACK)
            draw_text(screen, (canteen_pos_temp[0]+60, canteen_pos_temp[1]+20), canteen_review_temp, 10, BLACK)

            canteen_pressed_time -= dt
            # wait for 5s
            if canteen_pressed_time <= 0:
                del canteen_pressed_id

        ### get_user_pos button ###
        mouse = pygame.mouse.get_pos()
        if button_getUserPos_x < mouse[0] < button_getUserPos_x+button_getUserPos_w and button_getUserPos_y < mouse[1] < button_getUserPos_y+button_getUserPos_h: # mouse hover the button
            pygame.draw.rect(screen, [255, 0, 0], button_getUserPos)
            draw_text(screen, (button_getUserPos_x+(button_getUserPos_w//2), button_getUserPos_y+(button_getUserPos_h//2)), "Where am I?", int(button_getUserPos_h/2.5), color=BLACK)
        else:
            pygame.draw.rect(screen, [200, 0, 0], button_getUserPos)  # button
            draw_text(screen, (button_getUserPos_x+(button_getUserPos_w//2), button_getUserPos_y+(button_getUserPos_h//2)), "Where am I?", button_getUserPos_h//3, color=BLACK)


        ### get_nearest_canteen button ###
        if button_getNearestCanteen_x < mouse[0] < button_getNearestCanteen_x+button_getNearestCanteen_w and button_getNearestCanteen_y < mouse[1] < button_getNearestCanteen_y+button_getNearestCanteen_h: # mouse hover the button
            pygame.draw.rect(screen, [255, 0, 0], button_getNearesrCanteen)
            draw_text(screen, (button_getNearestCanteen_x+(button_getNearestCanteen_w//2), button_getNearestCanteen_y+(button_getNearestCanteen_h//2)), "The nearest canteen?", int(button_getNearestCanteen_h/2.5), color=BLACK)
        else:
            pygame.draw.rect(screen, [200, 0, 0], button_getNearesrCanteen)  # button
            draw_text(screen, (button_getNearestCanteen_x+(button_getNearestCanteen_w//2), button_getNearestCanteen_y+(button_getNearestCanteen_h//2)), "The nearest canteen?", button_getNearestCanteen_h//3, color=BLACK)

        
        
        pygame.display.update()
        clock.tick(FPS)
        # print('Running test')

    pygame.quit()
    sys.exit

if __name__ == '__main__':
    main()