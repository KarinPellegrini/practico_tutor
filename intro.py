import pygame, sys

print (pygame.ver)

size = (800,500)

screen = pygame.display.set_mode(size)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()