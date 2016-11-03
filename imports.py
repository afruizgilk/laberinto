try:
    import pygame,sys,random,threading,time,ConfigParser
    from pygame.locals import *
except (KeyboardInterrupt, SystemExit):
        raise
except:
    print("[ERR] Python: Error importando las librerias de python ")
    raise


def checkCollision(sprite1, sprite2):
    col = pygame.sprite.collide_rect(sprite1, sprite2)
    if col == True:
        return True
    else:
        return False

def cargar_fondo(archivo, ancho, alto, sin_canal=False):
    if(not sin_canal):
        imagen = pygame.image.load(archivo).convert_alpha()
    else:
        imagen = pygame.image.load(archivo)
    imagen_ancho, imagen_alto = imagen.get_size()
    tabla_fondos = []
    for fondo_x in range(0, imagen_ancho/ancho):
       linea = []
       tabla_fondos.append(linea)
       for fondo_y in range(0, imagen_alto/alto):
            cuadro = (fondo_x * ancho, fondo_y * alto, ancho, alto)
            linea.append(imagen.subsurface(cuadro))
    return tabla_fondos

def playsound(filez):
    pygame.mixer.init()
    pygame.mixer.music.load(filez)
    pygame.mixer.music.play(0,0)

"""def blitcollition(sprite , x,y,image):
    if(jugador.rect.x <= x-image[0]) or (jugador.rect.x )"""

def explosionb(x,y, defs=False):
    if(not defs):
        reloj=pygame.time.Clock()
        playsound('data/sounds/explosion.ogg')
        b = cargar_fondo("data/images/ex.png", 115, 105)
        for actual in xrange(6):
            pantalla.blit(b[actual][0], (x-50,y-50))
            rect = b[actual][0].get_rect()
            rect.x,rect.y = x,y
            update_status_section()
            if(rect.colliderect(jugador.rect)):
                if(jugador.vida > 0):
                    jugador.vida -= 20
                else:
                    jugador.vida = 0
            update_status_section()

            #print jugador.rect , rect , "x: " , x, " y: ", y
            pygame.display.flip()
            reloj.tick(10)
        return True
    else:
        i = 0
        playsound('data/sounds/explosion.ogg')
        b = cargar_fondo("data/images/ex.png", 115, 105)
        actual = 0
        while actual <= 6:
            if(i == 0):
                i+=1
                pantalla.blit(b[actual][0], (x-20,y-20))
                rect = b[actual][0].get_rect()
                rect.x,rect.y = x,y
                update_status_section()
                if(rect.colliderect(jugador.rect)):
                    if(jugador.vida > 0):
                        jugador.vida -= 20
                    else:
                        jugador.vida = 0
                """for e in ls_todos:
                    if(rect.colliderect(e.rect)):
                        e.tipo = "el_muerto"
                        e.image=images[2][0]"""
                update_status_section()
                pygame.display.flip()
                actual+=1
            else:
                if(i >= 900000):
                    i= -500
                else:
                    i+= 1
        return True

"""class Explosion(pygame.sprite.Sprite):
    b = cargar_fondo("data/images/ex.png", 115, 105, True)
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.b[0][0]
        self.rect = self.image.get_rect()
        self.rect.x = x-20
        self.rect.y = y-20
        self.i = 0
        self.plays = True
        self.cont = 0
    def play(self):
        playsound('data/sounds/explosion.ogg')
    def update(self):
        if(self.plays):
            self.play()
            self.plays=False

        if(self.cont == 0):
            self.cont+=1
            if(self.i<=6):
                self.i+=1
            else:
                ls_todos.remove(self)
            self.image=self.b[self.i][0]
            if(checkCollision(jugador,self)):
                if(jugador.vida > 0):
                    jugador.vida -= 20
                else:
                    jugador.vida = 0
            update_status_section()
            ls_elementos.draw(pantalla)
            pygame.display.flip()
        else:
            if(self.cont >= 999999):
                self.cont =0
            else:
                self.cont+=1"""




