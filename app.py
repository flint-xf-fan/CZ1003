import pygame
import sys
import math
import pandas as pd

# import * from utils

from canteen_class import Canteen, InputBox, userInput_food, userInput_price

##### application configuration #####
FPS = 60
SIZE = (1317, 794)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

LIGHT_RED = (155, 0, 0)
LIGHT_GREEN = (0, 200, 0)

APP_NAME = 'APP NAME TO BE DECIDED'
CANTEENS_PATH = 'assets/canteens.csv'
MAP_PATH = 'assets/NTUCampus.png'


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

    ToDo:
        * limit the user to only click any point within the map.
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
                # waiting = False
                # break

        if time <= 0:
            waiting = False


def get_distance_a_b(pos_a, pos_b):
    """ computes the absolute distance between pos_a and pos_b
    args:
        pos_a: (x, y) coords of a
        pos_b: (x, y) coords of b
    return:
        distance: absolute distance
    """
    return math.sqrt((pos_b[1] - pos_a[1])**2 + (pos_b[0] - pos_a[0])**2) 

def get_nearest_canteen(user_pos, canteens_list):
    min_distance = float('inf')
    # min_dist_canteen = canteens_list[0].name
    for canteen in canteens_list:
        d = get_distance_a_b(user_pos, canteen.pos)
        if d < min_distance:
            min_dist_canteen = canteen
            min_distance = d
    return min_dist_canteen


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
                                     row['price_range']))

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
        draw_text(screen, pos, canteen_id, 10)    

    return canteenButton_list

def search_foodType(user_input, canteens_list):
    """
    """
    # try:
        # assert user_input.lower() in ['mala', 'sandwich', 'thai', 'burgers', 'halal', 'western', 'noodles', 'fast food', 'korean', 'hala', 'japanese', 'drinks', 'chinese', 'pizza', 'vegetarian', 'pasteries', 'indonesian', 'bread', 'vietnamese', 'steamboat', 'indian', 'soup', 'pancakes']
    search_results = []
    # print(user_input)
    for canteen in canteens_list:
        food_types_list = canteen.food_types.split(',')
        # print(food_types_list)
        if user_input.lower() in food_types_list:
            search_results.append(canteen.name)

    return search_results
    # except:
        # pass
    

# def search_price(user_input, canteens_list):
#     """
#     """
#     search_results = []
#     try:
#         assert 


