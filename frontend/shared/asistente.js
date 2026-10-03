(function () {
    if (document.getElementById("marqueza-assistant-launcher")) return;

    const scriptUrl = document.currentScript.src;
    const stylesheet = document.createElement("link");
    stylesheet.rel = "stylesheet";
    stylesheet.href = new URL("asistente.css", scriptUrl).href;
    document.head.appendChild(stylesheet);

    const modules = [
        { name: "Inicio", key: "", aliases: ["inicio", "dashboard", "panel", "resumen"], description: "consultar un resumen de la actividad comercial y del inventario", details: "Presenta indicadores y gráficas para revisar ventas, cotizaciones y existencias. Es una vista de consulta, no un formulario para registrar operaciones.", countQuestion: "¿Qué módulos tiene MARQUEZA?", createQuestion: "¿Qué información muestra el inicio?" },
        { name: "Insumos", key: "marqueza_insumos", aliases: ["insumo", "insumos", "material", "materiales"], description: "administrar materias primas y materiales necesarios para la confección", details: "Cada insumo puede incluir nombre, categoría, proveedor, cantidad, unidad, precio unitario y estado. Los estados disponibles son Disponible, Agotado y Pedido; también puedes filtrar por categoría y nivel de inventario.", fields: "nombre, categoría, proveedor (opcional), cantidad, unidad, precio unitario y estado", singular: "insumo", plural: "insumos", countQuestion: "¿Cuántos insumos hay?", createQuestion: "¿Cómo registro un insumo?" },
        { name: "Productos", key: "marqueza_productos", aliases: ["producto", "productos", "prenda", "prendas"], description: "administrar el catálogo de prendas y sus existencias", details: "Un producto registra código automático, nombre, cantidad, precio y estado. El listado permite buscar y filtrar por categoría y nivel de stock. El indicador de stock es Bajo hasta 5 unidades, Medio de 6 a 20 y Bueno por encima de 20.", fields: "nombre, cantidad, precio y estado; el código se genera automáticamente", singular: "producto", plural: "productos", countQuestion: "¿Cuántos productos hay?", createQuestion: "¿Cómo creo un producto?" },
        { name: "Ventas", key: "marqueza_ventas", aliases: ["venta", "ventas"], description: "registrar y consultar las ventas realizadas", details: "Una venta registra fecha, cliente, producto, cantidad y total. Los clientes y productos se seleccionan de sus respectivos módulos; el total se calcula usando el precio del producto y la cantidad.", fields: "fecha, cliente, producto, cantidad y total calculado", singular: "venta", plural: "ventas", countQuestion: "¿Cuántas ventas hay?", createQuestion: "¿Cómo registro una venta?" },
        { name: "Cotizaciones", key: "marqueza_cotizaciones", aliases: ["cotizacion", "cotizaciones", "propuesta", "propuestas"], description: "preparar propuestas comerciales para clientes y hacer seguimiento", details: "Una cotización contiene fecha, cliente, uno o varios productos con cantidad y precio unitario, estado y notas. El total se calcula sumando cantidad por precio de cada producto. Los estados son Pendiente, Enviada, Aprobada y Rechazada; se pueden buscar, filtrar y exportar a PDF.", fields: "fecha, cliente, productos, cantidades, precios unitarios, estado y notas opcionales", singular: "cotización", plural: "cotizaciones", countQuestion: "¿Cuántas cotizaciones hay?", createQuestion: "¿Cómo creo una cotización?" },
        { name: "Clientes", key: "marqueza_clientes", aliases: ["cliente", "clientes"], description: "administrar la información de contacto de los clientes", details: "La ficha de cada cliente incluye nombre, documento, teléfono y correo. Las ventas y cotizaciones permiten seleccionar clientes registrados aquí.", fields: "nombre, documento, teléfono y correo", singular: "cliente", plural: "clientes", countQuestion: "¿Cuántos clientes hay?", createQuestion: "¿Cómo registro un cliente?" },
        { name: "Proveedores", key: "marqueza_proveedores", aliases: ["proveedor", "proveedores"], description: "mantener la información de los proveedores de la empresa", details: "Cada ficha puede incluir empresa, persona de contacto, teléfono, correo y dirección. Los proveedores registrados pueden asociarse a los insumos.", fields: "empresa, contacto, teléfono, correo y dirección", singular: "proveedor", plural: "proveedores", countQuestion: "¿Cuántos proveedores hay?", createQuestion: "¿Cómo agrego un proveedor?" },
        { name: "Usuarios", key: "marqueza_usuarios", aliases: ["usuario", "usuarios", "cuenta", "cuentas"], description: "administrar las cuentas de acceso al sistema y sus roles", details: "El módulo permite registrar y actualizar nombre, correo, rol y contraseña. Al editar, la nueva contraseña es opcional. Nunca compartas contraseñas por el chat.", fields: "nombre, correo, rol y contraseña al crear la cuenta", singular: "usuario", plural: "usuarios", countQuestion: "¿Cuántos usuarios hay?", createQuestion: "¿Cómo registro un usuario?" },
        { name: "Registro de actividad", key: "marqueza_bitacora", aliases: ["registro de actividad", "actividad", "auditoria", "historial", "errores"], description: "revisar el historial de acciones registradas en la aplicación", details: "Permite consultar actividad y cambios guardados por la aplicación, filtrar el historial y revisar eventos. Es una pantalla de consulta; no se crean registros manualmente desde allí.", singular: "evento", plural: "eventos", countQuestion: "¿Cuántos eventos hay?", createQuestion: "¿Qué guarda el registro de actividad?" }
    ];

    const projectContext = [
        "MARQUEZA es una aplicación web de gestión para una empresa de confecciones.",
        "Sus módulos visibles son Inicio, Insumos, Productos, Ventas, Cotizaciones, Clientes, Proveedores, Usuarios y Registro de actividad.",
        "La interfaz está hecha con HTML, CSS y JavaScript; el backend es una API REST en Flask y la base de datos es MariaDB/MySQL.",
        "Las pantallas usan localStorage como caché y algunas conservan registros locales; MarquezaApi intenta sincronizar los datos con el backend. Por eso, un conteo leído por este asistente desde el navegador no garantiza que sea el total actualizado del servidor.",
        "El asistente es local y funciona con reglas y respuestas preparadas. No usa un modelo de IA, no puede realizar cambios en los registros y no consulta directamente la base de datos.",
        "Los flujos principales conectan proveedores con insumos, y clientes con ventas y cotizaciones. Ventas selecciona un cliente y un producto; una cotización puede tener varios productos.",
        "Las cotizaciones son propuestas comerciales informativas, no facturas ni comprobantes de venta."
    ].join(" ");

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

    let conversationModule = currentModule();

    function answerQuestion(question) {
        const normalized = normalize(question);
        const mentionedModule = findModule(question);
        const targetModule = mentionedModule || conversationModule || currentModule();

        if (/\b(hola|buenas|buenos dias|buenas tardes|buenas noches)\b/.test(normalized)) {
            return "¡Hola! Soy el asistente de MARQUEZA. Puedo ayudarte a entender los módulos, los campos de los formularios y los pasos para registrar, buscar o editar información. ¿Qué necesitas hacer?";
        }

        if (/\b(gracias|muchas gracias|te agradezco)\b/.test(normalized)) {
            return "¡Con gusto! Si quieres, también puedo explicarte otro módulo o guiarte paso a paso.";
        }

        if (/\b(adios|hasta luego|nos vemos|chao)\b/.test(normalized)) {
            return "¡Hasta luego! Aquí estaré si necesitas ayuda con MARQUEZA.";
        }

        if (mentionedModule) conversationModule = mentionedModule;

        if (/\b(que puedes hacer|como me ayudas|ayuda|que sabes|que conoces|que puedes responder)\b/.test(normalized)) {
            return "Puedo explicar para qué sirve cada módulo, qué campos pide, cómo crear, buscar, editar o eliminar registros, cómo se relacionan los módulos y qué significan algunos estados o indicadores. También puedo contar registros de la caché local del navegador. No puedo ejecutar acciones por ti ni consultar la base de datos en tiempo real.";
        }

        if (/\b(que modulos|cuales modulos|lista de modulos|modulos tiene|secciones tiene)\b/.test(normalized)) {
            return `MARQUEZA tiene estos módulos: ${modules.map((module) => module.name).join(", ")}. ${projectContext}`;
        }

        if (/\b(api|backend|mysql|mariadb|servidor|conexion|localstorage|almacenamiento local|donde se guardan|como se guardan)\b/.test(normalized)) {
            return projectContext;
        }

        if (/\b(que es|que es marqueza|proyecto|tecnologia|frontend|backend|aplicacion)\b/.test(normalized) && !mentionedModule) {
            return projectContext;
        }

        if (/\b(estado|estados|pendiente|enviada|aprobada|rechazada)\b/.test(normalized) && targetModule.name === "Cotizaciones") {
            return "Los estados disponibles para las cotizaciones son Pendiente, Enviada, Aprobada y Rechazada. Puedes seleccionar el estado al crear o editar una cotización, y filtrar la lista por estado.";
        }

        if (/\b(stock bajo|nivel de stock|inventario bajo|pocas unidades)\b/.test(normalized) && targetModule.name === "Productos") {
            return "En Productos, el indicador se calcula por cantidad: Bajo hasta 5 unidades, Medio de 6 a 20 y Bueno por encima de 20. Puedes filtrar la lista por esos niveles.";
        }

        if (/\b(relacion|relaciona|asocia|vincula|depende|conecta)\b/.test(normalized)) {
            if (targetModule.name === "Ventas") return "El módulo Ventas utiliza clientes y productos que ya estén registrados. En cada venta eliges fecha, cliente, producto y cantidad; el total se calcula con el precio del producto.";
            if (targetModule.name === "Cotizaciones") return "Las cotizaciones se preparan para un cliente y pueden incluir varios productos. Se calcula el total de cada línea (cantidad por precio unitario) y el total de la propuesta.";
            if (targetModule.name === "Insumos") return "Un insumo puede asociarse con un proveedor registrado. El proveedor es opcional en el formulario; para seleccionarlo primero debe existir en Proveedores.";
            if (targetModule.name === "Productos") return "Los productos se pueden seleccionar en Ventas y Cotizaciones. Esas pantallas usan el nombre o código del producto y el precio registrado.";
            if (targetModule.name === "Proveedores") return "Los proveedores pueden asociarse a los insumos que suministran.";
            if (targetModule.name === "Clientes") return "Los clientes registrados se pueden seleccionar al crear una venta o una cotización.";
            return `${targetModule.name} forma parte del flujo de gestión de MARQUEZA. ${targetModule.details}`;
        }

        if (/\b(campos|que datos|que informacion|que incluye|que contiene|informacion maneja|datos guarda)\b/.test(normalized)) {
            return targetModule.fields
                ? `En ${targetModule.name} se manejan estos campos: ${targetModule.fields}. ${targetModule.details}`
                : `${targetModule.name}: ${targetModule.details}`;
        }

        if (/\b(cuantos|cuantas|total de registros|numero de registros|cantidad de registros|registros hay|cuantos registros|cuantas cotizaciones)\b/.test(normalized) || (/\b(hay|existen|total)\b/.test(normalized) && mentionedModule)) {
            const count = localCount(targetModule);
            if (count === null) {
                return `No encuentro datos de ${targetModule.name} en el almacenamiento local de este navegador, así que no puedo confirmar un total.`;
            }
            const countLabel = count === 1 ? targetModule.singular || targetModule.name.toLowerCase() : targetModule.plural || targetModule.name.toLowerCase();
            return `En la caché local de este navegador hay ${count} ${countLabel}. Puede que el dato no esté actualizado o que no coincida con el total del servidor.`;
        }

        if (/\b(que hace|que puedo hacer|que hay en|esta pagina|esta pantalla|para que sirve|como funciona|funciona)\b/.test(normalized)) {
            const count = localCount(targetModule);
            const countText = count === null ? "" : ` En la caché local hay ${count} registros.`;
            return `La pantalla de ${targetModule.name} sirve para ${targetModule.description}. ${targetModule.details}${countText}`;
        }

        if (/\b(crear|creo|agregar|agrego|anadir|registro|registrar|nuevo|nueva|guardar|guardo)\b/.test(normalized)) {
            if (targetModule.name === "Inicio" || targetModule.name === "Registro de actividad") {
                return `La pantalla de ${targetModule.name} sirve para consultar información; no es un formulario de creación de registros. Usa la barra lateral para abrir el módulo que quieras gestionar.`;
            }
            return `Para crear en ${targetModule.name}, abre esa pantalla desde la barra lateral y pulsa el botón para agregar o crear. Completa los campos obligatorios (${targetModule.fields || "los campos del formulario"}) y pulsa Guardar. Si el registro necesita un cliente, producto o proveedor relacionado, primero debe estar registrado en su módulo.`;
        }

        if (/\b(editar|edito|modificar|actualizar|cambiar)\b/.test(normalized)) {
            return `En ${targetModule.name}, localiza el registro en la lista, usa el botón con el lápiz para editarlo, cambia los campos necesarios y guarda. En Usuarios, cambiar la contraseña al editar es opcional.`;
        }

        if (/\b(eliminar|elimino|borrar|quito)\b/.test(normalized)) {
            return `En ${targetModule.name}, busca el registro y usa el botón con el icono de eliminar. El sistema pide confirmar antes de borrarlo; la eliminación no se puede deshacer.`;
        }

        if (/\b(buscar|busco|encontrar|filtrar|filtro)\b/.test(normalized)) {
            if (targetModule.name === "Cotizaciones") return "En Cotizaciones, escribe el nombre del cliente o producto en el buscador. También puedes filtrar la lista por Pendiente, Enviada, Aprobada o Rechazada.";
            if (targetModule.name === "Productos" || targetModule.name === "Insumos") return `En ${targetModule.name}, escribe parte del texto en el campo de búsqueda. También puedes filtrar por categoría${targetModule.name === "Productos" ? " y por nivel de stock" : ""}.`;
            return `En ${targetModule.name}, escribe parte del texto en el campo de búsqueda para filtrar los registros visibles.`;
        }

        if (/\b(exportar|descargar|pdf|excel|csv)\b/.test(normalized)) {
            return `En ${targetModule.name}, busca el botón Exportar o Descargar en la pantalla. El formato disponible depende del módulo; las cotizaciones permiten generar un PDF.`;
        }

        if (/\b(oscuro|claro|tema|modo oscuro)\b/.test(normalized)) {
            return "Puedes cambiar entre los temas claro y oscuro desde el control de tema de la barra lateral. En pantallas pequeñas, abre primero el menú si el control no está visible.";
        }

        if (/\b(contrasena|password|clave|seguridad|privacidad)\b/.test(normalized)) {
            return "Por seguridad, no escribas contraseñas, claves ni datos personales en este chat. El asistente solo responde con reglas locales y no necesita esos datos para ayudarte.";
        }

        if (mentionedModule || conversationModule) {
            const count = localCount(targetModule);
            const countText = count === null ? "" : ` En la caché de este navegador hay ${count} registros.`;
            return `Puedo ayudarte con ${targetModule.name}: ${targetModule.description}. ${targetModule.details}${countText} Puedes preguntarme por sus campos, cómo crear o editar un registro, o cuántos elementos aparecen en la caché local.`;
        }

        return `No reconocí exactamente la pregunta, pero puedo orientarte sobre MARQUEZA. ${projectContext} Prueba con «¿Cómo registro un cliente?», «¿Qué estados tienen las cotizaciones?» o «¿Qué campos tiene este módulo?».`;
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
    intro.append(createElement("p", "", "Hola, soy el asistente virtual de MARQUEZA."));
    intro.append(createElement("p", "", "Puedo explicar módulos, campos y pasos de uso. Respondo localmente con información preparada; no consulto la base de datos en tiempo real."));
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