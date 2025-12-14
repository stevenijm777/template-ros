#!/usr/bin/env python3
# ^ SHEBANG: Indica al sistema operativo que este archivo debe ejecutarse usando el intérprete de Python 3.

# IMPORTACIONES DE LIBRERÍAS
import os  # Para acceder a variables de entorno del sistema (como el nombre del robot).
import rospy  # La librería principal de ROS para Python. Permite crear nodos, publicar, suscribirse, etc.
from std_msgs.msg import String  # Importamos el tipo de mensaje 'String' (texto) estándar de ROS.
# Importamos la clase base DTROS de Duckietown. 
# Duckietown recomienda heredar de DTROS en lugar de usar rospy directamente para tener mejor integración con su sistema (logs, diagnósticos, apagado limpio).
from duckietown.dtros import DTROS, NodeType

# DEFINICIÓN DE LA CLASE DEL NODO
# Creamos una clase que hereda de DTROS. Esto convierte nuestra clase en un "Nodo de Duckietown".
class MyPublisherNode(DTROS):
    
    def __init__(self, node_name):
        """
        Constructor de la clase: Se ejecuta una sola vez al iniciar el nodo.
        Aquí configuramos los recursos (publicadores, suscriptores, parámetros).
        """
        
        # 1. INICIALIZAR EL NODO PADRE (DTROS)
        # Es obligatorio llamar al __init__ de la clase padre.
        # node_name: El nombre que tendrá el nodo en la red ROS.
        # node_type: Clasificación del nodo (GENERIC, DRIVER, PERCEPTION, etc.) útil para diagnósticos.
        super(MyPublisherNode, self).__init__(node_name=node_name, node_type=NodeType.GENERIC)

        # 2. OBTENER EL NOMBRE DEL ROBOT
        # Leemos la variable de entorno 'VEHICLE_NAME' que Docker inyecta automáticamente.
        # Esto es vital para que el robot sepa quién es (ej. 'duckiebot01').
        self._vehicle_name = os.environ['VEHICLE_NAME']

        # 3. CREAR EL PUBLICADOR (Publisher)
        # self.publisher: Objeto que nos permitirá enviar mensajes.
        # 'chatter': Nombre del TÓPICO (el canal) donde publicaremos. Cualquiera que se suscriba a 'chatter' escuchará esto.
        # String: El TIPO de dato que vamos a enviar. Debe coincidir con el import de std_msgs.
        # queue_size=10: Si publicamos muy rápido y nadie escucha, guarda hasta 10 mensajes en cola antes de borrar los viejos.
        self.publisher = rospy.Publisher('chatter', String, queue_size=10)


    def run(self):
        """
        Función principal donde ocurre la lógica repetitiva del nodo.
        """
        
        # 4. CONFIGURAR LA FRECUENCIA
        # rospy.Rate(1) define que el bucle intentará ejecutarse 1 vez por segundo (1 Hz).
        # Controla la velocidad del bucle while.
        rate = rospy.Rate(1) 
        
        # Preparamos el mensaje de texto una sola vez (f-string para insertar el nombre).
        message = f"Hello from {self._vehicle_name}!"

        # 5. BUCLE PRINCIPAL (While Loop)
        # rospy.is_shutdown(): Verifica si alguien (el usuario con Ctrl+C o el sistema) pidió apagar el nodo.
        # Mientras el nodo esté vivo, seguimos en el bucle.
        while not rospy.is_shutdown():
            
            # A. LOGGING (Registro)
            # Imprime el mensaje en la terminal y lo manda al sistema de logs de ROS (/rosout).
            # Es mejor que usar 'print' porque incluye fecha, hora y nivel de severidad.
            rospy.loginfo(f"Publishing message: {message}")
            
            # B. PUBLICAR
            # Envía el mensaje al tópico 'chatter' a través de la red.
            self.publisher.publish(message)
            
            # C. DORMIR (Sleep)
            # Pausa la ejecución el tiempo necesario para mantener la frecuencia de 1 Hz.
            # Si el bucle fue muy rápido, duerme más. Si fue lento, duerme menos o nada.
            rate.sleep()

# BLOQUE DE EJECUCIÓN PRINCIPAL
# Esto asegura que el código solo corra si ejecutamos este archivo directamente (no si lo importamos como librería).
if __name__ == '__main__':
    # 6. INSTANCIAR Y CORRER
    # Creamos el objeto de nuestra clase, asignándole el nombre 'my_publisher_node'.
    node = MyPublisherNode(node_name='my_publisher_node')
    
    # Llamamos a nuestra función personalizada run() para empezar a publicar.
    node.run()
    
    # 7. SPIN (Mantener vivo)
    # rospy.spin() evita que el programa termine inmediatamente.
    # Mantiene el nodo escuchando callbacks (aunque en este ejemplo simple no usamos suscriptores, es buena práctica dejarlo).
    rospy.spin()