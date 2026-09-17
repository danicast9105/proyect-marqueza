/* ============================================================
   insumos.js  —  MARQUEZA
   Maneja:
     • Toggle lateral (desktop ≥ 1025 px): Expande/colapsa la barra lateral.
     • Hamburger + menú desplegable (tablet / móvil ≤ 1024 px): Controla la barra superior responsive.
     • Drag lateral (solo desktop): Permite arrastrar la barra lateral para colapsarla.
     • Modo oscuro / claro: Cambia el tema visual de la aplicación.
     • Gestión de Insumos: CRUD (Crear, Leer, Actualizar, Eliminar) usando LocalStorage.
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
    if (isTopbar()) {
        body.classList.remove("sidebar-collapsed");
        body.style.paddingLeft = "0";
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

toggle.addEventListener("click", () => {
    if (isTopbar()) return;
    sidebar.classList.toggle("close");
    updateLayout();
});

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

sidebar.querySelectorAll(".nav_links a").forEach(link => {
    link.addEventListener("click", () => {
        if (isTopbar() && sidebar.classList.contains("open")) {
            toggleMobileMenu();
        }
    });
});

let resizeTimer;
window.addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
        if (!isTopbar()) {
            sidebar.classList.remove("open");
            if (!sidebar.classList.contains("close")) {
                sidebar.classList.add("close");
            }
            sidebar.style.left = "";
        }
        updateLayout();
    }, 100);
});

let isDragging = false;
let dragStartX = 0;
let sidebarStartLeft = 0;

sidebar.addEventListener("mousedown", (event) => {
    if (isTopbar()) return;
    if (event.target.closest(".toggle")) return;
    if (event.target.closest("header")) {
        isDragging = true;
        dragStartX = event.clientX;
        sidebarStartLeft = sidebar.getBoundingClientRect().left;
        sidebar.classList.add("dragging");
    }
});

document.addEventListener("mousemove", (event) => {
    if (!isDragging) return;

    const deltaX = event.clientX - dragStartX;
    let nextLeft = sidebarStartLeft + deltaX;
    const sidebarWidth = sidebar.offsetWidth;
    const minLeft = -sidebarWidth + 40;
    const maxLeft = 0;

    nextLeft = Math.max(minLeft, Math.min(maxLeft, nextLeft));
    sidebar.style.left = `${nextLeft}px`;
});

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
   GESTIÓN DE INSUMOS CON LOCAL STORAGE
   ───────────────────────────────────────────────────────── */
const STORAGE_KEY = 'marqueza_insumos';
const tableBody = document.querySelector(".cont_tabla tbody");
const btnAgregar = document.querySelector(".agregar");
const searchInput = document.querySelector(".cont_busqueda input");
const btnBuscar = document.getElementById("btnBuscar");
const btnExportPdf = document.getElementById("btnExportPdf");
const filtroCategoria = document.getElementById("filtroCategoria");
const estadoButtons = Array.from(document.querySelectorAll(".estado-btn"));
const modalInsumo = document.getElementById("modalInsumo");
const formInsumo = document.getElementById("formInsumo");
const proveedorSelect = document.getElementById("proveedor");
const btnCerrarModal = document.getElementById("cerrarModal");
const btnCancelar = document.getElementById("btnCancelar");
const modalEditarInsumo = document.getElementById("modalEditarInsumo");
const formEditarInsumo = document.getElementById("formEditarInsumo");
const editProveedorSelect = document.getElementById("editProveedor");
const btnCerrarEditModal = document.getElementById("cerrarEditModal");
const btnCancelarEdit = document.getElementById("btnCancelarEdit");

const getInsumos = () => {
    const storedData = localStorage.getItem(STORAGE_KEY);
    if (storedData) {
        try {
            const parsed = JSON.parse(storedData);
            return Array.isArray(parsed) ? parsed : [];
        } catch {
            localStorage.removeItem(STORAGE_KEY);
        }
    }
    return [
        { nombre: 'Tela algodón', categoria: 'Tela', cantidad: 25, unidad: 'metros', precioUnitario: 12.50, estado: 'Disponible' },
        { nombre: 'Botones negros', categoria: 'Complementos', cantidad: 120, unidad: 'piezas', precioUnitario: 0.15, estado: 'Disponible' }
    ];
};

const saveInsumos = (insumos) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(insumos));
};

