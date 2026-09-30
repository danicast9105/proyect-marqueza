(function () {
    const STORAGE_KEY = "marqueza_bitacora";
    const MAX_EVENTS = 500;

    function getSession() {
        try {
            const session = JSON.parse(localStorage.getItem("marqueza_usuario_sesion") || "null");
            return session && typeof session === "object" ? session : null;
        } catch {
            return null;
        }
    }

    function hasActiveSession() {
        const session = getSession();
        if (!session?.id) return false;
        try {
            return sessionStorage.getItem("marqueza_sesion_activa") === String(session.id);
        } catch {
            return false;
        }
    }

    function isPublicAccessPage() {
        const path = decodeURIComponent(window.location.pathname);
        return /\/(?:inicio_sesion\/inicio_sesion|olvido_contrasena\/(?:recuperar|restablecer))\.html$/.test(path);
    }

    function read() {
        try {
            const events = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
            return Array.isArray(events) ? events : [];
        } catch {
            return [];
        }
    }

    function log({ action, module = "Sistema", entity = "", detail = "", outcome = "success", actor, email, role }) {
        const session = getSession();
        const event = {
            id: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
            timestamp: new Date().toISOString(),
            actor: actor || session?.nombre || "Sin identificar",
            email: email ?? session?.correo ?? "",
            role: role ?? session?.rol ?? "",
            action,
            module,
            entity,
            detail,
            outcome
        };

        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify([event, ...read()].slice(0, MAX_EVENTS)));
        } catch (error) {
            console.error("No fue posible guardar el evento de auditoría.", error);
        }
        window.dispatchEvent(new CustomEvent("marqueza:audit", { detail: event }));
        return event;
    }

    function entityName(record) {
        if (!record || typeof record !== "object") return "Registro";
        const value = record.nombre || record.empresa || record.cliente || record.producto || record.codigo || record.documento || record.correo;
        return String(value || "Registro").slice(0, 120);
    }

    function recordChange(action, module, record) {
        const labels = { create: "Registro creado", update: "Registro actualizado", delete: "Registro eliminado" };
        const entity = entityName(record);
        return log({ action: labels[action] || action, module: moduleLabel(module), entity, detail: `${labels[action] || action}: ${entity}` });
    }

    function moduleLabel(module) {
        return String(module || "Sistema").replace(/^marqueza_/, "").replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
    }

    function guardPage() {
        if (isPublicAccessPage() || hasActiveSession()) return;
        const path = `${window.location.pathname}${window.location.search}`;
        log({ action: "Acceso denegado", module: "Acceso", entity: "Sesión requerida", detail: `Intento de acceso sin sesión a ${path}`, outcome: "denied" });
        window.location.replace("../inicio_sesion/inicio_sesion.html?motivo=sesion_requerida");
    }

    window.MarquezaAudit = { log, read, recordChange, guardPage };
    window.addEventListener("error", (event) => {
        const page = window.location.pathname.split("/").filter(Boolean).at(-2) || "Aplicación";
        log({ action: "Error de aplicación", module: moduleLabel(page), detail: String(event.message || "Error JavaScript").slice(0, 300), outcome: "error" });
    });
    window.addEventListener("unhandledrejection", (event) => {
        const reason = event.reason;
        const message = reason instanceof Error ? reason.message : String(reason || "Promesa rechazada");
        const page = window.location.pathname.split("/").filter(Boolean).at(-2) || "Aplicación";
        log({ action: "Error de aplicación", module: moduleLabel(page), detail: message.slice(0, 300), outcome: "error" });
    });
    guardPage();
})();