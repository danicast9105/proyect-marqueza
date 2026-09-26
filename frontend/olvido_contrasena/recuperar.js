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
            const users = this.readUsers();
            const user = users.find(item => String(item.correo || '').trim().toLowerCase() === correo.toLowerCase());
            if (!user) {
                Swal.fire({ icon: 'error', title: 'Correo no encontrado', text: 'No existe una cuenta local asociada a ese correo.' });
            } else {
                localStorage.setItem('marqueza_recuperacion', JSON.stringify({ correo, creadoEn: new Date().toISOString() }));
                await Swal.fire({ icon: 'success', title: 'Solicitud registrada', text: 'La recuperación se guardó localmente. Contacta al administrador para restablecer la contraseña.', confirmButtonText: 'Entendido' });
                this.form.reset();
            }
        } finally {
            button.disabled = false;
            button.classList.remove('is-loading');
        }
    }

    readUsers() {
        try {
            const users = JSON.parse(localStorage.getItem('marqueza_usuarios') || '[]');
            return Array.isArray(users) ? users : [];
        } catch {
            return [];
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('recoveryForm');
    if (form) form.addEventListener('submit', event => new PasswordRecoveryForm(form).submit(event));
});
