import pygame
import sys
import math
import pandas as pd

from utils import *

from canteen_class import Canteen, InputBox, userInput_food, userInput_price



APP_NAME = 'EatWhere'
CANTEENS_PATH = 'assets/canteens.csv'
MAP_PATH = 'assets/NTUCampus.png'
msg = 'Welcome to EatWhere' # welcome message 
msg_coords = [1200, 420]

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
                                     row['location'],
                                     (row['pos_x'], row['pos_y']),
                                     row['food_types'].lower(),
                                     row['opening_closing_times'],
                                     row['rating'],
                                     row['min_price'],
                                     row['max_price']))

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
        canteen_id = str(canteens_list[i].id)

        canteenButton_list.append(pygame.Rect(pos[0]-radius, pos[1]-radius, radius*2, radius*2))
        pygame.draw.circle(screen, color, pos, radius)
        # draw_text(screen, pos, canteen_id, 10)

    return canteenButton_list



##### main program #####
def main():
    global msg
    # settings
    pygame.init()

    clock = pygame.time.Clock()


    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption(APP_NAME)

    # load database(canteens.csv)
    canteens_df = pd.read_csv(CANTEENS_PATH)
    canteens_list = read_canteens(canteens_df) # a list of canteen objects


    map_img = pygame.image.load(MAP_PATH)

    # maybe move up or move to a separate configure file
    map_x = 0
    map_y = 0

    # button to ask user to select location on the map
    button_getUserPos_coords = [1097, 0, 220, 50]
    button_getUserPos = pygame.Rect(button_getUserPos_coords[0], button_getUserPos_coords[1], button_getUserPos_coords[2], button_getUserPos_coords[3])

    # button to get the nearest canteen
    button_getNearestCanteen_coords = [1097, 50, 220, 50]
    button_getNearesrCanteen = pygame.Rect(button_getNearestCanteen_coords[0], button_getNearestCanteen_coords[1], button_getNearestCanteen_coords[2], button_getNearestCanteen_coords[3])

    # button to sort canteens by (absolute) distance
    button_sortByDistance_coords = [1097, 100, 220, 50]
    button_sortByDistance = pygame.Rect(button_sortByDistance_coords[0],button_sortByDistance_coords[1],button_sortByDistance_coords[2],button_sortByDistance_coords[3])

    # button to sort canteens by Rating
    button_sortByRating_coords = [1097, 150, 220, 50]
    button_sortByRating = pygame.Rect(button_sortByRating_coords[0],button_sortByRating_coords[1],button_sortByRating_coords[2],button_sortByRating_coords[3])

    ## box input
    label_foodType_coords = [1200, 220, 220, 30]
    box_foodType_coords = [1097, 240, 220, 50]
    box_foodType = InputBox(box_foodType_coords[0],box_foodType_coords[1],box_foodType_coords[2],box_foodType_coords[3], userInput_food)

    label_price_coords = [1200, 320, 220, 30]
    box_price_coords = [1097, 340, 220, 50]
    box_price = InputBox(box_price_coords[0],box_price_coords[1],box_price_coords[2],box_price_coords[3], userInput_price)
    # Loop until the user clicks the close button.
    done = False
    dt = pygame.time.Clock().tick(FPS) / 1000
    while not done:

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                done = True

            # obtain mouse position on click
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position

                # if get_user_pos button is pressed
                if button_getUserPos.collidepoint(mouse_pos):
                    
                    # ask the user to click a position on the map and store it for later use
                    print('Now click one point on the map to get your location')
                    try:
                        user_pos = get_user_pos(screen, 10)
                        msg = 'Your location is '+ '({}, {})'.format(user_pos[0],user_pos[1])
                    except:
                        msg = 'You did not click any position'
                # if button is pressed
                if button_getNearesrCanteen.collidepoint(mouse_pos):
                    try:
                        assert 'user_pos' in locals()
                        msg = get_nearest_canteen(user_pos, canteens_list).name
                        # msg.insert(0, "The nearest canteen to your position is:")
                        pass
                    except:
                        msg = ['You did not input your position.',
                               'Please click the first button']

                # if sort_by_distance button is pressed
                if button_sortByDistance.collidepoint(mouse_pos):
                    try:
                        assert 'user_pos' in locals()
                        msg = sort_canteens_by_attr(canteens_list, attr='distance', user_pos=user_pos, k=12)
                        pass
                    except:
                        msg = ['You did not input your position.',
                               'Please click the first button']

                # if sort_by_rating button is pressed
                if button_sortByRating.collidepoint(mouse_pos):
                    msg = sort_canteens_by_attr(canteens_list, attr='rating', k=12)
                    # msg.insert(0, 'The rank of best canteens')
                    pass


                # check if mouse position is over one of the canteen buttons(circle)
                if 'canteen_buttons' in locals():
                    for i, canteen_button in enumerate(canteen_buttons):
                        if canteen_button.collidepoint(mouse_pos):
                            # draw the information about the cateen near it
                            canteen_pressed_id = i
                            canteen_pressed_time = 3
                            # print(canteens_list[i].name)

            box_foodType.handle_event(event)
            box_price.handle_event(event)
        ##### clean the screen #####
        screen.fill(WHITE)

        ##### app logic #####
        
        
        ### user input after entern is pressed comes here
        if userInput_food:
            # screen.fill(WHITE)
            userInput_str = userInput_food[0]
            msg = search_foodType(userInput_str, canteens_list)
            _ = userInput_food.pop()

        if userInput_price:
            # screen.fill(WHITE)
            userInput_str = userInput_price[0]
            msg = 'price box display test' # print(search_foodType(userInput_str, canteens_list))
            _ = userInput_price.pop()

        ##### drawing code goes here #####

        # Feed the box_input with events every frame
        box_price.update()
        box_foodType.update()

        box_foodType.draw(screen)
        box_price.draw(screen)
        draw_text(screen, (label_foodType_coords[0],label_foodType_coords[1]),
                 'Search By Food Type', size=20, color=BLACK)



        draw_text(screen, (label_price_coords[0],label_price_coords[1]),
                 'Search By Price', size=20, color=BLACK)

        ### display the map ###
        screen.blit(map_img, (map_x, map_y))
        ### draw canteens on the map ###
        canteen_buttons = draw_canteens(screen, canteens_list)

        # draw message to the screen
        draw_message(screen, (1200, 420), msg, 15, BLACK)

        ### show canteens information after user clicked the button/circle
        if 'canteen_pressed_id' in locals():
            id_temp = canteen_pressed_id

            canteen_pos_temp = canteens_list[id_temp].pos
            line_space = 0
            for attr, value in canteens_list[id_temp].__dict__.items():
                # print(attr)
                if not attr in ['id', 'pos', 'min_price', 'max_price']: # no data for food_types yet
                    draw_text(screen,
                            (canteen_pos_temp[0]+60, canteen_pos_temp[1]+line_space),
                            value,
                            20, BLACK)
                    line_space += 20

            canteen_pressed_time -= dt
            # wait for 3s
            if canteen_pressed_time <= 0:
                del canteen_pressed_id

        ### draw interactive buttons ###
        mouse = pygame.mouse.get_pos()

        draw_button(screen, button_getUserPos, button_getUserPos_coords, mouse, 'Where am I?', GREEN, RED, BLACK)
        draw_button(screen, button_getNearesrCanteen, button_getNearestCanteen_coords, mouse, 'The nearest canteen?', GREEN, RED, BLACK)
        draw_button(screen, button_sortByDistance, button_sortByDistance_coords, mouse, 'Sort by Distance', GREEN, RED, BLACK)
        draw_button(screen, button_sortByRating, button_sortByRating_coords, mouse, 'Sort by Rating', GREEN, RED, BLACK)

        pygame.display.update()
        clock.tick(FPS)
        # print('Running test')

    pygame.quit()
    sys.exit


if __name__ == '__main__':
    main()