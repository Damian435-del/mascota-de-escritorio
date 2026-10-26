# ---------- LIBRERÍAS (herramientas que usa el programa) ----------
import tkinter as tk      # para crear la ventana
import random             # para elegir cosas al azar (cuándo cambia de dirección)
import time               # para medir cuánto tiempo pasa sin que lo toques
from PIL import Image, ImageTk, ImageSequence, ImageOps   # Pillow: para trabajar con el GIF

# ---------- VENTANA PRINCIPAL ----------
root = tk.Tk()
root.overrideredirect(True)                       # quita los bordes y la barra de la ventana
root.attributes("-topmost", True)                 # la mantiene siempre por encima de otras ventanas
root.attributes("-transparentcolor", "#f0f0f0")   # el color gris #f0f0f0 se vuelve transparente

# ---------- AJUSTES (los puedes cambiar fácilmente) ----------
ZOOM = 2             # tamaño del Pokémon: 2 = el doble de grande
TIEMPO_SUENO = 30    # segundos sin tocarlo antes de que se duerma

# ---------- CARGAR EL GIF ----------
def cargar_frames(archivo):
    # Abre el GIF y devuelve dos listas de imágenes:
    # una normal y otra en espejo (para cuando camina hacia el otro lado)
    gif = Image.open(archivo)
    normales = []
    espejo = []
    for cuadro in ImageSequence.Iterator(gif):   # recorre cada cuadro del GIF
        im = cuadro.convert("RGBA")              # asegura que conserve la transparencia
        im = im.resize((im.width * ZOOM, im.height * ZOOM), Image.NEAREST)   # lo agranda sin difuminarlo
        normales.append(ImageTk.PhotoImage(im))                  # guarda la imagen normal
        espejo.append(ImageTk.PhotoImage(ImageOps.mirror(im)))   # guarda la imagen volteada
    return normales, espejo

frames_a, frames_b = cargar_frames("feraligatr.gif.gif")
frame_actual = 0     # número del cuadro de animación que se está mostrando

# ---------- ELEMENTOS QUE SE VEN EN LA VENTANA ----------
# El texto de las Zs (arriba del Pokémon) que aparece cuando duerme
label_zzz = tk.Label(root, text="", bg="#f0f0f0", fg="#3366cc",
                     font=("Arial", 14, "bold"))
label_zzz.pack()

# La imagen del Pokémon
label = tk.Label(root, image=frames_a[0], bg="#f0f0f0")
label.pack()

# ---------- DATOS DE PANTALLA Y POSICIÓN ----------
ancho_pantalla = root.winfo_screenwidth()   # ancho total de tu pantalla
ancho_pokemon = frames_a[0].width()         # ancho del Pokémon (para saber cuándo toca la pared)

x = 300               # posición horizontal inicial
y = 600               # posición vertical inicial
direccion = 1         # 1 = camina a la derecha, -1 = a la izquierda
saltando = False      # ¿está en medio de un salto?
dormido = False       # ¿está dormido?
contador_zzz = 0      # cuenta para animar las Zs
ultimo_toque = time.time()    # hora de la última vez que lo tocaste
root.geometry(f"+{x}+{y}")    # coloca la ventana en su posición inicial

# ---------- FUNCIÓN PRINCIPAL: CAMINAR ----------
# Se repite sola cada 100 milisegundos
def caminar():
    global x, direccion, frame_actual, dormido, contador_zzz

    # Si pasó mucho tiempo sin tocarlo, se duerme
    if not dormido and time.time() - ultimo_toque > TIEMPO_SUENO:
        dormido = True

    # --- Si está dormido ---
    if dormido:
        contador_zzz = contador_zzz + 1
        cantidad = (contador_zzz // 5) % 3 + 1     # cuenta 1, 2, 3 y vuelve a empezar
        label_zzz.config(text="Z" * cantidad)      # muestra "Z", "ZZ" o "ZZZ"
        # Se queda quieto mostrando el primer cuadro, mirando hacia donde iba
        if direccion == 1:
            label.config(image=frames_b[0])
        else:
            label.config(image=frames_a[0])
        root.after(100, caminar)   # vuelve a llamar a esta función en 100 ms
        return                     # sale de la función para no seguir caminando

    # --- Si está despierto ---
    # A veces (1 de cada 20 veces) cambia de dirección al azar
    if random.randint(1, 20) == 1:
        direccion = direccion * -1
    x = x + 5 * direccion      # se mueve 5 píxeles hacia donde mira

    # Paredes: si llega al borde de la pantalla, da la vuelta
    if x <= 0:
        x = 0
        direccion = 1
    if x >= ancho_pantalla - ancho_pokemon:
        x = ancho_pantalla - ancho_pokemon
        direccion = -1

    # Pasa al siguiente cuadro de la animación (y vuelve al primero al terminar)
    frame_actual = (frame_actual + 1) % len(frames_a)
    # Elige la imagen normal o la volteada según hacia dónde camina
    if direccion == 1:
        label.config(image=frames_b[frame_actual])
    else:
        label.config(image=frames_a[frame_actual])

    root.geometry(f"+{x}+{y}")   # mueve la ventana a la nueva posición
    root.after(100, caminar)     # repite esta función en 100 ms

# ---------- DESPERTAR ----------
def despertar():
    global dormido, ultimo_toque
    dormido = False
    ultimo_toque = time.time()     # reinicia el contador de tiempo
    label_zzz.config(text="")      # borra las Zs

# ---------- SALTO ----------
def saltar(event):
    global y, saltando
    despertar()          # tocarlo lo despierta
    if saltando:
        return           # si ya está saltando, no hace nada
    saltando = True
    y = y - 60           # sube 60 píxeles
    root.after(300, aterrizar)   # en 0.3 segundos llama a aterrizar

def aterrizar():
    global y, saltando
    y = y + 60           # baja de nuevo
    saltando = False

# ---------- CONTROLES DEL MOUSE ----------
label.bind("<Button-1>", saltar)                    # clic izquierdo: salta
label.bind("<Button-3>", lambda e: root.destroy())  # clic derecho: cierra el programa

# ---------- ARRANQUE ----------
caminar()          # inicia el movimiento
root.mainloop()    # mantiene la ventana abierta y atenta a tus clics