const getProveedores = () => {
    try {
        const proveedores = JSON.parse(localStorage.getItem("marqueza_proveedores") || "[]");
        return Array.isArray(proveedores) ? proveedores : [];
    } catch {
        return [];
    }
};

const cargarProveedores = (selectedValue = "") => {
    const proveedores = getProveedores();
    [proveedorSelect, editProveedorSelect].forEach(select => {
        if (!select) return;
        select.replaceChildren(new Option("Selecciona un proveedor", ""));
        proveedores.forEach(proveedor => {
            const empresa = String(proveedor.empresa || "").trim();
            if (empresa) select.appendChild(new Option(empresa, empresa));
        });
        select.value = selectedValue;
    });
};

const formatNumber = (value) => Number(value).toLocaleString('es-CO', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

const getEstadoPorCantidad = (cantidad) => {
    if (!Number.isFinite(cantidad) || cantidad <= 5) {
        return { label: 'Bajo', clase: 'estado-rojo' };
    }

    if (cantidad <= 20) {
        return { label: 'Medio', clase: 'estado-amarillo' };
    }

    return { label: 'Bueno', clase: 'estado-verde' };
};

const formatMoney = (value) => Number(value || 0).toLocaleString('es-CO', {
    style: 'currency',
    currency: 'COP',
    maximumFractionDigits: 0
});

const updateSummary = (records = getInsumos(), visibleRecords = records) => {
    const lowStock = records.filter(item => getEstadoPorCantidad(Number(item.cantidad)).label === 'Bajo').length;
    const available = records.filter(item => String(item.estado).toLowerCase() === 'disponible').length;
    const estimatedValue = records.reduce((total, item) => total + Number(item.cantidad || 0) * Number(item.precioUnitario || 0), 0);
    const setText = (id, value) => { const element = document.getElementById(id); if (element) element.textContent = value; };
    setText('totalInsumos', records.length);
    setText('insumosBajos', lowStock);
    setText('insumosDisponibles', available);
    setText('valorInsumos', formatMoney(estimatedValue));
    setText('resultadosInsumos', `${visibleRecords.length} ${visibleRecords.length === 1 ? 'resultado' : 'resultados'}`);
};

const getFilteredInsumos = () => {
    const textoBusqueda = searchInput.value.trim().toLowerCase();
    const categoriaSeleccionada = filtroCategoria.value;
    const estadoSeleccionado = estadoButtons.find(btn => btn.classList.contains('active'))?.dataset.status || 'Todos';

    return getInsumos().map((item, index) => ({ ...item, originalIndex: index }))
        .filter(item => {
            const estadoTexto = getEstadoPorCantidad(item.cantidad).label.toLowerCase();
            const cumpleBusqueda =
                item.nombre.toLowerCase().includes(textoBusqueda) ||
                item.categoria.toLowerCase().includes(textoBusqueda) ||
                String(item.proveedor || '').toLowerCase().includes(textoBusqueda) ||
                item.unidad.toLowerCase().includes(textoBusqueda) ||
                item.estado.toLowerCase().includes(textoBusqueda) ||
                estadoTexto.includes(textoBusqueda);

            const cumpleCategoria = !categoriaSeleccionada || item.categoria === categoriaSeleccionada;
            const cumpleEstado = estadoSeleccionado === 'Todos' || estadoTexto === estadoSeleccionado.toLowerCase();

            return cumpleBusqueda && cumpleCategoria && cumpleEstado;
        });
};

const renderTabla = () => {
    if (!tableBody) return;

    const insumos = getFilteredInsumos();

    updateSummary(getInsumos(), insumos);

    tableBody.innerHTML = "";

    if (!insumos.length) {
        tableBody.innerHTML = '<tr><td colspan="9" class="sin-resultados"><i class="bx bx-search-alt-2"></i><strong>No encontramos insumos</strong><span>Prueba con otra búsqueda o cambia los filtros.</span></td></tr>';
        return;
    }

    insumos.forEach((insumo) => {
        const estadoVisual = getEstadoPorCantidad(insumo.cantidad);
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td data-label="Nombre">${insumo.nombre}</td>
            <td data-label="Categoría">${insumo.categoria}</td>
            <td data-label="Proveedor">${insumo.proveedor || 'Sin proveedor'}</td>
            <td data-label="Cantidad">${insumo.cantidad}</td>
            <td data-label="Unidad">${insumo.unidad}</td>
            <td data-label="Precio">${formatNumber(insumo.precioUnitario)}</td>
            <td data-label="Estado"><span class="estado-badge ${estadoVisual.clase}">${estadoVisual.label}</span></td>
            <td data-label="Editar"><button type="button" class="btn-editar" data-index="${insumo.originalIndex}" title="Editar" aria-label="Editar"><i class="bx bx-pencil" aria-hidden="true"></i></button></td>
            <td data-label="Eliminar"><button type="button" class="btn-eliminar" data-index="${insumo.originalIndex}" title="Eliminar" aria-label="Eliminar"><i class="bx bx-trash-alt" aria-hidden="true"></i></button></td>
        `;
        tableBody.appendChild(tr);
    });
};

const actualizarCategorias = () => {
    const categorias = Array.from(new Set(getInsumos().map(item => item.categoria).filter(Boolean))).sort();
    const seleccionActual = filtroCategoria.value;
    filtroCategoria.innerHTML = '<option value="">Todas</option>' + categorias.map(cat => `
        <option value="${cat}"${cat === seleccionActual ? ' selected' : ''}>${cat}</option>
    `).join('');
};

const exportToPDF = () => {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF({ orientation: 'landscape' });
    const insumos = getFilteredInsumos();
    const rows = insumos.map(item => [
        item.nombre,
        item.categoria,
        item.proveedor || 'Sin proveedor',
        item.cantidad,
        item.unidad,
        formatNumber(item.precioUnitario),
        getEstadoPorCantidad(item.cantidad).label
    ]);

    doc.setFontSize(14);
    doc.text('Listado de Insumos', 14, 16);
    doc.setFontSize(10);
    doc.autoTable({
        startY: 22,
        head: [[ 'Nombre', 'Categoría', 'Proveedor', 'Cantidad', 'Unidad', 'Precio Unitario', 'Estado' ]],
        body: rows,
        theme: 'striped',
        headStyles: { fillColor: [39, 183, 245], textColor: 255 },
        alternateRowStyles: { fillColor: [245, 245, 245] },
        styles: { fontSize: 9, cellPadding: 4 }
    });
    doc.save('insumos-marquiza.pdf');
};

btnBuscar?.addEventListener("click", renderTabla);
searchInput?.addEventListener("input", renderTabla);
filtroCategoria?.addEventListener("change", renderTabla);
estadoButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        estadoButtons.forEach(button => button.classList.remove('active'));
        btn.classList.add('active');
        renderTabla();
    });
});
btnExportPdf?.addEventListener('click', exportToPDF);

tableBody?.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-index]");
    if (!button) return;
    const index = Number(button.dataset.index);
    if (button.classList.contains("btn-editar")) editarInsumo(index);
    if (button.classList.contains("btn-eliminar")) eliminarInsumo(index);
});

btnAgregar?.addEventListener("click", () => {
    cargarProveedores();
    modalInsumo.style.display = "flex";
    document.getElementById("nombre").focus();
});

const cerrarModal = () => {
    modalInsumo.style.display = "none";
    formInsumo.reset();
};

const cerrarEditModal = () => {
    modalEditarInsumo.style.display = "none";
    formEditarInsumo.reset();
};

btnCerrarModal?.addEventListener("click", cerrarModal);
btnCancelar?.addEventListener("click", cerrarModal);
btnCerrarEditModal?.addEventListener("click", cerrarEditModal);
btnCancelarEdit?.addEventListener("click", cerrarEditModal);

window.addEventListener("click", (e) => {
    if (e.target === modalInsumo) {
        cerrarModal();
    } else if (e.target === modalEditarInsumo) {
        cerrarEditModal();
    }
});

formInsumo?.addEventListener("submit", (e) => {
    e.preventDefault();
    const nombre = document.getElementById("nombre").value.trim();
    const categoria = document.getElementById("categoria").value.trim();
    const proveedor = proveedorSelect.value;
    const cantidad = Number(document.getElementById("cantidad").value);
    const unidad = document.getElementById("unidad").value.trim();
    const precioUnitario = Number(document.getElementById("precioUnitario").value);
    const estado = document.getElementById("estado").value;

    if (nombre.length < 2) {
        Swal.fire({ icon: 'warning', title: 'Nombre requerido', text: 'Ingrese un nombre válido para el insumo.', confirmButtonColor: '#27B7F5' });
        return;
    }

    if (!categoria || !proveedor || !unidad) {
        Swal.fire({ icon: 'warning', title: 'Campos incompletos', text: 'Complete la categoría, el proveedor y la unidad del insumo.', confirmButtonColor: '#27B7F5' });
        return;
    }

    if (!Number.isFinite(cantidad) || cantidad < 1) {
        Swal.fire({ icon: 'warning', title: 'Cantidad inválida', text: 'Ingrese una cantidad mayor o igual a 1.', confirmButtonColor: '#27B7F5' });
        return;
    }

    if (!Number.isFinite(precioUnitario) || precioUnitario < 0) {
        Swal.fire({ icon: 'warning', title: 'Precio inválido', text: 'Ingrese un precio unitario válido.', confirmButtonColor: '#27B7F5' });
        return;
    }

    const insumos = getInsumos();

    if (insumos.some(item => item.nombre.toLowerCase() === nombre.toLowerCase() && item.categoria.toLowerCase() === categoria.toLowerCase())) {
        Swal.fire({ icon: 'error', title: 'Insumo duplicado', text: 'Ya existe un insumo con el mismo nombre y categoría.', confirmButtonColor: '#27B7F5' });
        return;
    }

    insumos.push({ nombre, categoria, proveedor, cantidad, unidad, precioUnitario, estado });
    saveInsumos(insumos);
    actualizarCategorias();
    renderTabla();
    cerrarModal();
    Swal.fire('¡Guardado!', 'El insumo ha sido agregado correctamente.', 'success');
});

formEditarInsumo?.addEventListener("submit", (e) => {
    e.preventDefault();
    const index = Number(document.getElementById("editIndex").value);
    const nombre = document.getElementById("editNombre").value.trim();
    const categoria = document.getElementById("editCategoria").value.trim();
    const proveedor = editProveedorSelect.value;
    const cantidad = Number(document.getElementById("editCantidad").value);
    const unidad = document.getElementById("editUnidad").value.trim();
    const precioUnitario = Number(document.getElementById("editPrecioUnitario").value);
    const estado = document.getElementById("editEstado").value;

    const insumos = getInsumos();
    const actual = insumos[index];

    if (!actual) return;

    if (nombre.length < 2 || !categoria || !proveedor || !unidad || !Number.isFinite(cantidad) || cantidad < 1 || !Number.isFinite(precioUnitario) || precioUnitario < 0) {
        Swal.fire({ icon: 'warning', title: 'Revisa los datos', text: 'Asegúrate de completar todos los campos con valores válidos.', confirmButtonColor: '#27B7F5' });
        return;
    }

    if (insumos.some((item, i) => i !== index && item.nombre.toLowerCase() === nombre.toLowerCase() && item.categoria.toLowerCase() === categoria.toLowerCase())) {
        Swal.fire({ icon: 'error', title: 'Insumo duplicado', text: 'Ya existe otro insumo con el mismo nombre y categoría.', confirmButtonColor: '#27B7F5' });
        return;
    }

    insumos[index] = { nombre, categoria, proveedor, cantidad, unidad, precioUnitario, estado };
    saveInsumos(insumos);
    actualizarCategorias();
    renderTabla();
    cerrarEditModal();
    Swal.fire('¡Actualizado!', 'Los datos del insumo se han guardado.', 'success');
});

window.editarInsumo = (index) => {
    const insumos = getInsumos();
    const insumo = insumos[index];
    if (!insumo) return;

    document.getElementById("editIndex").value = index;
    document.getElementById("editNombre").value = insumo.nombre;
    document.getElementById("editCategoria").value = insumo.categoria;
    cargarProveedores(insumo.proveedor || "");
    document.getElementById("editCantidad").value = insumo.cantidad;
    document.getElementById("editUnidad").value = insumo.unidad;
    document.getElementById("editPrecioUnitario").value = insumo.precioUnitario;
    document.getElementById("editEstado").value = insumo.estado;

    modalEditarInsumo.style.display = "flex";
    document.getElementById("editNombre").focus();
};

window.eliminarInsumo = (index) => {
    Swal.fire({
        title: '¿Estás seguro?',
        text: "Esta acción eliminará el insumo.",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#e74c3c',
        cancelButtonColor: '#707070',
        confirmButtonText: 'Eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            const insumos = getInsumos();
            insumos.splice(index, 1);
            saveInsumos(insumos);
            actualizarCategorias();
            renderTabla();
            Swal.fire('¡Eliminado!', 'El insumo ha sido removido.', 'success');
        }
    });
};

cargarProveedores();
actualizarCategorias();
window.addEventListener("storage", (event) => {
    if (event.key === "marqueza_proveedores") cargarProveedores();
});
renderTabla();