# Ejercicio 1 — Mover la tortuga sin chocar con las paredes

Nodo que mueve la tortuga de `turtlesim`: si se acerca al borde gira, y si no, avanza.

## Funcionamiento

- Se suscribe a `/turtle1/pose` (`turtlesim/msg/Pose`) para conocer la posición y orientación.
- Publica en `/turtle1/cmd_vel` (`geometry_msgs/msg/Twist`) a 10 Hz.
- Calcula un punto `DIST_PREVISION` unidades por delante de la tortuga. Si ese punto cae a menos
  de `MARGEN` de alguna pared (el mundo va de 0 a ~11.08), **gira sin avanzar**. Si no, **avanza recto**.
- Al mirar hacia delante, en cuanto la tortuga apunta hacia dentro vuelve a avanzar,
  así que no se queda atascada girando junto a la pared.

```
turtlesim_node ──/turtle1/pose──▶ mover_tortuga ──/turtle1/cmd_vel──▶ turtlesim_node
```

## Requisitos

- ROS 2 Humble con el paquete `turtlesim`.
- Tener ROS cargado en la terminal (`source /opt/ros/humble/setup.bash`).

## Ejecución

En dos terminales distintas:

```bash
# Terminal 1: ventana de la tortuga
ros2 run turtlesim turtlesim_node

# Terminal 2: nodo que la mueve
python3 mover_tortuga.py
```

Para parar, pulsa `Ctrl+C` en cada terminal. Al cerrar el nodo, la tortuga se detiene.

## Parámetros

Se cambian en las constantes del principio de `mover_tortuga.py`:

| Constante        | Significado                                       |
|------------------|---------------------------------------------------|
| `MARGEN`         | Distancia a la pared que se considera peligrosa   |
| `DIST_PREVISION` | Cuánto mira hacia delante la tortuga              |
| `VEL_LINEAL`     | Velocidad de avance                               |
| `VEL_ANGULAR`    | Velocidad de giro                                 |

## Comprobación

```bash
rqt_graph                                                       # grafo de nodos y topics
ros2 run rqt_plot rqt_plot /turtle1/pose/x /turtle1/pose/y      # x e y nunca llegan a 0 ni a 11
```
