localStorage.removeItem("marqueza_usuario_sesion");
sessionStorage.removeItem("marqueza_sesion_activa");
const loginUrl = new URL("./inicio_sesion/inicio_sesion.html", document.currentScript.src);
window.location.replace(loginUrl);
