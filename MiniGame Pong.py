import pygame
import random

# Inicializar pygame
pygame.init()

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)

# Tamaño de la ventana
ANCHO = 1280
ALTO = 720
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("PONG")

# Velocidades
velocidad_pala = 14
velocidad_pelota = 10  # Velocidad inicial de la pelota

# Fuente para la puntuación
fuente = pygame.font.SysFont("Impact", 30)

# Tamaños de elementos
pala_ancho = 15
pala_alto = 100
pelota_ancho = 30
pelota_alto = 30

# Límite de vidas
vidas_iniciales = 5

# Cargar la música de fondo
pygame.mixer.music.load("musica.mp3")
pygame.mixer.music.play(-1, 0.0)  # Reproducir música en loop (-1 significa loop infinito)

# Cargar el sonido para cuando se anota un punto o se pierde una vida
sonido_punto = pygame.mixer.Sound("punto.mp3")

# Cargar la imagen de fondo
try:
    fondo_img = pygame.image.load("fondo.jpg")
    fondo_img = pygame.transform.scale(fondo_img, (ANCHO, ALTO))  # Escalar la imagen al tamaño de la ventana
except pygame.error:
    print("No se pudo cargar la imagen de fondo.")
    fondo_img = None


# Cargar la imagen de la pelota
pelota_img = pygame.image.load("toni.png")
pelota_img = pygame.transform.scale(pelota_img, (pelota_ancho, pelota_alto))  # Ajustar tamaño a la pelota

# Clase de la pelota
class Pelota:
    def __init__(self):
        self.x = ANCHO // 2 - pelota_ancho // 2
        self.y = ALTO // 2 - pelota_alto // 2
        self.vel_x = random.choice([velocidad_pelota, -velocidad_pelota])
        self.vel_y = random.choice([velocidad_pelota, -velocidad_pelota])

    def mover(self):
        self.x += self.vel_x
        self.y += self.vel_y

        # Rebote en los bordes superior e inferior
        if self.y <= 0 or self.y + pelota_alto >= ALTO:
            self.vel_y = -self.vel_y

    def dibujar(self, ventana):
        ventana.blit(pelota_img, (self.x, self.y))  # Dibujar la pelota como imagen

    def reiniciar(self):
        self.__init__()

# Clase para las palas
class Pala:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def mover(self, direccion):
        if direccion == "arriba" and self.y > 0:
            self.y -= velocidad_pala
        elif direccion == "abajo" and self.y + pala_alto < ALTO:
            self.y += velocidad_pala

    def dibujar(self, ventana):
        # Dibujar un borde negro para el efecto de neón
        pygame.draw.rect(ventana, NEGRO, (self.x - 2, self.y - 2, pala_ancho + 4, pala_alto + 4))
        # Dibujar la pala principal
        pygame.draw.rect(ventana, self.color, (self.x, self.y, pala_ancho, pala_alto))

