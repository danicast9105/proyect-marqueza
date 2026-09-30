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
            ["../log_errores/registro_actividad.html", "bx-history", "Registro de actividad"]
        ];
    }

    init() {
        if (!this.menu) return;
        this.menu.replaceChildren(...this.items.map(([href, icon, label]) => this.createItem(href, icon, label)));
        const logout = this.root.querySelector('.boton-contenido a[href="#"]');
        if (logout) {
            logout.href = "../inicio_sesion/inicio_sesion.html";
            logout.setAttribute("aria-label", "Cerrar sesión");
            logout.addEventListener("click", () => {
                window.MarquezaAudit?.log({ action: "Cierre de sesión", module: "Acceso", detail: "El usuario cerró la sesión." });
                localStorage.removeItem("marqueza_usuario_sesion");
                sessionStorage.removeItem("marqueza_sesion_activa");
            });
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

const assistantScript = document.createElement("script");
assistantScript.src = new URL("asistente.js", document.currentScript.src).href;
document.head.appendChild(assistantScript);
