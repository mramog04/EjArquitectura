#!/usr/bin/env python3
"""
Nodo ROS 2 que indica en qué zona de la ventana está la tortuga.

La ventana se divide en una cuadrícula de 3x3:

    arriba-izquierda | arriba-centro | arriba-derecha
    medio-izquierda  | medio-centro  | medio-derecha
    abajo-izquierda  | abajo-centro  | abajo-derecha

Cuando la tortuga cambia de zona:
  - lo escribe por terminal
  - cambia el color del rastro llamando al servicio /turtle1/set_pen

Uso:
    ros2 run turtlesim turtlesim_node      # en una terminal
    python3 zona_color_tortuga.py          # en otra terminal
"""
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from turtlesim.srv import SetPen

# El mundo de turtlesim va aprox. de 0 a 11.08 en X e Y
TAM_MUNDO = 11.08
TERCIO = TAM_MUNDO / 3

GROSOR_LAPIZ = 3

# Color (r, g, b) del rastro para cada zona
COLORES = {
    'arriba-izquierda': (255, 0, 0),      # rojo
    'arriba-centro':    (255, 128, 0),    # naranja
    'arriba-derecha':   (255, 255, 0),    # amarillo
    'medio-izquierda':  (0, 255, 0),      # verde
    'medio-centro':     (255, 255, 255),  # blanco
    'medio-derecha':    (0, 255, 255),    # cian
    'abajo-izquierda':  (0, 0, 255),      # azul
    'abajo-centro':     (128, 0, 255),    # morado
    'abajo-derecha':    (255, 0, 255),    # rosa
}


class ZonaTortuga(Node):
    def __init__(self):
        super().__init__('zona_tortuga')
        self.zona_actual = None

        # Cliente del servicio del lápiz (lo ofrece turtlesim_node)
        self.cliente_lapiz = self.create_client(SetPen, '/turtle1/set_pen')
        while not self.cliente_lapiz.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Esperando al servicio /turtle1/set_pen...')

        self.sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.get_logger().info('Nodo zona_tortuga iniciado')

    def cambiar_color(self, zona: str):
        r, g, b = COLORES[zona]
        peticion = SetPen.Request()
        peticion.r = r
        peticion.g = g
        peticion.b = b
        peticion.width = GROSOR_LAPIZ
        peticion.off = 0
        # Llamada asíncrona: no bloquea el nodo esperando la respuesta
        self.cliente_lapiz.call_async(peticion)

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
            self.cambiar_color(zona)


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
