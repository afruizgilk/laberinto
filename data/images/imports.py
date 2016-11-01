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

def cargar_fondo(archivo, ancho, alto):
    imagen = pygame.image.load(archivo).convert_alpha()
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

def explosionb(x,y):
    reloj=pygame.time.Clock()
    playsound('explosion.ogg')
    b = cargar_fondo("ex.png", 115, 105)
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
            b = Bullet("bala_e.png", self.rect.x, self.rect.y, self.direccion)
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
                playsound('ticking_clock.ogg')
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
    interprete.read("map.wr")
    try:
        imagen = interprete.get("lab1", "origen")
        mapa = interprete.get("lab1", "mapa").split("\n")
    except:
        print("Error en la lectura de la seccion")
        sys.exit(0)
    try:
        for ey, punto in enumerate(mapa):
            for ex,cd in enumerate(punto):
                if((interprete.get(cd, "muro") == "si") and (interprete.get(cd, "bloqueo") == "si") and (interprete.get(cd, "puerta") == "no")):
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
                    if((interprete.get(cd, "muro") == "no") and (interprete.get(cd, "bloqueo") == "no") and (interprete.get(cd, "puerta") == "no")):
                        #Ese es pasto
                        vx = interprete.get(cd, "vx")
                        vy = interprete.get(cd, "vy")
                        m = Elemento(ex*25,ey*25,"data/images/spritesterreno.png")
                        m.image=images[int(vx)][int(vy)]
                        m.tipo=interprete.get(cd, "nombre")
                        ls_elementos.add(m)
                        ls_todos.add(m)
                    else:
                        if((interprete.get(cd, "muro") == "no") and (interprete.get(cd, "bloqueo") == "si") and (interprete.get(cd, "puerta") == "si")):
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
                            if((interprete.get(cd, "muro") == "no") and (interprete.get(cd, "bloqueo") == "si") and (interprete.get(cd, "puerta") == "no")):
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
    key = pygame.image.load("key.png")
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

    def get_color(self):
        l_colores=[]
        for i in range(len(self.lista)):
            l_colores.append(self.color_n)
        l_colores[self.cursor] = self.color_s
        return l_colores

    def draw_menu(self):
        y=self.start[1]
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

class Juego:
    nivel=0
    surface=None

    def __init__(self,nivel,surface):
        self.nivel = nivel
        self.surface = surface

    def start_0(self):
        c_fondo = (255,0,0)
        ALTO = 600
        ANCHO = 800
        global vxi,vyi
        vxi=25
        vyi=25
        pygame.init()
        pantalla = pygame.display.set_mode((ANCHO, ALTO+30))
        pygame.display.set_caption(" El laberinto de la muerte - [v1] ", 'Spine Runtime')
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
                picture = pygame.image.load("gameover.png")
                picture = pygame.transform.scale(picture, (ANCHO, ALTO+10))
                rect = picture.get_rect()
                #print "VIDA : " , jugador.vida
                muerto = True
                update_status_section()
                sub.fill((0,0,0))
                tipo.set_bold(True)
                teclas1 = tipo2.render("Presione ESC para salir" , 1 , (255,0,0))
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
                        terminar = True
                    if event.key == pygame.K_SPACE:
                        playsound("shot.ogg")
                        b = Bullet("bala.png", jugador.rect.x, jugador.rect.y, jugador.direccion)
                        ls_bajasj.add(b)
                        ls_todos.add(b)

                    """if event.key == pygame.K_t:
                        for i in ls_DL:
                            jugador.rect.x,jugador.rect.y = i.rect.x, i.rect.y"""
                    if event.key == pygame.K_e:
                        for el in ls_DL:
                            if(checkCollision(jugador,el)):
                                if(el.tipo == "dinamita"):
                                    playsound("open.ogg")
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
                                    playsound("open.ogg")
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
                                        playsound("er.ogg")
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
                            playsound("hit.ogg")
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
                    playsound("go.ogg")
                    flag_sonido=False
                rect = rect.move((0,0))
                pantalla.blit(picture, rect)
                pantalla.blit(teclas1, [ANCHO/2-180,ALTO/2+100])
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
                        playsound("win.ogg")
                        flag_sonido=False
                    picturewin = pygame.image.load("win.png")
                    picturewin = pygame.transform.scale(picturewin, (ANCHO, ALTO+10))
                    win = True
                    sub.fill((0,0,0))
                    pantalla.blit(picturewin, [0,0])
                    teclas1 = tipo2.render("Presione ESC para salir" , 1 , (255,0,0))
                    teclas2 = tipo2.render("Presione N para juego nuevo " , 1 , (255,0,0))
                    pantalla.blit(teclas1, [ANCHO/2-180,ALTO/2+100])
                    pantalla.blit(teclas2, [ANCHO/2-220,ALTO/2+200])


            if(not cont_llave == 0 and not win):
                pantalla.blit(rq_llave, [ANCHO/2-200,ALTO/2-100])
                pic = pygame.image.load("key2.png")
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
