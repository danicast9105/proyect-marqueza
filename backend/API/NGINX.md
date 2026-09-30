# NGINX para la API MARQUEZA

La imagen de la API escucha dentro del contenedor en el puerto `80`, y sus rutas incluyen el prefijo `/api` (por ejemplo, `/api/health`). El proxy debe conservar esa ruta al reenviar la solicitud.

## Si usas el proxy integrado de Dokploy

Esta es la opción recomendada al desplegar la API en Dokploy:

1. Configura la aplicacion con el Dockerfile de `backend/API`.
2. En la configuracion de dominio o proxy de Dokploy, selecciona el puerto interno `80`.
3. Asigna el dominio de la API y activa HTTPS desde Dokploy.
4. No agregues otro NGINX en el mismo servidor escuchando en los puertos `80` o `443`; Dokploy ya utiliza esos puertos para publicar aplicaciones.

## Si NGINX es externo a Dokploy

El archivo [`nginx.conf`](nginx.conf) contiene la configuracion lista para copiar al NGINX externo. Reenvia el dominio al puerto publicado de la API y supone que el puerto `80` del contenedor se publica solo en `127.0.0.1:5000` del servidor:

```nginx
server {
    listen 80;
    server_name api.ejemplo.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

Reemplaza `api.ejemplo.com` por el dominio real. En este ejemplo, `proxy_pass` no incluye una ruta final para que NGINX conserve `/api/...` al reenviar. El destino `127.0.0.1:5000` solo sirve si el puerto del contenedor se publicó en ese puerto del host; si NGINX y la API están en una red Docker compartida, usa el nombre del servicio de la API y el puerto `80` como destino.

Valida y recarga NGINX en el servidor:

```sh
sudo nginx -t
sudo systemctl reload nginx
```

Si NGINX está en el mismo servidor que Dokploy, no uses este ejemplo sin cambiar la arquitectura: ambos pueden intentar ocupar los puertos `80` y `443`. En ese caso, usa el proxy de Dokploy o coloca NGINX en otra máquina.

## Verificar

Abre `https://api.ejemplo.com/api/health`. La respuesta debe indicar `"status": "ok"` y `"database": "conectada"`. Si falla, confirma que el dominio apunta al proxy, que el upstream usa el puerto correcto y que MySQL es accesible desde la API.

El backend actualmente permite CORS desde cualquier origen (`*`). Antes de usarlo en producción, limita el origen permitido al dominio real del frontend.