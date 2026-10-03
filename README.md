# Proyecto MARQUEZA

Aplicacion de gestion con frontend multipagina en `frontend/` y API Flask en `backend/API/`.

## Ejecutar frontend y backend

1. Importa `database_marqueza.sql` en MariaDB 10.11 o posterior. El script elimina y vuelve a crear las tablas de la aplicacion, asi que no lo ejecutes sobre datos que quieras conservar. Revisa las credenciales en `backend/API/.env` y confirma que MariaDB este iniciado.
2. En PowerShell, instala y ejecuta el backend:

	```powershell
	cd backend/API
	py -m venv .venv
	.\.venv\Scripts\Activate.ps1
	pip install -r requirements.txt
	py app.py
	```

3. Sirve la carpeta raiz del proyecto con Live Server y abre `http://localhost:5500/`. La entrada siempre dirige al inicio de sesión. La API Flask escucha por defecto en `http://localhost:5000/api`; no abras las paginas con `file://`.
4. Comprueba `http://localhost:5000/api/health`. La respuesta debe indicar `"status": "ok"` y `"database": "conectada"`.

## Acceso remoto con Dev Tunnels

Para abrir la aplicación desde otro dispositivo, ejecuta Flask y reenvía el puerto `5000` desde la vista **Ports** de VS Code. Abre `https://<id-del-tunel>-5000.use.devtunnels.ms/frontend/inicio_sesion/inicio_sesion.html`; el mismo host sirve el frontend y la API. Mantén el túnel privado u organizacional: no hagas público el puerto mientras las rutas de datos no tengan autorización propia.

Si la API esta en otro host o puerto, define `window.MARQUEZA_API_BASE_URL` antes de cargar `frontend/shared/api.js`, por ejemplo:

```html
<script>window.MARQUEZA_API_BASE_URL = "https://api.ejemplo.com/api";</script>
```

## Desplegar en Dokploy

El repositorio incluye [compose.yaml](compose.yaml) y un [Dockerfile](Dockerfile) en la raiz. Compose despliega la aplicacion (frontend y API en el mismo dominio) y MariaDB con un volumen persistente. La base se inicializa desde `database_marqueza.sql` solo la primera vez que se crea el volumen.

1. Sube los cambios a GitHub y crea en Dokploy un proyecto y una aplicacion de tipo **Docker Compose**, conectada a este repositorio. Usa la raiz del repositorio como directorio y `compose.yaml` como archivo Compose.
2. En **Environment** de la aplicacion, define `MARIADB_ROOT_PASSWORD` y `MARIADB_PASSWORD` con contrasenas largas y unicas. Puedes usar `MARIADB_USER=marqueza_app`; no cambies `MARIADB_DATABASE` ni `MYSQL_DB`, ya que el esquema incluido crea `marqueza_db`. La plantilla de variables esta en [.env.dokploy.example](.env.dokploy.example); no subas credenciales reales al repositorio.
3. Guarda y despliega. Espera a que el servicio `db` este saludable y luego que termine el build de `app`. La base no publica ningun puerto a Internet y sus datos quedan en el volumen `marqueza_db_data`.
4. En la configuracion de dominios de Dokploy, asigna tu dominio a `app` en el puerto interno `5000` y activa HTTPS. No hace falta crear otro contenedor NGINX: el proxy de Dokploy sirve el frontend y la API desde el mismo dominio.
5. Abre `https://tu-dominio/`. Para verificar la API y MariaDB, abre `https://tu-dominio/api/health`; la respuesta esperada incluye `"status": "ok"` y `"database": "conectada"`.
6. (Opcional) Para habilitar recuperacion de contrasena por correo, configura las variables `SMTP_*` de la plantilla y cambia `FRONTEND_RESET_URL` a `https://tu-dominio/frontend/olvido_contrasena/restablecer.html`. Para Gmail usa una contrasena de aplicacion. Si no configuras SMTP, esa funcion no enviara correos.

**Importante sobre la base de datos:** el SQL inicial elimina y vuelve a crear las tablas. Se ejecuta automaticamente solo cuando MariaDB inicializa un volumen vacio. No borres el volumen para "reiniciar" la aplicacion: perderias los datos. Configura copias de seguridad del volumen/base de datos desde tu servidor antes de usarla con datos reales.

El frontend detecta automaticamente cuando se sirve detras de un dominio de produccion y utiliza ese mismo origen para llamar a `/api`. En desarrollo conserva el puerto local `5000` y el comportamiento de Dev Tunnels.

Para enviar correos de recuperación con Gmail, activa la verificación en dos pasos y crea una contraseña de aplicación. Copia las variables SMTP de `backend/API/.env.example` a `backend/API/.env` y reemplaza el correo y la contraseña de ejemplo. Añádelas sin borrar las variables MySQL que ya existan; `.env` está excluido de Git. Reinicia Flask después de modificarlas.

La plantilla usa Gmail por STARTTLS (`SMTP_PORT=587`, `SMTP_USE_SSL=false`). Para un proveedor con SSL implícito en el puerto 465, cambia `SMTP_PORT=465` y `SMTP_USE_SSL=true`. `FRONTEND_RESET_URL` debe apuntar a `frontend/olvido_contrasena/restablecer.html` y ser accesible desde el dispositivo que recibirá el mensaje.

El correo contiene un enlace de un solo uso para establecer una contraseña nueva; nunca envía la contraseña actual en texto claro.

## Asistente local

El asistente flotante ofrece ayuda contextual sobre los módulos, los campos de sus formularios, las relaciones entre registros y los pasos habituales para crear, buscar, editar o eliminar información. Sus respuestas se generan localmente con reglas y contexto del proyecto; no se envían mensajes a un proveedor externo y no puede modificar registros ni consultar la base de datos en tiempo real. Los conteos que ofrece proceden de la caché local del navegador y podrían no coincidir con los datos actuales del servidor.
