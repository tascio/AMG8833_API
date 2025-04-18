import numpy as np
import cv2
import pygame
import requests

URL = '' #URL del docker es. http://172.16.0.1:5050

def get_tmax():
    return float(requests.post(f'{URL}/api/v1.0/get_tmax').json()['t_max'])
def get_tthermistor():
    return float(requests.post(f'{URL}/api/v1.0/get_tthermistor').json()['t_thermistor'])
def get_array():
    data = requests.post(f'{URL}/api/v1.0/get_tarray').json()
    array = np.zeros((8, 8))
    for key, value in data.items():
        row = int(key[5])
        col = int(key[6])
        array[row, col] = value
    return array

VMIN=20
VMAX=40
FPS=30
INTERP = 10 #6 default

# Interpolation Properties
pix_res = (8, 8)  # original resolution
pix_mult = INTERP  # multiplier for interpolation
interp_res = (pix_res[0] * pix_mult, pix_res[1] * pix_mult)

# Funzione di interpolazione
def interp_lanczos(z_var, scale=INTERP):
    z_var = cv2.GaussianBlur(z_var, (3, 3), 0)  # Riduce il rumore
    return cv2.resize(z_var, (z_var.shape[1] * scale, z_var.shape[0] * scale), interpolation=cv2.INTER_LANCZOS4)

# Inizializzazione di Pygame
pygame.init()
WINDOW_SIZE = (640, 640)  # Dimensione finestra (es. 8*6=48 pixel interpolati, scalati a 480x480)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('AMG8833 Image Interpolation')

#RENDER TEMPS
#AVANZATO
def temp_to_color(temp, vmin=VMIN, vmax=VMAX):
    norm_temp = (temp - vmin) / (vmax - vmin)
    norm_temp = np.clip(norm_temp, 0, 1) * 255
    color = cv2.applyColorMap(np.uint8([norm_temp]), cv2.COLORMAP_JET)[0][0]
    return (int(color[2]), int(color[1]), int(color[0]))
#STANDARD
# def temp_to_color(temp, vmin=VMIN, vmax=VMAX):
#     norm_temp = (temp - vmin) / (vmax - vmin)  # Normalizza tra 0 e 1
#     norm_temp = np.clip(norm_temp, 0, 1)
#     if norm_temp < 0.5:
#         r = 0
#         g = int(255 * (1 - 2 * norm_temp))
#         b = 255
#     else:
#         r = int(255 * (2 * norm_temp - 1))
#         g = int(255 * (2 - 2 * norm_temp))
#         b = 0
#     return (r, g, b)

# Loop principale
pix_to_read = 64  # read all 64 pixels
clock = pygame.time.Clock()  # Per controllare il framerate

running = True
while running:
    # Gestione eventi Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    T_thermistor = get_tthermistor()
    pixels = get_array()
    T_max = get_tmax()
    print('Thermistor: ', T_thermistor)
    print('All Pixels :\n', pixels)
    print('Max temp° => ', T_max)

    # Interpolazione dei dati
    new_z = interp_lanczos(np.reshape(pixels, pix_res))
    
    # Converti i dati in un'immagine RGB per Pygame
    img_array = np.zeros((interp_res[1], interp_res[0], 3), dtype=np.uint8)
    for i in range(interp_res[0]):
        for j in range(interp_res[1]):
            temp = new_z[j, i]  # Nota: Pygame usa (y, x)
            img_array[j, i] = temp_to_color(temp, vmin=VMIN, vmax=VMAX)

    # Crea una superficie Pygame dall'array
    img_surface = pygame.surfarray.make_surface(np.transpose(img_array, (1, 0, 2)))
    img_surface = pygame.transform.scale(img_surface, WINDOW_SIZE)  # Scala alla dimensione della finestra

    # Disegna sulla finestra
    screen.blit(img_surface, (0, 0))

    #CREA LA BARRA LATERALE
    for i in range(256):
        color = temp_to_color(VMIN + (VMAX-VMIN) * i / 255)
        pygame.draw.rect(screen, color, (WINDOW_SIZE[0] - 20, i * WINDOW_SIZE[1] // 256, 20, WINDOW_SIZE[1] // 256))

    pygame.display.flip()  # Aggiorna lo schermo

    clock.tick(FPS)  # Limita a 30 FPS per non sovraccaricare

pygame.quit()
