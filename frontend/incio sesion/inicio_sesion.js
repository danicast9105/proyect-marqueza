/* llamada al formulario */
const formulario = document.getElementById('formulario');

/* condicion y evento de formulario */
if (!formulario) {
    console.error('Formulario no encontrado: asegúrate de que el elemento tenga id="formulario"');
} else {
    formulario.addEventListener('submit', function (event) {
        event.preventDefault();
        /* obtención de los valores de los campos */
        const username = document.getElementById('usuario');
        const password = document.getElementById('contraseña');

        const usernameValue = username ? username.value.trim() : '';
        const passwordValue = password ? password.value : '';
        
        /* condición de campos vacíos */
        if (!usernameValue || !passwordValue) {
            alert('Por favor completa todos los campos');
            return;
        }
        /* validación de credenciales */
        if (usernameValue === 'admin' && passwordValue === 'admin123') {
            Swal.fire({
                title: "Inicio de sesión exitoso",
                icon: "success",
                text: "Bienvenido " + usernameValue,
            });
        } 
        /* mensaje de error para credenciales incorrectas */
        else {
            Swal.fire({
                icon: "error",
                title: "Error",
                text: " Tu usuario o contraseña son incorrectos",
            });
        }
    });
}