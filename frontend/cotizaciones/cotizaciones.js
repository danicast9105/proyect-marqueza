class CotizacionesPage {
    constructor() {
        this.storageKey = "marqueza_cotizaciones";
        this.body = document.getElementById("cotizacionesBody");
        this.emptyState = document.getElementById("emptyState");
        this.modal = document.getElementById("modalCotizacion");
        this.form = document.getElementById("formCotizacion");
        this.search = document.getElementById("buscarCotizacion");
        this.statusFilter = document.getElementById("filtroEstado");
        this.clientSelect = document.getElementById("quoteCliente");
    }

    init() {
        this.bindEvents();
        this.loadClients();
        this.setDefaultDate();
        this.updateDashboard();
        this.renderQuotes();
    }

    read(key, fallback = []) {
        try {
            const value = JSON.parse(localStorage.getItem(key) || "null");
            return Array.isArray(value) ? value : fallback;
        } catch {
            return fallback;
        }
    }

    readQuotes() { return this.read(this.storageKey); }

    saveQuotes(quotes) { localStorage.setItem(this.storageKey, JSON.stringify(quotes)); }

    money(value) {
        return Number(value || 0).toLocaleString("es-CO", { style: "currency", currency: "COP", maximumFractionDigits: 0 });
    }

    number(value) { return Number(value || 0).toLocaleString("es-CO"); }

    sum(records, selector) { return records.reduce((total, record) => total + selector(record), 0); }

    loadClients(selectedClient = "") {
        const clients = this.read("marqueza_clientes");
        this.clientSelect.replaceChildren(new Option("Selecciona un cliente", ""));
        clients.forEach(client => {
            const name = (client.nombre || "").trim();
            if (name) this.clientSelect.appendChild(new Option(name, name));
        });
        this.clientSelect.value = selectedClient;
    }

    updateDashboard() {
        const insumos = this.read("marqueza_insumos");
        const productos = this.read("marqueza_productos");
        const ventas = this.read("marqueza_ventas");
        const quotes = this.readQuotes();
        const gastos = this.sum(insumos, item => Number(item.cantidad) * Number(item.precioUnitario));
        const valorProductos = this.sum(productos, item => Number(item.cantidad) * Number(item.precio));
        const totalVentas = this.sum(ventas, item => Number(item.total));
        const unidadesCompradas = this.sum(insumos, item => Number(item.cantidad));
        const unidadesStock = this.sum(productos, item => Number(item.cantidad));
        const proyectado = this.sum(quotes.filter(item => item.estado !== "Rechazada"), item => Number(item.total));

        this.setText("totalGastos", this.money(gastos));
        this.setText("detalleInsumos", `${this.number(unidadesCompradas)} unidades compradas`);
        this.setText("valorProductos", this.money(valorProductos));
        this.setText("detalleProductos", `${this.number(productos.length)} productos registrados`);
        this.setText("totalVentas", this.money(totalVentas));
        this.setText("detalleVentas", `${this.number(ventas.length)} operaciones`);
        this.setText("totalCotizaciones", this.number(quotes.filter(item => item.estado !== "Rechazada").length));
        this.setText("detalleCotizaciones", `${this.money(proyectado)} proyectado`);
        this.setText("balanceCompras", this.number(unidadesCompradas));
        this.setText("balanceStock", this.number(unidadesStock));
        this.setText("balanceEmitidas", this.number(quotes.length));
        const balanceRatio = unidadesCompradas ? Math.min(100, Math.round((unidadesStock / unidadesCompradas) * 100)) : 0;
        document.getElementById("balanceBarFill").style.width = `${balanceRatio}%`;
        this.setText("balanceNota", quotes.length ? `El inventario representa el ${balanceRatio}% de las unidades compradas registradas.` : "Registra una cotización para comenzar el seguimiento comercial.");
    }

    setText(id, value) { const element = document.getElementById(id); if (element) element.textContent = value; }

    renderQuotes() {
        const query = (this.search.value || "").trim().toLowerCase();
        const status = this.statusFilter.value;
        const quotes = this.readQuotes().map((quote, index) => ({ ...quote, index })).filter(quote => {
            const text = `${quote.cliente} ${quote.producto} ${quote.notas}`.toLowerCase();
            return (!query || text.includes(query)) && (!status || quote.estado === status);
        });
        this.body.replaceChildren();
        this.emptyState.style.display = quotes.length ? "none" : "block";
        quotes.forEach(quote => {
            const row = document.createElement("tr");
            row.innerHTML = `<td>${quote.fecha}</td><td>${this.escape(quote.cliente)}</td><td>${this.escape(quote.producto)}</td><td>${this.number(quote.cantidad)}</td><td>${this.money(quote.total)}</td><td><span class="status">${quote.estado}</span></td><td><div class="row-actions"><button type="button" data-action="edit" data-index="${quote.index}" aria-label="Editar cotización"><i class="bx bx-edit"></i></button><button type="button" data-action="delete" data-index="${quote.index}" aria-label="Eliminar cotización"><i class="bx bx-trash"></i></button></div></td>`;
            this.body.appendChild(row);
        });
    }

    escape(value) { const element = document.createElement("span"); element.textContent = value || ""; return element.innerHTML; }

    openModal(index = -1) {
        const quote = index >= 0 ? this.readQuotes()[index] : null;
        document.getElementById("quoteIndex").value = index;
        document.getElementById("modalTitle").textContent = quote ? "Editar cotización" : "Nueva cotización";
        document.getElementById("quoteFecha").value = quote?.fecha || new Date().toISOString().slice(0, 10);
        this.loadClients(quote?.cliente || "");
        document.getElementById("quoteProducto").value = quote?.producto || "";
        document.getElementById("quoteCantidad").value = quote?.cantidad || "";
        document.getElementById("quotePrecio").value = quote?.precioUnitario || "";
        document.getElementById("quoteEstado").value = quote?.estado || "Pendiente";
        document.getElementById("quoteNotas").value = quote?.notas || "";
        this.modal.classList.add("active");
        this.modal.setAttribute("aria-hidden", "false");
        document.getElementById("quoteCliente").focus();
    }

    closeModal() { this.modal.classList.remove("active"); this.modal.setAttribute("aria-hidden", "true"); this.form.reset(); this.setDefaultDate(); }

    setDefaultDate() { document.getElementById("quoteFecha").value = new Date().toISOString().slice(0, 10); }

    submit(event) {
        event.preventDefault();
        const quantity = Number(document.getElementById("quoteCantidad").value);
        const unitPrice = Number(document.getElementById("quotePrecio").value);
        if (!Number.isFinite(quantity) || quantity < 1 || !Number.isFinite(unitPrice) || unitPrice < 0) return;
        const quote = { fecha: document.getElementById("quoteFecha").value, cliente: document.getElementById("quoteCliente").value.trim(), producto: document.getElementById("quoteProducto").value.trim(), cantidad: quantity, precioUnitario: unitPrice, total: quantity * unitPrice, estado: document.getElementById("quoteEstado").value, notas: document.getElementById("quoteNotas").value.trim() };
        const index = Number(document.getElementById("quoteIndex").value);
        const quotes = this.readQuotes();
        if (index >= 0) quotes[index] = quote; else quotes.unshift(quote);
        this.saveQuotes(quotes);
        this.closeModal();
        this.updateDashboard();
        this.renderQuotes();
    }

    bindEvents() {
        document.getElementById("btnNuevaCotizacion").addEventListener("click", () => this.openModal());
        document.getElementById("btnActualizar").addEventListener("click", () => this.updateDashboard());
        document.getElementById("btnCerrarModal").addEventListener("click", () => this.closeModal());
        document.getElementById("btnCancelar").addEventListener("click", () => this.closeModal());
        this.form.addEventListener("submit", event => this.submit(event));
        this.search.addEventListener("input", () => this.renderQuotes());
        this.statusFilter.addEventListener("change", () => this.renderQuotes());
        this.body.addEventListener("click", event => {
            const button = event.target.closest("button[data-action]");
            if (!button) return;
            const index = Number(button.dataset.index);
            if (button.dataset.action === "edit") this.openModal(index);
            if (button.dataset.action === "delete") { const quotes = this.readQuotes(); quotes.splice(index, 1); this.saveQuotes(quotes); this.updateDashboard(); this.renderQuotes(); }
        });
        this.modal.addEventListener("click", event => { if (event.target === this.modal) this.closeModal(); });
    }
}

document.addEventListener("DOMContentLoaded", () => {
    new CotizacionesPage().init();
});
