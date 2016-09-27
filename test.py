import pygame
from pygame.locals import *
pygame.init()
img_path="/home/matt/Pictures/8251176.jpeg"
infoObject = pygame.display.Info()
window = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
pygame.display.toggle_fullscreen()
img = pygame.image.load(img_path)
while True:
        events = pygame.event.get()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        window.blit(img, (infoObject.current_w/2, infoObject.current_h/2)) #Replace (0, 0) with desired coordinates
        pygame.display.flip()
