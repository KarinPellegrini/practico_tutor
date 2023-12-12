import pygame, random

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#inicializamos pygame
pygame.init()
pygame.mixer.init() #para el sonmido
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #creamos la pantalla
pygame.display.set_caption("Invasión de aliens")

clock = pygame.time.Clock() #reloj para controlar los frames por segundo

#creamos nuestra clase jugador, Esto significa que la clase Player está siendo definida como una subclase de pygame.sprite.Sprite
class Player(pygame.sprite.Sprite): 
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("assets/player.png").convert() #para cargar la imagen del jugador
		self.image.set_colorkey(BLACK) #eliminamos el fondo negro de la imagen
		self.rect = self.image.get_rect() #para obtener el rectangulo que abarca el área del shooter
		self.rect.centerx = WIDTH//2 #para centrar el shooter al inicio del juego
		self.rect.bottom = HEIGHT - 10 #para ubicar el shooter abajo
		self.speed_x= 0 #iniciamos en 0 la velocidad en la que se mueve

	def update(self):
		self.speed_x = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speed_x = -6
		if keystate[pygame.K_RIGHT]:
			self.speed_x = 6
		self.rect.x += self.speed_x
		#para que el shooter no se salga de la pantalla
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0 #si el borde es menor que 0 lo igualo para que no pueda seguir mas

	#para las balas
	def shoot(self):
		bullet_instance = Bullet(self.rect.centerx, self.rect.top) # Instanciar un objeto de la clase Bullet
		all_sprites.add(bullet_instance)  # Agregar la bala al grupo de todos los sprites
		bullets.add(bullet_instance)  # Agregar la bala al grupo de balas


class Enemy (pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		original_image = pygame.image.load("assets/SHEET.png").convert()
		self.image = pygame.transform.scale(original_image,(50,50))
		self.image.set_colorkey(BLACK)

		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width) #que aparezca en un lugar random
		self.rect.y = random.randrange(-100, -40)
		self.speedy = random.randrange(1, 10)
		self.speed_x = random.randrange(-5,5)

	def update(self):
		self.rect.y += self.speedy #aumentamos la velocidad
		self.rect.x +=self.speed_x
		if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25:
			self.rect.y = random.randrange(-100, -40)
			self.speedy = random.randrange(1, 10)	

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load("assets/laser1.png")
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.centerx = x
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy #hacemos que suba en automático
		#cuando sale de la ventana debemos eliminar las balas de la lista
		if self.rect.bottom < 0:
			self.kill()

	#update() es comúnmente utilizado en juegos implementados con pygame para realizar actualizaciones a los atributos o propiedades del sprite en cada cuadro (frame) del juego
#Cargar imagen de fondo
background = pygame.image.load("assets/background3.jpg").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
all_sprites = pygame.sprite.Group()	#creamos un grupo
enemy_list = pygame.sprite.Group() #grupo meteoros
bullets = pygame.sprite.Group()


player = Player() #player es del tipo Player()
all_sprites.add(player) #agregamos al jugador al array
for i in range(8):
	enemy = Enemy()
	all_sprites.add(enemy)
	enemy_list.add(enemy)

running = True #inicializamos en true
while running: #buque principal
	clock.tick(60) #60 frames x seg
	for event in pygame.event.get(): #event para salir de la ventana
		if event.type == pygame.QUIT:
			running = False

		#cada vez que se apreta la barra espaciadora dispara
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.shoot()


	all_sprites.update()

	#colisiones alien-laser

	hits = pygame.sprite.groupcollide(enemy_list, bullets, True, True)
	for hit in hits:
		enemy = Enemy()
		all_sprites.add(enemy) 
		enemy_list.add(enemy)
	#Hacemos las colisiones - jugador - enemigo
	hits = pygame.sprite.spritecollide(player, enemy_list, True) #los objetos que se choquen van a desaparecer
	if hits:
		#si hay algo dentro de la lista significa que me pegó un meteoro
		running = False



	screen.blit(background, [0,0]) #para el background

	all_sprites.draw(screen) #dibujamos el shooter en pantalla

	pygame.display.flip()

pygame.quit()




