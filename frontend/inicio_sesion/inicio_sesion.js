class LoginForm {
    constructor(formulario) {
        this.formulario = formulario;
        this.username = formulario.querySelector("#usuario");
        this.password = formulario.querySelector("#contraseña");
        this.passwordToggle = formulario.querySelector("#toggle-contrasena");
    }

    init() {
        this.formulario.addEventListener("submit", (event) => this.submit(event));
        this.passwordToggle?.addEventListener("click", () => this.togglePasswordVisibility());
    }

    togglePasswordVisibility() {
        const isPasswordHidden = this.password.type === "password";
        this.password.type = isPasswordHidden ? "text" : "password";
        this.passwordToggle.setAttribute("aria-label", isPasswordHidden ? "Ocultar contraseña" : "Mostrar contraseña");
        this.passwordToggle.setAttribute("aria-pressed", String(isPasswordHidden));
        this.passwordToggle.querySelector(".password-icon-show").hidden = !isPasswordHidden;
        this.passwordToggle.querySelector(".password-icon-hide").hidden = isPasswordHidden;
    }

    async submit(event) {
        event.preventDefault();
        const username = this.username?.value || "";
        const password = this.password?.value || "";

        if (!username.length || !password.length) {
            return Swal.fire({ icon: "warning", title: "Campos incompletos", text: "Por favor completa todos los campos." });
        }

        if (!await window.MarquezaAudit.reserveSession()) {
            window.MarquezaAudit.showActiveElsewhereAlert();
            return;
        }

        let user;
        try {
            const result = await window.MarquezaApi.request("/auth/login", {
                method: "POST",
                body: JSON.stringify({ usuario: username, contrasena: password })
            });
            user = result.usuario;
            if (!window.MarquezaAudit.activateSession(user.id)) {
                try {
                    await window.MarquezaApi.request("/auth/logout", {
                        method: "POST",
                        headers: { Authorization: `Bearer ${result.token}` },
                        suppressSessionRedirect: true
                    });
                } catch (error) {
                    await window.MarquezaApi.notifyError(error, "No se pudo cerrar la sesión duplicada");
                }
                window.MarquezaAudit.showActiveElsewhereAlert();
                return;
            }
            localStorage.setItem("marqueza_usuario_sesion", JSON.stringify({ ...user, token: result.token }));
            window.MarquezaAudit?.log({ action: "Inicio de sesión", module: "Acceso", detail: "Inicio de sesión autorizado.", actor: user.nombre, email: user.correo, role: user.rol });
        } catch (error) {
            window.MarquezaAudit.releaseSession({ pendingOnly: true });
            window.MarquezaAudit?.log({ action: "Inicio de sesión rechazado", module: "Acceso", entity: username, detail: error.message, outcome: "denied", actor: username });
            return window.MarquezaApi.notifyError(error, "No se pudo iniciar sesión");
        }
        window.location.replace("../inicio/inicio.html");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const formulario = document.getElementById("formulario");
    if (formulario) new LoginForm(formulario).init();
    if (new URLSearchParams(window.location.search).get("motivo") === "sesion_requerida") {
        window.Swal?.fire({ icon: "warning", title: "Inicia sesión", text: "Necesitas una sesión activa para entrar a esa sección." });
        window.history.replaceState({}, "", window.location.pathname);
    } else if (new URLSearchParams(window.location.search).get("motivo") === "usuario_activo_otra_pestana") {
        window.MarquezaAudit.showActiveElsewhereAlert();
        window.history.replaceState({}, "", window.location.pathname);
    } else if (new URLSearchParams(window.location.search).get("motivo") === "servidor_desconectado") {
        window.Swal?.fire({ icon: "warning", title: "Conexión perdida", text: "El servidor dejó de responder. Vuelve a iniciar sesión cuando esté disponible." });
        window.history.replaceState({}, "", window.location.pathname);
    }
});
