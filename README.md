# EjArquitectura

Para ejecuttarlo hay que abrir tres terminales,
en una ejecutar la movida de la tortuga, que es lo que recibe lo que publican nuestros nodos para mover la tortuga comando: ros2 run turtlesim turtlesim_node

En otra ejecutamos el nodo que publica los movimientos de la pinche tortuga: python3 mover_tortuga.py

y en otra el nodo que va escuchado lo que publica donde se mueve la tortuga para calcular donde vergas esta y utiliza un servicio de la primera pantalla para cambiar el color del lapiz: python zona_tortuga.py
