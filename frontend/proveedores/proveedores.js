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
}

document.addEventListener("DOMContentLoaded", () => {
    new MarquezaAppShell().init();
    new ProveedoresPage().init();
});
