#!/usr/bin/env python3
"""
Nodo ROS 2 que mueve la tortuga de turtlesim sin chocar con las paredes.

- Si la tortuga se acerca al borde -> gira sobre sí misma.
- Si no                             -> avanza en línea recta.

Uso:
    ros2 run turtlesim turtlesim_node      # en una terminal
    python3 mover_tortuga.py               # en otra terminal
"""
import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

# El mundo de turtlesim va aprox. de 0 a 11.08 en X e Y
LIMITE_MIN = 0.0
LIMITE_MAX = 11.08

MARGEN = 1.0        # distancia a la pared que consideramos "peligrosa"
DIST_PREVISION = 1.0  # cuánto "miramos hacia delante" en la dirección de avance

VEL_LINEAL = 5.0
VEL_ANGULAR = 5.0


class MoverTortuga(Node):
    def __init__(self):
        super().__init__('mover_tortuga')
        self.pose = None

        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)

        # Bucle de control a 10 Hz
        self.timer = self.create_timer(0.1, self.control)
        self.get_logger().info('Nodo mover_tortuga iniciado')

    def pose_callback(self, msg: Pose):
        self.pose = msg

    def cerca_del_borde(self) -> bool:
        """Mira un punto por delante de la tortuga; si cae cerca de la pared, hay peligro."""
        x_futuro = self.pose.x + DIST_PREVISION * math.cos(self.pose.theta)
        y_futuro = self.pose.y + DIST_PREVISION * math.sin(self.pose.theta)

        return (x_futuro < LIMITE_MIN + MARGEN or x_futuro > LIMITE_MAX - MARGEN or
                y_futuro < LIMITE_MIN + MARGEN or y_futuro > LIMITE_MAX - MARGEN)

    def control(self):
        if self.pose is None:
            return  # todavía no hemos recibido la posición

        cmd = Twist()
        if self.cerca_del_borde():
            # Cerca de la pared: girar sin avanzar
            cmd.linear.x = 0.0
            cmd.angular.z = VEL_ANGULAR
        else:
            # Camino libre: avanzar recto
            cmd.linear.x = VEL_LINEAL
            cmd.angular.z = 0.0

        self.pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    nodo = MoverTortuga()
    try:
        rclpy.spin(nodo)
    except KeyboardInterrupt:
        pass
    finally:
        # Parar la tortuga al salir
        nodo.pub.publish(Twist())
        nodo.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
