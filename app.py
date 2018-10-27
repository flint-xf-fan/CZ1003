import pygame
import sys


FPS = 60
SIZE = (1024, 720)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# necessary to display text to screen
def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()



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



def main():
    # settings
    pygame.init()
    
    clock = pygame.time.Clock() # Used to manage how fast the screen updates


    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("APP NAME To Be Decided")
    
    map_img = pygame.image.load("assets/NTUCampus.png")
    map_x = 100
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
                    

        screen.fill(WHITE)

        ##### draing code goes here #####


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
        
        ### display the map ###
        screen.blit(map_img, (map_x, map_y))
        
        
        pygame.display.update()
        clock.tick(FPS)
        # print('Running test')

    pygame.quit()
    sys.exit

if __name__ == '__main__':
    main()