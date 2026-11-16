#!/usr/bin/env python3
"""
Nodo ROS 2 que añade una segunda tortuga y hace que las dos dibujen un círculo a la vez,
cada una con un color de lápiz distinto.

Pasos:
  1. Crea la tortuga 'turtle2' con el servicio /spawn (en la misma posición que turtle1).
  2. Cambia el color del lápiz de cada tortuga con /turtleX/set_pen.
  3. Publica en /turtle1/cmd_vel y /turtle2/cmd_vel una velocidad lineal y angular constantes,
     que hacen que cada tortuga describa un círculo de radio = VEL_LINEAL / VEL_ANGULAR.
     turtle1 gira a la izquierda y turtle2 a la derecha, así que dibujan un "8".

Uso:
    ros2 run turtlesim turtlesim_node      # en una terminal
    python3 dos_tortugas_circulo.py        # en otra terminal
"""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn, SetPen

# turtle1 aparece siempre en el centro de la ventana mirando a la derecha
CENTRO = 5.544445

VEL_LINEAL = 2.0
VEL_ANGULAR = 1.0      # radio del círculo = 2.0 / 1.0 = 2 unidades
GROSOR_LAPIZ = 3

# Configuración de cada tortuga: nombre -> (color r, g, b), sentido de giro (1 izq., -1 der.)
TORTUGAS = {
    'turtle1': ((255, 0, 0), 1),    # rojo, gira a la izquierda
    'turtle2': ((0, 255, 0), -1),   # verde, gira a la derecha
}


class DosTortugasCirculo(Node):
    def __init__(self):
        super().__init__('dos_tortugas_circulo')

        self.crear_turtle2()
        for nombre, (color, _) in TORTUGAS.items():
            self.cambiar_color(nombre, color)

        # Un publicador de velocidad para cada tortuga
        self.pubs = {
            nombre: self.create_publisher(Twist, f'/{nombre}/cmd_vel', 10)
            for nombre in TORTUGAS
        }

        # Bucle de control a 10 Hz
        self.timer = self.create_timer(0.1, self.mover)
        self.get_logger().info('Las dos tortugas están dibujando círculos')

    def llamar_servicio(self, tipo, nombre_servicio, peticion):
        """Espera a que el servicio exista, lo llama y espera la respuesta."""
        cliente = self.create_client(tipo, nombre_servicio)
        while not cliente.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(f'Esperando al servicio {nombre_servicio}...')
        futuro = cliente.call_async(peticion)
        rclpy.spin_until_future_complete(self, futuro)
        return futuro.result()

    def crear_turtle2(self):
        # Si turtle2 ya existe (por haber ejecutado el nodo antes), no se vuelve a crear
        servicios = [nombre for nombre, _ in self.get_service_names_and_types()]
        if '/turtle2/set_pen' in servicios:
            self.get_logger().info('turtle2 ya existe, no se crea de nuevo')
            return

        peticion = Spawn.Request()
        peticion.x = CENTRO
        peticion.y = CENTRO
        peticion.theta = 0.0
        peticion.name = 'turtle2'
        respuesta = self.llamar_servicio(Spawn, '/spawn', peticion)
        self.get_logger().info(f'Tortuga creada: {respuesta.name}')

    def cambiar_color(self, nombre, color):
        peticion = SetPen.Request()
        peticion.r, peticion.g, peticion.b = color
        peticion.width = GROSOR_LAPIZ
        peticion.off = 0
        self.llamar_servicio(SetPen, f'/{nombre}/set_pen', peticion)
        self.get_logger().info(f'Lápiz de {nombre} -> RGB{color}')

    def mover(self):
        for nombre, (_, sentido) in TORTUGAS.items():
            cmd = Twist()
            cmd.linear.x = VEL_LINEAL
            cmd.angular.z = sentido * VEL_ANGULAR
            self.pubs[nombre].publish(cmd)

    def parar(self):
        for pub in self.pubs.values():
            pub.publish(Twist())


def main(args=None):
    rclpy.init(args=args)
    nodo = DosTortugasCirculo()
    try:
        rclpy.spin(nodo)
    except KeyboardInterrupt:
        pass
    finally:
        nodo.parar()
        nodo.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
