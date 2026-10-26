# Mascota de escritorio en Python

Una mascota animada que camina por la parte de abajo de tu pantalla, salta cuando le haces clic y se duerme si no la tocas. Hecha con Python y tkinter como proyecto para aprender a programar.

## Qué hace

- Camina de lado a lado y cambia de dirección al azar
- Rebota en los bordes de la pantalla
- Salta con clic izquierdo
- Se duerme (aparecen Zs animadas) si pasan 30 segundos sin tocarla
- Se cierra con clic derecho
- Usa una ventana sin bordes y transparente que siempre queda encima

## Cómo usarlo

1. Instala [Python 3](https://www.python.org/downloads/).
2. Instala la librería Pillow abriendo una terminal y escribiendo:
   `pip install pillow`
3. Consigue un GIF animado de tu personaje favorito y guárdalo en la misma carpeta con el nombre que desees, o cambia el nombre en el código.
4. Ejecuta el programa:
   `python mascota.py`

## Qué aprendí

- Crear ventanas con tkinter
- Animar imágenes cuadro por cuadro con Pillow
- Usar funciones, variables globales y eventos del mouse
- Repetir acciones con `root.after()`

## Ideas para mejorar

- Que siga al mouse
- Sonidos o frases al hacer clic

## Nota

Proyecto personal sin fines de lucro. Los personajes pertenecen a sus respectivos dueños, por eso las imágenes no se incluyen.