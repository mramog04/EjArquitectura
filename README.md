# EjArquitectura

Ejercicios de ROS 2 (Humble) con `turtlesim`. Cada carpeta tiene su propio README con la explicación y cómo ejecutarlo.

| Ejercicio | Descripción |
|---|---|
| [ejercicio1_mover_tortuga](ejercicio1_mover_tortuga/) | Mover la tortuga sin chocar con las paredes: si se acerca al borde gira, si no avanza |
| [ejercicio2_zona_tortuga](ejercicio2_zona_tortuga/) | Escribir por terminal en qué zona de la ventana (3x3) está la tortuga cuando cambia de zona |
| [ejercicio3_color_por_zona](ejercicio3_color_por_zona/) | Cambiar el color del rastro al cambiar de zona, usando el servicio `/turtle1/set_pen` |
| [ejercicio4_dos_tortugas_circulo](ejercicio4_dos_tortugas_circulo/) | Añadir una segunda tortuga (servicio `/spawn`), cada una con un color de lápiz, y que las dos dibujen un círculo a la vez |

## Ejecución rápida (ejercicio 3 completo)

Hacen falta tres terminales:

```bash
# Terminal 1: la ventana de la tortuga, que recibe lo que publican nuestros nodos
ros2 run turtlesim turtlesim_node

# Terminal 2: el nodo que publica los movimientos de la tortuga
python3 ejercicio1_mover_tortuga/mover_tortuga.py

# Terminal 3: el nodo que escucha la posición, calcula la zona y cambia el color del lápiz
python3 ejercicio3_color_por_zona/zona_color_tortuga.py
```
