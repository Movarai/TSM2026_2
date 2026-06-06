# 🚀 DOFBOT Parameter Server Launch File
# =======================================
#
# Este launch file inicia el servidor centralizado de parámetros del DOFBot.
#
# Función:
#   1. Lee la configuración desde config/dofbot_params.yaml
#   2. Carga los parámetros en el ROS2 Parameter Server
#   3. Inicia el nodo del servidor de parámetros
#
# Uso:
#   $ ros2 launch dofbot_config param_srv.launch.py
#
# Parámetros cargados:
#   - joint_names: Nombres de las 7 articulaciones
#   - robot_ip: Dirección IP del robot
#   - robot_name: Identificador del robot
#   - vel_lin: Velocidad lineal máxima
#   - vel_ang: Velocidad angular máxima

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution


def generate_launch_description():
    """
    Genera la descripción del launch file.
    
    Returns:
        LaunchDescription: Descripción con nodos a ejecutar
    """
    
    # 📁 Obtener ruta del paquete
    pkg_share = get_package_share_directory('dofbot_config')
    
    # 📋 Ruta al archivo de configuración YAML
    config_file = PathJoinSubstitution([pkg_share, 'config', 'dofbot_params.yaml'])

    # 🤖 Nodo del servidor de parámetros
    # ===================================
    # Crea una instancia del servidor que:
    # - Lee los parámetros desde config_file (YAML)
    # - Los carga en el Parameter Server de ROS2
    # - Valida cambios en tiempo real
    # - Proporciona interface para otros nodos
    param_server_node = Node(
        package='dofbot_config',              # Nombre del paquete
        executable='param_srv',                # Comando a ejecutar (definido en setup.py)
        name='dofbot_config',                  # Nombre del nodo
        output='screen',                       # Mostrar logs en terminal
        parameters=[config_file],              # Cargar parámetros desde YAML
    )

    # 📦 Crear descripción del launch
    return LaunchDescription([
        param_server_node,
    ])
