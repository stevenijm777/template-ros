#!/usr/bin/env python3
import os
import rospy
from duckietown.dtros import DTROS, NodeType
from sensor_msgs.msg import CompressedImage
import cv2
from cv_bridge import CvBridge

class CameraReaderNode(DTROS):
    def __init__(self, node_name):
        # Inicializar la clase padre
        super(CameraReaderNode,self).__init__(
            node_name=node_name,
            node_type=NodeType.VISUALIZATION
        )

        # 1. Obtener el nombre del vehiculo y construir el topico
        self._vehicle_name = os.environ['VEHICLE_NAME']
        self._camera_topic = f'/{self._vehicle_name}/camera_node/image/compressed'

        # 2. Herramientas de imagen
        self._bridge = CvBridge() # para converir de ROS a OpenCV
        self._window = "camera-reader"

        # 3. Configurar ventana y suscriptor
        cv2.namedWindow(self._window, cv2.WINDOW_AUTOSIZE)
        self.sub = rospy.Subscriber(self._camera_topic, CompressedImage, self.callback)

    def callback(self, msg):
        # convertir mensaje ROS comprimido a imagen OpenCV
        image = self._bridge.compressed_imgmsg_to_cv2(msg)

        # mostrar la imagen en la ventana
        cv2.imshow(self._window, image)
        cv2.waitKey(1)  # necesario para actualizar la ventana

if __name__ == '__main__':
    # Inicializar el nodo
    node = CameraReaderNode(node_name='camera_reader_node')
    # Mantener el nodo en ejecucion
    rospy.spin()