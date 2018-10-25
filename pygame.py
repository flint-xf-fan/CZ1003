import pygame
def display_map():
    introScreenImage = pygame.image.load("NTUCampus.png")
    screen = pygame.display.set_mode((900,700))
    screen.blit(introScreenImage,(0,0))
    pygame.display.flip()
#main program
pygame.init()
display_map()
#End