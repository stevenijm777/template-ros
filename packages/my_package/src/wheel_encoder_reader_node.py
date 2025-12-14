#!/usr/bin/env python3
import os
import rospy
from duckietown.dtros import DTROS, NodeType
from duckietown_msgs.msg import WheelEncoderStamped

class WheelEncoderReaderNode(DTROS):

   def __init__(self, node_name):
       # Inicializar la clase padre DTROS como tipo PERCEPCIÓN
       super(WheelEncoderReaderNode, self).__init__(
           node_name=node_name,
           node_type=NodeType.PERCEPTION
       )
       
       # Obtener nombre del vehículo
       self._vehicle_name = os.environ['VEHICLE_NAME']
       
       # Definir los tópicos específicos para cada rueda
       self._left_encoder_topic = f"/{self._vehicle_name}/left_wheel_encoder_node/tick"
       self._right_encoder_topic = f"/{self._vehicle_name}/right_wheel_encoder_node/tick"
       
       # Variables para almacenar los últimos valores leídos
       self._ticks_left = None
       self._ticks_right = None
       
       # Crear suscriptores (uno para cada rueda)
       self.sub_left = rospy.Subscriber(
           self._left_encoder_topic,
           WheelEncoderStamped,
           self.callback_left
       )
       self.sub_right = rospy.Subscriber(
           self._right_encoder_topic,
           WheelEncoderStamped,
           self.callback_right
       )

   def callback_left(self, data):
       # Imprimir información estática solo una vez (log_once)
       rospy.loginfo_once(f"Left encoder resolution: {data.resolution}")
       rospy.loginfo_once(f"Left encoder type: {data.type}")
       # Actualizar variable con los ticks actuales
       self._ticks_left = data.data

   def callback_right(self, data):
       rospy.loginfo_once(f"Right encoder resolution: {data.resolution}")
       rospy.loginfo_once(f"Right encoder type: {data.type}")
       self._ticks_right = data.data

   def run(self):
       # Definir frecuencia de actualización del log (20 Hz)
       rate = rospy.Rate(20)
       
       while not rospy.is_shutdown():
           # Solo imprimir si hemos recibido datos de ambas ruedas
           if self._ticks_left is not None and self._ticks_right is not None:
               msg = (
                   f"Wheel encoder ticks [LEFT, RIGHT]: "
                   f"{self._ticks_left}, {self._ticks_right}"
               )
               rospy.loginfo(msg)
           rate.sleep()

if __name__ == '__main__':
   node = WheelEncoderReaderNode(node_name='wheel_encoder_reader_node')
   node.run()
   rospy.spin()