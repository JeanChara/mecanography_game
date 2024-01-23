from pickle import FALSE, TRUE
import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
FONT_SIZE = 36
VERDE = (0, 255, 0)


# Inicializar la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Mecanografía")
clock = pygame.time.Clock()

# Cargar la fuente
font = pygame.font.Font(None, FONT_SIZE)

# Lista de palabras/Enunciados para el juego
palabras = ["Enunciado"
            , "juego"
            , "teclado"
            , "programacion"
            , "pygame"
            , "mecanografia"
            , "Prototipo"]

# seleccion y reproduccion de musica
music_files = ["../sfx/song1.OGG",] # Agregar musica en caso se desee, la musica utilizada no es de nuestra pertenencia
current_song_index = 0
pygame.mixer.music.load(music_files[current_song_index])
pygame.mixer.music.set_volume(0.15)
pygame.mixer.music.play()

# Función para obtener una nueva palabra aleatoria
def obtener_palabra_aleatoria():
    return random.choice(palabras)
def dividir_en_lineas(texto, limite_caracteres):
    palabras = texto.split()
    lineas = []
    linea_actual = ""
    for palabra in palabras:
        if len(linea_actual) + len(palabra) <= limite_caracteres:
            linea_actual += palabra + " "
        else:
            lineas.append(linea_actual.rstrip())
            linea_actual = palabra + " "
    lineas.append(linea_actual.rstrip())
    return lineas
