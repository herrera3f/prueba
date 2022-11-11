import pygame  , random
Ancho = 840
Alto = 500


pygame.init()
pygame.mixer.init()


screen = pygame.display.set_mode([Alto,Ancho])
fondo = pygame.image.load("fondo1.jpg").convert()
ventana = pygame.display.set_mode((Ancho, Alto))
pygame.display.set_caption("juego space Meteors")

EJECUTAR = True
fps = 60
score = 0 
vida = 100
negro = (0,0,0)
blanco = (255,255,255)
clock = pygame.time.Clock()

def texto_puntuacion(frame,text,size, x,y):
    fuente = pygame.font.SysFont('Small Fonts', size,bold=True)
    text_frame= fuente.render(text, True, blanco,negro)
    text_rect = text_frame.get_rect()
    text_rect.midtop = (x, y)
    frame.blit(text_frame, text_rect)
    
   
def barra_de_vida(frame, x, y, nivel):
    longitud = 100
    alto = 20
    fill = int((nivel / 100) * longitud)
    border = pygame.Rect(x, y, longitud, alto)
    fill = pygame.Rect(x, y, fill, alto)
    pygame.draw.rect(frame, (255,0,55), border)
    pygame.draw.rect(frame, negro, border, 4)



class jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("nave.png").convert_alpha()
        self.image.set_colorkey(negro)
        pygame.display.set_icon(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = Ancho / 2
        self.rect.centery = Alto - 50
        self.velocidad_x = 0
        self.vida = 100
        
        
    def update(self):
        self.velocidad_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.velocidad_x = -5
        if keystate[pygame.K_RIGHT]:
            self.velocidad_x = 5
        self.rect.x += self.velocidad_x
        if self.rect.right > Ancho:
            self.rect.right = Ancho
        if self.rect.left < 0:
            self.rect.left = 0
            
    def disparar(self):
        bala = Balas(self.rect.centerx, self.rect.top)
        grupo_jugador.add(bala)
        grupo_balas_jugador.add(bala)

            
class Enemigo(pygame.sprite.Sprite):
    def __init__(self,x, y):
        super().__init__()
        self.image = pygame.image.load("meteormed.png").convert_alpha()
        self.image.set_colorkey(negro)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(Ancho - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.velocidad_y = random.randrange(1, 5)
        self.velocidad_x = random.randrange(-5, 3)
        
    def update(self):
       
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        if self.rect.top > Alto + 10 or self.rect.left < -25 or self.rect.right > Ancho+ 22 :
            self.rect.x = random.randrange(Ancho - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.velocidad_y = random.randrange(1, 10)

            
class Balas(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("laser1.png").convert_alpha()
        self.rect = self.image.get_rect() 
        self.rect.centerx = x
        self.rect.y = y
        self.velocidad_y = -18
        
    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom < 0:
            self.kill()


grupo_enemigos = pygame.sprite.Group()
grupo_jugador = pygame.sprite.Group()
grupo_balas_jugador = pygame.sprite.Group()


player = jugador()
grupo_jugador.add(player)
grupo_balas_jugador.add(player)
meteoro = Enemigo(0,0)
grupo_enemigos.add(meteoro)



for x in range(10):
    meteoro = Enemigo(x*100, 0)
    grupo_enemigos.add(meteoro)

  
EJECUTA = True    
while EJECUTAR:
    clock.tick(fps)
    ventana.blit(fondo, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            EJECUTAR = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.disparar()
    

    grupo_enemigos.update()
    grupo_jugador.update()
    grupo_balas_jugador.update()
    grupo_jugador.draw(ventana)
    grupo_enemigos.draw(ventana)
    
    colicion1 = pygame.sprite.groupcollide(grupo_enemigos, grupo_balas_jugador, True, True)
    for i in colicion1:
        score += 10
        meteoro = Enemigo(300,10)
        grupo_enemigos.add(meteoro)
       

    hits = pygame.sprite.spritecollide(player, grupo_enemigos, True)
    for hit in hits:
        player.vida -= 10
        meteoro = Enemigo(1,1)
        grupo_enemigos.add(meteoro)
        grupo_jugador.add(Enemigo)
        if vida <= 0:
            EJECUTAR = False
            
    texto_puntuacion(ventana,(' puntuacion: '+str(score)+'    '),30,Ancho-85,2)
    barra_de_vida(ventana,  Ancho-285,0,player.vida)
   

            
    
    pygame.display.flip()
pygame.quit()  

  