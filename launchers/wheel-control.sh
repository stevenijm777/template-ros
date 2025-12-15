#!/bin/bash
source /environment.sh

# Inicializar el entorno de lanzamiento
dt-launchfile-init

# Ejecutar el script de Python 
rosrun my_package wheel_control_node.py

dt-launchfile-join
