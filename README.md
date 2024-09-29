# ChinaTown Tracking 

Este proyecto es un **sistema de seguimiento de pedidos** basado en la creación de **contenedores** a los que se les pueden asignar **paquetes**. A cada paquete se le pueden agregar **estados**, que se notificarán al destinatario a través de **WhatsApp utilizando Twilio**. Además, el sistema proporciona una interfaz donde los usuarios pueden ingresar su **tracking ID** para ver los estados del paquete en tiempo real.

## Funcionalidades principales

- **Gestión de contenedores y paquetes**: Los usuarios pueden crear contenedores y asignar paquetes a ellos.
- **Actualización de estados de paquetes**: Los paquetes pueden tener varios estados, como "En tránsito", "Entregado", etc.
- **Notificaciones por WhatsApp**: Utilizando la API de Twilio, los estados de los paquetes se envían automáticamente al destinatario a través de WhatsApp.
- **Interfaz de seguimiento**: Los usuarios pueden ingresar su número de tracking en una interfaz web para consultar los estados del paquete.
- **Multilinguaje**: El sistema soporta múltiples idiomas, incluyendo español y chino.
- **Base de datos MySQL**: El sistema utiliza MySQL para almacenar la información de los pedidos, contenedores y paquetes.
 
## Archivos importantes

- `run_servers.sh`: El script que automatiza la creación del entorno virtual, instalación de dependencias, compilación de traducciones y ejecución de los servidores.
- `requirements.txt`: El archivo que contiene las dependencias necesarias para este proyecto.
- `manage.py`: El archivo de Django que gestiona el servidor UI.
- `main.py`: El archivo principal de FastAPI que contiene la aplicación API.

## Configuración

### Crear .env

```bash
API_SERVER=
API_PORT=
UI_SERVER=
UI_PORT=
PROTOCOL=
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
DATABASE_SERVER=
DATABASE_PORT=3306
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
```

## Correr servidor

```bash
./run.sh <UI_PORT> <API_PORT>
