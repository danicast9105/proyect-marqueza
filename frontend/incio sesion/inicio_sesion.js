class LoginForm {
    constructor(formulario) {
        this.formulario = formulario;
        this.username = formulario.querySelector("#usuario");
        this.password = formulario.querySelector("#contraseña");
    }

    init() {
        this.formulario.addEventListener("submit", (event) => this.submit(event));
    }

    submit(event) {
        event.preventDefault();
        const username = this.username?.value.trim() || "";
        const password = this.password?.value || "";

        if (!username || !password) {
            return Swal.fire({ icon: "warning", title: "Campos incompletos", text: "Por favor completa todos los campos." });
        }

        const valid = username === "admin" && password === "admin123";
        Swal.fire({
            title: valid ? "Inicio de sesión exitoso" : "Error",
            icon: valid ? "success" : "error",
            text: valid ? `Bienvenido ${username}` : "Tu usuario o contraseña son incorrectos"
        });
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const formulario = document.getElementById("formulario");
    if (formulario) new LoginForm(formulario).init();
});
