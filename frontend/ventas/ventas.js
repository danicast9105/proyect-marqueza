class VentasPage extends MarquezaCrudPage {
    constructor() {
        super({
            storageKey: "marqueza_ventas",
            modalId: "modalVenta",
            formId: "formVenta",
            fields: ["fecha", "cliente", "producto", "cantidad", "total"],
            columns: ["fecha", "cliente", "producto", "cantidad", "total"]
        });
    }
}

document.addEventListener("DOMContentLoaded", () => {
    new MarquezaAppShell().init();
    new VentasPage().init();
});
