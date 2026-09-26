class MarquezaSidebar {
    constructor() {
        this.shell = new MarquezaAppShell();
    }

    init() {
        this.shell.init();
    }
}

document.addEventListener("DOMContentLoaded", () => {
    new MarquezaSidebar().init();
});
