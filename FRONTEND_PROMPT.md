# Prompt maestro del frontend MARQUEZA

## Contexto del proyecto

MARQUEZA es una aplicacion web de gestion para una empresa de confecciones. El repositorio contiene un backend Flask en `backend/API` y un frontend multipagina sin framework, construido con HTML semantico, CSS por modulo y JavaScript del navegador. La interfaz usa Boxicons, ECharts, SweetAlert2 y jsPDF desde CDN.

## Pantallas existentes

- `frontend/inicio`: dashboard con metricas y cuatro graficas ECharts.
- `frontend/insumos`: CRUD de insumos, filtros, busqueda y exportacion PDF.
- `frontend/productos`: CRUD de productos, filtros y exportacion PDF.
- `frontend/clientes`: CRUD local de clientes.
- `frontend/proveedores`: CRUD local de proveedores.
- `frontend/ventas`: CRUD local de ventas.
- `frontend/usuarios`: CRUD de usuarios y filtros.
- `frontend/ayuda`: buscador y filtros de tarjetas de ayuda.
- `frontend/registro`: validacion del formulario de registro.
- `frontend/incio sesion`: validacion de inicio de sesion.
- `frontend/fondo`: logos, fondos e imagenes decorativas.

Cada pantalla mantiene su trio de archivos HTML, CSS y JS. `frontend/shared` contiene ahora la capa comun para tema, navegacion y almacenamiento.

## Reglas de arquitectura

1. Mantener separacion estricta: HTML para estructura, CSS para presentacion y JavaScript para comportamiento.
2. No agregar `onclick`, `onsubmit` ni estilos inline. Usar `addEventListener` y clases CSS.
3. Encapsular comportamiento en clases. Cada modulo debe tener una clase de pagina y clases pequenas para responsabilidades especificas.
4. Reutilizar `MarquezaAppShell` para tema, menu lateral, responsive y preferencia de modo.
5. Usar `MarquezaStorage` como adaptador temporal de `localStorage`. La futura API Flask debe sustituirlo sin cambiar el renderizado.
6. No cambiar las claves actuales de `localStorage` sin migracion: `marqueza_clientes`, `marqueza_proveedores` y `marqueza_ventas`.
7. Conservar los IDs y clases que usa el CSS existente mientras se migra cada pantalla.
8. Escapar texto generado desde datos antes de insertarlo en HTML cuando el origen deje de ser local.
9. Usar nombres descriptivos en espanol o ingles consistente; evitar variables de una sola letra.
10. Mantener accesibilidad: botones reales, `aria-label` en iconos, foco visible, navegacion por teclado y mensajes de estado.
11. Mantener rutas relativas funcionando desde cada carpeta. Los recursos compartidos se referencian como `../shared/...` desde una pantalla.
12. Las dependencias CDN deben conservarse hasta que exista un gestor de paquetes o una estrategia local equivalente.

## Contrato recomendado para un modulo CRUD

```js
class CrudPage {
    constructor({ storageKey, formId, modalId, fields, columns }) {}
    init() {}
    readRecords() {}
    writeRecords(records) {}
    collectForm() {}
    render(query = "") {}
    openModal(recordIndex = -1) {}
    closeModal() {}
    deleteRecord(recordIndex) {}
}

document.addEventListener("DOMContentLoaded", () => {
    new MarquezaAppShell().init();
    new ClientesPage().init();
});
```

La clase de pagina debe coordinar el flujo; el acceso a datos, modal, renderizado y eventos deben ser metodos separados. Los botones de filas deben usar delegacion de eventos sobre la tabla.

## Direccion visual

La identidad usa cian MARQUEZA, azul marino para contraste, coral para acciones destacadas, fondo marfil y sombras suaves. Cada modulo puede tener una identidad secundaria:

- Dashboard: cian y azul marino, visualizacion de datos limpia.
- Insumos: verde azulado para estados de inventario.
- Productos: coral para catalogo y acciones.
- Clientes: azul marino y cian para datos de contacto.
- Proveedores: verde para abastecimiento.
- Ventas: coral y dorado para transacciones.
- Usuarios: azul sobrio para administracion.
- Ayuda: amarillo suave para orientacion.
- Registro e inicio de sesion: composicion centrada, foco en legibilidad y validacion.

Usar variables CSS, `@media` para tablet y movil, tablas desplazables horizontalmente y estados claros de hover, focus, error y vacio. No mezclar reglas de un modulo con otro.

## Backend y siguiente migracion

El frontend actual usa datos locales en varios CRUD y el backend Flask expone controladores, modelos y rutas en `backend/API`. La siguiente etapa debe sustituir gradualmente el adaptador local por `fetch` contra la API, centralizar la URL base y mostrar estados de carga/error. No duplicar logica de validacion ni inventar rutas que no existan en `swagger.json`.

## Checklist de calidad

- Abrir cada HTML directamente o desde el servidor y comprobar que no haya recursos 404.
- Probar menu colapsado, menu movil, tema persistente y teclado.
- Probar crear, editar, buscar y eliminar en cada CRUD.
- Confirmar que los datos existentes de `localStorage` siguen visibles.
- Ejecutar una comprobacion de sintaxis sobre cada JS.
- Revisar que no queden handlers inline ni CSS inline.
- Validar desktop, tablet y movil.
