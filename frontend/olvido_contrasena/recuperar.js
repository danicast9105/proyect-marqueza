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
            const response = await fetch('http://localhost:5000/auth/forgot-password', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ correo })
            });
            const data = await response.json().catch(() => ({}));
            if (!response.ok) throw new Error(data.message || 'No fue posible enviar el correo.');
            await Swal.fire({ icon: 'success', title: 'Correo enviado', text: 'Revisa tu bandeja de entrada y sigue el enlace para cambiar tu contraseña.', confirmButtonText: 'Entendido' });
            this.form.reset();
        } catch (error) {
            Swal.fire({ icon: 'error', title: 'No se pudo enviar', text: error.message || 'Verifica que el servidor esté activo e inténtalo de nuevo.' });
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
