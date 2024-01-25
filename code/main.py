import pygame
import sys
import random

class MainGame:
    def __init__(self):
        # Inicializar Pygame
        pygame.init()
        
        # Configuración de la pantalla
        self.WIDTH, self.HEIGHT = 800, 600
        self.FPS = 60
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.FONT_SIZE = 30
        self.VERDE = (0, 255, 0)
        
        # Inicializar la pantalla
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Juego de Mecanografía")
        self.clock = pygame.time.Clock()

        # Cargar la fuente
        self.font = pygame.font.Font("../fuente/Cafe.ttf", self.FONT_SIZE)

        # Lista de palabras/Enunciados para el juego
        self.palabras = ["Microprocesador",
                        "Memoria RAM",
                        "Registro", 
                        "Instrucción", 
                        "Teclado", 
                        "Programacion", 
                        "Pygame", 
                        "Mecanografia",
                        "Bus de datos",
                        "Bus de direcciones",
                        "Memoria Cache",
                        "ALU (Unidad Lógica Aritmética)",
                        "Sistema Operativo",
                        "BIOS",
                        "Interruptor",
                        "Decodificador de Instrucciones",
                        "mov ah, dato",
                        "Lenguaje maquina",
                        "8 bits = 1 byte",
                        "1 Kilobyte (KB) = 1024 bytes",
                        "1 Megabyte (MB) = 1.024 KB",
                        "1 Gigabyte (GB) = 1.024 MB",
                        "1 Terabyte (TB) = 1.024 GB"]
        
    # Función para obtener una nueva palabra aleatoria de nuestro array de palabras
    def obtener_palabra_aleatoria(self):
        return random.choice(self.palabras)

    def dividir_en_lineas(self, texto, limite_caracteres):
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

    def mostrar_palabra_actual(self, palabra_actual):
        palabra_lineas = self.dividir_en_lineas(palabra_actual, 50)
        for i, linea in enumerate(palabra_lineas):
            palabra_renderizada = self.font.render(linea, True, self.BLACK)
            y_offset = i * (palabra_renderizada.get_height() + 10)
            self.screen.blit(palabra_renderizada, (self.WIDTH // 2 - palabra_renderizada.get_width() // 2, self.HEIGHT // 3+30 - palabra_renderizada.get_height() // 2 + y_offset))

    def mostrar_temporizador(self, tiempo_restante):
        texto_temporizador = self.font.render("Tiempo Restante: {} s".format(tiempo_restante), True, self.BLACK)
        self.screen.blit(texto_temporizador, (20, 15))

    def mostrar_estadisticas_basicas(self, aciertos, fallos):
        aciertos_renderizados = self.font.render("Aciertos: "+str(aciertos), True, self.BLACK)
        self.screen.blit(aciertos_renderizados, (self.WIDTH // 4 +30, self.HEIGHT // 9))

        fallos_renderizados = self.font.render("Fallos: "+str(fallos), True, self.BLACK)
        self.screen.blit(fallos_renderizados, (self.WIDTH // 2 +30, self.HEIGHT // 9))
    def mostrar_estadisticas_finales(self, aciertos, fallos, letras_acertadas, tiempo_limite):
        fondo = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        fondo.fill((0, 0, 0, 128)) # Fondo semi-transparente
        self.screen.blit(fondo, (0, 0))

        mensaje = self.font.render("Juego Terminado", True, self.WHITE)
        self.screen.blit(mensaje, (self.WIDTH // 2 - mensaje.get_width() // 2, self.HEIGHT // 3))
        palabras_por_segundo = (letras_acertadas // 5) / tiempo_limite

        estadisticas_aciertos = self.font.render("Aciertos: " + str(aciertos), True, self.WHITE)
        estadisticas_fallos = self.font.render("Fallos: " + str(fallos), True, self.WHITE)
        estadisticas_letras_acertadas = self.font.render("Letras acertadas: " + str(letras_acertadas), True, self.WHITE)
        estadisticas_palabras_por_segundo = self.font.render("Palabras por segundo: " + str(palabras_por_segundo), True, self.WHITE)
        estadisticas_fin = self.font.render("Presiona ENTER para volver al menu", True, self.WHITE)

        self.screen.blit(estadisticas_aciertos, (self.WIDTH // 2 - estadisticas_aciertos.get_width() // 2, self.HEIGHT // 2))
        self.screen.blit(estadisticas_fallos, (self.WIDTH // 2 - estadisticas_fallos.get_width() // 2, self.HEIGHT // 2 + 50))
        self.screen.blit(estadisticas_letras_acertadas, (self.WIDTH // 2 - estadisticas_letras_acertadas.get_width() // 2, self.HEIGHT // 2 + 100))
        self.screen.blit(estadisticas_palabras_por_segundo, (self.WIDTH // 2 - estadisticas_palabras_por_segundo.get_width() // 2, self.HEIGHT // 2 + 150))
        self.screen.blit(estadisticas_fin, (self.WIDTH // 2 - estadisticas_fin.get_width() // 2, self.HEIGHT // 2 + 200))
        
        pygame.display.flip()


    # Función principal del juego
    def run(self):
        # seleccion y reproduccion de musica
        music_files = ["../sfx/song1.OGG",] # Agregar musica en caso se desee, la musica utilizada no es de nuestra pertenencia
        current_song_index = 0
        pygame.mixer.music.load(music_files[current_song_index])
        pygame.mixer.music.set_volume(0.15)
        pygame.mixer.music.play()

        background = pygame.image.load("../img/fondo.jpg").convert()
        palabra_actual = self.obtener_palabra_aleatoria()
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
        tiempo_limite = 50
        tiempo_restante = tiempo_limite
        aux_tiempo = 0

        while True:
            imagen = pygame.transform.scale(background,(self.WIDTH,self.HEIGHT))
            self.screen.blit(imagen, [0,0])

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
                            letras_correctas.append(palabra_actual[0:1]) # mostramos letras correctas actuales
                            palabra_actual = palabra_actual[1:] # eliminamos primera letra del enunciado / palabra
                            letras_acertadas += 1
                            input_usuario = ""
                        else:
                            input_usuario = ""
                            fallos += 1
                            tiempo_restante -= 1
                    elif event.key == pygame.K_RETURN and not temporizador_iniciado: # Para iniciar el temporizador e iniciar el juego al presionar ENTER
                        temporizador_iniciado = True
                        aciertos = 0
                        fallos = 0
                        letras_acertadas = 0
                        letras_correctas = []
                        input_usuario = ""
                        palabra_actual = self.obtener_palabra_aleatoria()

            if temporizador_iniciado == True: # cuando nuestra ultima entrada coincide con la palabra restante
                if input_usuario == palabra_actual:
                    palabra_completada = True
                    palabra_actual = self.obtener_palabra_aleatoria()
                    input_usuario = ""
                    tiempo_restante += 5
                else:
                    palabra_completada = False
                
                if palabra_completada:
                    aciertos += 1
                    letras_correctas = [] 
                    felicitacion = True
                    # generando datos para mensaje dinamico en figura
                    cord_x = random.randint(0+radio, self.WIDTH-radio)
                    cord_y = random.randint(0+radio, self.HEIGHT-radio)
                    cord_y_inicial = cord_y
                
                if felicitacion: # imprime una figura que indica un aumento en aciertos
                    cord_y -= speed_y
                    pygame.draw.circle(self.screen, self.BLACK, (cord_x, cord_y), radio)
                    point_font = pygame.font.Font(None, 50)
                    extra_points = point_font.render("+1", True, self.WHITE)
                    self.screen.blit(extra_points, (cord_x-(radio/2.2), cord_y-(radio/2.2)))
                    if cord_y == (cord_y_inicial - 60):
                        felicitacion = False

                self.mostrar_palabra_actual(palabra_actual) # Renderizar la palabra actual
                letras_renderizadas = self.font.render("Letras correctas: " + "".join(letras_correctas), True, self.VERDE)
                self.screen.blit(letras_renderizadas, (self.WIDTH // 4+30, self.HEIGHT // 6))
                self.mostrar_estadisticas_basicas(aciertos, fallos)
                self.mostrar_temporizador(tiempo_restante)

                # Actualizar la pantalla
                pygame.display.flip()
                # Controlar la velocidad del juego
                self.clock.tick(self.FPS)

                if temporizador_iniciado:
                    aux_tiempo += 1
                    if aux_tiempo >= 60:
                        tiempo_restante -= aux_tiempo//60
                        aux_tiempo = 0

                    if tiempo_restante <= 0: # Finalizar el juego cuando el temporizador llega a cero
                        self.mostrar_estadisticas_finales(aciertos, fallos, letras_acertadas, tiempo_limite)
                        temporizador_iniciado = False
                        tiempo_restante = tiempo_limite

def run_game():
    juego = MainGame()
    juego.run()
    
if __name__ == "__main__":
    juego = MainGame()
    juego.run()
