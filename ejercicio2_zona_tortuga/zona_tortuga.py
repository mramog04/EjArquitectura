#!/usr/bin/env python3
"""
Nodo ROS 2 que indica en qué zona de la ventana está la tortuga.

La ventana se divide en una cuadrícula de 3x3:

    arriba-izquierda | arriba-centro | arriba-derecha
    medio-izquierda  | medio-centro  | medio-derecha
    abajo-izquierda  | abajo-centro  | abajo-derecha

Solo escribe por terminal cuando la tortuga cambia de zona.

Uso:
    ros2 run turtlesim turtlesim_node      # en una terminal
    python3 zona_tortuga.py                # en otra terminal
"""
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

# El mundo de turtlesim va aprox. de 0 a 11.08 en X e Y
TAM_MUNDO = 11.08
TERCIO = TAM_MUNDO / 3


class ZonaTortuga(Node):
    def __init__(self):
        super().__init__('zona_tortuga')
        self.zona_actual = None
        self.sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.get_logger().info('Nodo zona_tortuga iniciado')

    def calcular_zona(self, x: float, y: float) -> str:
        # Horizontal: X crece hacia la derecha
        if x < TERCIO:
            columna = 'izquierda'
        elif x < 2 * TERCIO:
            columna = 'centro'
        else:
            columna = 'derecha'

        # Vertical: en turtlesim Y crece hacia ARRIBA
        if y > 2 * TERCIO:
            fila = 'arriba'
        elif y > TERCIO:
            fila = 'medio'
        else:
            fila = 'abajo'

        return f'{fila}-{columna}'

    def pose_callback(self, msg: Pose):
        zona = self.calcular_zona(msg.x, msg.y)
        if zona != self.zona_actual:
            self.zona_actual = zona
            self.get_logger().info(f'La tortuga está en: {zona}')


def main(args=None):
    rclpy.init(args=args)
    nodo = ZonaTortuga()
    try:
        rclpy.spin(nodo)
    except KeyboardInterrupt:
        pass
    finally:
        nodo.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