class Enemigo(pygame.sprite.Sprite):
    paredes=None
    elementos=None
    image_arriba = []
    image_abajo =  []
    image_derecha = []
    image_izquierda=[]

    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)

        matrizimg = cargar_fondo("data/images/spritesene.png", 21,21)
        for i in range(7,8):
            self.image_abajo.append(matrizimg[i][0])
        for i in range(7,8):
            self.image_izquierda.append(matrizimg[i][1])
        for i in range(7,8):
            self.image_derecha.append(matrizimg[i][2])
        for i in range(7,8):
            self.image_arriba.append(matrizimg[i][3])
        self.probabilidad = random.randrange(0,100)
        self.incremento = 1
        self.image = self.image_derecha[0]
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.direccion="arriba"
        self.cont = 1 #Control de velocidad para los enemigos
        self.vida = 100
        self.flag = True
        self.cont_disparos = 0 #Control de los disparos

    def update_probabilidad(self):
        self.probabilidad = random.randrange(0,100)

    def get_direccion(self):
        flagd=False
        flagi=False
        save = (self.rect.x,self.rect.y)

        for muro in self.paredes:
            self.rect.x+=20
            if(checkCollision(self,muro)):
                flagd = True
                print "Con derecha"
            self.rect.x-=40
            if(checkCollision(self,muro)):
                flagi = True
                print "Con izquierda"
        self.rect.x, self.rect.y = save[0],save[1]
        if(not(flagd and flagi)):
            self.direccion = "arriba"

    def update(self):

        if(self.cont == 0):
            self.cont += 1
            """self.update_probabilidad()
            if(self.probabilidad > 0 and self.probabilidad < 50):
                self.direccion = "derecha"
            else:
                self.direccion = "arriba"""

            ls_choque=pygame.sprite.spritecollide(self, self.paredes, False)
            for muro in ls_choque:
                if(muro.tipo == "pared" or muro.tipo == "d_dinamita"):
                    if self.direccion == "derecha":
                       self.rect.right=muro.rect.left
                       self.direccion = "izquierda"
                    else:
                        if self.direccion == "izquierda":
                            self.rect.left=muro.rect.right
                            self.direccion = "derecha"
                        else:
                            if self.direccion == "arriba":
                                self.rect.bottom=muro.rect.top
                                self.direccion = "abajo"
                            else:
                                if self.direccion == "abajo":
                                    self.rect.top=muro.rect.bottom
                                    self.direccion = "arriba"

            if(self.direccion=="derecha"):
                self.rect.x+=1
            if(self.direccion=="izquierda"):
                self.rect.x-=1
            if(self.direccion == "arriba"):
                self.rect.y+=1
            if(self.direccion == "abajo"):
                self.rect.y-=1
        else:
            if(self.cont >= 5):
                self.cont = 0
            else:
                self.cont += 1

        if(self.cont_disparos == 0):
            self.cont_disparos+=1
            b = Bullet("data/images/bala_e.png", self.rect.x, self.rect.y, self.direccion)
            ls_balas_e.add(b)
            ls_todos.add(b)
        else:
            if(self.cont_disparos > 500):
                self.cont_disparos=0
            else:
                self.cont_disparos+=1




class Elemento(pygame.sprite.Sprite):
    def __init__(self, x, y, archivo):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(archivo).convert()
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.contdin = 0
        self.tipo = "ninguno"

    def update_rect(self,x,y):
        self.rect = self.image.get_rect()
        self.rect.x= x
        self.rect.y= y

    def update(self):
        if(self.tipo == "dinamita_a"):
            if(self.contdin == 0):
                playsound('data/sounds/ticking_clock.ogg')
            self.contdin += 1
            if(self.contdin >= 600):
                if(explosionb(self.rect.x,self.rect.y)):
                    self.image = images[2][0]
                    self.contdin=0
                    self.tipo = "d_dinamita"
                else:
                    print("Error inesperado en la ejecucion")
                    sys.exit(0)


def dibujarmapa(archivo,ls_todos,ls_muros,ls_elementos,ls_DL):
    global images
    images = cargar_fondo("data/images/spritesterreno.png", vxi,vyi)
    interprete = ConfigParser.ConfigParser()
    interprete.read(archivo)
    try:
        imagen = interprete.get("lab1", "origen")
        mapa = interprete.get("lab1", "mapa").split("\n")
    except:
        print("Error en la lectura de la seccion")
        sys.exit(0)
    try:
        for ey, punto in enumerate(mapa):
            for ex,cd in enumerate(punto):
                if((interprete.get(cd, "muro") == "si") and (interprete.get(cd, "bloqueo") == "si") and (interprete.get(cd, "puerta") == "no") and (interprete.get(cd, "vida") == "no")):
                    #Muros
                    vx = interprete.get(cd, "vx")
                    vy = interprete.get(cd, "vy")
                    m = Elemento(ex*25,ey*25,"data/images/spritesterreno.png")
                    m.image=images[int(vx)][int(vy)]
                    m.tipo=interprete.get(cd, "nombre")
                    m.update_rect(ex*25,ey*25)
                    ls_muros.add(m)
                    ls_elementos.add(m)
                    ls_todos.add(m)

                else:
                    if((interprete.get(cd, "muro") == "no") and (interprete.get(cd, "bloqueo") == "no") and (interprete.get(cd, "puerta") == "no") and (interprete.get(cd, "vida") == "no")):
                        #Ese es pasto
                        vx = interprete.get(cd, "vx")
                        vy = interprete.get(cd, "vy")
                        m = Elemento(ex*25,ey*25,"data/images/spritesterreno.png")
                        m.image=images[int(vx)][int(vy)]
                        m.tipo=interprete.get(cd, "nombre")
                        ls_elementos.add(m)
                        ls_todos.add(m)
                    else:
                        if((interprete.get(cd, "muro") == "no") and (interprete.get(cd, "bloqueo") == "si") and (interprete.get(cd, "puerta") == "si") and (interprete.get(cd, "vida") == "no")):
                            #Esta es la puerta para ganar
                            vx = interprete.get(cd, "vx")
                            vy = interprete.get(cd, "vy")
                            m = Elemento(ex*25,ey*25,"data/images/spritesterreno.png")
                            m.image=images[int(vx)][int(vy)]
                            m.tipo=interprete.get(cd, "nombre")
                            m.rect[2],m.rect[3] = 25,25 #Coreccion a la imagen
                            ls_muros.add(m)
                            ls_elementos.add(m)
                            ls_todos.add(m)


                        else:
                            if((interprete.get(cd, "muro") == "no") and (interprete.get(cd, "bloqueo") == "si") and (interprete.get(cd, "puerta") == "no") and (interprete.get(cd, "vida") == "no")):
                                #Dinamitas
                                vx = interprete.get(cd, "vx")
                                vy = interprete.get(cd, "vy")
                                m = Elemento(ex*25,ey*25,"data/images/spritesterreno.png")
                                m.image=images[int(vx)][int(vy)]
                                m.tipo=interprete.get(cd, "nombre")
                                m.rect[2],m.rect[3] = 25,25 #Coreccion a la imagen
                                print m.rect
                                ls_muros.add(m)
                                ls_elementos.add(m)
                                ls_todos.add(m)
                                ls_DL.add(m)
                            else:
                                if((interprete.get(cd, "muro") == "no") and (interprete.get(cd, "bloqueo") == "no") and (interprete.get(cd, "puerta") == "no") and (interprete.get(cd, "vida") == "si")):
                                    #Corazones
                                    vx = interprete.get(cd, "vx")
                                    vy = interprete.get(cd, "vy")
                                    m = Elemento(ex*25,ey*25,"data/images/spritesterreno.png")
                                    m.image=images[int(vx)][int(vy)]
                                    m.tipo=interprete.get(cd, "nombre")
                                    m.rect[2],m.rect[3] = 25,25 #Coreccion a la imagen
                                    ls_muros.add(m)
                                    ls_elementos.add(m)
                                    ls_todos.add(m)
                                    ls_DL.add(m)

    except:
        print("Archivo de configuracion corrupto reinstale el juego o contacte al soporte")
        sys.exit(0)

