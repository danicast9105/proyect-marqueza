class ClientesPage extends MarquezaCrudPage {
    constructor() {
        super({
            storageKey: "marqueza_clientes",
            modalId: "modalCliente",
            formId: "formCliente",
            fields: ["nombre", "documento", "telefono", "correo"],
            columns: ["nombre", "documento", "telefono", "correo"]
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
        this.updateSummary(this.readRecords(), visible);
    }

    updateSummary(records, visibleRecords) {
        const setText = (id, value) => { const element = document.getElementById(id); if (element) element.textContent = value; };
        const emails = records.filter(record => String(record.correo || "").trim()).length;
        const phones = records.filter(record => String(record.telefono || "").trim()).length;
        const complete = records.filter(record => [record.nombre, record.documento, record.telefono, record.correo].every(value => String(value || "").trim())).length;
        setText("totalClientes", records.length);
        setText("correosClientes", emails);
        setText("telefonosClientes", phones);
        setText("coberturaClientes", `${records.length ? Math.round((complete / records.length) * 100) : 0}%`);
        setText("resultadosClientes", `${visibleRecords.length} ${visibleRecords.length === 1 ? "resultado" : "resultados"}`);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    new MarquezaAppShell().init();
    new ClientesPage().init();
});
