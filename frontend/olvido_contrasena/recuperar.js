class PasswordRecoveryForm {
    constructor(form) {
        this.form = form;
        this.email = form.querySelector('#correo');
    }

    async submit(event) {
        event.preventDefault();
        const correo = this.email.value.trim();
        if (!this.email.checkValidity()) {
            Swal.fire({ icon: 'warning', title: 'Correo inválido', text: 'Ingresa un correo electrónico válido.' });
            return;
        }

        const button = this.form.querySelector('button');
        button.disabled = true;
        button.classList.add('is-loading');
        try {
            const result = await window.MarquezaApi.request("/auth/forgot-password", {
                method: "POST",
                body: JSON.stringify({ correo })
            });
            await Swal.fire({ icon: 'success', title: 'Revisa tu correo', text: result.message || 'Si la cuenta existe, recibirás un enlace para cambiar la contraseña.', confirmButtonText: 'Entendido' });
            this.form.reset();
        } catch (error) {
            window.MarquezaApi.notifyError(error, "No se pudo solicitar la recuperación");
        } finally {
            button.disabled = false;
            button.classList.remove('is-loading');
        }
    }

}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('recoveryForm');
    if (form) form.addEventListener('submit', event => new PasswordRecoveryForm(form).submit(event));
});