def lifebars(player, surface, pos):
    # Colores
    NEGRO = (0,0,0)
    BLANCO = (255,255,255)
    AZUL = (0,0,255)
    ROJO = (255,0,0)
    VERDE = (0,255,0)
    AMARILLO = (255,255,0)
    if(player.vida > 75):
        color = VERDE
    elif(player.vida > 50):
        color = AMARILLO
    else:
        color = ROJO
    pygame.draw.rect(surface, color, (pos[0],pos[1],player.vida,10))


def update_status_section():
    #STATS E INVENTARIO DEL JUGADOR
    sub.fill((0,0,0))
    blood = tipo.render("Vida actual: " , 1 , (255,0,0))
    sub.blit(blood, [10,5])
    lifebars(jugador, sub, [140,8])
    items = tipo.render("Items: " , 1 , (255,0,0))
    sub.blit(items, [300,5])
    pos1,pos2 = 370, 2
    key = pygame.image.load("data/images/key.png")
    #sub.blit(key, (pos1,pos2))
    for i in range(1, jugador.llaves+1):
        sub.blit(key, (pos1,pos2))
        pos1+=25

class Menu:
    lista = []
    tam_font = 32
    font_path = 'data/fonts/coders_crux.ttf'
    font = pygame.font.Font
    dest_surface = pygame.Surface
    start=(0,0)
    def __init__(self, datos, surface, position):
        self.lista = datos
        self.dest_surface = surface
        self.start = position
        self.color_n = (255,0,0)
        self.color_s = (0,255,0)
        self.cursor = 0
        self.imagem = pygame.image.load("data/images/main.jpg")
        self.imagem = pygame.transform.scale(self.imagem, (800, 600))


    def get_color(self):
        l_colores=[]
        for i in range(len(self.lista)):
            l_colores.append(self.color_n)
        l_colores[self.cursor] = self.color_s
        return l_colores

    def draw_menu(self):
        y=self.start[1]
        self.dest_surface.blit(self.imagem, [0,0])
        l = self.get_color()
        for i in range(len(self.lista)):
            tipo = pygame.font.Font(self.font_path, self.tam_font)
            text = tipo.render(self.lista[i] , 1 , l[i])
            self.dest_surface.blit(text, (self.start[0],y))
            y+=50
        pygame.display.flip()



class Jugador(pygame.sprite.Sprite):

    # Atributos
    paredes=None
    elementos=None
    image_arriba = []
    image_abajo =  []
    image_derecha = []
    image_izquierda=[]

    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)

        matrizimg = cargar_fondo("data/images/spritespsj.png", 25,25)
        for i in xrange(3):
            self.image_abajo.append(matrizimg[i][4])
        for i in xrange(3):
            self.image_izquierda.append(matrizimg[i][5])
        for i in xrange(3):
            self.image_derecha.append(matrizimg[i][6])
        for i in xrange(3):
            self.image_arriba.append(matrizimg[i][7])

        self.increment_x, self.increment_y = 1,1
        self.image = self.image_arriba[2]
        self.direccion = "arriba"
    	self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.vida = 100
        self.cont = 0
        self.llaves = 0

    # Control del movimiento
    def ir_arr(self):
        """ Usuario pulsa flecha izquierda """
        self.direccion = "arriba"
        if(self.cont<2):
            self.cont+=1
        else:
            self.cont=0

        self.image=self.image_arriba[self.cont]
        self.rect.y -= self.increment_y

    def ir_abaj(self):
        """ Usuario pulsa flecha izquierda """
        self.direccion = "abajo"
        if(self.cont<2):
            self.cont+=1
        else:
            self.cont=0

        self.image=self.image_abajo[self.cont]
        self.rect.y += self.increment_y

    def ir_izq(self):
        """ Usuario pulsa flecha izquierda """
        self.direccion = "izquierda"
        if(self.cont<2):
            self.cont+=1
        else:
            self.cont=0
        self.image=self.image_izquierda[self.cont]
        self.rect.x -= self.increment_x

    def ir_der(self):
        """ Usuario pulsa flecha derecha """
        self.direccion = "derecha"
        if(self.cont<2):
            self.cont+=1
        else:
            self.cont=0
        self.image=self.image_derecha[self.cont]
        self.rect.x += self.increment_x

    def no_mover(self):
        """ Usuario no pulsa teclas """
        self.vel_x = 0

    def update(self):
        ls_choque=pygame.sprite.spritecollide(self, self.paredes, False)
        for muro in ls_choque:
            if(muro.tipo == "pared" or muro.tipo == "d_dinamita"):
                if self.direccion == "derecha":
                   self.rect.right=muro.rect.left
                else:
                    if self.direccion == "izquierda":
                        self.rect.left=muro.rect.right
                    else:
                        if self.direccion == "arriba":
                            self.rect.top=muro.rect.bottom
                        else:
                            if self.direccion == "abajo":
                                self.rect.bottom=muro.rect.top
