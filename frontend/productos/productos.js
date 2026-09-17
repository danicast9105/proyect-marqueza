/* ============================================================
   productos.js — MARQUEZA
   Gestión de Productos:
   - Menú lateral / responsive igual a Gestión de Insumos.
   - Buscar
   - Agregar / editar / eliminar
   - Filtros
   - Exportar PDF
   ============================================================ */

const body = document.querySelector("body");
const sidebar = body?.querySelector(".barra_lateral");
const toggle = body?.querySelector(".toggle");
const hamburger = document.getElementById("hamburger");
const modeSwitch = body?.querySelector(".toggle_switch");
const modeText = body?.querySelector(".modo_texto");

const searchInput = document.getElementById("searchInput") ||
    document.querySelector(".cont_busqueda input");
const searchButton = document.getElementById("btnBuscar");
const btnExportPdf = document.getElementById("btnExportPdf");
const btnAgregar = document.querySelector(".agregar");

const filtroCategoria = document.getElementById("filtroCategoria");
const estadoButtons = Array.from(document.querySelectorAll(".estado-btn"));

const tbody = document.querySelector(".cont_tabla tbody");
const modal = document.getElementById("modalProducto");
const form = document.getElementById("formProducto");
const btnCerrar = document.getElementById("cerrarModal");
const btnCancelar = document.getElementById("btnCancelar");

const STORAGE_KEY = "marqueza_productos";
let editIndex = -1;

const getProductos = () => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
        try {
            const parsed = JSON.parse(stored);
            return Array.isArray(parsed) ? parsed : [];
        } catch (error) {
            console.error("No se pudo leer los productos:", error);
        }
    }

    const iniciales = [
        { codigo: "P001", nombre: "Camiseta básica", cantidad: 20, precio: 35000, estado: "Activo", categoria: "Camisetas" },
        { codigo: "P002", nombre: "Pantalón jean", cantidad: 8, precio: 85000, estado: "Activo", categoria: "Pantalones" }
    ];
    localStorage.setItem(STORAGE_KEY, JSON.stringify(iniciales));
    return iniciales;
};

const saveProductos = (productos) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(productos));
};

const formatNumber = (value) =>
    Number(value || 0).toLocaleString("es-CO", {
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    });

const getEstadoPorCantidad = (cantidad) => {
    const n = Number(cantidad);
    if (!Number.isFinite(n) || n <= 5) {
        return { label: "Bajo", clase: "estado-rojo" };
    }
    if (n <= 20) {
        return { label: "Medio", clase: "estado-amarillo" };
    }
    return { label: "Bueno", clase: "estado-verde" };
};

const formatMoney = value => Number(value || 0).toLocaleString("es-CO", {
    style: "currency",
    currency: "COP",
    maximumFractionDigits: 0
});

const updateSummary = (records = getProductos(), visibleRecords = records) => {
    const lowStock = records.filter(item => getEstadoPorCantidad(item.cantidad).label === "Bajo").length;
    const units = records.reduce((total, item) => total + Number(item.cantidad || 0), 0);
    const catalogValue = records.reduce((total, item) => total + Number(item.cantidad || 0) * Number(item.precio || 0), 0);
    const setText = (id, value) => { const element = document.getElementById(id); if (element) element.textContent = value; };
    setText("totalProductos", records.length);
    setText("productosBajos", lowStock);
    setText("unidadesProductos", formatNumber(units));
    setText("valorProductos", formatMoney(catalogValue));
    setText("resultadosProductos", `${visibleRecords.length} ${visibleRecords.length === 1 ? "resultado" : "resultados"}`);
};

const getFilteredProductos = () => {
    const query = (searchInput?.value || "").trim().toLowerCase();
    const categoria = filtroCategoria?.value || "";
    const estadoSeleccionado =
        estadoButtons.find(btn => btn.classList.contains("active"))?.dataset.status || "Todos";

    return getProductos()
        .map((item, index) => ({ ...item, originalIndex: index }))
        .filter(item => {
            const estadoVisual = getEstadoPorCantidad(item.cantidad).label;
            const texto = [
                item.codigo,
                item.nombre,
                item.cantidad,
                item.precio,
                item.estado,
                item.categoria,
                estadoVisual
            ].join(" ").toLowerCase();

            const coincideBusqueda = !query || texto.includes(query);
            const coincideCategoria = !categoria || item.categoria === categoria;
            const coincideEstado =
                estadoSeleccionado === "Todos" ||
                estadoVisual.toLowerCase() === estadoSeleccionado.toLowerCase();

            return coincideBusqueda && coincideCategoria && coincideEstado;
        });
};

const actualizarCategorias = () => {
    if (!filtroCategoria) return;

    const categorias = [...new Set(
        getProductos().map(item => item.categoria).filter(Boolean)
    )].sort((a, b) => a.localeCompare(b));

    const actual = filtroCategoria.value;
    filtroCategoria.innerHTML =
        '<option value="">Todas</option>' +
        categorias.map(categoria =>
            `<option value="${categoria}" ${categoria === actual ? "selected" : ""}>${categoria}</option>`
        ).join("");
};

