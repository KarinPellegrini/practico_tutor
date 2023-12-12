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

#Funcion par a dibujar texto
def draw_text(surface, text, size, x, y):
	font = pygame.font.SysFont("verdana", size) #fuente
	text_surface = font.render(text, True, WHITE) #lugar para pintar el texto
	text_rect = text_surface.get_rect() 
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)

#creamos nuestra clase jugador, Esto significa que la clase Player está siendo definida como una subclase de pygame.sprite.Sprite
class Player(pygame.sprite.Sprite): 
	def __init__(self):
		super().__init__()
		original_image = pygame.image.load("assets/navecom.png").convert()
		self.image = pygame.transform.scale(original_image,(110,110))
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
		self.rect.x = random.randint(0, WIDTH - self.rect.width) #que aparezca en un lugar random
		self.rect.y = random.randint(-100, -40)
		self.speedy = random.randint(1, 10)
		self.speed_x = random.randint(-5,5)

	MAX_ENEMIES = 7
 
	def update(self):  
		self.rect.y += self.speedy #aumentamos la velocidad
		self.rect.x += self.speed_x
		if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25:
			self.rect.x = random.randint(0, WIDTH - self.rect.width)
			self.rect.y = random.randint(-100, -40)
			self.speedy = random.randint(1,10)



			if len(enemy_list) < self.MAX_ENEMIES:
				enemy = Enemy()
				all_sprites.add(enemy)
				enemy_list.add(enemy)


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

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (100, 100, 100)  # Color base del botón
        self.text = text
        self.font = pygame.font.SysFont("Arial", 20)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos) 



#Cargar imagen de fondo
background = pygame.image.load("assets/background3.jpg").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
backgroundInicio = pygame.image.load("assets/background2.jpg").convert()
backgroundInicio = pygame.transform.scale(backgroundInicio, (WIDTH, HEIGHT))
all_sprites = pygame.sprite.Group()	#creamos un grupo
enemy_list = pygame.sprite.Group() #grupo meteoros
bullets = pygame.sprite.Group()
    
#para los botones
start_button = Button(300, 200, 200, 50, "Iniciar juego")
quit_button = Button(300, 300, 200, 50, "Salir")

buttons = [start_button, quit_button]



player = Player() #player es del tipo Player()
all_sprites.add(player) #agregamos al jugador al array
for i in range(8):
	enemy = Enemy()
	all_sprites.add(enemy)
	enemy_list.add(enemy)

score = 0
running = True # Inicializ amos en True
in_menu = True
while running: # Bucle principal
    screen.blit(backgroundInicio, [0,0])

    if in_menu:

        draw_text(screen, "¡Cuidado con los aliens!", 50, WIDTH // 2, 100)
        for button in buttons:
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # si el botón presionado es el botón izquierdo del mouse.
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.is_clicked(pos):
                        if button.text == "Iniciar juego":
                            in_menu = False  # Iniciar juego
                        elif button.text == "Salir":  
                            running = False  # Salir del juego
  
        pygame.display.flip()  # Mostrar el menú

    else:
        clock.tick(60) # 60 frames por segundo
        
        for event in pygame.event.get(): # Evento para salir de la ventana
            if event.type == pygame.QUIT:
                running = False

            # Disparar cada vez que se presiona la barra espaciadora
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        all_sprites.update()

        # Colisiones alien-laser
        hits = pygame.sprite.groupcollide(enemy_list, bullets, True, True)
        for hit in hits:
            score += 10
            enemy = Enemy()
            all_sprites.add(enemy)
            enemy_list.add(enemy)

        # Hacemos las colisiones - jugador - enemigo
        hits = pygame.sprite.spritecollide(player, enemy_list, True) # Los objetos que se choquen van a desaparecer
        if hits:
            # Si hay algo dentro de la lista significa que me pegó un meteoro
            running = False

        screen.blit(background, [0,0]) # Colocar el fondo

        all_sprites.draw(screen) # Dibujar el shooter en pantalla

        # Marcador
        draw_text(screen, f"Puntaje: {score}", 25, WIDTH//2, 10)
        pygame.display.flip()  # Mostrar el juego

pygame.quit()                                      







