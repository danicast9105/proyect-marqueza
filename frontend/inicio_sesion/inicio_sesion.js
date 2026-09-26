class LoginForm {
    constructor(formulario) {
        this.formulario = formulario;
        this.username = formulario.querySelector("#usuario");
        this.password = formulario.querySelector("#contraseña");
    }

    init() {
        this.formulario.addEventListener("submit", (event) => this.submit(event));
    }

    getUsers() {
        try {
            const users = JSON.parse(localStorage.getItem("marqueza_usuarios") || "[]");
            return Array.isArray(users) ? users : [];
        } catch {
            return [];
        }
    }

    submit(event) {
        event.preventDefault();
        const username = this.username?.value.trim() || "";
        const password = this.password?.value || "";

        if (!username || !password) {
            return Swal.fire({ icon: "warning", title: "Campos incompletos", text: "Por favor completa todos los campos." });
        }

        const users = this.getUsers();
        if (!users.length) {
            window.MarquezaAudit?.log({ action: "Usuario no registrado", module: "Acceso", entity: username, detail: "No hay usuarios registrados para validar el acceso.", outcome: "denied", actor: username, email: "", role: "Usuario" });
            return Swal.fire({ icon: "info", title: "No hay usuarios registrados", text: "Registra un usuario desde el módulo Usuarios antes de iniciar sesión." });
        }

        const user = users.find(item => String(item.nombre || "").trim().toLowerCase() === username.toLowerCase());
        if (!user) {
            window.MarquezaAudit?.log({ action: "Usuario no registrado", module: "Acceso", entity: username, detail: "Intento de inicio de sesión con un usuario no registrado.", outcome: "denied", actor: username, email: "", role: "Usuario" });
            return Swal.fire({ icon: "error", title: "Usuario no registrado", text: "El usuario no está registrado en el sistema." });
        }

        const valid = String(user.contrasena || "") === password;
        if (valid) {
            localStorage.setItem("marqueza_usuario_sesion", JSON.stringify({ nombre: user.nombre, correo: user.correo, rol: user.rol }));
            window.MarquezaAudit?.log({ action: "Inicio de sesión", module: "Acceso", detail: "Inicio de sesión autorizado." });
        } else {
            window.MarquezaAudit?.log({ action: "Inicio de sesión rechazado", module: "Acceso", entity: username, detail: "Contraseña incorrecta para usuario registrado.", outcome: "denied", actor: username });
        }
        Swal.fire({
            title: valid ? "Inicio de sesión exitoso" : "Error",
            icon: valid ? "success" : "error",
            text: valid ? `Bienvenido ${user.nombre}` : "El usuario o la contraseña son incorrectos."
        }).then(() => {
            if (valid) window.location.href = "../inicio/inicio.html";
        });
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const formulario = document.getElementById("formulario");
    if (formulario) new LoginForm(formulario).init();
    if (new URLSearchParams(window.location.search).get("motivo") === "sesion_requerida") {
        window.Swal?.fire({ icon: "warning", title: "Inicia sesión", text: "Necesitas una sesión activa para entrar a esa sección." });
        window.history.replaceState({}, "", window.location.pathname);
    }
});
