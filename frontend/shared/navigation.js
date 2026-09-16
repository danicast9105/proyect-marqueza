class MarquezaNavigation {
    constructor(root = document) {
        this.root = root;
        this.menu = root.querySelector(".links_menu");
        this.items = [
            ["../inicio/inicio.html", "bx-home-alt", "Inicio"],
            ["../insumos/insumos.html", "bx-task", "Insumos"],
            ["../productos/productos.html", "bxs-t-shirt", "Productos"],
            ["../ventas/ventas.html", "bx-money-withdraw", "Ventas"],
            ["../cotizaciones/cotizaciones.html", "bx-file", "Cotizaciones"],
            ["../clientes/clientes.html", "bx-group", "Clientes"],
            ["../proveedores/proveedores.html", "bx-package", "Proveedores"],
            ["../usuarios/usuarios.html", "bx-user-circle", "Usuarios"],
            ["../ayuda/ayuda.html", "bx-help-circle", "Ayuda"]
        ];
    }

    init() {
        if (!this.menu) return;
        this.menu.replaceChildren(...this.items.map(([href, icon, label]) => this.createItem(href, icon, label)));
        const logout = this.root.querySelector('.boton-contenido a[href="#"]');
        if (logout) {
            logout.href = "../incio%20sesion/inicio%20sesion.html";
            logout.setAttribute("aria-label", "Cerrar sesión");
        }
    }

    createItem(href, icon, label) {
        const item = document.createElement("li");
        item.className = "nav_links";
        const link = document.createElement("a");
        link.href = href;
        if (decodeURIComponent(window.location.pathname).endsWith(href.split("/").pop())) {
            link.setAttribute("aria-current", "page");
        }
        link.setAttribute("aria-label", label);

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
