/* ============================================================
   usuarios.js  —  MARQUEZA
   Maneja:
     • Toggle lateral (desktop ≥ 1025 px): Expande/colapsa la barra lateral.
     • Hamburger + menú desplegable (tablet / móvil ≤ 1024 px): Controla la barra superior responsive.
     • Drag lateral (solo desktop): Permite arrastrar la barra lateral para colapsarla.
     • Modo oscuro / claro: Cambia el tema visual de la aplicación.
    • Gestión de Usuarios: CRUD (Crear, Leer, Actualizar, Eliminar) usando la API.
   ============================================================ */

// --- Selección de elementos del DOM para la interfaz general ---
const body = document.querySelector("body");
const sidebar = body.querySelector(".barra_lateral");
const toggle = body.querySelector(".toggle");
const hamburger = document.getElementById("hamburger");
const modeSwitch = body.querySelector(".toggle_switch");
const modeText = body.querySelector(".modo_texto");

/**
 * Detecta si la ventana tiene un ancho de tablet o móvil (<= 1024px).
 * @returns {boolean} True si es vista móvil/tablet.
 */
const isTopbar = () => window.innerWidth <= 1024;

/* ─────────────────────────────────────────────────────────
   MODO OSCURO / CLARO
   ───────────────────────────────────────────────────────── */
modeSwitch.addEventListener("click", () => {
    body.classList.toggle("dark");
    modeText.innerText = body.classList.contains("dark") ? "Claro" : "Oscuro";
});

/**
 * Ajusta el espaciado del body (padding) dependiendo de si la barra lateral 
 * está expandida, colapsada o en modo superior (móvil).
 */
function updateLayout() {
    // Si estamos en modo topbar (tablet/móvil)
    if (isTopbar()) {
        body.classList.remove("sidebar-collapsed");
        body.style.paddingLeft = "0";
        // requestAnimationFrame asegura que el cálculo se haga después del renderizado del navegador
        requestAnimationFrame(() => {
            body.style.paddingTop = `${sidebar.getBoundingClientRect().height}px`;
        });
    } else {
        body.style.paddingTop = "0";
        if (sidebar.classList.contains("close")) {
            body.classList.add("sidebar-collapsed");
            body.style.paddingLeft = "88px";
        } else {
            body.classList.remove("sidebar-collapsed");
            body.style.paddingLeft = "250px";
        }
    }
}

updateLayout();

/* ─────────────────────────────────────────────────────────
   DESKTOP — toggle lateral (flecha)
   ───────────────────────────────────────────────────────── */
toggle.addEventListener("click", () => {
    if (isTopbar()) return; // Ignorar en móvil
    sidebar.classList.toggle("close");
    updateLayout();
});

/* ─────────────────────────────────────────────────────────
   TABLET / MÓVIL — hamburger → despliega/colapsa topbar
   ───────────────────────────────────────────────────────── */
/**
 * Abre o cierra el menú desplegable en dispositivos móviles.
 */
function toggleMobileMenu() {
    const isOpen = sidebar.classList.toggle("open");

    if (isOpen) {
        sidebar.classList.remove("close");
    } else {
        sidebar.classList.add("close");
    }

    updateLayout();

    setTimeout(() => {
        if (isTopbar()) {
            body.style.paddingTop = `${sidebar.getBoundingClientRect().height}px`;
        }
    }, 450);
}

hamburger.addEventListener("click", toggleMobileMenu);

hamburger.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        toggleMobileMenu();
    }
});

// Cerrar menú al seleccionar una opción (útil en móvil)
sidebar.querySelectorAll(".nav_links a").forEach(link => {
    link.addEventListener("click", () => {
        if (isTopbar() && sidebar.classList.contains("open")) {
            toggleMobileMenu();
        }
    });
});

/* ─────────────────────────────────────────────────────────
   RESIZE — sincronizar estado al cambiar tamaño de ventana
   ───────────────────────────────────────────────────────── */
let resizeTimer;
window.addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
        if (!isTopbar()) {
            sidebar.classList.remove("open");
            // En desktop, preferimos que inicie colapsada
            if (!sidebar.classList.contains("close")) {
                sidebar.classList.add("close");
            }
            sidebar.style.left = ""; // Limpiar cualquier posición residual del drag
        }
        updateLayout();
    }, 100);
});

/* ─────────────────────────────────────────────────────────
   DESKTOP — arrastrar barra lateral con el mouse
   ───────────────────────────────────────────────────────── */
