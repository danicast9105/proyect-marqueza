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
        this.itemsContainer = document.getElementById("quoteItems");
        this.products = [];
    }

    init() {
        this.bindEvents();
        this.loadClients();
        this.loadProducts();
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

    loadProducts() {
        this.products = this.read("marqueza_productos");
    }

    productOptions(selected = "") {
        const options = [new Option("Selecciona un producto", "")];
        this.products.forEach(product => {
            const value = String(product.nombre || product.codigo || "").trim();
            if (!value) return;
            const label = product.codigo ? `${product.codigo} - ${value}` : value;
            const option = new Option(label, value);
            option.dataset.price = String(Number(product.precio || 0));
            option.dataset.code = String(product.codigo || "");
            options.push(option);
        });
        options.forEach(option => { if (option.value === selected) option.selected = true; });
        return options;
    }

    addProductLine(item = {}) {
        const line = document.createElement("div");
        line.className = "product-line";
        const select = document.createElement("select");
        select.required = true;
        select.append(...this.productOptions(item.nombre));
        const quantity = document.createElement("input");
        quantity.type = "number"; quantity.min = "1"; quantity.value = item.cantidad || 1; quantity.required = true;
        const price = document.createElement("input");
        price.type = "number"; price.min = "0"; price.step = "0.01"; price.value = item.precio ?? ""; price.required = true;
        select.addEventListener("change", () => {
            const selected = select.selectedOptions[0];
            if (selected?.dataset.price !== undefined) price.value = selected.dataset.price;
            this.updateQuoteTotal();
        });
        quantity.addEventListener("input", () => this.updateQuoteTotal());
        price.addEventListener("input", () => this.updateQuoteTotal());
        const fields = [["Producto", select], ["Cantidad", quantity], ["Precio unitario", price]];
        fields.forEach(([label, control]) => { const wrapper = document.createElement("label"); wrapper.append(label, control); line.appendChild(wrapper); });
        const remove = document.createElement("button");
        remove.type = "button"; remove.className = "remove-product"; remove.title = "Quitar producto"; remove.setAttribute("aria-label", "Quitar producto"); remove.innerHTML = "<i class=\"bx bx-trash\"></i>";
        remove.addEventListener("click", () => { if (this.itemsContainer.children.length > 1) { line.remove(); this.updateQuoteTotal(); } });
        line.appendChild(remove);
        this.itemsContainer.appendChild(line);
        this.updateQuoteTotal();
    }

    updateQuoteTotal() {
        const total = [...this.itemsContainer.querySelectorAll(".product-line")].reduce((sum, line) => {
            return sum + Number(line.querySelectorAll("input")[0].value || 0) * Number(line.querySelectorAll("input")[1].value || 0);
        }, 0);
        document.getElementById("quoteTotal").textContent = `Total: ${this.money(total)}`;
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
            row.innerHTML = `<td>${quote.fecha}</td><td>${this.escape(quote.cliente)}</td><td>${this.escape(quote.producto)}</td><td>${this.number(quote.cantidad)}</td><td>${this.money(quote.total)}</td><td><span class="status">${quote.estado}</span></td><td><div class="row-actions"><button type="button" data-action="download" data-index="${quote.index}" aria-label="Descargar cotización en PDF" title="Descargar PDF"><i class="bx bx-download"></i></button><button type="button" data-action="edit" data-index="${quote.index}" aria-label="Editar cotización" title="Editar"><i class="bx bx-pencil"></i></button><button type="button" data-action="delete" data-index="${quote.index}" aria-label="Eliminar cotización" title="Eliminar"><i class="bx bx-trash-alt"></i></button></div></td>`;
            this.body.appendChild(row);
        });
    }

    escape(value) { const element = document.createElement("span"); element.textContent = value || ""; return element.innerHTML; }

    async loadLogoDataUrl() {
        const image = new Image();
        image.src = "../fondo/icono 3.png";
        await new Promise((resolve, reject) => { image.onload = resolve; image.onerror = reject; });
        const canvas = document.createElement("canvas");
        canvas.width = image.naturalWidth;
        canvas.height = image.naturalHeight;
        canvas.getContext("2d").drawImage(image, 0, 0);
        return canvas.toDataURL("image/png");
    }

    getQuoteItems(quote) {
        const source = Array.isArray(quote.productos) && quote.productos.length
            ? quote.productos
            : [{ nombre: quote.producto, cantidad: quote.cantidad, precio: quote.precioUnitario }];
        const grouped = new Map();
        source.forEach(item => {
            const name = String(item.nombre || "Producto").trim();
            const code = String(item.codigo || "").trim();
            const key = code || name.toLowerCase();
            const quantity = Number(item.cantidad || 0);
            const price = Number(item.precio || 0);
            const current = grouped.get(key) || { codigo: code, nombre: name, cantidad: 0, total: 0 };
            current.cantidad += quantity;
            current.total += quantity * price;
            grouped.set(key, current);
        });
        return [...grouped.values()].map(item => ({ ...item, precio: item.cantidad ? item.total / item.cantidad : 0 }));
    }

    async downloadPdf(index) {
        const quote = this.readQuotes()[index];
        const pdfConstructor = window.jspdf?.jsPDF;
        if (!quote || !pdfConstructor) {
            window.Swal?.fire({ icon: "error", title: "No se pudo generar el PDF", text: "Revisa tu conexión a Internet e inténtalo de nuevo." });
            return;
        }
        const doc = new pdfConstructor({ unit: "mm", format: "a4" });
        const margin = 18;
        const pageWidth = doc.internal.pageSize.getWidth();
        const pageHeight = doc.internal.pageSize.getHeight();
        const contentWidth = pageWidth - margin * 2;
        const colors = { navy: [18, 48, 74], teal: [39, 183, 245], ink: [38, 55, 70], muted: [96, 112, 124], pale: [242, 247, 249], line: [218, 226, 231] };
        const money = value => this.money(value);
        const safe = value => String(value || "No especificado");
        const quoteNumber = String(index + 1).padStart(4, "0");
        const items = this.getQuoteItems(quote);
        const logoDataUrl = await this.loadLogoDataUrl().catch(() => null);
        let y = 48;

        const footer = () => {
            doc.setDrawColor(...colors.line);
            doc.line(margin, pageHeight - 27, pageWidth - margin, pageHeight - 27);
            doc.setTextColor(...colors.muted);
            doc.setFont("helvetica", "normal");
            doc.setFontSize(7.5);
            const legal = "Este documento es una cotización informativa y no constituye factura, documento equivalente ni comprobante de venta. No es válido como documento de referencia legal, soporte fiscal o soporte contable, de acuerdo con la normativa colombiana vigente.";
            doc.text(doc.splitTextToSize(legal, contentWidth), margin, pageHeight - 21);
            doc.setFontSize(8);
            doc.text("MARQUEZA | Documento generado electrónicamente", margin, pageHeight - 8);
            doc.text(`Página ${doc.internal.getNumberOfPages()}`, pageWidth - margin, pageHeight - 8, { align: "right" });
        };

        const header = () => {
            doc.setFillColor(...colors.navy);
            doc.rect(0, 0, pageWidth, 35, "F");
            doc.setFillColor(...colors.teal);
            doc.rect(0, 35, pageWidth, 2, "F");
            if (logoDataUrl) doc.addImage(logoDataUrl, "PNG", margin, 6, 18, 24);
            doc.setTextColor(255, 255, 255);
            doc.setFont("helvetica", "bold");
            doc.setFontSize(21);
            doc.text("MARQUEZA", margin + 23, 16);
            doc.setFont("helvetica", "normal");
            doc.setFontSize(9);
            doc.text("CONFECCIONES QUE INSPIRAN", margin + 23, 24);
            doc.setFont("helvetica", "bold");
            doc.setFontSize(11);
            doc.text("COTIZACIÓN", pageWidth - margin, 14, { align: "right" });
            doc.setFont("helvetica", "normal");
            doc.setFontSize(9);
            doc.text(`#${quoteNumber}  |  ${safe(quote.fecha)}`, pageWidth - margin, 22, { align: "right" });
        };

        const ensureSpace = requiredHeight => {
            if (y + requiredHeight <= pageHeight - 36) return;
            footer();
            doc.addPage();
            header();
            y = 50;
        };

        const sectionTitle = title => {
            doc.setTextColor(...colors.navy);
            doc.setFont("helvetica", "bold");
            doc.setFontSize(10);
            doc.text(title.toUpperCase(), margin, y);
            doc.setDrawColor(...colors.teal);
            doc.setLineWidth(.7);
            doc.line(margin, y + 3, margin + 18, y + 3);
            y += 10;
        };

        header();
        doc.setTextColor(...colors.navy);
        doc.setFont("helvetica", "bold");
        doc.setFontSize(18);
        doc.text("Propuesta comercial", margin, y);
        y += 8;
        doc.setTextColor(...colors.muted);
        doc.setFont("helvetica", "normal");
        doc.setFontSize(10);
        const paragraph = `A continuación presentamos la cotización solicitada para ${safe(quote.cliente)}, con ${items.length} producto${items.length === 1 ? "" : "s"} seleccionado${items.length === 1 ? "" : "s"}. Esta propuesta resume las condiciones económicas registradas y sirve como base para la revisión y conversación comercial entre las partes.`;
        const paragraphLines = doc.splitTextToSize(paragraph, contentWidth);
        doc.text(paragraphLines, margin, y);
        y += paragraphLines.length * 5 + 12;

        sectionTitle("Información del cliente");
        ensureSpace(31);
        doc.setFillColor(...colors.pale);
        doc.roundedRect(margin, y, contentWidth, 25, 2, 2, "F");
        doc.setTextColor(...colors.muted);
        doc.setFontSize(8);
        doc.text("CLIENTE", margin + 7, y + 8);
        doc.text("FECHA DE EMISIÓN", pageWidth / 2 + 3, y + 8);
        doc.setTextColor(...colors.ink);
        doc.setFont("helvetica", "bold");
        doc.setFontSize(10);
        doc.text(safe(quote.cliente), margin + 7, y + 16);
        doc.text(safe(quote.fecha), pageWidth / 2 + 3, y + 16);
        y += 36;

        sectionTitle("Detalle de la propuesta");
        ensureSpace(39 + items.length * 18);
        const tableTop = y;
        doc.setFillColor(...colors.navy);
        doc.roundedRect(margin, tableTop, contentWidth, 10, 2, 2, "F");
        doc.setTextColor(255, 255, 255);
        doc.setFont("helvetica", "bold");
        doc.setFontSize(8);
        doc.text("CONCEPTO", margin + 6, tableTop + 6.5);
        doc.text("CANT.", pageWidth - 78, tableTop + 6.5, { align: "right" });
        doc.text("VALOR UNITARIO", pageWidth - 49, tableTop + 6.5, { align: "right" });
        doc.text("TOTAL", pageWidth - margin - 5, tableTop + 6.5, { align: "right" });
        let rowTop = tableTop + 10;
        items.forEach(item => {
            const rowHeight = 18;
            doc.setFillColor(255, 255, 255);
            doc.setDrawColor(...colors.line);
            doc.rect(margin, rowTop, contentWidth, rowHeight, "FD");
            doc.setTextColor(...colors.ink);
            doc.setFont("helvetica", "normal");
            doc.setFontSize(9);
            doc.text(doc.splitTextToSize(safe(item.nombre), 57), margin + 6, rowTop + 8);
            doc.text(this.number(item.cantidad), pageWidth - 78, rowTop + 11, { align: "right" });
            doc.text(money(item.precio), pageWidth - 49, rowTop + 11, { align: "right" });
            doc.setFont("helvetica", "bold");
            doc.text(money(item.total), pageWidth - margin - 5, rowTop + 11, { align: "right" });
            rowTop += rowHeight;
        });
        y = rowTop + 7;
        doc.setTextColor(...colors.muted);
        doc.setFont("helvetica", "normal");
        doc.setFontSize(8);
        doc.text(`Estado de la cotización: ${safe(quote.estado)}`, margin, y);
        doc.setFillColor(...colors.teal);
        doc.roundedRect(pageWidth - 74, y - 6, 56, 13, 2, 2, "F");
        doc.setTextColor(255, 255, 255);
        doc.setFont("helvetica", "bold");
        doc.setFontSize(8);
        doc.text(`TOTAL ${money(quote.total)}`, pageWidth - 46, y + 2, { align: "center" });
        y += 18;

        if (quote.notas) {
            const notesLines = doc.splitTextToSize(quote.notas, contentWidth - 12);
            ensureSpace(notesLines.length * 5 + 25);
            sectionTitle("Observaciones");
            doc.setFillColor(...colors.pale);
            doc.roundedRect(margin, y, contentWidth, notesLines.length * 5 + 10, 2, 2, "F");
            doc.setTextColor(...colors.muted);
            doc.setFont("helvetica", "normal");
            doc.setFontSize(9);
            doc.text(notesLines, margin + 6, y + 7);
            y += notesLines.length * 5 + 20;
        }

        ensureSpace(24);
        doc.setTextColor(...colors.navy);
        doc.setFont("helvetica", "bold");
        doc.setFontSize(10);
        doc.text("Gracias por considerar a MARQUEZA", margin, y);
        doc.setTextColor(...colors.muted);
        doc.setFont("helvetica", "normal");
        doc.setFontSize(8.5);
        doc.text("Quedamos atentos para ampliar la información de esta propuesta.", margin, y + 7);
        footer();
        doc.save(`cotizacion-marqueza-${safe(quote.fecha)}-${index + 1}.pdf`);
    }

    openModal(index = -1) {
        const quote = index >= 0 ? this.readQuotes()[index] : null;
        document.getElementById("quoteIndex").value = index;
        document.getElementById("modalTitle").textContent = quote ? "Editar cotización" : "Nueva cotización";
        document.getElementById("quoteFecha").value = quote?.fecha || new Date().toISOString().slice(0, 10);
        this.loadClients(quote?.cliente || "");
        this.itemsContainer.replaceChildren();
        const items = quote?.productos?.length ? quote.productos : [{ nombre: quote?.producto || "", cantidad: quote?.cantidad || 1, precio: quote?.precioUnitario || "" }];
        items.forEach(item => this.addProductLine(item));
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
        const products = [...this.itemsContainer.querySelectorAll(".product-line")].map(line => {
            const select = line.querySelector("select");
            const inputs = line.querySelectorAll("input");
            return { codigo: select.selectedOptions[0]?.dataset.code || "", nombre: select.value, cantidad: Number(inputs[0].value), precio: Number(inputs[1].value) };
        });
        if (!products.length || products.some(item => !item.nombre || !Number.isFinite(item.cantidad) || item.cantidad < 1 || !Number.isFinite(item.precio) || item.precio < 0)) {
            window.Swal?.fire({ icon: "warning", title: "Datos inválidos", text: "Selecciona productos e ingresa cantidades y precios válidos." });
            return;
        }
        const quote = { fecha: document.getElementById("quoteFecha").value, cliente: document.getElementById("quoteCliente").value.trim(), producto: products.map(item => item.nombre).join(", "), cantidad: products.reduce((sum, item) => sum + item.cantidad, 0), precioUnitario: products[0].precio, total: products.reduce((sum, item) => sum + item.cantidad * item.precio, 0), productos: products, estado: document.getElementById("quoteEstado").value, notas: document.getElementById("quoteNotas").value.trim() };
        const index = Number(document.getElementById("quoteIndex").value);
        const quotes = this.readQuotes();
        if (index >= 0) quotes[index] = quote; else quotes.unshift(quote);
        window.MarquezaAudit?.recordChange(index >= 0 ? "update" : "create", this.storageKey, quote);
        this.saveQuotes(quotes);
        this.closeModal();
        this.updateDashboard();
        this.renderQuotes();
        window.Swal?.fire({ icon: "success", title: index >= 0 ? "Cotización actualizada" : "Cotización guardada", text: "La información se guardó correctamente.", timer: 1600, showConfirmButton: false });
    }

    bindEvents() {
        document.getElementById("btnNuevaCotizacion").addEventListener("click", () => this.openModal());
        document.getElementById("btnActualizar").addEventListener("click", () => this.updateDashboard());
        document.getElementById("btnCerrarModal").addEventListener("click", () => this.closeModal());
        document.getElementById("btnCancelar").addEventListener("click", () => this.closeModal());
        this.form.addEventListener("submit", event => this.submit(event));
        this.search.addEventListener("input", () => this.renderQuotes());
        this.statusFilter.addEventListener("change", () => this.renderQuotes());
        document.getElementById("btnAgregarProducto").addEventListener("click", () => this.addProductLine());
        this.body.addEventListener("click", event => {
            const button = event.target.closest("button[data-action]");
            if (!button) return;
            const index = Number(button.dataset.index);
            if (button.dataset.action === "download") { this.downloadPdf(index); return; }
            if (button.dataset.action === "edit") this.openModal(index);
            if (button.dataset.action === "delete") {
                const removeQuote = () => { const quotes = this.readQuotes(); const [quote] = quotes.splice(index, 1); window.MarquezaAudit?.recordChange("delete", this.storageKey, quote); this.saveQuotes(quotes); this.updateDashboard(); this.renderQuotes(); window.Swal?.fire({ icon: "success", title: "Cotización eliminada", text: "La cotización se eliminó correctamente.", timer: 1600, showConfirmButton: false }); };
                if (window.Swal) window.Swal.fire({ icon: "warning", title: "¿Eliminar cotización?", text: "Esta acción no se puede deshacer.", showCancelButton: true, confirmButtonText: "Eliminar", cancelButtonText: "Cancelar", confirmButtonColor: "#d4554d" }).then(result => { if (result.isConfirmed) removeQuote(); });
            }
        });
        this.modal.addEventListener("click", event => { if (event.target === this.modal) this.closeModal(); });
        window.MarquezaRealtime?.subscribe(({ key }) => {
            if (key === "marqueza_productos") {
                this.loadProducts();
                this.itemsContainer.querySelectorAll(".product-line select").forEach(select => {
                    const selected = select.value;
                    select.replaceChildren(...this.productOptions(selected));
                });
            }
            if (key === "marqueza_clientes") this.loadClients(this.clientSelect.value);
            if (key === this.storageKey) { this.updateDashboard(); this.renderQuotes(); }
        });
    }
}

document.addEventListener("DOMContentLoaded", () => {
    new CotizacionesPage().init();
});
