class RegistroForm {
    constructor(formulario) {
        this.formulario = formulario;
        this.usuario = formulario.querySelector("#usuario");
        this.correo = formulario.querySelector("#correo");
        this.rol = formulario.querySelector("#rol");
        this.contrasena = formulario.querySelector("#contrasena");
        this.confirmacion = formulario.querySelector("#confirmar_contrasena");
    }

    init() {
        this.formulario.addEventListener("submit", (event) => this.submit(event));
    }

    showMessage(icon, title, text) {
        Swal.fire({ icon, title, text, confirmButtonText: "Aceptar" });
    }

    isValidUsername(value) {
        return /^[A-Za-z0-9]{3,20}$/.test(value);
    }

    isValidPassword(value) {
        return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/.test(value);
    }

    submit(event) {
        event.preventDefault();
        const usuario = this.usuario.value.trim();
        const correo = this.correo.value.trim();
        const rol = this.rol.value;
        const contrasena = this.contrasena.value;
        const confirmacion = this.confirmacion.value;

        if (!this.isValidUsername(usuario)) return this.showMessage("error", "Error de registro", "El nombre de usuario debe tener entre 3 y 20 caracteres y solo puede contener letras y números.");
        if (!correo) return this.showMessage("error", "Error de registro", "Ingresa un correo electrónico válido.");
        if (rol === "Ninguno") return this.showMessage("error", "Error de registro", "Debes seleccionar un rol válido para continuar.");
        if (!this.isValidPassword(contrasena)) return this.showMessage("error", "Error de registro", "La contraseña debe tener al menos 8 caracteres, incluir una letra mayúscula, una letra minúscula y un número.");
        if (contrasena !== confirmacion) return this.showMessage("error", "Error de registro", "Las contraseñas no coinciden.");

        const users = this.readUsers();
        if (users.some(item => String(item.nombre || "").toLowerCase() === usuario.toLowerCase())) return this.showMessage("warning", "Usuario existente", "Ese nombre de usuario ya está registrado.");
        if (users.some(item => String(item.correo || "").toLowerCase() === correo.toLowerCase())) return this.showMessage("warning", "Correo existente", "Ese correo ya está registrado.");
        users.push({ nombre: usuario, correo, rol, contrasena });
        localStorage.setItem("marqueza_usuarios", JSON.stringify(users));
        Swal.fire({ icon: "success", title: "Registro exitoso", text: "Tu cuenta ha sido guardada localmente.", confirmButtonText: "Continuar" }).then(() => this.formulario.reset());
    }

    readUsers() {
        try {
            const users = JSON.parse(localStorage.getItem("marqueza_usuarios") || "[]");
            return Array.isArray(users) ? users : [];
        } catch {
            return [];
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const formulario = document.getElementById("formulario");
    if (formulario) new RegistroForm(formulario).init();
});