let isDragging = false;
let dragStartX = 0; 
let sidebarStartLeft = 0; 

// Inicia el arrastre si se hace clic en el header
sidebar.addEventListener("mousedown", (event) => {
    if (isTopbar()) return; 
    if (event.target.closest(".toggle")) return; 
    // Si el click es en el header de la barra lateral
    if (event.target.closest("header")) {
        isDragging = true;
        dragStartX = event.clientX;
        sidebarStartLeft = sidebar.getBoundingClientRect().left;
        sidebar.classList.add("dragging");
    }
});

// Mueve la barra mientras se arrastra el mouse
document.addEventListener("mousemove", (event) => {
    if (!isDragging) return;

    const deltaX = event.clientX - dragStartX;
    let nextLeft = sidebarStartLeft + deltaX;
    
    // Define los límites de arrastre para la barra lateral
    const sidebarWidth = sidebar.offsetWidth;
    const minLeft = -sidebarWidth + 40;
    const maxLeft = 0;

    nextLeft = Math.max(minLeft, Math.min(maxLeft, nextLeft));
    sidebar.style.left = `${nextLeft}px`;
});

// Suelta la barra y decide si colapsar o expandir
document.addEventListener("mouseup", () => {
    if (!isDragging) return;
    isDragging = false;
    sidebar.classList.remove("dragging");

    if (sidebar.getBoundingClientRect().left < -sidebar.offsetWidth / 2) {
        sidebar.classList.add("close");
    } else {
        sidebar.classList.remove("close");
    }

    sidebar.style.left = "0";
    updateLayout();
});

sidebar.addEventListener("mouseleave", () => {
    if (isDragging) {
        isDragging = false;
        sidebar.classList.remove("dragging");
        sidebar.style.left = "0";
    }
});

/* ─────────────────────────────────────────────────────────
   GESTIÓN DE USUARIOS CON LOCAL STORAGE
   ───────────────────────────────────────────────────────── */

if (false) {

// --- Constantes y Selectores para la gestión de usuarios ---
const STORAGE_KEY = 'marqueza_usuarios';
const tableBody = document.querySelector(".cont_tabla tbody");
const btnAgregar = document.querySelector(".agregar");
const searchInput = document.querySelector(".cont_busqueda input");
const btnBuscar = document.querySelector(".cont_busqueda button:not(.agregar)");
const modalUsuario = document.getElementById("modalUsuario"); // Modal Agregar
const formUsuario = document.getElementById("formUsuario");
const btnCerrarModal = document.getElementById("cerrarModal");
const btnCancelar = document.getElementById("btnCancelar");
const modalEditarUsuario = document.getElementById("modalEditarUsuario");
const formEditarUsuario = document.getElementById("formEditarUsuario");
const btnCerrarEditModal = document.getElementById("cerrarEditModal");
const btnCancelarEdit = document.getElementById("btnCancelarEdit");

// Función para obtener usuarios de Local Storage
const getUsuarios = () => {
    const storedData = localStorage.getItem(STORAGE_KEY);
    return storedData ? JSON.parse(storedData) : [
        { nombre: 'Admin', correo: 'admin@example.com', rol: 'Administrador', contrasena: '1234' }
    ];
};

/**
 * Guarda el array de usuarios en el almacenamiento local del navegador.
 * @param {Array} usuarios - Lista de objetos de usuario.
 */
const saveUsuarios = (usuarios) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(usuarios));
};

/**
 * Limpia y vuelve a generar las filas de la tabla basadas en los usuarios almacenados.
 * Soporta filtrado por texto.
 * @param {string} filtro - Texto para buscar en nombre o correo.
 */
