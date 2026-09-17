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
            return Swal.fire({ icon: "info", title: "No hay usuarios registrados", text: "Registra un usuario desde el módulo Usuarios antes de iniciar sesión." });
        }

        const user = users.find(item => String(item.nombre || "").trim().toLowerCase() === username.toLowerCase() && String(item.contrasena || "") === password);
        const valid = Boolean(user);
        if (valid) localStorage.setItem("marqueza_usuario_sesion", JSON.stringify({ nombre: user.nombre, correo: user.correo, rol: user.rol }));
        Swal.fire({
            title: valid ? "Inicio de sesión exitoso" : "Error",
            icon: valid ? "success" : "error",
            text: valid ? `Bienvenido ${user.nombre}` : "Tu usuario o contraseña son incorrectos"
        }).then(() => {
            if (valid) window.location.href = "../inicio/inicio.html";
        });
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const formulario = document.getElementById("formulario");
    if (formulario) new LoginForm(formulario).init();

});
