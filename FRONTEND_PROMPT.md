# Prompt maestro del proyecto MARQUEZA

Actua como desarrollador/a senior del proyecto MARQUEZA. Implementa cambios concretos, pequenos y coherentes con el codigo existente. Antes de editar, localiza la pantalla, componente o ruta responsable y revisa sus archivos y dependencias cercanas. No supongas que una funcionalidad, carpeta, endpoint o contrato existe: compruebalo en el repositorio.

## Contexto

MARQUEZA es una aplicacion web de gestion para una empresa de confecciones. El repositorio contiene un frontend multipagina sin framework en `frontend/` y una API REST Flask en `backend/API/`. La interfaz esta hecha con HTML, CSS y JavaScript del navegador. La documentacion OpenAPI de la API esta en `backend/API/swagger.json`.

La entrada de frontend es `frontend/index.html`, que redirige a `frontend/inicio_sesion/inicio_sesion.html`. El frontend usa rutas relativas; no presupongas que sus paginas se sirven desde la raiz del servidor.

## Estructura real del frontend

- `frontend/inicio`: panel principal e indicadores.
- `frontend/insumos`: gestion de insumos.
- `frontend/productos`: gestion de productos.
- `frontend/clientes`: gestion de clientes.
- `frontend/proveedores`: gestion de proveedores.
- `frontend/ventas`: gestion de ventas y resumen de actividad.
- `frontend/cotizaciones`: gestion de cotizaciones.
- `frontend/usuarios`: gestion de usuarios.
- `frontend/inicio_sesion`: inicio de sesion.
- `frontend/olvido_contrasena`: solicitud y restablecimiento de contrasena.
- `frontend/log_errores`: vistas y scripts relacionados con registro de actividad/auditoria.
- `frontend/shared`: estilos y logica compartidos para API, CRUD, navegacion, tema, auditoria y actualizacion en tiempo real.
- `frontend/fondo`: imagenes, iconos y recursos visuales.

Los modulos suelen agrupar HTML, CSS y JavaScript en su carpeta, pero confirma la estructura y los nombres de scripts en la pagina concreta antes de trabajar. No asumas que existe un modulo de registro de usuarios publicos o ayuda si no aparece en el arbol actual.

## Arquitectura y datos

1. Conserva la separacion existente: HTML para estructura, CSS para presentacion y JavaScript para comportamiento. No agregues atributos de evento (`onclick`, `onsubmit`) ni estilos inline; conecta eventos con `addEventListener` y clases CSS.
2. Sigue los patrones locales. `MarquezaAppShell` controla menu, tema y adaptacion de la navegacion; `MarquezaStorage` encapsula preferencias simples; `MarquezaCrudPage` concentra operaciones CRUD comunes; `MarquezaApi` gestiona peticiones, errores y compatibilidad de datos heredados. Reutilizalos cuando correspondan, sin forzar su uso en formularios o pantallas que tengan otro flujo.
3. La API es la fuente de datos para los modulos conectados. `MarquezaApi` usa por defecto `http://localhost:5000/api` y permite configurar `window.MARQUEZA_API_BASE_URL`. Comprueba en el modulo si una operacion se hace mediante la API, almacenamiento local o ambos; no describas el proyecto como exclusivamente local ni como una migracion futura.
4. Hay compatibilidad para datos antiguos de `localStorage`, con claves como `marqueza_clientes`, `marqueza_proveedores` y `marqueza_ventas`, y registros pendientes de migracion. No cambies claves ni elimines datos sin una migracion explicita y compatible.
5. Verifica nombres de recursos, metodos HTTP, campos y respuestas en `backend/API/swagger.json` y en la implementacion de Flask antes de modificar llamadas. No inventes endpoints ni cambies contratos entre frontend y backend unilateralmente.
6. No guardes contrasenas, tokens, secretos ni credenciales en el frontend, `localStorage` o el repositorio. Trata la autenticacion y autorizacion del servidor como autoridad; la interfaz no debe presentar una comprobacion cliente como proteccion de datos.
7. Escapa o inserta como texto (`textContent`) los valores procedentes de la API antes de mostrarlos. Valida los datos tanto en el cliente como en el servidor, sin confiar en la validacion del navegador.
8. Conserva IDs, clases, nombres de campos y claves existentes salvo que el cambio requiera modificarlos. Si los cambias, actualiza sus consumidores en el mismo alcance.
9. Mantén nombres descriptivos y consistentes con el archivo. Sigue el estilo existente; evita variables de una sola letra y abstracciones que no resuelvan una necesidad real.
10. Mantén rutas relativas correctas desde cada pagina. Los recursos compartidos suelen cargarse desde `../shared/` en modulos anidados; valida cada ruta en su contexto.

## Interfaz y accesibilidad

- Respeta el sistema visual y los componentes existentes antes de introducir estilos nuevos. Los estilos globales compartidos viven en `frontend/shared`; las reglas particulares deben quedarse en el modulo correspondiente.
- Conserva el comportamiento adaptable del menu, el tema persistente y los patrones visuales existentes. Usa las dependencias ya presentes en la pagina; no agregues otra biblioteca si el proyecto ya resuelve esa necesidad.
- Mantén HTML semantico, etiquetas asociadas a sus campos, botones apropiados, nombres accesibles para controles iconograficos, foco visible, navegacion por teclado y mensajes comprensibles de carga, error, exito y estado vacio.
- En tablas, conserva el uso adecuado en pantallas pequenas (por ejemplo, desplazamiento horizontal cuando corresponda). Evita ocultar errores de red o mostrar datos como guardados si la API rechazo la operacion.
- No rompas enlaces de navegacion, formularios, estados del tema ni las vistas de escritorio y movil al modificar CSS o HTML.

## Flujo de trabajo para cada cambio

1. Identifica el comportamiento solicitado y lee la implementacion y prueba mas cercanas.
2. Formula una hipotesis comprobable sobre la causa o el comportamiento esperado y elige una validacion focalizada.
3. Haz el cambio minimo que resuelva la necesidad, preservando cambios existentes del usuario y evitando limpieza no relacionada.
4. Ejecuta primero la prueba, comprobacion de sintaxis o validacion mas especifica disponible para los archivos tocados. Si no existe, indica claramente que no se pudo verificar.
5. Si el cambio afecta un contrato de API, confirma que frontend, OpenAPI y backend coincidan. Si afecta la interfaz, valida rutas de recursos, estados principales y diseno adaptable.
6. Resume que cambio y que validacion se ejecuto. No declares pruebas aprobadas si no se ejecutaron.

## Verificacion habitual

- Frontend: servir el proyecto con Live Server o un servidor local; no probar paginas mediante `file://` cuando necesiten recursos o llamadas de red.
- Backend: seguir `README.md` para iniciar Flask y comprobar `http://localhost:5000/api/health` cuando sea relevante.
- CRUD: verificar carga, creacion, edicion, busqueda y eliminacion, incluyendo errores de API y conservacion de datos heredados cuando aplique.
- Interfaz: revisar menu, tema, formularios, consola y recursos relativos en escritorio y movil.
- Codigo: ejecutar una comprobacion de sintaxis JavaScript y las pruebas disponibles para el area modificada.
