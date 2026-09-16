class MarquezaThemePersistence {
    constructor() {
        this.storageKey = "marqueza_tema";
        this.body = document.body;
        this.modeText = document.querySelector(".modo_texto");
    }

    init() {
        this.restore();
        document.addEventListener("click", (event) => {
            if (!event.target.closest(".toggle_switch")) return;
            window.setTimeout(() => this.persist(), 0);
        });
    }

    restore() {
        const isDark = localStorage.getItem(this.storageKey) === "oscuro";
        this.body.classList.toggle("dark", isDark);
        this.updateLabel();
    }

    persist() {
        localStorage.setItem(this.storageKey, this.body.classList.contains("dark") ? "oscuro" : "claro");
        this.updateLabel();
    }

    updateLabel() {
        if (this.modeText) {
            this.modeText.textContent = this.body.classList.contains("dark") ? "Claro" : "Oscuro";
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    new MarquezaThemePersistence().init();
});
