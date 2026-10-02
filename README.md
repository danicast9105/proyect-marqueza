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

## Desplegar la API en Dokploy

Consulta [backend/API/NGINX.md](backend/API/NGINX.md) para enrutar el dominio a la API con Dokploy o con un NGINX externo.

1. Crea una aplicacion desde este repositorio y selecciona **Dockerfile** como tipo de build. Configura `backend/API` como contexto y `backend/API/Dockerfile` como ruta del Dockerfile.
2. Expone el puerto `80` y asigna un dominio, por ejemplo `api.tudominio.com`. La imagen inicia Gunicorn y escucha en `0.0.0.0`.
3. En las variables de entorno de Dokploy define `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD` y `MYSQL_DB` con los datos de una base MariaDB accesible desde la aplicacion. Los nombres `MYSQL_*` se conservan por compatibilidad con el driver MySQL/MariaDB; `MYSQL_PORT` usa por defecto `3306`. Importa `database_marqueza.sql` en esa base antes de probar la API.
4. Para recuperar contrasenas, configura `SMTP_HOST`, `SMTP_USERNAME`, `SMTP_PASSWORD` y `SMTP_FROM`. El puerto predeterminado es `587`; para SSL implicito usa `SMTP_PORT=465` y `SMTP_USE_SSL=true`. Define `FRONTEND_RESET_URL` con la URL publica de `olvido_contrasena/restablecer.html`.
5. Despues del despliegue, comprueba `https://api.tudominio.com/api/health`. Debe responder con `"status": "ok"` y `"database": "conectada"`.
6. Cuando tengas el dominio real de la API, en `frontend/shared/api.js` reemplaza `http://localhost:5000/api` por `https://api.tudominio.com/api` y vuelve a desplegar el frontend. Asi el navegador llamara a la API publicada y no a su propio `localhost`.

`backend/API/.dockerignore` excluye `.env` y archivos locales del build. Guarda las credenciales en las variables de entorno de Dokploy, no en la imagen ni en Git.

Para enviar correos de recuperación con Gmail, activa la verificación en dos pasos y crea una contraseña de aplicación. Copia las variables SMTP de `backend/API/.env.example` a `backend/API/.env` y reemplaza el correo y la contraseña de ejemplo. Añádelas sin borrar las variables MySQL que ya existan; `.env` está excluido de Git. Reinicia Flask después de modificarlas.

La plantilla usa Gmail por STARTTLS (`SMTP_PORT=587`, `SMTP_USE_SSL=false`). Para un proveedor con SSL implícito en el puerto 465, cambia `SMTP_PORT=465` y `SMTP_USE_SSL=true`. `FRONTEND_RESET_URL` debe apuntar a `frontend/olvido_contrasena/restablecer.html` y ser accesible desde el dispositivo que recibirá el mensaje.

El correo contiene un enlace de un solo uso para establecer una contraseña nueva; nunca envía la contraseña actual en texto claro.