class Bullet(pygame.sprite.Sprite): #Hereda de la clase sprite

    def __init__(self, img_name, x,y, direccion): #img para cargar, y su padre(de donde debe salir la bala)
    	pygame.sprite.Sprite.__init__(self)
    	self.image = pygame.image.load(img_name).convert_alpha()
    	self.rect = self.image.get_rect()
    	self.rect.x = x
    	self.rect.y = y
        self.speed = 1
        self.direccion = direccion
    def update(self):

        if(self.direccion == "derecha"): #derecha
            self.rect.x += self.speed
        if(self.direccion == "izquierda"):#izquierda
            self.rect.x -= self.speed
        if(self.direccion == "arriba"):#arriba
            self.rect.y -= self.speed
        if(self.direccion == "abajo"):#abajo
            self.rect.y += self.speed

class Bullet_boss(pygame.sprite.Sprite):
    paredes=None
    elementos=None
    image_arriba = []
    image_abajo =  []
    image_derecha = []
    image_izquierda=[]
    moves=[]
    i=0
    i2=0
    def __init__(self, x,y, pos_p): #img para cargar, y su padre(de donde debe salir la bala)
    	pygame.sprite.Sprite.__init__(self)
    	self.matrizimg = cargar_fondo("data/images/shot_boss.png", 61,63)
        for i in range(2):
            self.image_abajo.append(self.matrizimg[i][0])
        for i in range(2):
            self.image_izquierda.append(self.matrizimg[i][1])
        for i in range(2):
            self.image_derecha.append(self.matrizimg[i][2])
        for i in range(2):
            self.image_arriba.append(self.matrizimg[i][3])
        self.image = self.image_izquierda[1]
    	self.rect = self.image.get_rect()
    	self.rect.x = x
    	self.rect.y = y
        self.speed = 1
        self.cont = 0
        self.explosion = True

    def go(self,pos):
        p = [[self.rect.x,self.rect.y],pos]
        x0 = p[0][0]
        y0 = p[0][1]
        x1 = p[1][0]
        y1 = p[1][1]
        res = []
        dx = (x1 - x0)
        dy = (y1 - y0)
        if (dy < 0) :
            dy = -1*dy
            stepy = -1
        else :
            stepy = 1
        if (dx < 0) :
            dx = -1*dx
            stepx = -1
        else :
            stepx = 1
        x = x0
        y = y0
        if(dx>dy) :
            p = 2*dy - dx
            incE = 2*dy
            incNE = 2*(dy-dx)
            while (x != x1) :
                x = x + stepx
                if (p < 0) :
                    p = p + incE
                else :
                    y = y + stepy
                    p = p + incNE
                p_new = [x, y]
                res.append(p_new)
        else :
            p = 2*dx - dy
            incE = 2*dx
            incNE = 2*(dx-dy)
            while (y != y1) :
                y = y + stepy
                if (p < 0) :
                    p = p + incE
                else :
                    x = x + stepx
                    p = p + incNE

                p_new = [x, y]
                res.append(p_new)
        self.moves=res
        self.i = 0
    def update(self):
        for e in ls_muros:
            if(checkCollision(e,self)):
                if(self.explosion):
                    ls_balas_boss.remove(self)
                    ls_todos.remove(self)
                    explosionb(self.rect.x,self.rect.y, True)
                    self.explosion=False
        if(checkCollision(jugador,self)):
            if(self.explosion):
                jugador.vida -= random.randrange(40,80)
                ls_balas_boss.remove(self)
                ls_todos.remove(self)
                explosionb(self.rect.x,self.rect.y, True)
        if(self.cont == 0):
            self.cont += 1
            if(self.i2 <= 1):
                self.image = self.matrizimg[random.randrange(0,2)][random.randrange(0,4)]
                self.i2+=1
                if(self.i < len(self.moves)):
                    self.rect.x,self.rect.y = self.moves[self.i][0],self.moves[self.i][1]
                    self.i += 1 #para que recorra el siguiente
                else:
                    ls_balas_boss.remove(self)
                    ls_todos.remove(self)
                    """explo = Explosion(self.rect.x,self.rect.y)
                    ls_todos.add(explo)"""
                    explosionb(self.rect.x,self.rect.y, True)
            else:
                self.i2=0


        else:
            if(self.cont >= 15):
                self.cont = 0
            else:
                self.cont += 1

