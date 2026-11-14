(function () {
    const EVENT_NAME = "marqueza:datos-actualizados";
    const PREFIX = "marqueza_";
    const IGNORED_KEYS = new Set([
        "marqueza_tema",
        "marqueza_usuario_sesion",
        "marqueza_bitacora",
        "marqueza_recuperacion"
    ]);

    function isDataKey(key) {
        return typeof key === "string" && key.startsWith(PREFIX) && !IGNORED_KEYS.has(key);
    }

    function publish(key, operation = "actualizado") {
        if (!isDataKey(key)) return;
        window.dispatchEvent(new CustomEvent(EVENT_NAME, { detail: { key, operation } }));
    }

    const originalSetItem = Storage.prototype.setItem;
    Storage.prototype.setItem = function (key, value) {
        const normalizedKey = String(key);
        const previousValue = this === window.localStorage ? this.getItem(normalizedKey) : null;
        originalSetItem.call(this, key, value);
        if (this === window.localStorage) {
            const nextValue = this.getItem(normalizedKey);
            if (previousValue !== nextValue) publish(normalizedKey, "actualizado");
        }
    };

    const originalRemoveItem = Storage.prototype.removeItem;
    Storage.prototype.removeItem = function (key) {
        const normalizedKey = String(key);
        const existed = this === window.localStorage && this.getItem(normalizedKey) !== null;
        originalRemoveItem.call(this, key);
        if (existed) publish(normalizedKey, "eliminado");
    };

    window.addEventListener("storage", (event) => {
        if (event.storageArea === window.localStorage) {
            publish(event.key, event.newValue === null ? "eliminado" : "actualizado");
        }
    });

    window.MarquezaRealtime = {
        subscribe(callback) {
            const listener = (event) => callback(event.detail);
            window.addEventListener(EVENT_NAME, listener);
            return () => window.removeEventListener(EVENT_NAME, listener);
        }
    };
})();