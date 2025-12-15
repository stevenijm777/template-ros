#!/usr/bin/env python3
import os
import rospy
from duckietown.dtros import DTROS, NodeType
from duckietown_msgs.msg import WheelsCmdStamped

# Configuraciones de aceleracion y direccion 
THROTTLE_LEFT = 0.5 # 50% de potencia
DIRECTION_LEFT = 1 # 1 = adelante
THROTTLE_RIGHT = 0.3 # 30% de potencia
DIRECTION_RIGHT = -1 # -1 = reversa

class WheelControlNode(DTROS):
    def __init__(self, node_name):
        super(WheelControlNode, self).__init__(
            node_name=node_name,
            node_type=NodeType.GENERIC
        )
        # Obtener nombre del vehículo
        vehicle_name = os.environ['VEHICLE_NAME']
        wheels_topic = f"/{vehicle_name}/wheels_driver_node/wheels_cmd"

        # Calcula la velocidad final 
        self._vel_left = THROTTLE_LEFT * DIRECTION_LEFT
        self._vel_right = THROTTLE_RIGHT * DIRECTION_RIGHT

        # Inicializa el Publisher
        self._publisher = rospy.Publisher(
            wheels_topic,
            WheelsCmdStamped,
            queue_size=1
        )
    def run(self):
        # Publicar a 10 Hz
        rate = rospy.Rate(10)
        message = WheelsCmdStamped(vel_left=self._vel_left, vel_right=self._vel_right)

        while not rospy.is_shutdown():
            self._publisher.publish(message)
            rate.sleep()

    def on_shutdown(self):
        # Detener las ruedas al apagar el nodo
        stop = WheelsCmdStamped(vel_left=0.0, vel_right=0.0)
        self._publisher.publish(stop)

if __name__ == '__main__':
    # Inicializar el nodo
    node = WheelControlNode(node_name='wheel_control_node')
    # Ejecutar el nodo
    node.run()
    rospy.spin()