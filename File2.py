#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading,time,pygame,sys

pygame.init()
pantalla = pygame.display.set_mode((1000,600))
tipo = pygame.font.SysFont("monospace", 15)
tipo.set_bold(True)
teclas1 = tipo.render("Presione ESC para salir" , 1 , (255,0,0))
pantalla.blit(teclas1,(100,100))
pygame.display.flip()
def worker():
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        for i in range(10,100):
            pantalla.fill((0,0,0))
            pantalla.blit(teclas1,(i,100))
            pygame.display.flip()

def servicio():
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        break
        if(raw_input("Si?") == "no"):
            w.do_run = False
            w.join()
            break

global w
#Asignacion nombres y creacion de threads
w = threading.Thread(target=worker, name='Worker' )  #Se asigna el nombre al Thread de Worker con la accion worker()
t = threading.Thread(target=servicio, name='Servicio') #Se asigna el nombre al Thread de Servicio con la accion servicio()


#Se lanzan los threads
w.start()
t.start()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            w.do_run = False
            w.join()
            t.do_run = False
            t.join()
            pygame.display.quit()
            sys.exit(0)