const renderTabla = (filtro = "") => {
    if (!tableBody) return;
    // Mapeamos los usuarios para conservar su índice original del localStorage
    let usuarios = getUsuarios().map((u, i) => ({ ...u, originalIndex: i }));

    // Lógica de filtrado
    if (filtro) {
        const termino = filtro.toLowerCase();
        usuarios = usuarios.filter(u => 
            u.nombre.toLowerCase().includes(termino) || 
            u.correo.toLowerCase().includes(termino)
        );
    }

    tableBody.innerHTML = ""; 

    usuarios.forEach((usuario) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${usuario.nombre}</td>
            <td>${usuario.correo}</td>
            <td>${usuario.rol}</td>
            <td>********</td>
            <td><button class="btn-editar" onclick="editarUsuario(${usuario.originalIndex})">Editar</button></td>
            <td><button class="btn-eliminar" onclick="eliminarUsuario(${usuario.originalIndex})">Eliminar</button></td>
        `;
        tableBody.appendChild(tr);
    });
};

// --- Listeners para Búsqueda ---
btnBuscar?.addEventListener("click", () => renderTabla(searchInput.value));

// Búsqueda en tiempo real mientras el usuario escribe
searchInput?.addEventListener("input", () => renderTabla(searchInput.value));

// --- Control del Modal de Agregar ---
btnAgregar?.addEventListener("click", () => {
    modalUsuario.style.display = "flex";
    document.getElementById("nombre").focus();
});

// Función para cerrar el modal
const cerrarModal = () => {
    modalUsuario.style.display = "none";
    formUsuario.reset();
};

// Función para cerrar el modal de edición
const cerrarEditModal = () => {
    modalEditarUsuario.style.display = "none";
    formEditarUsuario.reset();
};

btnCerrarModal?.addEventListener("click", cerrarModal);
btnCancelar?.addEventListener("click", cerrarModal);
btnCerrarEditModal?.addEventListener("click", cerrarEditModal);
btnCancelarEdit?.addEventListener("click", cerrarEditModal);

// Cerrar modales si se hace clic en el fondo oscuro
window.addEventListener("click", (e) => {
    if (e.target === modalUsuario) {
        cerrarModal();
    } else if (e.target === modalEditarUsuario) {
        cerrarEditModal();
    }
});

// --- Lógica de Guardado (Nuevo Usuario) ---
formUsuario?.addEventListener("submit", (e) => {
    e.preventDefault();
    const nombre = document.getElementById("nombre").value.trim();
    const correo = document.getElementById("correo").value.trim();
    const rol = document.getElementById("rol").value;
    const contrasena = document.getElementById("contrasena").value;
    const confirmarContrasena = document.getElementById("confirmarContrasena").value;

    // Validación de coincidencia de contraseñas
    if (contrasena !== confirmarContrasena) {
        Swal.fire({
            icon: 'error',
            title: 'Error de validación',
            text: 'Las contraseñas no coinciden. Por favor, verifícalas.',
            confirmButtonColor: '#27B7F5',
            customClass: {
                container: 'swal-above-modal' // Clase personalizada para asegurar que esté encima
            }
        });
        return;
    }

    const usuarios = getUsuarios();

    // Validar longitud del nombre
    if (nombre.length < 3) {
        Swal.fire({
            icon: 'warning',
            title: 'Nombre muy corto',
            text: 'El nombre debe tener al menos 3 caracteres.',
            confirmButtonColor: '#27B7F5',
            customClass: {
                container: 'swal-above-modal'
            }
        });
        return;
    }

    // Verificar si el usuario ya existe por correo electrónico
    if (usuarios.some(u => u.correo === correo)) {
        Swal.fire({
            icon: 'error',
            title: 'Usuario ya registrado',
            text: 'El correo electrónico ingresado ya se encuentra en uso por otro usuario.',
            confirmButtonColor: '#27B7F5',
            customClass: {
                container: 'swal-above-modal'
            }
        });
        return;
    }

    usuarios.push({ nombre, correo, rol, contrasena });
    saveUsuarios(usuarios);
    renderTabla(searchInput.value);
    cerrarModal();
    Swal.fire('¡Guardado!', 'El usuario ha sido creado con éxito.', 'success');
});

// --- Lógica de Actualización (Editar Usuario) ---
formEditarUsuario?.addEventListener("submit", (e) => {
    e.preventDefault();
    const index = document.getElementById("editIndex").value;
    const nombre = document.getElementById("editNombre").value.trim();
    const correo = document.getElementById("editCorreo").value.trim();
    const rol = document.getElementById("editRol").value;
    const nuevaPass = document.getElementById("editContrasena").value;

    const usuarios = getUsuarios();

    // Verificar si el nuevo nombre ya existe en otro usuario
    if (usuarios.some((u, i) => u.nombre.toLowerCase() === nombre.toLowerCase() && i != index)) {
        Swal.fire({
            icon: 'error',
            title: 'Nombre en uso',
            text: 'Este nombre de usuario ya pertenece a otra persona.',
            confirmButtonColor: '#27B7F5',
            customClass: {
                container: 'swal-above-modal'
            }
        });
        return;
    }

    // Verificar si el nuevo correo ya existe en otro usuario (excluyendo al actual)
    if (usuarios.some((u, i) => u.correo === correo && i != index)) {
        Swal.fire({
            icon: 'error',
            title: 'Correo en uso',
            text: 'Este correo electrónico ya pertenece a otro usuario registrado.',
            confirmButtonColor: '#27B7F5',
            customClass: {
                container: 'swal-above-modal'
            }
        });
        return;
    }

    const usuarioActual = usuarios[index];

    usuarios[index] = {
        nombre,
        correo,
        rol,
        contrasena: nuevaPass || usuarioActual.contrasena
    };

    saveUsuarios(usuarios);
    renderTabla(searchInput.value);
    cerrarEditModal();
    Swal.fire('¡Actualizado!', 'Los cambios se han guardado correctamente.', 'success');
});

// Función global para editar usuarios
window.editarUsuario = (index) => {
    const usuarios = getUsuarios();
    const usuario = usuarios[index];

    // Llenar el formulario del modal de edición
    document.getElementById("editIndex").value = index;
    document.getElementById("editNombre").value = usuario.nombre;
    document.getElementById("editCorreo").value = usuario.correo;
    document.getElementById("editRol").value = usuario.rol;
    document.getElementById("editContrasena").value = ""; 

    // Mostrar el modal
    modalEditarUsuario.style.display = "flex";
    document.getElementById("editNombre").focus();
};

// Función global para eliminar usuarios (necesaria para el atributo onclick)
window.eliminarUsuario = (index) => {
    Swal.fire({
        title: '¿Estás seguro?',
        text: "Esta acción no se puede deshacer",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#e74c3c',
        cancelButtonColor: '#707070',
        confirmButtonText: 'Eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            const usuarios = getUsuarios();
            usuarios.splice(index, 1);
            saveUsuarios(usuarios);
            renderTabla(searchInput.value);
            Swal.fire('¡Eliminado!', 'El usuario ha sido removido.', 'success');
        }
    });
};

// Inicializar la tabla al cargar el script
renderTabla();
}

/* ─────────────────────────────────────────────────────────
   GESTIÓN DE USUARIOS CON API
   ───────────────────────────────────────────────────────── */
const API_URL = "http://localhost:5000/usuarios/";
const apiTableBody = document.querySelector(".cont_tabla tbody");
const apiSearchInput = document.querySelector(".cont_busqueda input");
const apiModalUsuario = document.getElementById("modalUsuario");
const apiFormUsuario = document.getElementById("formUsuario");
const apiModalEditar = document.getElementById("modalEditarUsuario");
const apiFormEditar = document.getElementById("formEditarUsuario");
let usuariosApi = [];

const mostrarErrorApi = (error) => {
    const mensaje = error.message || "No fue posible completar la operación.";
    if (window.Swal) Swal.fire("Error", mensaje, "error"); else alert(mensaje);
};

const requestApi = async (url, options = {}) => {
    const response = await fetch(url, {
        ...options,
        headers: { "Content-Type": "application/json", ...(options.headers || {}) }
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.error || data.message || "Error en la API.");
    return data;
};

const escapeHtmlApi = (value) => String(value ?? "")
    .replaceAll("&", "&amp;").replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;").replaceAll('"', "&quot;");

const renderTablaApi = (filtro = "") => {
    const termino = filtro.toLowerCase();
    const filtrados = usuariosApi.filter(usuario =>
        String(usuario.nombre).toLowerCase().includes(termino) ||
        String(usuario.correo).toLowerCase().includes(termino)
    );
    apiTableBody.innerHTML = filtrados.map(usuario => `
        <tr>
            <td>${escapeHtmlApi(usuario.id)}</td>
            <td>${escapeHtmlApi(usuario.nombre)}</td>
            <td>${escapeHtmlApi(usuario.correo)}</td>
            <td>${Number(usuario.estado) === 1 ? "Activo" : "Inactivo"}</td>
            <td>${escapeHtmlApi(usuario.det_etc_id)}</td>
            <td><button class="btn-editar" onclick="editarUsuarioApi(${usuario.id})">Editar</button>
            <button class="btn-eliminar" onclick="eliminarUsuarioApi(${usuario.id})">Eliminar</button></td>
        </tr>`).join("");
};

const cargarUsuariosApi = async () => {
    try {
        usuariosApi = await requestApi(API_URL);
        renderTablaApi(apiSearchInput.value);
    } catch (error) {
        apiTableBody.innerHTML = '<tr><td colspan="6">No se pudieron cargar los usuarios.</td></tr>';
        mostrarErrorApi(error);
    }
};

const cerrarModalApi = () => { apiModalUsuario.style.display = "none"; apiFormUsuario.reset(); };
const cerrarEditarApi = () => { apiModalEditar.style.display = "none"; apiFormEditar.reset(); };
document.querySelector(".agregar").addEventListener("click", () => { apiFormUsuario.reset(); apiModalUsuario.style.display = "flex"; });
document.getElementById("cerrarModal").addEventListener("click", cerrarModalApi);
document.getElementById("btnCancelar").addEventListener("click", cerrarModalApi);
document.getElementById("cerrarEditModal").addEventListener("click", cerrarEditarApi);
document.getElementById("btnCancelarEdit").addEventListener("click", cerrarEditarApi);
document.querySelector(".cont_busqueda button:not(.agregar)").addEventListener("click", () => renderTablaApi(apiSearchInput.value));
apiSearchInput.addEventListener("input", () => renderTablaApi(apiSearchInput.value));
window.addEventListener("click", (event) => {
    if (event.target === apiModalUsuario) cerrarModalApi();
    if (event.target === apiModalEditar) cerrarEditarApi();
});

const datosFormularioApi = (prefijo = "") => {
    const ids = prefijo === "edit"
        ? { nombre: "editNombre", correo: "editCorreo", contrasena: "editContrasena", estado: "editEstado", detEtcId: "editDetEtcId" }
        : { nombre: "nombre", correo: "correo", contrasena: "contrasena", estado: "estado", detEtcId: "detEtcId" };
    const campos = Object.fromEntries(Object.entries(ids).map(([campo, id]) => [campo, document.getElementById(id)]));
    const campoFaltante = Object.entries(campos).find(([, elemento]) => !elemento);
    if (campoFaltante) throw new Error(`No se encontró el campo ${campoFaltante[0]} del formulario.`);

    return {
        nombre: campos.nombre.value.trim(),
        correo: campos.correo.value.trim(),
        contrasena: campos.contrasena.value,
        estado: Number(campos.estado.value),
        det_etc_id: Number(campos.detEtcId.value)
    };
};

apiFormUsuario.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (document.getElementById("contrasena").value !== document.getElementById("confirmarContrasena").value) {
        mostrarErrorApi(new Error("Las contraseñas no coinciden.")); return;
    }
    try {
        const resultado = await requestApi(API_URL, { method: "POST", body: JSON.stringify(datosFormularioApi()) });
        cerrarModalApi(); await cargarUsuariosApi();
        if (window.Swal) Swal.fire("Guardado", `Usuario creado con el ID ${resultado.id}.`, "success");
    } catch (error) { mostrarErrorApi(error); }
});

apiFormEditar.addEventListener("submit", async (event) => {
    event.preventDefault();
    const id = document.getElementById("editIndex").value;
    try {
        await requestApi(`${API_URL}${id}`, { method: "PUT", body: JSON.stringify(datosFormularioApi("edit")) });
        cerrarEditarApi(); await cargarUsuariosApi();
        if (window.Swal) Swal.fire("Actualizado", "Los cambios fueron guardados.", "success");
    } catch (error) { mostrarErrorApi(error); }
});

window.editarUsuarioApi = (id) => {
    const usuario = usuariosApi.find(item => Number(item.id) === Number(id));
    if (!usuario) return;
    document.getElementById("editIndex").value = usuario.id;
    document.getElementById("editNombre").value = usuario.nombre || "";
    document.getElementById("editCorreo").value = usuario.correo || "";
    document.getElementById("editContrasena").value = usuario.contrasena || "";
    document.getElementById("editEstado").value = usuario.estado;
    document.getElementById("editDetEtcId").value = usuario.det_etc_id || "";
    apiModalEditar.style.display = "flex";
};

window.eliminarUsuarioApi = async (id) => {
    const confirmado = window.Swal
        ? (await Swal.fire({ title: "¿Eliminar usuario?", text: "Esta acción no se puede deshacer.", icon: "warning", showCancelButton: true, confirmButtonText: "Eliminar", cancelButtonText: "Cancelar" })).isConfirmed
        : confirm("¿Eliminar usuario? Esta acción no se puede deshacer.");
    if (!confirmado) return;
    try {
        await requestApi(`${API_URL}${id}`, { method: "DELETE" });
        await cargarUsuariosApi();
        if (window.Swal) Swal.fire("Eliminado", "El usuario fue eliminado.", "success");
    } catch (error) { mostrarErrorApi(error); }
};

cargarUsuariosApi();