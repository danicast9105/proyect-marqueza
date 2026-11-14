const loginUrl = new URL("../inicio_sesion/inicio_sesion.html?motivo=servidor_desconectado", document.currentScript.src);
const expiredSessionUrl = new URL("../inicio_sesion/inicio_sesion.html?motivo=sesion_requerida", document.currentScript.src);

class MarquezaApi {
    static get baseUrl() {
        const hostname = window.location.hostname;
        const isDevTunnel = hostname.endsWith(".devtunnels.ms");
        const isLocal = hostname === "localhost" || hostname === "127.0.0.1";
        const apiHost = isDevTunnel
            ? `${window.location.protocol}//${hostname.replace(/-(5500|5000)(?=\.)/, "-5000")}`
            : isLocal
                ? `${window.location.protocol}//${hostname}:5000`
                : window.location.origin;
        const localApiUrl = `${apiHost}/api`;
        return (window.MARQUEZA_API_BASE_URL || localApiUrl).replace(/\/+$/, "");
    }

    static async request(path, options = {}) {
        const suppressSessionRedirect = options.suppressSessionRedirect === true;
        const requestOptions = { ...options };
        delete requestOptions.suppressSessionRedirect;
        const sessionToken = this.sessionToken();
        let response;
        try {
            response = await fetch(`${this.baseUrl}${path}`, {
                ...requestOptions,
                headers: {
                    ...(options.body ? { "Content-Type": "application/json" } : {}),
                    ...(sessionToken ? { Authorization: `Bearer ${sessionToken}` } : {}),
                    ...options.headers
                }
            });
        } catch {
            let session = null;
            try {
                session = JSON.parse(localStorage.getItem("marqueza_usuario_sesion") || "null");
            } catch {
                session = null;
            }
            const hasActiveSession = session?.id && sessionStorage.getItem("marqueza_sesion_activa") === String(session.id);
            const isLoginPage = window.location.pathname.endsWith("/inicio_sesion/inicio_sesion.html");
            if (hasActiveSession && !isLoginPage && !suppressSessionRedirect) {
                localStorage.removeItem("marqueza_usuario_sesion");
                sessionStorage.removeItem("marqueza_sesion_activa");
                window.MarquezaAudit?.releaseSession();
                window.location.replace(loginUrl);
            }
            throw new Error("No se pudo conectar con la API. Comprueba que el backend esté iniciado.");
        }

        const text = await response.text();
        let payload = null;
        if (text) {
            try {
                payload = JSON.parse(text);
            } catch {
                payload = { message: text };
            }
        }
        if (!response.ok) {
            const message = payload?.mensaje || payload?.message || `Error HTTP ${response.status}`;
            if (response.status === 401 && sessionToken && !path.startsWith("/auth/")) {
                localStorage.removeItem("marqueza_usuario_sesion");
                sessionStorage.removeItem("marqueza_sesion_activa");
                window.MarquezaAudit?.releaseSession();
                window.location.replace(expiredSessionUrl);
            }
            throw new Error(message);
        }
        return payload;
    }

    static sessionToken() {
        const storedSession = localStorage.getItem("marqueza_usuario_sesion");
        if (!storedSession) return null;

        let session;
        try {
            session = JSON.parse(storedSession);
        } catch (error) {
            console.error("No fue posible leer la sesión almacenada.", error);
            throw new Error("No fue posible leer la sesión almacenada. Cierra sesión y vuelve a ingresar.");
        }
        return typeof session?.token === "string" && session.token ? session.token : null;
    }

    static list(resource) {
        return this.request(`/${resource}/`);
    }

    static create(resource, record) {
        return this.request(`/${resource}/`, { method: "POST", body: JSON.stringify(record) });
    }

    static update(resource, id, record) {
        return this.request(`/${resource}/${encodeURIComponent(id)}`, {
            method: "PUT",
            body: JSON.stringify(record)
        });
    }

    static remove(resource, id) {
        return this.request(`/${resource}/${encodeURIComponent(id)}`, { method: "DELETE" });
    }

    static async load(resource, storageKey = `marqueza_${resource}`) {
        const pendingKey = `${storageKey}_pendientes_migracion`;
        let pending = this.cached(pendingKey);
        if (localStorage.getItem(pendingKey) === null) {
            pending = this.cached(storageKey)
                .filter(record => record.id === undefined || record.id === null)
                .map((record, index) => ({ ...record, __localKey: `${Date.now()}-${index}` }));
            if (pending.length) localStorage.setItem(pendingKey, JSON.stringify(pending));
        }
        const records = await this.list(resource);
        if (!Array.isArray(records)) throw new Error(`La respuesta de ${resource} no es una lista válida.`);
        const combined = [...records, ...pending];
        localStorage.setItem(storageKey, JSON.stringify(combined));
        return combined;
    }

    static consumeLegacy(storageKey, localKey) {
        if (!localKey) return;
        const pendingKey = `${storageKey}_pendientes_migracion`;
        const pending = this.cached(pendingKey).filter(record => record.__localKey !== localKey);
        localStorage.setItem(pendingKey, JSON.stringify(pending));
        localStorage.setItem(storageKey, JSON.stringify(this.cached(storageKey).filter(record => record.__localKey !== localKey)));
    }

    static cached(storageKey) {
        try {
            const records = JSON.parse(localStorage.getItem(storageKey) || "[]");
            return Array.isArray(records) ? records : [];
        } catch {
            return [];
        }
    }

    static notifyError(error, title = "No se pudo completar la operación") {
        const message = error instanceof Error ? error.message : String(error);
        if (window.Swal) {
            return window.Swal.fire({ icon: "error", title, text: message });
        }
        window.alert(`${title}: ${message}`);
        return Promise.resolve();
    }
}

window.MarquezaApi = MarquezaApi;
void window.MarquezaAudit?.syncPending?.();
