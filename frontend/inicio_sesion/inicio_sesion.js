class LoginForm {
    constructor(formulario) {
        this.formulario = formulario;
        this.username = formulario.querySelector("#usuario");
        this.password = formulario.querySelector("#contraseña");
    }

    init() {
        this.formulario.addEventListener("submit", (event) => this.submit(event));
    }

    async submit(event) {
        event.preventDefault();
        const username = this.username?.value.trim() || "";
        const password = this.password?.value || "";

        if (!username || !password) {
            return Swal.fire({ icon: "warning", title: "Campos incompletos", text: "Por favor completa todos los campos." });
        }

        let user;
        try {
            const result = await window.MarquezaApi.request("/auth/login", {
                method: "POST",
                body: JSON.stringify({ usuario: username, contrasena: password })
            });
            user = result.usuario;
            localStorage.setItem("marqueza_usuario_sesion", JSON.stringify({ ...user, token: result.token }));
            sessionStorage.setItem("marqueza_sesion_activa", String(user.id));
            window.MarquezaAudit?.log({ action: "Inicio de sesión", module: "Acceso", detail: "Inicio de sesión autorizado.", actor: user.nombre, email: user.correo, role: user.rol });
        } catch (error) {
            window.MarquezaAudit?.log({ action: "Inicio de sesión rechazado", module: "Acceso", entity: username, detail: error.message, outcome: "denied", actor: username });
            return window.MarquezaApi.notifyError(error, "No se pudo iniciar sesión");
        }
        Swal.fire({
            title: "Inicio de sesión exitoso",
            icon: "success",
            text: `Bienvenido ${user.nombre}`
        }).then(() => {
            window.location.href = "../inicio/inicio.html";
        });
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const formulario = document.getElementById("formulario");
    if (formulario) new LoginForm(formulario).init();
    if (new URLSearchParams(window.location.search).get("motivo") === "sesion_requerida") {
        window.Swal?.fire({ icon: "warning", title: "Inicia sesión", text: "Necesitas una sesión activa para entrar a esa sección." });
        window.history.replaceState({}, "", window.location.pathname);
    } else if (new URLSearchParams(window.location.search).get("motivo") === "servidor_desconectado") {
        window.Swal?.fire({ icon: "warning", title: "Conexión perdida", text: "El servidor dejó de responder. Vuelve a iniciar sesión cuando esté disponible." });
        window.history.replaceState({}, "", window.location.pathname);
    }
});