class Boss(pygame.sprite.Sprite):

    paredes=None
    elementos=None
    image_arriba = []
    image_abajo =  []
    image_derecha = []
    image_izquierda=[]
    moves=[]
    shot=False
    probabilidad=random.randrange(0,100)
    probabilidad1=random.randrange(0,100)
    def __init__(self, x,y):

        pygame.sprite.Sprite.__init__(self)
        matrizimg = cargar_fondo("data/images/boss.png", 32,32)
        """for i in range(7,8):
            self.image_abajo.append(matrizimg[i][0])
        for i in range(7,8):
            self.image_izquierda.append(matrizimg[i][1])
        for i in range(7,8):
            self.image_derecha.append(matrizimg[i][2])
        for i in range(7,8):
            self.image_arriba.append(matrizimg[i][3])"""
        self.probabilidad = random.randrange(0,100)
        self.incremento = 1
        self.image = cargar_fondo("data/images/boss.png", 32,32)[0][0]
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.vida = 1000
        self.speed = 5
        self.i=0
        self.reloj = pygame.time.Clock()
        self.cont = 0

    def getLife(self):
    	return self.life

    def update_prob(self):
        self.probabilidad=random.randrange(0,100)
        self.probabilidad1=random.randrange(0,100)

    def setLife(self,life):
    	self.life = life

    def getSpeed(self):
        return self.speed

    def restartMovements(self,pos):
        p = [[self.rect.x,self.rect.y],pos]
        x0 = p[0][0]
        y0 = p[0][1]
        x1 = p[1][0]
        y1 = p[1][1]
        res = []
        dx = (x1 - x0)
        dy = (y1 - y0)
        if (dy < 0) :
            dy = -1*dy
            stepy = -1
        else :
            stepy = 1
        if (dx < 0) :
            dx = -1*dx
            stepx = -1
        else :
            stepx = 1
        x = x0
        y = y0
        if(dx>dy) :
            p = 2*dy - dx
            incE = 2*dy
            incNE = 2*(dy-dx)
            while (x != x1) :
                x = x + stepx
                if (p < 0) :
                    p = p + incE
                else :
                    y = y + stepy
                    p = p + incNE
                p_new = [x, y]
                res.append(p_new)
        else :
            p = 2*dx - dy
            incE = 2*dx
            incNE = 2*(dx-dy)
            while (y != y1) :
                y = y + stepy
                if (p < 0) :
                    p = p + incE
                else :
                    x = x + stepx
                    p = p + incNE

                p_new = [x, y]
                res.append(p_new)
        self.moves=res
        self.i = 0

    def update(self): #se mueve
        self.update_prob()
        if(self.probabilidad < 3 and self.probabilidad1 > 98):
            s = Bullet_boss(self.rect.x,self.rect.y,0)
            s.go([jugador.rect.x,jugador.rect.y])
            ls_balas_boss.add(s)
            ls_todos.add(s)
            self.shot=True
        else:
            if(self.cont == 0):
                self.cont += 1
                if(self.i < len(self.moves)):
                    self.rect.x,self.rect.y = self.moves[self.i][0],self.moves[self.i][1]
                    self.i += 1 #para que recorra el siguiente
            else:
                if(self.cont >= 5):
                    self.cont = 0
                else:
                    self.cont += 1

