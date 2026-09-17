class ProveedoresPage extends MarquezaCrudPage {
    constructor() {
        super({
            storageKey: "marqueza_proveedores",
            modalId: "modalProveedor",
            formId: "formProveedor",
            fields: ["empresa", "contacto", "telefono", "correo", "direccion"],
            columns: ["empresa", "contacto", "telefono", "correo", "direccion"]
        });
    }

    init() {
        super.init();
        this.updateSummary(this.readRecords(), this.readRecords());
    }

    render(query = "") {
        super.render(query);
        const normalizedQuery = query.trim().toLowerCase();
        const visible = this.readRecords().filter(record => !normalizedQuery || JSON.stringify(record).toLowerCase().includes(normalizedQuery));
        const emptyState = document.querySelector(".empty-state");
        if (emptyState) emptyState.style.display = visible.length ? "none" : "block";
        this.updateSummary(this.readRecords(), visible);
    }

    updateSummary(records, visibleRecords) {
        const setText = (id, value) => {
            const element = document.getElementById(id);
            if (element) element.textContent = value;
        };
        const contacts = records.filter(record => String(record.contacto || "").trim()).length;
        const phones = records.filter(record => String(record.telefono || "").trim()).length;
        const complete = records.filter(record => this.fields.every(field => String(record[field] || "").trim())).length;
        setText("totalProveedores", records.length);
        setText("contactosProveedores", contacts);
        setText("telefonosProveedores", phones);
        setText("fichasProveedores", `${records.length ? Math.round((complete / records.length) * 100) : 0}%`);
        setText("resultadosProveedores", `${visibleRecords.length} ${visibleRecords.length === 1 ? "resultado" : "resultados"}`);
    }

    openModal(index = -1) {
        super.openModal(index);
        const title = document.getElementById("modalProveedorTitle");
        if (title) title.textContent = index >= 0 ? "Editar proveedor" : "Nuevo proveedor";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    new MarquezaAppShell().init();
    new ProveedoresPage().init();
});
