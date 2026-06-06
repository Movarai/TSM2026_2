# dofbot_config

## Descripción General

`dofbot_config` es un paquete ROS2 especializado en la **gestión centralizada de parámetros y configuración del robot DOFBot**. Este paquete actúa como un servidor de parámetros dinámicos que permite definir, validar y actualizar configuraciones críticas del robot en tiempo de ejecución sin necesidad de reiniciar el sistema.

El DOFBot es un manipulador robótico de 6 grados de libertad (6 DOF) con gripper, diseñado para tareas de manipulación y automatización. Este paquete coordina todos los parámetros necesarios para su operación.

---

## Estructura del Paquete

```
dofbot_config/
├── README.md                    # Documentación del paquete
├── package.xml                  # Metadatos ROS2
├── setup.py                     # Configuración de instalación
├── setup.cfg                    # Configuración adicional
├── LICENSE                      # Licencia MIT
│
├── dofbot_config/
│   ├── __init__.py             # Inicialización del módulo
│   └── parameter_server.py     # Servidor de parámetros con validación
│
├── config/
│   └── dofbot_params.yaml      # Parámetros por defecto del robot
│
├── launch/
│   └── param_srv.launch.py     # Launch file para iniciar el servidor
│
├── resource/
│   └── dofbot_config           # Recurso del paquete
│
└── test/
    ├── test_copyright.py       # Tests de derechos de autor
    ├── test_flake8.py          # Tests de estilo PEP8
    └── test_pep257.py          # Tests de docstrings
```

---

## Archivos Principales

### 1. **config/dofbot_params.yaml** - Configuración Central

Archivo YAML que contiene todos los parámetros por defecto del DOFBot:

- **joint_names**: Lista de las 7 juntas (6 articulaciones + gripper)
- **robot_ip**: Dirección IP para comunicación con el robot real
- **robot_name**: Identificador (VIRTUAL o nombre real del robot)
- **vel_lin**: Velocidad lineal de movimiento (m/s)
- **vel_ang**: Velocidad angular de movimiento (rad/s)

**Importancia:** Define la configuración central del robot de forma legible y fácil de modificar.

---

### 2. **dofbot_config/parameter_server.py** - Servidor de Parámetros

Nodo ROS2 que implementa:

- Declaración de parámetros con descriptores
- Validación dinámica de parámetros
- Callbacks para cambios en tiempo real
- Validación robusta de IPs con regex

**Importancia:** Evita errores por parámetros inválidos y permite reconfiguraciones sin reiniciar.

---

### 3. **launch/param_srv.launch.py** - Orquestador

Launch file que inicializa el servidor con la configuración por defecto desde YAML.

---

## Cómo Usar

### Instalación

```bash
cd ~/ROS2Dev/ws_scara
colcon build --packages-select dofbot_config
source install/setup.bash
```

### Ejecutar

```bash
# Con launch file (RECOMENDADO)
ros2 launch dofbot_config param_srv.launch.py

# O directamente
ros2 run dofbot_config param_srv
```

### Consultar Parámetros

```bash
# Ver parámetro
ros2 param get /dofbot_config robot_ip

# Cambiar parámetro (con validación)
ros2 param set /dofbot_config vel_lin 0.05
```

---

## Validaciones

- `time_period`: Debe ser ≥ 0.0
- `robot_ip`: IPv4 válida (ej: 192.168.200.128)
- `vel_lin`, `vel_ang`: Valores numéricos

---

## Referencias

- [ROS2 Parameters](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-ROS2-System.html)

---

**Licencia:** MIT | **Mantenedor:** Felipe Rivas (rivascf@gmail.com)
