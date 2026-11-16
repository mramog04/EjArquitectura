# Ejercicio 2 — Zona en la que está la tortuga

Nodo que escribe por terminal en qué zona de la ventana está la tortuga, **solo cuando cambia de zona**.

## Funcionamiento

La ventana (de 0 a ~11.08 en X e Y) se divide en una cuadrícula de 3x3:

```
arriba-izquierda | arriba-centro | arriba-derecha
medio-izquierda  | medio-centro  | medio-derecha
abajo-izquierda  | abajo-centro  | abajo-derecha
```

- Se suscribe a `/turtle1/pose` (`turtlesim/msg/Pose`).
- Calcula la zona con la posición `x, y`. En turtlesim la **Y crece hacia arriba**.
- Guarda la última zona y solo escribe cuando la nueva es distinta.

```
turtlesim_node ──/turtle1/pose──▶ zona_tortuga ──▶ terminal
```

## Requisitos

- ROS 2 Humble con el paquete `turtlesim`.
- Tener ROS cargado en la terminal (`source /opt/ros/humble/setup.bash`).

## Ejecución

Este nodo no mueve la tortuga, solo la observa. Para que se mueva, usa el nodo del
ejercicio 1 o el teclado. En tres terminales:

```bash
# Terminal 1: ventana de la tortuga
ros2 run turtlesim turtlesim_node

# Terminal 2: mover la tortuga (elige una opción)
python3 ../ejercicio1_mover_tortuga/mover_tortuga.py   # automático
ros2 run turtlesim turtle_teleop_key                   # con las flechas del teclado

# Terminal 3: nodo de zonas
python3 zona_tortuga.py
```

## Salida de ejemplo

```
[INFO] [zona_tortuga]: La tortuga está en: medio-centro
[INFO] [zona_tortuga]: La tortuga está en: medio-derecha
[INFO] [zona_tortuga]: La tortuga está en: arriba-derecha
[INFO] [zona_tortuga]: La tortuga está en: arriba-centro
```
