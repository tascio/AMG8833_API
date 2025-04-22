import numpy as np
import cv2
import pygame
import socketio

VMIN = 18
VMAX = 32
FPS = 30
INTERP = 10
URL = 'http://172.16.98.7:5060'
latest_data = {
    't_max': None,
    't_thermistor': None,
    't_array': np.zeros((8, 8))
}

sio = socketio.Client()

@sio.event
def connect():
    print("✅ Connesso al WebSocket")

@sio.on('sensor_data')
def on_sensor_data(data):
    global latest_data
    latest_data['t_max'] = data['t_max']
    latest_data['t_thermistor'] = data['t_thermistor']
    arr = np.zeros((8, 8))
    for key, val in data['t_array'].items():
        row = int(key[5])
        col = int(key[6])
        arr[row][col] = val
    latest_data['t_array'] = arr

@sio.event
def disconnect():
    print("🔌 Disconnesso dal WebSocket")

sio.connect(URL)  #IP del container websocket_manager

pix_res = (8, 8)
interp_res = (pix_res[0] * INTERP, pix_res[1] * INTERP)

def interp_lanczos(z_var, scale=INTERP):
    z_var = cv2.GaussianBlur(z_var, (3, 3), 0)
    return cv2.resize(z_var, (z_var.shape[1] * scale, z_var.shape[0] * scale), interpolation=cv2.INTER_LANCZOS4)

def temp_to_color(temp, vmin=VMIN, vmax=VMAX):
    norm_temp = (temp - vmin) / (vmax - vmin)
    norm_temp = np.clip(norm_temp, 0, 1) * 255
    color = cv2.applyColorMap(np.uint8([norm_temp]), cv2.COLORMAP_JET)[0][0]
    return (int(color[2]), int(color[1]), int(color[0]))

pygame.init()
WINDOW_SIZE = (640, 640)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('AMG8833 Image via WebSocket')
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    t_max = latest_data['t_max']
    t_thermistor = latest_data['t_thermistor']
    pixels = latest_data['t_array']

    if t_max is not None and t_thermistor is not None:
        print('Thermistor:', t_thermistor)
        print('Max temp° =>', t_max)

        new_z = interp_lanczos(pixels)

        img_array = np.zeros((interp_res[1], interp_res[0], 3), dtype=np.uint8)
        for i in range(interp_res[0]):
            for j in range(interp_res[1]):
                temp = new_z[j, i]
                img_array[j, i] = temp_to_color(temp)

        img_surface = pygame.surfarray.make_surface(np.transpose(img_array, (1, 0, 2)))
        img_surface = pygame.transform.scale(img_surface, WINDOW_SIZE)

        screen.blit(img_surface, (0, 0))

        # Barra colore laterale
        for i in range(256):
            color = temp_to_color(VMIN + (VMAX - VMIN) * i / 255)
            pygame.draw.rect(screen, color, (WINDOW_SIZE[0] - 20, i * WINDOW_SIZE[1] // 256, 20, WINDOW_SIZE[1] // 256))

        pygame.display.flip()

    clock.tick(FPS)

pygame.quit()