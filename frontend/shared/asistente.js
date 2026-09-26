(function () {
    if (document.getElementById("marqueza-assistant-launcher")) return;

    const scriptUrl = document.currentScript.src;
    const stylesheet = document.createElement("link");
    stylesheet.rel = "stylesheet";
    stylesheet.href = new URL("asistente.css", scriptUrl).href;
    document.head.appendChild(stylesheet);

    const modules = [
        { name: "Inicio", key: "", aliases: ["inicio", "dashboard", "panel", "resumen"], description: "un panel con indicadores y gráficas de ventas, cotizaciones e inventario", details: "Resume la actividad comercial y muestra comparaciones de ventas, cotizaciones y existencias.", countQuestion: "¿Qué módulos tiene MARQUEZA?", createQuestion: "¿Qué información muestra el inicio?" },
        { name: "Insumos", key: "marqueza_insumos", aliases: ["insumo", "insumos", "material", "materiales"], description: "la gestión del inventario de materias primas e insumos", details: "Permite consultar nombre, código, cantidad, precio, estado y proveedor relacionado.", singular: "insumo", plural: "insumos", countQuestion: "¿Cuántos insumos hay?", createQuestion: "¿Cómo registro un insumo?" },
        { name: "Productos", key: "marqueza_productos", aliases: ["producto", "productos", "prenda", "prendas"], description: "la gestión del catálogo y las existencias de productos", details: "Organiza los productos con su código, nombre, cantidad disponible, precio y estado.", singular: "producto", plural: "productos", countQuestion: "¿Cuántos productos hay?", createQuestion: "¿Cómo creo un producto?" },
        { name: "Ventas", key: "marqueza_ventas", aliases: ["venta", "ventas"], description: "el registro y consulta de ventas", details: "Las ventas se relacionan con clientes y productos; el total depende de las cantidades y precios registrados.", singular: "venta", plural: "ventas", countQuestion: "¿Cuántas ventas hay?", createQuestion: "¿Cómo registro una venta?" },
        { name: "Cotizaciones", key: "marqueza_cotizaciones", aliases: ["cotizacion", "cotizaciones", "propuesta", "propuestas"], description: "la creación y seguimiento de cotizaciones para clientes", details: "Una cotización puede incluir productos, cantidades, precios y un total. En esta pantalla aparecen los estados Pendiente, Enviada, Aprobada y Rechazada.", singular: "cotización", plural: "cotizaciones", countQuestion: "¿Cuántas cotizaciones hay?", createQuestion: "¿Qué estados puede tener una cotización?" },
        { name: "Clientes", key: "marqueza_clientes", aliases: ["cliente", "clientes"], description: "los datos de contacto de los clientes", details: "La pantalla de clientes permite manejar nombre, documento, teléfono y correo.", singular: "cliente", plural: "clientes", countQuestion: "¿Cuántos clientes hay?", createQuestion: "¿Cómo registro un cliente?" },
        { name: "Proveedores", key: "marqueza_proveedores", aliases: ["proveedor", "proveedores"], description: "la información de los proveedores", details: "El proyecto relaciona proveedores con información de persona y canales de contacto.", singular: "proveedor", plural: "proveedores", countQuestion: "¿Cuántos proveedores hay?", createQuestion: "¿Cómo agrego un proveedor?" },
        { name: "Usuarios", key: "marqueza_usuarios", aliases: ["usuario", "usuarios", "cuenta", "cuentas"], description: "las cuentas y roles de acceso al sistema", details: "El módulo administra cuentas y sus datos de acceso. No compartas contraseñas en este chat.", singular: "usuario", plural: "usuarios", countQuestion: "¿Cuántos usuarios hay?", createQuestion: "¿Cómo registro un usuario?" },
        { name: "Registro de actividad", key: "marqueza_bitacora", aliases: ["registro de actividad", "actividad", "auditoria", "historial", "errores"], description: "el historial de actividad registrado en la aplicación", details: "Permite consultar eventos de auditoría, acciones y actividad guardada por la aplicación.", singular: "evento", plural: "eventos", countQuestion: "¿Cuántos eventos hay?", createQuestion: "¿Qué guarda el registro de actividad?" }
    ];

    function normalize(value) {
        return value.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    }

    function currentModule() {
        const path = normalize(decodeURIComponent(window.location.pathname));
        return modules.find((module) => module.aliases.some((alias) => path.includes(alias))) || modules[0];
    }

    function findModule(question) {
        const normalized = normalize(question);
        return modules.find((module) => module.aliases.some((alias) => normalized.includes(normalize(alias))));
    }

    function localCount(module) {
        if (!module.key) return null;
        try {
            const value = localStorage.getItem(module.key);
            if (value === null) return 0;
            const records = JSON.parse(value);
            return Array.isArray(records) ? records.length : null;
        } catch {
            return null;
        }
    }

    function answerQuestion(question) {
        const normalized = normalize(question);
        const activeModule = currentModule();
        const targetModule = findModule(question) || activeModule;

        if (/\b(hola|buenas|buenos dias|buenas tardes|buenas noches)\b/.test(normalized)) {
            return "Hola. Puedo orientarte sobre esta pantalla, los módulos y el proyecto MARQUEZA. ¿Qué quieres consultar?";
        }

        if (/\b(api|backend|mysql|servidor|conecta|conexion|localstorage|almacenamiento local|guardan los datos|almacenan los datos|donde se guardan)\b/.test(normalized)) {
            return "El backend de MARQUEZA usa Flask y MySQL, y expone una API REST. El frontend está hecho con HTML, CSS y JavaScript; varias pantallas todavía guardan sus registros en localStorage. Por eso, un dato visible en el navegador no necesariamente está sincronizado con MySQL.";
        }

        if (/\b(proyecto|marqueza|sistema|aplicacion|tecnologia|frontend|modulos|modulo)\b/.test(normalized)) {
            return "MARQUEZA es una aplicación de gestión para una empresa de confecciones. Reúne clientes, proveedores, productos, insumos, ventas, cotizaciones, usuarios y registro de actividad. Su propósito es centralizar contactos, inventario y seguimiento comercial. El frontend usa HTML, CSS y JavaScript; el backend usa Flask y MySQL, aunque algunas pantallas aún trabajan con datos locales.";
        }

        if (/\b(estado|estados|pendiente|enviada|aprobada|rechazada)\b/.test(normalized) && targetModule.name === "Cotizaciones") {
            return "Las cotizaciones pueden estar Pendientes, Enviadas, Aprobadas o Rechazadas. Puedes revisar y filtrar esos estados desde la pantalla de Cotizaciones.";
        }

        if (/\b(datos|campos|informacion|incluye|contiene|guarda|almacena)\b/.test(normalized) && findModule(question)) {
            return `${targetModule.name} ${targetModule.details}`;
        }

        if (/\b(relacion|relaciona|asocia|vincula|depende)\b/.test(normalized)) {
            if (targetModule.name === "Ventas") return "Las ventas se relacionan con un cliente y con los productos vendidos. Las líneas de producto incluyen cantidades; el valor depende de los precios registrados.";
            if (targetModule.name === "Cotizaciones") return "Las cotizaciones se preparan para clientes y pueden incluir productos, cantidades, precios y un total.";
            if (targetModule.name === "Insumos") return "Los insumos pueden relacionarse con un proveedor y con detalles de producción.";
            if (targetModule.name === "Productos") return "Los productos pueden relacionarse con sus insumos y con las ventas en las que se incluyen.";
            return `${targetModule.name} forma parte del flujo de gestión de MARQUEZA. ${targetModule.details}`;
        }

        if (/\b(cuantos|cuantas|total|cantidad|numero|registros)\b/.test(normalized) || (/\b(hay|existen)\b/.test(normalized) && findModule(question))) {
            const count = localCount(targetModule);
            if (count === null) {
                return `No encuentro datos de ${targetModule.name} en el almacenamiento local de este navegador, así que no puedo confirmar un total.`;
            }
            const countLabel = count === 1 ? targetModule.singular || targetModule.name.toLowerCase() : targetModule.plural || targetModule.name.toLowerCase();
            return `Hay ${count} ${countLabel} en el almacenamiento local de este navegador.`;
        }

        if (/\b(que hace|que puedo hacer|que hay en|esta pagina|esta pantalla|para que sirve|funciona)\b/.test(normalized)) {
            const count = localCount(targetModule);
            const countText = count === null ? "" : ` Actualmente hay ${count} registros locales.`;
            return `Esta es la pantalla de ${targetModule.name}: ${targetModule.description}. ${targetModule.details}${countText}`;
        }

        if (/\b(crear|creo|agregar|agrego|anadir|registro|registrar|nuevo|nueva|guardar|guardo|editar|edito|eliminar|elimino|buscar|busco|filtrar|filtro)\b/.test(normalized)) {
            if (targetModule.name === "Inicio" || targetModule.name === "Registro de actividad") {
                return `La pantalla de ${targetModule.name} sirve para consultar información; no es un formulario de creación de registros. Usa la barra lateral para abrir el módulo que quieras gestionar.`;
            }
            return `En ${targetModule.name}, usa el botón principal para crear un registro. Después de guardarlo, aparecerá en la tabla, donde podrás consultarlo, editarlo o eliminarlo.`;
        }

        if (findModule(question)) {
            const count = localCount(targetModule);
            const countText = count === null ? " No hay datos locales disponibles para contar." : ` Hay ${count} registros locales.`;
            return `El módulo ${targetModule.name} se usa para ${targetModule.description.replace(/^la gestión de |^el registro y consulta de |^la creación y seguimiento de |^los datos de contacto de |^la información de |^las cuentas y roles de acceso al sistema/, "")}. ${targetModule.details}${countText}`;
        }

        return "Puedo responder sobre el proyecto, esta pantalla y los conteos guardados localmente. No tengo un servicio de IA conectado ni acceso a información fuera de la aplicación. Prueba preguntando, por ejemplo: ¿Qué hace esta página? o ¿Cuántos clientes hay?";
    }

    function suggestedQuestions(module) {
        if (module.name === "Inicio") {
            return [module.countQuestion, "¿Cómo se guardan los datos?", "¿Qué muestra esta pantalla?"];
        }
        if (module.name === "Registro de actividad") {
            return [module.createQuestion, module.countQuestion, "¿Qué módulos tiene MARQUEZA?"];
        }
        return [module.countQuestion, module.createQuestion, `¿Qué datos maneja ${module.name}?`];
    }

    function createElement(tagName, className, text) {
        const element = document.createElement(tagName);
        if (className) element.className = className;
        if (text) element.textContent = text;
        return element;
    }

    const launcher = createElement("button", "marqueza-assistant-launcher");
    launcher.id = "marqueza-assistant-launcher";
    launcher.type = "button";
    launcher.setAttribute("aria-label", "Abrir asistente MARQUEZA");
    launcher.setAttribute("aria-expanded", "false");
    launcher.title = "Abrir asistente";
    launcher.innerHTML = "<span class='marqueza-assistant-launcher-mark'><i class='bx bxs-message-rounded-dots' aria-hidden='true'></i><i class='bx bx-sparkles' aria-hidden='true'></i></span>";

    const panel = createElement("section", "marqueza-assistant-panel");
    panel.id = "marqueza-assistant-panel";
    panel.setAttribute("role", "dialog");
    panel.setAttribute("aria-labelledby", "marqueza-assistant-title");
    panel.setAttribute("aria-modal", "false");
    panel.hidden = true;

    const header = createElement("header", "marqueza-assistant-header");
    const identity = createElement("div", "marqueza-assistant-identity");
    const avatar = createElement("span", "marqueza-assistant-avatar");
    avatar.innerHTML = "<i class='bx bxs-message-rounded-dots' aria-hidden='true'></i>";
    const heading = createElement("div", "marqueza-assistant-heading");
    const title = createElement("h2", "", "Asistente MARQUEZA");
    title.id = "marqueza-assistant-title";
    heading.append(title, createElement("p", "", "Preguntas sobre MARQUEZA"));
    identity.append(avatar, heading);
    const closeButton = createElement("button", "marqueza-assistant-close");
    closeButton.type = "button";
    closeButton.setAttribute("aria-label", "Cerrar asistente");
    closeButton.title = "Cerrar";
    closeButton.innerHTML = "<i class='bx bx-x' aria-hidden='true'></i>";
    header.append(identity, closeButton);

    const messages = createElement("div", "marqueza-assistant-messages");
    messages.setAttribute("aria-live", "polite");
    messages.setAttribute("aria-label", "Conversacion");
    const intro = createElement("div", "marqueza-assistant-intro");
    intro.append(createElement("p", "", "Hola, soy tu asistente contextual."));
    intro.append(createElement("p", "", "Pregunta por los módulos, los datos o cómo realizar una tarea."));
    const suggestions = createElement("div", "marqueza-assistant-suggestions");
    suggestedQuestions(currentModule()).forEach((suggestion) => {
        const button = createElement("button", "marqueza-assistant-suggestion", suggestion);
        button.type = "button";
        button.addEventListener("click", () => submitQuestion(suggestion));
        suggestions.appendChild(button);
    });
    intro.appendChild(suggestions);
    messages.appendChild(intro);

    const form = createElement("form", "marqueza-assistant-form");
    const input = createElement("input", "marqueza-assistant-input");
    input.type = "text";
    input.name = "question";
    input.placeholder = "Escribe tu pregunta...";
    input.autocomplete = "off";
    input.setAttribute("aria-label", "Escribe tu pregunta");
    const sendButton = createElement("button", "marqueza-assistant-send");
    sendButton.type = "submit";
    sendButton.setAttribute("aria-label", "Enviar pregunta");
    sendButton.title = "Enviar";
    sendButton.innerHTML = "<i class='bx bx-send' aria-hidden='true'></i>";
    form.append(input, sendButton);
    panel.append(header, messages, form);
    document.body.append(launcher, panel);

    function addMessage(text, sender) {
        const message = createElement("p", `marqueza-assistant-message is-${sender}`, text);
        messages.appendChild(message);
        messages.scrollTop = messages.scrollHeight;
    }

    function submitQuestion(question) {
        const value = question.trim();
        if (!value) return;
        addMessage(value, "user");
        input.value = "";
        addMessage(answerQuestion(value), "assistant");
        input.focus();
    }

    function setOpen(isOpen) {
        panel.hidden = !isOpen;
        launcher.setAttribute("aria-expanded", String(isOpen));
        launcher.setAttribute("aria-label", isOpen ? "Cerrar asistente MARQUEZA" : "Abrir asistente MARQUEZA");
        launcher.title = isOpen ? "Cerrar asistente" : "Abrir asistente";
        if (isOpen) input.focus();
    }

    launcher.addEventListener("click", () => setOpen(panel.hidden));
    closeButton.addEventListener("click", () => setOpen(false));
    form.addEventListener("submit", (event) => {
        event.preventDefault();
        submitQuestion(input.value);
    });
    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && !panel.hidden) {
            setOpen(false);
            launcher.focus();
        }
    });
})();