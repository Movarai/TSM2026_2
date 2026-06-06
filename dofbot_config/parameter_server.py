#!/usr/bin/env python3
"""
 DOFBOT Parameter Server

Servidor centralizado de parámetros para el robot DOFBot.
Proporciona:
  - Declaración y gestión de parámetros dinámicos
  - Validación robusta de valores
  - Callbacks para cambios en tiempo real
  - Validación de direcciones IP con regex

Este nodo actúa como autoridad central para la configuración del robot,
evitando inconsistencias y errores por parámetros inválidos.
"""

import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rcl_interfaces.msg import ParameterDescriptor, SetParametersResult

import re

# Expresión regular para validar IPv4
# Valida rangos 0-255 en cada octeto
IPV4_REGEX = r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"


class DofbotParamSrv(Node):
    """
    Servidor de parámetros para DOFBot.
    
    Declara, valida y gestiona parámetros críticos del robot:
    - Nombres de juntas
    - Configuración de red (IP del robot)
    - Velocidades de movimiento
    - Períodos de muestreo
    """
    
    def __init__(self, node_name):
        super().__init__(node_name)
        
        # Declarar parámetro individual con descriptor
        # El descriptor proporciona información adicional sobre el parámetro
        self.declare_parameter(
            name='time_period',
            value=0.01,   # Valor por defecto (segundos)
            descriptor=ParameterDescriptor(
                description="Período de muestreo de telemetría en segundos."
            )
        )

        # Declarar múltiples parámetros de una vez
        # Esta es la forma eficiente de declarar varios parámetros juntos
        self.declare_parameters(
            namespace="",
            parameters=[
                ('vel_lin', 0.0),                                    # Velocidad lineal (m/s)
                ('vel_ang', 0.0),                                    # Velocidad angular (rad/s)
                ('joint_names', rclpy.Parameter.Type.STRING_ARRAY),  # Nombres de juntas
                ('robot_ip', rclpy.Parameter.Type.STRING),           # IP del robot
                ('robot_name', rclpy.Parameter.Type.STRING)          # Nombre identificador
            ]
        )

        # Leer parámetro después de declararlo
        # Se utiliza get_parameter() para obtener valores en el código
        self.__time_period = self.get_parameter("time_period").get_parameter_value().double_value

        # Registrar callback para validar cambios de parámetros
        # Esta función se ejecuta ANTES de que el parámetro se actualice
        # Si retorna False, el cambio es rechazado
        self.add_on_set_parameters_callback(self._on_parameter_change)

        self.get_logger().info(f"{node_name} inicializado correctamente.")

    def _on_parameter_change(self, params: list[Parameter]):
        """
        Callback que se ejecuta cuando un parámetro intenta cambiar.
        
        Valida cada parámetro ANTES de permitir el cambio.
        Si alguno no pasa la validación, se rechaza TODO el cambio.
        
        Args:
            params: Lista de parámetros que intentan cambiar
            
        Returns:
            SetParametersResult: Indicador de éxito/fracaso de la validación
        """
        success = True
        
        # Validar cada parámetro
        for param in params:
            # Validación: time_period debe ser >= 0
            if param.name == 'time_period':
                if param.value < 0.0:
                    self.get_logger().warning(
                        f"Parámetro '{param.name}' debe ser mayor o igual a cero. "
                        f"Valor rechazado: {param.value}"
                    )
                    success = False
            
            # Validación: robot_ip debe ser una IPv4 válida
            if param.name == 'robot_ip':
                success = self._validate_ip(param.value)
                if not success:
                    self.get_logger().warning(
                        f"Parámetro '{param.name}' no es una IP válida. "
                        f"Valor rechazado: {param.value}"
                    )

        # Crear mensaje de resultado
        result_msg = SetParametersResult()
        result_msg.successful = success
        result_msg.reason = "Error en la validación de parámetros." if not success else ""

        return result_msg
    
    def _validate_ip(self, ip: str) -> bool:
        """
        Valida que una cadena sea una dirección IPv4 válida.
        
        Utiliza regex para verificar:
        - Formato correcto (A.B.C.D)
        - Cada octeto en rango 0-255
        
        Args:
            ip: Cadena a validar
            
        Returns:
            bool: True si es IP válida, False en caso contrario
            
        Ejemplos:
            _validate_ip("192.168.200.128") -> True
            _validate_ip("999.999.999.999") -> False
            _validate_ip("192.168.1") -> False
        """
        return bool(re.match(IPV4_REGEX, ip))


def init_srv(args=None):
    """
    Función principal que inicia el servidor de parámetros.
    
    Pasos:
    1. Inicializa ROS2
    2. Crea instancia del servidor
    3. Mantiene el nodo activo (spin)
    4. Maneja señales de interrupción (Ctrl+C)
    5. Limpia recursos al salir
    """
    rclpy.init(args=args)
    
    # Crear instancia del servidor
    param_srv = DofbotParamSrv("dofbot_config")
    
    try:
        # Mantener el nodo activo procesando callbacks
        rclpy.spin(param_srv)
    except KeyboardInterrupt:
        # Manejo de Ctrl+C
        param_srv.get_logger().info('Keyboard Interrupt (SIGINT) recibido. Apagando...')
    finally:
        # Limpiar recursos
        rclpy.shutdown()


if __name__ == "__main__":
    init_srv()