# Función para mostrar la puntuación y vidas
def mostrar_puntuacion(vidas_jugador1, vidas_jugador2):
    texto = fuente.render(f"{vidas_jugador1} - {vidas_jugador2}", True, BLANCO)
    ventana.blit(texto, (ANCHO // 2 - texto.get_width() // 2, 20))

# Función para mostrar los mensajes de ganador y perdedor
def mostrar_mensaje(texto, x, y, color):
    mensaje = fuente.render(texto, True, color)
    ventana.blit(mensaje, (x - mensaje.get_width() // 2, y - mensaje.get_height() // 2))

# Función para manejar el juego
def juego(modo_multijugador, lado_jugador1, lado_jugador2, velocidad_pelota):
    # Iniciar vidas
    vidas_jugador1 = vidas_iniciales
    vidas_jugador2 = vidas_iniciales

    # Crear objetos
    pelota = Pelota()

    # Crear palas con colores específicos
    pala_jugador1 = Pala(30, ALTO // 2 - pala_alto // 2, VERDE) if lado_jugador1 == "izquierda" else Pala(ANCHO - 30 - pala_ancho, ALTO // 2 - pala_alto // 2, VERDE)
    pala_jugador2 = Pala(ANCHO - 30 - pala_ancho, ALTO // 2 - pala_alto // 2, ROJO) if lado_jugador2 == "derecha" else Pala(30, ALTO // 2 - pala_alto // 2, ROJO)

    # Reloj de control de FPS
    reloj = pygame.time.Clock()

    # Bucle principal del juego
    while True:
        # Dibujar el fondo si está disponible, si no, rellenar con negro
        if fondo_img:
            ventana.blit(fondo_img, (0, 0))
        else:
            ventana.fill(NEGRO)

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Obtener las teclas presionadas
        teclas = pygame.key.get_pressed()

        # Si se presiona Escape, regresar al menú
        if teclas[pygame.K_ESCAPE]:
            pygame.time.delay(500)  # Pausar brevemente antes de regresar al menú
            return menu()

        # Movimiento de las palas para multijugador
        if modo_multijugador:
            if teclas[pygame.K_w]:
                pala_jugador1.mover("arriba")
            if teclas[pygame.K_s]:
                pala_jugador1.mover("abajo")
            if teclas[pygame.K_UP]:
                pala_jugador2.mover("arriba")
            if teclas[pygame.K_DOWN]:
                pala_jugador2.mover("abajo")
        else:
            # Movimiento del jugador 1
            if teclas[pygame.K_w]:
                pala_jugador1.mover("arriba")
            if teclas[pygame.K_s]:
                pala_jugador1.mover("abajo")

            # Movimiento automático de la máquina (jugador 2)
            if pelota.y < pala_jugador2.y + pala_alto // 2:
                pala_jugador2.mover("arriba")
            elif pelota.y > pala_jugador2.y + pala_alto // 2:
                pala_jugador2.mover("abajo")

        # Mover la pelota
        pelota.mover()

        # Colisiones con las palas
        if (pelota.x <= pala_jugador1.x + pala_ancho and pelota.y + pelota_alto >= pala_jugador1.y and pelota.y <= pala_jugador1.y + pala_alto):
            pelota.vel_x = -pelota.vel_x

        if (pelota.x + pelota_ancho >= pala_jugador2.x and pelota.y + pelota_alto >= pala_jugador2.y and pelota.y <= pala_jugador2.y + pala_alto):
            pelota.vel_x = -pelota.vel_x

        # Verificar si alguien ha perdido una vida
        if pelota.x <= 0:
            vidas_jugador2 -= 1
            sonido_punto.play()  # Reproducir sonido cuando jugador 2 pierde una vida
            pelota.reiniciar()
            pygame.time.delay(1500)  # Pausa de 1.5 segundos
        elif pelota.x + pelota_ancho >= ANCHO:
            vidas_jugador1 -= 1
            sonido_punto.play()  # Reproducir sonido cuando jugador 1 pierde una vida
            pelota.reiniciar()
            pygame.time.delay(1500)  # Pausa de 1.5 segundos

        # Mostrar la puntuación y vidas
        mostrar_puntuacion(vidas_jugador1, vidas_jugador2)

        # Verificar si un jugador ha perdido todas las vidas
        if vidas_jugador1 <= 0:
            ventana.fill(NEGRO)
            mostrar_mensaje("WINNER Enhorabuena campeón.", ANCHO // 2, ALTO // 4, VERDE)
            mostrar_mensaje("LOSER Mejor dedicate a la petanca.", ANCHO // 2, ALTO * 3 // 4, ROJO)
            pygame.display.update()
            pygame.time.delay(4000)  # Pausar 4 segundos
            break  # Terminar el juego si un jugador gana

        if vidas_jugador2 <= 0:
            ventana.fill(NEGRO)
            mostrar_mensaje("WINNER Enhorabuena campeón.", ANCHO // 2, ALTO // 4, VERDE)
            mostrar_mensaje("LOSER Mejor dedicate a la petanca.", ANCHO // 2, ALTO * 3 // 4, ROJO)
            pygame.display.update()
            pygame.time.delay(4000)  # Pausar 4 segundos
            break  # Terminar el juego si un jugador gana

        # Dibujar los elementos del juego
        pelota.dibujar(ventana)
        pala_jugador1.dibujar(ventana)
        pala_jugador2.dibujar(ventana)

        # Actualizar la pantalla
        pygame.display.update()

        # Controlar la velocidad del juego
        reloj.tick(60)

# Función para mostrar el menú de inicio
def menu():
    global velocidad_pelota  # Usar la variable global para cambiar la velocidad
    # Mostrar menú inicial
    while True:
        ventana.fill(NEGRO)
        texto_bienvenida = fuente.render("Bienvenido a PONG!", True, BLANCO)
        ventana.blit(texto_bienvenida, (ANCHO // 2 - texto_bienvenida.get_width() // 2, ALTO // 4))

        texto_opciones = fuente.render("Presiona 'S' para jugar Individual o 'M' para Multijugador", True, BLANCO)
        ventana.blit(texto_opciones, (ANCHO // 2 - texto_opciones.get_width() // 2, ALTO // 2))

        # Opciones de velocidad
        texto_velocidad = fuente.render(f"Velocidad bola: {velocidad_pelota}", True, BLANCO)
        ventana.blit(texto_velocidad, (ANCHO // 2 - texto_velocidad.get_width() // 2, ALTO // 2 + 40))

        # Opciones para elegir la velocidad
        texto_vel_1 = fuente.render("Presiona '1' para velocidad 5", True, BLANCO)
        texto_vel_2 = fuente.render("Presiona '2' para velocidad 10", True, BLANCO)
        texto_vel_3 = fuente.render("Presiona '3' para velocidad 15", True, BLANCO)

        ventana.blit(texto_vel_1, (ANCHO // 2 - texto_vel_1.get_width() // 2, ALTO // 2 + 80))
        ventana.blit(texto_vel_2, (ANCHO // 2 - texto_vel_2.get_width() // 2, ALTO // 2 + 120))
        ventana.blit(texto_vel_3, (ANCHO // 2 - texto_vel_3.get_width() // 2, ALTO // 2 + 160))

        # Mensaje de "Created and designed by"
        texto_creditos = fuente.render("**** Created and designed by: A. Raño © ****", True, ROJO)
        ventana.blit(texto_creditos, (ANCHO // 2 - texto_creditos.get_width() // 2, ALTO - 80))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_m:  # Multijugador
                    modo_multijugador = True
                    lado_jugador1 = "izquierda"  # Default lado izquierdo
                    lado_jugador2 = "derecha"  # Default lado derecho
                    return juego(modo_multijugador, lado_jugador1, lado_jugador2, velocidad_pelota)
                elif evento.key == pygame.K_s:  # Jugador vs Máquina
                    modo_multijugador = False
                    lado_jugador1 = "izquierda"  # Default lado izquierdo
                    lado_jugador2 = "derecha"  # Máquina juega en el lado derecho
                    return juego(modo_multijugador, lado_jugador1, lado_jugador2, velocidad_pelota)
                elif evento.key == pygame.K_1:  # Velocidad 5
                    velocidad_pelota = 5
                elif evento.key == pygame.K_2:  # Velocidad 10
                    velocidad_pelota = 10
                elif evento.key == pygame.K_3:  # Velocidad 15
                    velocidad_pelota = 15

# Llamar al menú para iniciar el juego
menu()

# Cerrar pygame al finalizar
pygame.quit()
