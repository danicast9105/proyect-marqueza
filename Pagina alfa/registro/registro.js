const formulario = document.getElementById('formulario');
const inputUsuario = document.getElementById('usuario');
const inputCorreo = document.getElementById('correo');
const selectRol = document.getElementById('rol');
const inputContrasena = document.getElementById('contrasena');
const inputConfirmarContrasena = document.getElementById('confirmar_contrasena');

function mostrarError(mensaje) {
    Swal.fire({
        icon: 'error',
        title: 'Error de registro',
        text: mensaje,
        confirmButtonText: 'Aceptar'
    });
}

function validarUsuario(usuario) {
    const usuarioRegex = /^[A-Za-z0-9]{3,20}$/;
    return usuarioRegex.test(usuario);
}

function validarContrasena(contrasena) {
    const contrasenaRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
    return contrasenaRegex.test(contrasena);
}

formulario.addEventListener('submit', function(event) {
    event.preventDefault();

    const usuario = inputUsuario.value.trim();
    const correo = inputCorreo.value.trim();
    const rol = selectRol.value;
    const contrasena = inputContrasena.value;
    const confirmarContrasena = inputConfirmarContrasena.value;

    if (!validarUsuario(usuario)) {
        mostrarError('El nombre de usuario debe tener entre 3 y 20 caracteres y solo puede contener letras y números.');
        return;
    }

    if (!correo) {
        mostrarError('Ingresa un correo electrónico válido.');
        return;
    }

    if (rol === 'Ninguno') {
        mostrarError('Debes seleccionar un rol válido para continuar.');
        return;
    }

    if (!validarContrasena(contrasena)) {
        mostrarError('La contraseña debe tener al menos 8 caracteres, incluir una letra mayúscula, una letra minúscula y un número.');
        return;
    }

    if (contrasena !== confirmarContrasena) {
        mostrarError('Las contraseñas no coinciden.');
        return;
    }

    Swal.fire({
        icon: 'success',
        title: 'Registro exitoso',
        text: 'Tu cuenta ha sido creada con éxito.',
        confirmButtonText: 'Continuar'
    }).then(() => {
        formulario.reset();
    });
});
