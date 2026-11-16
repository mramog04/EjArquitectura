# Ejercicio 3 — Cambiar el color del rastro según la zona

Amplía el ejercicio 2: cuando la tortuga cambia de zona, además de escribirlo por terminal,
**cambia el color del rastro** que deja.

## Funcionamiento

El lápiz de la tortuga no se controla con un topic, sino con un **servicio** que ya ofrece
`turtlesim_node`: `/turtle1/set_pen`, de tipo `turtlesim/srv/SetPen`.

```
uint8 r        # rojo  (0-255)
uint8 g        # verde (0-255)
uint8 b        # azul  (0-255)
uint8 width    # grosor del rastro
uint8 off      # 1 = no pinta, 0 = pinta
---
               # respuesta vacía
```

El nodo `zona_color_tortuga`:

- Se suscribe a `/turtle1/pose` y calcula la zona (cuadrícula de 3x3, igual que en el ejercicio 2).
- Es **cliente** del servicio `/turtle1/set_pen`. Al arrancar espera a que el servicio esté disponible.
- Al cambiar de zona, llama al servicio con `call_async`, para no bloquear el nodo, usando el color de la zona:

| | izquierda | centro | derecha |
|---|---|---|---|
| **arriba** | rojo | naranja | amarillo |
| **medio** | verde | blanco | cian |
| **abajo** | azul | morado | rosa |

```
turtlesim_node ──/turtle1/pose──▶ zona_color_tortuga ──/turtle1/set_pen (servicio)──▶ turtlesim_node
```

## Requisitos

- ROS 2 Humble con el paquete `turtlesim`.
- Tener ROS cargado en la terminal (`source /opt/ros/humble/setup.bash`).

## Ejecución

En tres terminales:

```bash
# Terminal 1: ventana de la tortuga
ros2 run turtlesim turtlesim_node

# Terminal 2: mover la tortuga (elige una opción)
python3 ../ejercicio1_mover_tortuga/mover_tortuga.py   # automático
ros2 run turtlesim turtle_teleop_key                   # con las flechas del teclado

# Terminal 3: nodo de zonas con cambio de color
python3 zona_color_tortuga.py
```

## Probar el servicio a mano

Con la tortuga abierta, se puede cambiar el color del lápiz desde la terminal:

```bash
ros2 service call /turtle1/set_pen turtlesim/srv/SetPen "{r: 255, g: 0, b: 0, width: 3, off: 0}"
```

## Parámetros

En `zona_color_tortuga.py`:

- `COLORES`: diccionario zona → `(r, g, b)`.
- `GROSOR_LAPIZ`: grosor del rastro.