class Juego:
    nivel=0
    surface=None

    def __init__(self,nivel,surface):
        self.nivel = nivel
        self.surface = surface

    def start_1(self, vida_j=100):
        global ANCHO,ALTO,pantalla,jugador,ls_todos,sub,tipo,ls_balas_boss,ls_muros
        c_fondo = (255,0,0)
        ALTO = 600
        ANCHO = 800
        global vxi,vyi
        vxi=25
        vyi=25
        pygame.init()
        pantalla = pygame.display.set_mode((ANCHO, ALTO+30))
        pygame.display.set_caption(" El laberinto de la muerte lvl 2 - [v1] ", 'Spine Runtime')
        pantalla.fill(c_fondo)
        sub = pantalla.subsurface([0,ALTO, ANCHO, 30]) #Dibuja una surface sobre la pantalla
        tipo = pygame.font.SysFont("monospace", 15)
        tipo.set_bold(True)
        sub.fill((0,0,0))

        ls_enemigos=pygame.sprite.Group()
        ls_todos=pygame.sprite.Group()
        ls_muros=pygame.sprite.Group()
        ls_elementos=pygame.sprite.Group()
        ls_DL=pygame.sprite.Group()
        ls_jugador=pygame.sprite.Group()
        ls_bajasj=pygame.sprite.Group()
        ls_balas_boss = pygame.sprite.Group()


        boss = Boss(800/2,600/2)
        boss.paredes=ls_muros
        ls_enemigos.add(boss)
        ls_todos.add(boss)

        jugador = Jugador(500,200)
        jugador.paredes=ls_muros
        jugador.vida=vida_j
        ls_jugador.add(jugador)
        ls_todos.add(jugador)

        m = dibujarmapa("map1.wr",ls_todos,ls_muros,ls_elementos,ls_DL)

        ls_todos.draw(pantalla)
        ls_enemigos.draw(pantalla)
        ls_jugador.draw(pantalla)

        pygame.display.flip()
        pygame.display.flip()
        reloj = pygame.time.Clock()
        terminar=False
        muerto = False
        win = False
        flag_sonido=True
        cont_llave = 0
        while not terminar:
            jugador.vida=100
            tipo2 = pygame.font.Font("data/fonts/sk.ttf", 90)
            if(jugador.vida <= 0):
                #print("Muerto prro")
                global picture
                picture = pygame.image.load("data/images/gameover.png")
                picture = pygame.transform.scale(picture, (ANCHO, ALTO+10))
                rect = picture.get_rect()
                #print "VIDA : " , jugador.vida
                muerto = True
                update_status_section()
                sub.fill((0,0,0))
                tipo.set_bold(True)
                teclas1 = tipo2.render("Presione ESC para ir al menu" , 1 , (255,0,0))
                teclas2 = tipo2.render("Presione N para juego nuevo " , 1 , (255,0,0))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    terminar=True
                    salir=True

                elif event.type==pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        terminar=True
                        salir=True

                    if event.key == pygame.K_n:
                        self.start_0()
                    if event.key == pygame.K_SPACE:
                        playsound("data/sounds/shot.ogg")
                        b = Bullet("data/images/bala.png", jugador.rect.x, jugador.rect.y, jugador.direccion)
                        ls_bajasj.add(b)
                        ls_todos.add(b)

                    """if event.key == pygame.K_t:
                        for i in ls_DL:
                            jugador.rect.x,jugador.rect.y = i.rect.x, i.rect.y"""
                    if event.key == pygame.K_e:
                        for el in ls_DL:
                            if(checkCollision(jugador,el)):
                                if(el.tipo == "dinamita"):
                                    playsound("data/sounds/open.ogg")
                                    x,y = el.rect.x, el.rect.y
                                    ls_DL.remove(el)
                                    ls_todos.remove(el)
                                    ls_muros.remove(el)
                                    ls_elementos.remove(el)
                                    m=Elemento(x,y,"data/images/spritesterreno.png")
                                    m.image=images[1][1]
                                    m.rect[2],m.rect[3] = 25,25 #Coreccion a la imagen
                                    m.tipo="dinamita_a"

                                    ls_todos.add(m)
                                    ls_muros.add(m)

                                else:
                                    playsound("data/sounds/open.ogg")
                                    jugador.llaves+=1
                                    x,y = el.rect.x, el.rect.y
                                    ls_DL.remove(el)
                                    ls_todos.remove(el)
                                    ls_muros.remove(el)
                                    ls_elementos.remove(el)
                                    m=Elemento(x,y,"data/images/spritesterreno.png")
                                    m.image=images[3][0]
                                    m.rect[2],m.rect[3] = 25,25 #Coreccion a la imagen
                                    m.tipo="dinamita"

                                    ls_todos.add(m)
                                    ls_muros.add(m)

                        for el in ls_elementos:
                            if(checkCollision(jugador,el)):
                                if(el.tipo == "puerta"):
                                    if(jugador.llaves >= 2):
                                        win=True
                                    else:
                                        playsound("data/sounds/er.ogg")
                                        cont_llave=1

            for b in ls_bajasj:
                for m in ls_muros:
                    if(checkCollision(b,m)):
                        ls_bajasj.remove(b)
                        ls_todos.remove(b)
                for e in ls_enemigos:
                    if(e.vida <= 0):
                        ls_enemigos.remove(e)
                        ls_todos.remove(e)

                    if(checkCollision(b,e)):
                        e.vida -= 20
                        ls_bajasj.remove(b)
                        ls_todos.remove(b)
                for b_e in ls_balas_boss:
                    if(checkCollision(b,b_e)):
                        ls_bajasj.remove(b)
                        ls_todos.remove(b)

            for c in ls_elementos:
                if(c.tipo == "vida"):
                    if(checkCollision(jugador,c)):
                        jugador.vida+=40
                        c.tipo = "piso"
                        c.image=images[0][1]


            T=pygame.key.get_pressed()
            boss.restartMovements([jugador.rect.x,jugador.rect.y])
            if T[pygame.K_LEFT]:
                jugador.update()
                jugador.ir_izq()

            if T[pygame.K_RIGHT]:
                jugador.update()
                jugador.ir_der()

            if T[pygame.K_UP]:
                jugador.update()
                jugador.ir_arr()

            if T[pygame.K_DOWN]:
                jugador.update()
                jugador.ir_abaj()



            for e in ls_enemigos:
                if(checkCollision(jugador,e)):
                    jugador.vida-=random.randrange(15,30)



            if(muerto and not win):
                if(flag_sonido):
                    playsound("data/sounds/go.ogg")
                    flag_sonido=False
                rect = rect.move((0,0))
                pantalla.blit(picture, rect)
                pantalla.blit(teclas1, [ANCHO/2-210,ALTO/2+100])
                pantalla.blit(teclas2, [ANCHO/2-220,ALTO/2+200])
            else:
                if(not win):
                    pantalla.fill(c_fondo)
                    sub.fill ((0,0,0))
                    ls_todos.draw(pantalla)
                    ls_bajasj.draw(pantalla)
                    ls_balas_boss.draw(pantalla)
                    ls_enemigos.draw(pantalla)
                    ls_jugador.draw(pantalla)
                    ls_enemigos.update()
                    ls_balas_boss.update()
                    #ls_balas_e.draw(pantalla)
                    ls_todos.update()

                    update_status_section()
                else:
                    global picturewin
                    if(flag_sonido):
                        playsound("data/sounds/win.ogg")
                        flag_sonido=False
                    picturewin = pygame.image.load("data/images/win.png")
                    picturewin = pygame.transform.scale(picturewin, (ANCHO, ALTO+10))
                    win = True
                    sub.fill((0,0,0))
                    pantalla.blit(picturewin, [0,0])
                    teclas1 = tipo2.render("Fin del juego" , 1 , (255,0,0))
                    #teclas2 = tipo2.render("Presione N para juego nuevo " , 1 , (255,0,0))
                    pantalla.blit(teclas1, [ANCHO/2-180,ALTO/2+100])
                    #pantalla.blit(teclas2, [ANCHO/2-220,ALTO/2+200])


            if(not cont_llave == 0 and not win):
                pantalla.blit(rq_llave, [ANCHO/2-200,ALTO/2-100])
                pic = pygame.image.load("data/images/key2.png")
                pic = pygame.transform.scale(pic, (50,50))
                pantalla.blit(pic, [ANCHO/2+140, ALTO/2-60])
                cont_llave+=1

            pygame.display.flip()

    def start_0(self):
        global ANCHO,ALTO,jugador,pantalla,sub,tipo,ls_todos
        c_fondo = (255,0,0)
        ALTO = 600
        ANCHO = 800
        global vxi,vyi
        vxi=25
        vyi=25
        pygame.init()
        pantalla = pygame.display.set_mode((ANCHO, ALTO+30))
        pygame.display.set_caption(" El laberinto de la muerte lvl 1 - [v1] ", 'Spine Runtime')
        pantalla.fill(c_fondo)
        sub = pantalla.subsurface([0,ALTO, ANCHO, 30]) #Dibuja una surface sobre la pantalla
        tipo = pygame.font.SysFont("monospace", 15)
        tipo.set_bold(True)
        sub.fill((0,0,0))

        global ls_balas_e
        ls_muros=pygame.sprite.Group()
        ls_elementos=pygame.sprite.Group()
        ls_enemigos=pygame.sprite.Group()
        ls_todos=pygame.sprite.Group()
        ls_jugador = pygame.sprite.Group()
        ls_bajasj = pygame.sprite.Group()
        ls_DL = pygame.sprite.Group()
        ls_balas_e = pygame.sprite.Group()

        m = dibujarmapa("map.wr",ls_todos,ls_muros,ls_elementos,ls_DL)

        jugador=Jugador(ANCHO/2,ALTO/2)
        ls_todos.add(jugador)
        jugador.paredes=ls_muros
        jugador.elementos=ls_elementos
        ls_jugador.add(jugador)

        cont = 0
        for llodin in ls_DL:
            if(not cont == 2):
                llodin.tipo = "llave"
                cont+=1
            else:
                llodin.tipo = "dinamita"


        enemigos_pos = [(4,16,"arriba"),(1,15,"arriba"),(20,2,"derecha"),(30,4,"arriba"),(12,18,"arriba"),(24,9,"arriba"),(22,5,"derecha"),(16,22,"derecha"),(7,10,"arriba"), (4,19,"arriba")]
        for i in enemigos_pos:
            x,y,direccion = i[0],i[1],i[2]
            en = Enemigo(x*25,y*25)
            en.direccion = direccion
            en.paredes = ls_muros
            ls_todos.add(en)
            ls_enemigos.add(en)

        """enemigosc=0
        while enemigosc < 10:
            lista = ls_elementos.sprites()
            m = lista[random.randrange(0,len(ls_muros))]
            if(m.tipo == "piso"):
                en = Enemigo(m.rect.x,m.rect.y)
                en.paredes = ls_muros
                ls_todos.add(en)
                ls_enemigos.add(en)
                enemigosc+=1"""

        pygame.display.flip()
        reloj = pygame.time.Clock()
        terminar=False
        muerto = False
        win = False
        flag_sonido=True
        cont_llave = 0
        while not terminar:

            #jugador.vida = 100
            tipo2 = pygame.font.Font("data/fonts/sk.ttf", 90)
            if(cont_llave < 200):
                rq_llave = tipo2.render("Necesitas las llaves" , 1 , (44,26,7))
            else:
                cont_llave = 0

            if(jugador.vida <= 0):
                #print("Muerto prro")
                global picture
                picture = pygame.image.load("data/images/gameover.png")
                picture = pygame.transform.scale(picture, (ANCHO, ALTO+10))
                rect = picture.get_rect()
                #print "VIDA : " , jugador.vida
                muerto = True
                update_status_section()
                sub.fill((0,0,0))
                tipo.set_bold(True)
                teclas1 = tipo2.render("Presione ESC para ir al menu" , 1 , (255,0,0))
                teclas2 = tipo2.render("Presione N para juego nuevo " , 1 , (255,0,0))



            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    terminar=True
                    salir=True

                elif event.type==pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        terminar=True
                        salir=True

                    if event.key == pygame.K_n:
                        self.start_0()
                    if event.key == pygame.K_SPACE:
                        playsound("data/sounds/shot.ogg")
                        b = Bullet("data/images/bala.png", jugador.rect.x, jugador.rect.y, jugador.direccion)
                        ls_bajasj.add(b)
                        ls_todos.add(b)

                    """if event.key == pygame.K_t:
                        for i in ls_DL:
                            jugador.rect.x,jugador.rect.y = i.rect.x, i.rect.y"""
                    if event.key == pygame.K_e:
                        for el in ls_DL:
                            if(checkCollision(jugador,el)):
                                if(el.tipo == "dinamita"):
                                    playsound("data/sounds/open.ogg")
                                    x,y = el.rect.x, el.rect.y
                                    ls_DL.remove(el)
                                    ls_todos.remove(el)
                                    ls_muros.remove(el)
                                    ls_elementos.remove(el)
                                    m=Elemento(x,y,"data/images/spritesterreno.png")
                                    m.image=images[1][1]
                                    m.rect[2],m.rect[3] = 25,25 #Coreccion a la imagen
                                    m.tipo="dinamita_a"

                                    ls_todos.add(m)
                                    ls_muros.add(m)

                                else:
                                    playsound("data/sounds/open.ogg")
                                    jugador.llaves+=1
                                    x,y = el.rect.x, el.rect.y
                                    ls_DL.remove(el)
                                    ls_todos.remove(el)
                                    ls_muros.remove(el)
                                    ls_elementos.remove(el)
                                    m=Elemento(x,y,"data/images/spritesterreno.png")
                                    m.image=images[3][0]
                                    m.rect[2],m.rect[3] = 25,25 #Coreccion a la imagen
                                    m.tipo="dinamita"

                                    ls_todos.add(m)
                                    ls_muros.add(m)

                        for el in ls_elementos:
                            if(checkCollision(jugador,el)):
                                if(el.tipo == "puerta"):
                                    if(jugador.llaves >= 2):
                                        win=True
                                    else:
                                        playsound("data/sounds/er.ogg")
                                        cont_llave=1

            T=pygame.key.get_pressed()

            if T[pygame.K_LEFT]:
                jugador.update()
                jugador.ir_izq()
            if T[pygame.K_RIGHT]:
                jugador.update()
                jugador.ir_der()
            if T[pygame.K_UP]:
                jugador.update()
                jugador.ir_arr()
            if T[pygame.K_DOWN]:
                jugador.update()
                jugador.ir_abaj()

            for bala in ls_bajasj:
                    for muro in ls_muros:
                        if(checkCollision(bala,muro)): # si se choco
                            ls_bajasj.remove(bala)
                            ls_todos.remove(bala)
                    for enemigo in ls_enemigos:
                        if(checkCollision(bala,enemigo)): # si se choco
                            playsound("data/sounds/hit.ogg")
                            enemigo.vida -= random.randrange(10,30)
                            ls_bajasj.remove(bala)
                            ls_todos.remove(bala)

                        if(enemigo.vida <= 0):
                            ls_enemigos.remove(enemigo)
                            ls_todos.remove(enemigo)
            for enemigo in ls_enemigos:
                if(checkCollision(jugador,enemigo)): # si se choco
                    if(not jugador.vida <= 0):
                        jugador.vida -= 1
                    else:
                        break

            for bala_e in ls_balas_e:
                for muro in ls_muros:
                    if(checkCollision(bala_e,muro)):
                        ls_todos.remove(bala_e)
                        ls_balas_e.remove(bala_e)
                if(checkCollision(bala_e,jugador)):
                    jugador.vida -= random.randrange(3,20)
                    ls_todos.remove(bala_e)
                    ls_balas_e.remove(bala_e)
                for bala_j in ls_bajasj:
                    if(checkCollision(bala_e,bala_j)):
                        ls_bajasj.remove(bala_j)
                        ls_todos.remove(bala_j)
                        ls_todos.remove(bala_e)
                        ls_balas_e.remove(bala_e)

            if(muerto and not win):
                if(flag_sonido):
                    playsound("data/sounds/go.ogg")
                    flag_sonido=False
                rect = rect.move((0,0))
                pantalla.blit(picture, rect)
                pantalla.blit(teclas1, [ANCHO/2-210,ALTO/2+100])
                pantalla.blit(teclas2, [ANCHO/2-220,ALTO/2+200])
            else:
                if(not win):
                    pantalla.fill(c_fondo)
                    sub.fill ((0,0,0))
                    ls_todos.draw(pantalla)
                    ls_bajasj.draw(pantalla)
                    ls_enemigos.draw(pantalla)
                    ls_jugador.draw(pantalla)
                    ls_enemigos.update()
                    ls_balas_e.draw(pantalla)
                    ls_todos.update()

                    update_status_section()
                else:
                    global picturewin
                    if(flag_sonido):
                        playsound("data/sounds/win.ogg")
                        flag_sonido=False
                    picturewin = pygame.image.load("data/images/win.png")
                    picturewin = pygame.transform.scale(picturewin, (ANCHO, ALTO+10))
                    win = True
                    sub.fill((0,0,0))
                    pantalla.blit(picturewin, [0,0])

                    self.start_1()
                    #teclas1 = tipo2.render("Presione ESC para salir" , 1 , (255,0,0))
                    #teclas2 = tipo2.render("Presione N para juego nuevo " , 1 , (255,0,0))
                    #pantalla.blit(teclas1, [ANCHO/2-180,ALTO/2+100])
                    #pantalla.blit(teclas2, [ANCHO/2-220,ALTO/2+200])


            if(not cont_llave == 0 and not win):
                pantalla.blit(rq_llave, [ANCHO/2-200,ALTO/2-100])
                pic = pygame.image.load("data/images/key2.png")
                pic = pygame.transform.scale(pic, (50,50))
                pantalla.blit(pic, [ANCHO/2+140, ALTO/2-60])
                cont_llave+=1

            pygame.display.flip()
    def Iniciar_j(self):
        if(self.nivel == 0):
            self.start_0()
        elif(self.nivel==1):
            self.start_1()
        else:
            print("Nivel invalido")