def sort_canteens_by_attr(canteens_list, attr='distance', user_pos=None, k=5):
    """
    args:
        user_pos:
        canteens_list:
        attr: distance or rating
        k: top k canteens to be returned
    """
    if attr == 'distance':
        canteens_list_sorted = sorted(canteens_list, key=lambda x: get_distance_a_b(user_pos, x.pos))
    else:
        # the format of canteen.rating is 4/5
        canteens_list_sorted = sorted(canteens_list, key=lambda x: x.rating.split('/')[0], reverse=True)
    return [(canteens_list_sorted[i].name, canteens_list_sorted[i].rating) for i in range(k)]

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

    # maybe move up or move to a separate configure file
    map_x = 0 
    map_y = 0

    # button to ask user to select location on the map
    button_getUserPos_coords = [1097, 0, 220, 50]
    button_getUserPos = pygame.Rect(button_getUserPos_coords[0], button_getUserPos_coords[1], button_getUserPos_coords[2], button_getUserPos_coords[3])

    # button to get the nearest canteen
    button_getNearestCanteen_coords = [1020, 50, 220, 50]
    button_getNearesrCanteen = pygame.Rect(button_getNearestCanteen_coords[0], button_getNearestCanteen_coords[1], button_getNearestCanteen_coords[2], button_getNearestCanteen_coords[3])

    # button to sort canteens by (absolute) distance
    button_sortByDistance_coords = [1020, 100, 220, 50]
    button_sortByDistance = pygame.Rect(button_sortByDistance_coords[0],button_sortByDistance_coords[1],button_sortByDistance_coords[2],button_sortByDistance_coords[3])

    # button to sort canteens by Rating
    button_sortByRating_coords = [1020, 150, 220, 50]
    button_sortByRating = pygame.Rect(button_sortByRating_coords[0],button_sortByRating_coords[1],button_sortByRating_coords[2],button_sortByRating_coords[3])

    ## box input
    label_foodType_coords = [1020, 300, 220, 30]
    box_foodType_coords = [1020, 350, 220, 50]
    box_foodType = InputBox(box_foodType_coords[0],box_foodType_coords[1],box_foodType_coords[2],box_foodType_coords[3], userInput_food)

    label_price_coords = [1020, 400, 220, 30]
    box_price_coords = [1020, 450, 220, 50]
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
                    user_pos = get_user_pos(screen, 10)

                # if get_user_pos button is pressed
                if button_getNearesrCanteen.collidepoint(mouse_pos):
                    try:
                        assert 'user_pos' in locals()
                        print("The nearest canteen to your position is:", get_nearest_canteen(user_pos, canteens_list).name)
                        pass
                    except:
                        print('You have not input your position yet.')

                # if sort_by_distance button is pressed
                if button_sortByDistance.collidepoint(mouse_pos):
                    try:
                        assert 'user_pos' in locals()
                        print("The nearest 5 canteens are:", sort_canteens_by_attr(canteens_list, attr='distance', user_pos=user_pos, k=5))
                        pass
                    except:
                        print('You have not input your position yet.')

                # if sort_by_rating button is pressed
                if button_sortByRating.collidepoint(mouse_pos):
                    print("The top 5 canteens by ratings are:", sort_canteens_by_attr(canteens_list, attr='rating', k=5))
                    pass


                # check if mouse position is over one of the canteen buttons(circle)
                if 'canteen_buttons' in locals():
                    for i, canteen_button in enumerate(canteen_buttons):
                        if canteen_button.collidepoint(mouse_pos):
                            # canteen_name_temp = canteens_list[i].name
                            # canteen_pos_temp = canteens_list[i].pos
                            # draw the information about the cateen near it
                            canteen_pressed_id = i
                            canteen_pressed_time = 3
                            print(canteens_list[i].name)
                            # draw_text(screen, (canteen_pos_temp[0]+20, canteen_pos_temp[1]), canteen_name_temp, 10, BLACK)

            box_foodType.handle_event(event)
            box_price.handle_event(event)
        ##### clean the screen #####
        screen.fill(WHITE)

        ##### app logic #####
        

        ### user input after entern is pressed comes here
        if userInput_food:
            userInput_str = userInput_food[0]
            print(search_foodType(userInput_str, canteens_list))
            _ = userInput_food.pop()
            
        if userInput_price:
            userInput_str = userInput_price[0]
            print('price search box tested')
            # print(search_foodType(userInput_str, canteens_list))
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

        i = 1
        for canteen_test in canteens_list:
            draw_text(screen, (1200, 600+i*12), canteen_test.name, 12)
            i += 1

        ### show canteens information after user clicked the button/circle
        if 'canteen_pressed_id' in locals():
            id_temp = canteen_pressed_id

            canteen_pos_temp = canteens_list[id_temp].pos
            line_space = 5
            for attr, value in canteens_list[id_temp].__dict__.items():
                # print(attr)
                if not attr in ['id', 'pos', 'food_types']: # no data for food_types yet
                    draw_text(screen, 
                            (canteen_pos_temp[0]+60, canteen_pos_temp[1]+line_space),
                            value,
                            10, BLACK)
                    line_space += 10

            canteen_pressed_time -= dt
            # wait for 3s
            if canteen_pressed_time <= 0:
                del canteen_pressed_id

        ### draw interactive buttons ###
        mouse = pygame.mouse.get_pos()
        
        draw_button(screen, button_getUserPos, button_getUserPos_coords, mouse, 'Where am I?', GREEN, RED, BLACK)
        draw_button(screen, button_getNearesrCanteen, button_getNearestCanteen_coords, mouse, 'The nearest canteen?', GREEN, RED, BLACK)
        draw_button(screen, button_sortByDistance, button_sortByDistance_coords, mouse, 'Sort by Distance (top5)', GREEN, RED, BLACK)
        draw_button(screen, button_sortByRating, button_sortByRating_coords, mouse, 'Sort by Rating (Top5)', GREEN, RED, BLACK)

        pygame.display.update()
        clock.tick(FPS)
        # print('Running test')

    pygame.quit()
    sys.exit

def draw_button(screen, button, button_coords, mouse_pos, text, color=GREEN, active_color=RED, text_color=BLACK):
    """
    args:
        screen: pygame screen object
        button: pygame.Rect object
        button_coords: list of button coordinates - [x,y,w,h]
        mouse_pos: coords of mouse - (x,y)
        text: text to be displayed on the button
        color: default color of button
        active_color: color when mouse hovers on the button
        text_color: color of button text
    """
    if button_coords[0] < mouse_pos[0] < button_coords[0]+button_coords[2] and button_coords[1] < mouse_pos[1] < button_coords[1]+button_coords[3]: # mouse hover the button
        pygame.draw.rect(screen, RED, button)
        draw_text(screen, (button_coords[0]+(button_coords[2]//2), button_coords[1]+(button_coords[3]//2)), text, int(button_coords[3]/2.5), color=BLACK)
    else:
        pygame.draw.rect(screen, GREEN, button)  # button
        draw_text(screen, (button_coords[0]+(button_coords[2]//2), button_coords[1]+(button_coords[3]//2)), text, button_coords[3]//3, color=BLACK)

if __name__ == '__main__':
    main()