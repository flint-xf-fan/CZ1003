import pygame
import math
# import re
##### application configuration #####
FPS = 60
SIZE = (1317, 794)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

LIGHT_RED = (155, 0, 0)
LIGHT_GREEN = (0, 200, 0)


def draw_text(screen, pos, text, size=5, color=BLACK):
    # text_surface = pygame.font.Font(font, size).render(text, True, color)
    text_surface = pygame.font.SysFont("arial", size).render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = pos
    screen.blit(text_surface, text_rect)

def draw_message(screen, pos=(1200, 420), msg='', size=10, color=BLACK):
    if isinstance(msg, list) or isinstance(msg, tuple):
        i = 1
        for m in msg:
            draw_text(screen, (pos[0],pos[1]+i*(size+2)), m, size, color)
            i += 1
    else:
        # print(msg, 'test')
        draw_text(screen, pos, msg, size, color)

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


def get_user_pos(screen, time):
    """
    Makes the program halt for 'time' seconds or until the user performs the action.

    ToDo:
        * limit the user to only click any point within the map.
    """
    clock = pygame.time.Clock()
    waiting = True
    # draw_message(screen, (1200, 420), 'Now click one point on the map to get your location', 15)
    while waiting:
        dt = clock.tick(FPS) / 1000  # Takes the time between each loop and convert to seconds.
        time -= dt
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                user_pos = event.pos
                # print('Your position is:', user_pos)
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
    print(['{} Rating: {}'.format(canteens_list_sorted[i].name, canteens_list_sorted[i].rating) for i in range(k)])
    return ['{} Rating: {}'.format(canteens_list_sorted[i].name, canteens_list_sorted[i].rating) for i in range(k)]


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


def search_by_price(user_input, canteens_list):
    search_results = []
    try:
        assert ',' in user_input
        price_range =  user_input.split(',')
        range_low = float(price_range[0])
        range_high = float(price_range[1])
        assert range_low <= range_high

    except:
        return 'Error! Input format example: 5,10.5'

    for canteen in canteens_list:
        min_price = float(canteen.min_price)
        max_price = float(canteen.max_price)
        if min_price <= range_low <= max_price or min_price <= range_high <= max_price:
            search_results.append(canteen.name)
    if search_results==[]:
        return 'No such food in this range exist'

    return search_results