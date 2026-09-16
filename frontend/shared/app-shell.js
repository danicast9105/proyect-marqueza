/**
 * Componentes compartidos de la interfaz MARQUEZA.
 * La clase evita duplicar la lógica de tema y navegación en cada pantalla.
 */
class MarquezaStorage {
    constructor(namespace = "marqueza") {
        this.namespace = namespace;
    }

    get(key, fallback = null) {
        const value = localStorage.getItem(`${this.namespace}_${key}`);
        return value === null ? fallback : value;
    }

    set(key, value) {
        localStorage.setItem(`${this.namespace}_${key}`, value);
    }
}

class MarquezaAppShell {
    constructor(root = document) {
        this.body = root.body;
        this.sidebar = root.querySelector(".barra_lateral");
        this.toggle = root.querySelector(".toggle");
        this.hamburger = root.getElementById("hamburger");
        this.modeSwitch = root.querySelector(".toggle_switch");
        this.modeText = root.querySelector(".modo_texto");
        this.storage = new MarquezaStorage();
        this.resizeTimer = null;
    }

    init() {
        if (!this.body || !this.sidebar) return;
        this.restoreTheme();
        this.bindEvents();
        this.updateLayout();
    }

    isTopbar() {
        return window.innerWidth <= 1024;
    }

    restoreTheme() {
        const isDark = this.storage.get("tema") === "oscuro";
        this.body.classList.toggle("dark", isDark);
        this.updateModeText();
    }

    toggleTheme() {
        const isDark = this.body.classList.toggle("dark");
        this.storage.set("tema", isDark ? "oscuro" : "claro");
        this.updateModeText();
    }

    updateModeText() {
        if (this.modeText) {
            this.modeText.textContent = this.body.classList.contains("dark") ? "Claro" : "Oscuro";
        }
    }

    toggleMobileMenu() {
        const isOpen = this.sidebar.classList.toggle("open");
        this.sidebar.classList.toggle("close", !isOpen);
        this.updateLayout();
    }

    updateLayout() {
        if (this.isTopbar()) {
            this.body.style.paddingLeft = "0";
            this.body.style.paddingTop = `${this.sidebar.getBoundingClientRect().height}px`;
            return;
        }

        this.body.style.paddingTop = "0";
        this.body.style.paddingLeft = this.sidebar.classList.contains("close") ? "88px" : "250px";
    }

    bindEvents() {
        this.modeSwitch?.addEventListener("click", () => this.toggleTheme());
        this.toggle?.addEventListener("click", () => {
            if (this.isTopbar()) return;
            this.sidebar.classList.toggle("close");
            this.updateLayout();
        });
        this.hamburger?.addEventListener("click", () => this.toggleMobileMenu());
        this.hamburger?.addEventListener("keydown", (event) => {
            if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                this.toggleMobileMenu();
            }
        });
        this.sidebar.querySelectorAll(".nav_links a").forEach((link) => {
            link.addEventListener("click", () => {
                if (this.isTopbar() && this.sidebar.classList.contains("open")) {
                    this.toggleMobileMenu();
                }
            });
        });
        window.addEventListener("resize", () => {
            clearTimeout(this.resizeTimer);
            this.resizeTimer = setTimeout(() => this.updateLayout(), 100);
        });
    }
}

window.MarquezaAppShell = MarquezaAppShell;
window.MarquezaStorage = MarquezaStorage;