def mostrar_palabra_actual(palabra_actual):
    palabra_lineas = dividir_en_lineas(palabra_actual, 50)
    for i, linea in enumerate(palabra_lineas):
        palabra_renderizada = font.render(linea, True, BLACK)
        y_offset = i * (palabra_renderizada.get_height() + 10)  # Puedes ajustar el espaciado vertical
        screen.blit(palabra_renderizada, (WIDTH // 2 - palabra_renderizada.get_width() // 2, HEIGHT // 3 - palabra_renderizada.get_height() // 2 + y_offset))

def mostrar_estadisticas_basicas(aciertos,fallos):
    aciertos_renderizados = font.render("Aciertos: "+str(aciertos), True, BLACK)
    screen.blit(aciertos_renderizados, (WIDTH // 4 , HEIGHT // 15))

    fallos_renderizados = font.render("Fallos: "+str(fallos), True, BLACK)
    screen.blit(fallos_renderizados, (WIDTH // 2 , HEIGHT // 15))
def mostrar_temporizador(tiempo_restante):
    texto_temporizador = font.render("Tiempo Restante: {} s".format(tiempo_restante), True, BLACK)
    screen.blit(texto_temporizador, (10, 10))
def mostrar_estadisticas_finales(aciertos, fallos,letras_acertadas, tiempo_limite):
    fondo = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    fondo.fill((0, 0, 0, 128))  # Fondo semi-transparente
    screen.blit(fondo, (0, 0))

    mensaje = font.render("Juego Terminado", True, WHITE)
    screen.blit(mensaje, (WIDTH // 2 - mensaje.get_width() // 2, HEIGHT // 3))
    palabras_por_segundo = (letras_acertadas//5)/ tiempo_limite

    estadisticas_aciertos = font.render("Aciertos: " + str(aciertos), True, WHITE)
    estadisticas_fallos = font.render("Fallos: " + str(fallos), True, WHITE)
    estadisticas_letras_acertadas = font.render("Letras acertadas: " + str(letras_acertadas), True, WHITE)
    estadisticas_palabras_por_segundo = font.render("Palabras por segundo: " + str(palabras_por_segundo), True, WHITE)
    estadisticas_fin = font.render("Presiona ENTER para volver al menu", True, WHITE)

    screen.blit(estadisticas_aciertos, (WIDTH // 2 - estadisticas_aciertos.get_width() // 2, HEIGHT // 2))
    screen.blit(estadisticas_fallos, (WIDTH // 2 - estadisticas_fallos.get_width() // 2, HEIGHT // 2 + 50))
    screen.blit(estadisticas_letras_acertadas, (WIDTH // 2 - estadisticas_letras_acertadas.get_width() // 2, HEIGHT // 2 + 100))
    screen.blit(estadisticas_palabras_por_segundo, (WIDTH // 2 - estadisticas_palabras_por_segundo.get_width() // 2, HEIGHT // 2 + 150))
    screen.blit(estadisticas_fin, (WIDTH // 2 - estadisticas_fin.get_width() // 2, HEIGHT // 2 + 200))
    
    pygame.display.flip()

#Lista de palabras correctas
letras_correctas = []


# Función principal del juego
def run():

    background = pygame.image.load("../img/background_mecanography.png").convert()
    palabra_actual = obtener_palabra_aleatoria()
    input_usuario = ""
    palabra_completada = False
    aciertos = 0
    fallos = 0
    letras_acertadas = 0
    letras_correctas = []
    radio = 40
    speed_y = 1
    felicitacion = False
    temporizador_iniciado = True
    tiempo_limite = 10 # default
    tiempo_restante = tiempo_limite
    aux_tiempo = 0


    while True:
        imagen = pygame.transform.scale(background,(WIDTH,HEIGHT))
        screen.blit(imagen,[0,0]) # Fondo 

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Para cerrar el juego
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN: # Para presionar una tecla
                if event.key == pygame.K_ESCAPE: # Para cerrar el juego al presionar ESC
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_BACKSPACE: # Para borrar la entrada del usuario
                    input_usuario = input_usuario[:-1] # Eliminar el último carácter de la entrada del usuario
                elif event.key in range(32, 127):
                    input_usuario += event.unicode # Añadir el carácter presionado
                    if (palabra_actual[0:1] == input_usuario):
                        letras_correctas.append(palabra_actual[0:1]) # aun sin uso, (para poner de otro color las letras ya ingresadas)
                        palabra_actual = palabra_actual[1:] # eliminamos primera letra del enunciado / palabra
                        letras_acertadas += 1
                        input_usuario = ""
                    else:
                        input_usuario = ""
                        fallos += 1
                # presione enter
                elif event.key == pygame.K_RETURN and not temporizador_iniciado: # Para iniciar el temporizador e iniciar el juego al presionar escape
                    temporizador_iniciado = True
                    aciertos = 0
                    fallos = 0
                    letras_acertadas = 0
                    letras_correctas = []
                    input_usuario = ""
                    palabra_actual = obtener_palabra_aleatoria()


        
        if temporizador_iniciado == True:
            # cuando nuestra ultima entrada coincide con la palabra restante
            if input_usuario == palabra_actual: 
                palabra_completada = True
                palabra_actual = obtener_palabra_aleatoria()
                input_usuario = ""

            else:
                palabra_completada = False
            
            if palabra_completada:
                aciertos += 1
                letras_correctas = [] 
                felicitacion = True

                # generando datos para mensaje dinamico en figura
                cord_x = random.randint(0+radio,WIDTH-radio)
                cord_y = random.randint(0+radio,HEIGHT-radio)
                cord_y_inicial = cord_y
            
            if felicitacion:# imprime una figura que indica un aumento en aciertos
                cord_y -= speed_y
                pygame.draw.circle(screen,BLACK,(cord_x,cord_y),radio)
                point_font = pygame.font.Font(None, 50)
                extra_points = point_font.render("+1", True, WHITE)
                screen.blit(extra_points, (cord_x-(radio/2.2),cord_y-(radio/2.2)))
                if cord_y == (cord_y_inicial - 60):
                    felicitacion = False

            # Renderizar la palabra actual
            mostrar_palabra_actual(palabra_actual)
        
            # buscar forma para convertir en gris las palabras ya escritas, para que se vea mejor el progreso.
            letras_renderizadas = font.render("Letras correctas: " + "".join(letras_correctas), True, VERDE)
            screen.blit(letras_renderizadas, (WIDTH // 4, HEIGHT // 10))

            mostrar_estadisticas_basicas(aciertos,fallos)
            mostrar_temporizador(tiempo_restante)

            # Actualizar la pantalla
            pygame.display.flip()

            # Controlar la velocidad del juego
            clock.tick(FPS)

            if temporizador_iniciado:
                
                aux_tiempo += 1
                if aux_tiempo >= 60:
                    tiempo_restante -= aux_tiempo//60
                    aux_tiempo = 0

                # Finalizar el juego cuando el temporizador llega a cero
                if tiempo_restante <= 0:
                    mostrar_estadisticas_finales(aciertos,fallos,letras_acertadas,tiempo_limite)

                    temporizador_iniciado = False
                    tiempo_restante = tiempo_limite

def run_game():
    run()

if __name__ == "__main__":
    run()

    