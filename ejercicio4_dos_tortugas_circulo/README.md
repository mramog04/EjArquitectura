# Ejercicio 4 — Dos tortugas dibujando un círculo a la vez

Nodo que añade una segunda tortuga y hace que las dos dibujen un círculo al mismo tiempo,
cada una con un color de lápiz distinto.

## Funcionamiento

1. **Crear la segunda tortuga** con el servicio `/spawn` (`turtlesim/srv/Spawn`), que ofrece `turtlesim_node`:
   ```
   float32 x
   float32 y
   float32 theta
   string name
   ---
   string name
   ```
   `turtle2` aparece en el mismo punto que `turtle1`, el centro de la ventana. Si ya existe
   (por haber ejecutado el nodo antes con la misma ventana abierta), no se vuelve a crear.

2. **Cambiar el color del lápiz** de cada tortuga con su servicio `/turtleX/set_pen`
   (igual que en el ejercicio 3):
   - `turtle1` → rojo
   - `turtle2` → verde

3. **Dibujar el círculo**: a 10 Hz se publica en `/turtle1/cmd_vel` y `/turtle2/cmd_vel`
   un `Twist` con velocidad lineal y angular **constantes**. Una tortuga que avanza y gira a la vez
   a velocidad constante describe un círculo de radio:

   ```
   radio = VEL_LINEAL / VEL_ANGULAR = 2.0 / 1.0 = 2
   ```

   `turtle1` gira a la izquierda (`angular.z > 0`) y `turtle2` a la derecha (`angular.z < 0`).
   Como salen del mismo punto, una dibuja su círculo por arriba y la otra por abajo, y juntas forman un **8**.

```
                   ┌──/spawn, /turtle1/set_pen, /turtle2/set_pen (servicios)──┐
dos_tortugas_circulo                                                          ▼
                   ├──/turtle1/cmd_vel──▶ turtlesim_node
                   └──/turtle2/cmd_vel──▶ turtlesim_node
```

## Requisitos

- ROS 2 Humble con el paquete `turtlesim`.
- Tener ROS cargado en la terminal (`source /opt/ros/humble/setup.bash`).

## Ejecución

En dos terminales:

```bash
# Terminal 1: ventana de la tortuga
ros2 run turtlesim turtlesim_node

# Terminal 2: crea turtle2 y pone a las dos a dibujar
python3 dos_tortugas_circulo.py
```

Para parar, pulsa `Ctrl+C`. Las dos tortugas se detienen al cerrar el nodo.

## Salida de ejemplo

```
[INFO] [dos_tortugas_circulo]: Tortuga creada: turtle2
[INFO] [dos_tortugas_circulo]: Lápiz de turtle1 -> RGB(255, 0, 0)
[INFO] [dos_tortugas_circulo]: Lápiz de turtle2 -> RGB(0, 255, 0)
[INFO] [dos_tortugas_circulo]: Las dos tortugas están dibujando círculos
```

## Parámetros

En `dos_tortugas_circulo.py`:

| Constante      | Significado                                                  |
|----------------|--------------------------------------------------------------|
| `VEL_LINEAL`   | Velocidad de avance                                          |
| `VEL_ANGULAR`  | Velocidad de giro (el radio es `VEL_LINEAL / VEL_ANGULAR`)   |
| `GROSOR_LAPIZ` | Grosor del rastro                                            |
| `TORTUGAS`     | Color y sentido de giro de cada tortuga                      |