const renderTabla = () => {
    if (!tbody) return;

    const productos = getFilteredProductos();
    updateSummary(getProductos(), productos);
    tbody.innerHTML = "";

    if (!productos.length) {
        tbody.innerHTML = '<tr><td colspan="7" class="sin-resultados"><i class="bx bx-search-alt-2"></i><strong>No encontramos productos</strong><span>Prueba con otra búsqueda o cambia los filtros.</span></td></tr>';
        return;
    }

    productos.forEach(producto => {
        const estadoVisual = getEstadoPorCantidad(producto.cantidad);
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td data-label="Código">${producto.codigo || ""}</td>
            <td data-label="Nombre">${producto.nombre || ""}</td>
            <td data-label="Cantidad">${producto.cantidad ?? ""}</td>
            <td data-label="Precio">${formatNumber(producto.precio)}</td>
            <td data-label="Estado">
                <span class="estado-badge ${estadoVisual.clase}">
                    ${estadoVisual.label}
                </span>
            </td>
            <td data-label="Editar">
                <button type="button" class="btn-editar" data-index="${producto.originalIndex}" title="Editar" aria-label="Editar">
                    <i class="bx bx-pencil" aria-hidden="true"></i>
                </button>
            </td>
            <td data-label="Eliminar">
                <button type="button" class="btn-eliminar" data-index="${producto.originalIndex}" title="Eliminar" aria-label="Eliminar">
                    <i class="bx bx-trash-alt" aria-hidden="true"></i>
                </button>
            </td>
        `;

        tbody.appendChild(tr);
    });
};

const abrirModal = (index = -1) => {
    if (!modal || !form) return;

    editIndex = index;
    form.reset();

    const titulo = modal.querySelector("h2");

    if (index >= 0) {
        const producto = getProductos()[index];
        if (!producto) return;

        if (titulo) titulo.textContent = "Editar Producto";

        document.getElementById("codigo").value = producto.codigo || "";
        document.getElementById("nombre").value = producto.nombre || "";
        document.getElementById("cantidad").value = producto.cantidad ?? "";
        document.getElementById("precio").value = producto.precio ?? "";
        document.getElementById("estado").value = producto.estado || "";
    } else {
        if (titulo) titulo.textContent = "Agregar Producto";
    }

    modal.classList.add("active");
    modal.style.display = "flex";
    document.getElementById("codigo")?.focus();
};

const cerrarModal = () => {
    if (!modal) return;
    modal.classList.remove("active");
    modal.style.display = "none";
    form?.reset();
    editIndex = -1;

    const titulo = modal.querySelector("h2");
    if (titulo) titulo.textContent = "Agregar Producto";
};

const exportToPDF = () => {
    if (!window.jspdf?.jsPDF) {
        window.Swal?.fire({ icon: "error", title: "No se pudo exportar", text: "Revisa tu conexión a Internet e inténtalo de nuevo." });
        return;
    }

    const { jsPDF } = window.jspdf;
    const doc = new jsPDF({ orientation: "landscape" });
    const productos = getFilteredProductos();

    const rows = productos.map(item => [
        item.codigo || "",
        item.nombre || "",
        item.cantidad ?? "",
        formatNumber(item.precio),
        getEstadoPorCantidad(item.cantidad).label
    ]);

    doc.setFontSize(16);
    doc.text("Listado de Productos - MARQUEZA", 14, 16);

    doc.setFontSize(9);
    doc.text(`Registros: ${productos.length}`, 14, 22);

    if (typeof doc.autoTable === "function") {
        doc.autoTable({
            startY: 28,
            head: [["Código", "Nombre", "Cantidad", "Precio", "Estado"]],
            body: rows,
            theme: "striped",
            headStyles: { fillColor: [39, 183, 245], textColor: 255 },
            styles: { fontSize: 9, cellPadding: 4 }
        });
    } else {
        let y = 32;
        doc.setFontSize(10);
        rows.forEach(row => {
            doc.text(row.join(" | "), 14, y);
            y += 7;
            if (y > 190) {
                doc.addPage();
                y = 20;
            }
        });
    }

    doc.save("productos-marqueza.pdf");
    window.Swal?.fire({ icon: "success", title: "Exportación lista", text: "El listado de productos se descargó correctamente.", timer: 1600, showConfirmButton: false });
};

form?.addEventListener("submit", event => {
    event.preventDefault();

    const codigo = document.getElementById("codigo").value.trim();
    const nombre = document.getElementById("nombre").value.trim();
    const cantidad = Number(document.getElementById("cantidad").value);
    const precio = Number(document.getElementById("precio").value);
    const estado = document.getElementById("estado").value.trim();

    if (!codigo || !nombre || !Number.isFinite(cantidad) || cantidad < 0 ||
        !Number.isFinite(precio) || precio < 0 || !estado) {
        window.Swal?.fire({ icon: "warning", title: "Datos incompletos", text: "Completa todos los campos con valores válidos." });
        return;
    }

    const productos = getProductos();
    const producto = {
        codigo,
        nombre,
        cantidad,
        precio,
        estado,
        categoria: "General"
    };

    const editing = editIndex >= 0;
    if (editing) {
        producto.categoria = productos[editIndex]?.categoria || "General";
        productos[editIndex] = producto;
    } else {
        productos.push(producto);
    }

    saveProductos(productos);
    actualizarCategorias();
    renderTabla();
    cerrarModal();
    window.Swal?.fire({ icon: "success", title: editing ? "Producto actualizado" : "Producto guardado", text: "La información se guardó correctamente.", timer: 1600, showConfirmButton: false });
});

tbody?.addEventListener("click", event => {
    const button = event.target.closest("button[data-index]");
    if (!button) return;

    const index = Number(button.dataset.index);
    const productos = getProductos();

    if (button.classList.contains("btn-editar")) {
        abrirModal(index);
        return;
    }

    if (button.classList.contains("btn-eliminar")) {
        const removeProduct = () => {
            productos.splice(index, 1);
            saveProductos(productos);
            actualizarCategorias();
            renderTabla();
            window.Swal?.fire({ icon: "success", title: "Producto eliminado", text: "El producto se eliminó correctamente.", timer: 1600, showConfirmButton: false });
        };
        if (!window.Swal) return;
        window.Swal.fire({ icon: "warning", title: "¿Eliminar producto?", text: "Esta acción no se puede deshacer.", showCancelButton: true, confirmButtonText: "Eliminar", cancelButtonText: "Cancelar", confirmButtonColor: "#d4554d" }).then(result => { if (result.isConfirmed) removeProduct(); });
    }
});

searchButton?.addEventListener("click", renderTabla);
searchInput?.addEventListener("input", renderTabla);
searchInput?.addEventListener("keydown", event => {
    if (event.key === "Enter") {
        event.preventDefault();
        renderTabla();
    }
});

filtroCategoria?.addEventListener("change", renderTabla);

estadoButtons.forEach(button => {
    button.addEventListener("click", () => {
        estadoButtons.forEach(btn => btn.classList.remove("active"));
        button.classList.add("active");
        renderTabla();
    });
});

btnExportPdf?.addEventListener("click", exportToPDF);
btnAgregar?.addEventListener("click", () => abrirModal());
btnCerrar?.addEventListener("click", cerrarModal);
btnCancelar?.addEventListener("click", cerrarModal);

window.addEventListener("click", event => {
    if (event.target === modal) cerrarModal();
});

/* ============================================================
   MENÚ LATERAL — MISMA LÓGICA DE GESTIÓN DE INSUMOS
   ============================================================ */

const isTopbar = () => window.innerWidth <= 1024;

function updateLayout() {
    if (!body || !sidebar) return;

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

modeSwitch?.addEventListener("click", () => {
    body.classList.toggle("dark");
    if (modeText) {
        modeText.innerText = body.classList.contains("dark") ? "Claro" : "Oscuro";
    }
});

toggle?.addEventListener("click", () => {
    if (isTopbar()) return;

    sidebar.classList.toggle("close");
    updateLayout();
});

function toggleMobileMenu() {
    if (!sidebar) return;

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

hamburger?.addEventListener("click", toggleMobileMenu);

hamburger?.addEventListener("keydown", event => {
    if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        toggleMobileMenu();
    }
});

sidebar?.querySelectorAll(".nav_links a").forEach(link => {
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
        if (!isTopbar() && sidebar) {
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

sidebar?.addEventListener("mousedown", event => {
    if (isTopbar()) return;
    if (event.target.closest(".toggle")) return;

    if (event.target.closest("header")) {
        isDragging = true;
        dragStartX = event.clientX;
        sidebarStartLeft = sidebar.getBoundingClientRect().left;
        sidebar.classList.add("dragging");
    }
});

document.addEventListener("mousemove", event => {
    if (!isDragging || !sidebar) return;

    const deltaX = event.clientX - dragStartX;
    let nextLeft = sidebarStartLeft + deltaX;

    const sidebarWidth = sidebar.offsetWidth;
    const minLeft = -sidebarWidth + 40;
    const maxLeft = 0;

    nextLeft = Math.max(minLeft, Math.min(maxLeft, nextLeft));
    sidebar.style.left = `${nextLeft}px`;
});

document.addEventListener("mouseup", () => {
    if (!isDragging || !sidebar) return;

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

sidebar?.addEventListener("mouseleave", () => {
    if (isDragging) {
        isDragging = false;
        sidebar.classList.remove("dragging");
        sidebar.style.left = "0";
        updateLayout();
    }
});

updateLayout();
actualizarCategorias();
renderTabla();
