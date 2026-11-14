class PasswordResetForm {
    constructor(form) {
        this.form = form;
        this.password = form.querySelector("#nuevaContrasena");
        this.confirmation = form.querySelector("#confirmarContrasena");
        this.token = new URLSearchParams(window.location.search).get("token") || "";
    }

    init() {
        if (!this.token) {
            this.form.querySelectorAll("input, button").forEach(control => { control.disabled = true; });
            window.Swal?.fire({ icon: "error", title: "Enlace inválido", text: "Solicita un nuevo enlace de recuperación." });
            return;
        }
        this.form.addEventListener("submit", event => this.submit(event));
    }

    async submit(event) {
        event.preventDefault();
        if (this.password.value.length < 8) {
            window.Swal?.fire({ icon: "warning", title: "Contraseña muy corta", text: "Usa al menos 8 caracteres." });
            return;
        }
        if (this.password.value !== this.confirmation.value) {
            window.Swal?.fire({ icon: "warning", title: "Las contraseñas no coinciden", text: "Verifica ambas contraseñas e inténtalo de nuevo." });
            return;
        }

        const button = this.form.querySelector("button");
        button.disabled = true;
        try {
            const result = await window.MarquezaApi.request("/auth/reset-password", {
                method: "POST",
                body: JSON.stringify({ token: this.token, nueva_contrasena: this.password.value })
            });
            await window.Swal?.fire({ icon: "success", title: "Contraseña actualizada", text: result.message || "Ya puedes iniciar sesión con tu nueva contraseña." });
            window.location.href = "../inicio_sesion/inicio_sesion.html";
        } catch (error) {
            window.MarquezaApi.notifyError(error, "No se pudo cambiar la contraseña");
            button.disabled = false;
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("resetForm");
    if (form) new PasswordResetForm(form).init();
});
