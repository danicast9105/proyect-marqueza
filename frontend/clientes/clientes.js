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
}

document.addEventListener("DOMContentLoaded", () => {
    new MarquezaAppShell().init();
    new ClientesPage().init();
});
