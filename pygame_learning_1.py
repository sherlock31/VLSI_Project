import sys, pygame
pygame.init()

screen = pygame.display.set_mode([720,720])

nand_gate_image = pygame.image.load('nand_40.jpg')

screen.fill((255,255,255))
while True:
    
    screen.blit(nand_gate_image, [0,680])
    
    pygame.display.update()
      

