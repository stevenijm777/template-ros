#!/usr/bin/env python3
# ^ SHEBANG: Indica al sistema operativo que este archivo debe ejecutarse usando el
import rospy  # La librería principal de ROS para Python. Permite crear nodos, publicar, suscribirse, etc.
from duckietown.dtros import DTROS, NodeType  # Importamos la clase base DTROS de Duckietown.
from std_msgs.msg import String  # Importamos el tipo de mensaje 'String' (texto

class MySubscriberNode(DTROS):

    def __init__(self, node_name):
        # 1. Inicializar la clase padre DTROS
        super(MySubscriberNode, self).__init__(
            node_name=node_name, 
            node_type=NodeType.GENERIC
        )
        
        # 2. CONSTRUIR EL SUSCRIPTOR
        # rospy.Subscriber(topico, tipo_mensaje, funcion_callback)
        # 'chatter': El nombre del tópico que vamos a escuchar (debe coincidir con el publicador).
        # String: El tipo de dato esperado.
        # self.callback: La función que se ejecutará CADA VEZ que llegue un mensaje nuevo.
        self.sub = rospy.Subscriber('chatter', String, self.callback)

    def callback(self, data):
        """
        Esta función se ejecuta automáticamente cuando llega un mensaje al tópico 'chatter'.
        'data' contiene el mensaje recibido.
        """
        # data.data accede al contenido del String
        rospy.loginfo("I heard '%s'", data.data)

if __name__ == '__main__':
    # Crear e inicializar el nodo
    node = MySubscriberNode(node_name='my_subscriber_node')

    # rospy.spin() mantiene el nodo vivo y escuchando mensajes
    rospy.spin()
    