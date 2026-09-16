class MarquezaNavigation {
    constructor(root = document) {
        this.root = root;
        this.menu = root.querySelector(".links_menu");
        this.items = [
            ["../inicio/inicio.html", "bx-home-alt", "Inicio"],
            ["../ventas/ventas.html", "bx-task", "Ventas"],
            ["../productos/productos.html", "bxs-t-shirt", "Productos"],
            ["../ventas/ventas.html", "bx-money-withdraw", "Pedidos"],
            ["../cotizaciones/cotizaciones.html", "bx-link", "Cotizaciones"],
            ["../clientes/clientes.html", "bx-group", "Clientes"],
            ["../proveedores/proveedores.html", "bx-package", "Proveedores"],
            ["../usuarios/usuarios.html", "bx-user-circle", "Usuarios"],
            ["../ayuda/ayuda.html", "bx-help-circle", "Ayuda"]
        ];
    }

    init() {
        if (!this.menu) return;
        this.menu.replaceChildren(...this.items.map(([href, icon, label]) => this.createItem(href, icon, label)));
    }

    createItem(href, icon, label) {
        const item = document.createElement("li");
        item.className = "nav_links";
        const link = document.createElement("a");
        link.href = href;
        if (window.location.pathname.endsWith(href.split("/").pop())) {
            link.setAttribute("aria-current", "page");
        }

        const iconElement = document.createElement("i");
        iconElement.className = `bx ${icon} icon`;
        const text = document.createElement("span");
        text.className = "texto nav_texto";
        text.textContent = label;

        link.append(iconElement, text);
        item.appendChild(link);
        return item;
    }
}

new MarquezaNavigation().init();
