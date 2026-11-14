(function () {
    const main = document.querySelector(".cont_2");
    if (!main || !window.MarquezaAudit) return;

    main.classList.add("audit-page");
    main.replaceChildren();
    main.innerHTML = `
        <header class="audit-heading">
            <div>
                <span class="audit-eyebrow">Seguridad y seguimiento</span>
                <h1>Registro de actividad</h1>
                <p>Accesos, cambios y errores registrados en este navegador.</p>
            </div>
            <div class="audit-actions">
                <button type="button" class="audit-icon-button" id="auditRefresh" title="Actualizar" aria-label="Actualizar"><i class="bx bx-refresh"></i></button>
                <button type="button" class="audit-export" id="auditExport"><i class="bx bx-download" aria-hidden="true"></i><span>Exportar CSV</span></button>
            </div>
        </header>
        <section class="audit-summary" aria-label="Resumen de actividad">
            <div class="audit-stat"><span>Eventos registrados</span><strong id="auditTotal">0</strong><i class="bx bx-list-ul" aria-hidden="true"></i></div>
            <div class="audit-stat"><span>Cambios en registros</span><strong id="auditChanges">0</strong><i class="bx bx-edit-alt" aria-hidden="true"></i></div>
            <div class="audit-stat audit-stat-denied"><span>Accesos rechazados</span><strong id="auditDenied">0</strong><i class="bx bx-shield-x" aria-hidden="true"></i></div>
            <div class="audit-stat audit-stat-error"><span>Errores de aplicación</span><strong id="auditErrors">0</strong><i class="bx bx-error-circle" aria-hidden="true"></i></div>
        </section>
        <section class="audit-toolbar" aria-label="Filtros de actividad">
            <label class="audit-search"><i class="bx bx-search" aria-hidden="true"></i><input id="auditSearch" type="search" placeholder="Buscar persona, módulo o detalle" aria-label="Buscar en la actividad"></label>
            <label class="audit-filter-label" for="auditFilter">Tipo de evento</label>
            <select id="auditFilter" aria-label="Filtrar por tipo de evento">
                <option value="all">Todos los eventos</option>
                <option value="changes">Cambios de registros</option>
                <option value="access">Accesos</option>
                <option value="errors">Errores</option>
            </select>
            <span class="audit-results" id="auditResults" aria-live="polite">0 eventos</span>
        </section>
        <section class="audit-table-section" aria-label="Eventos registrados">
            <div class="audit-table-scroll">
                <table class="audit-table">
                    <thead><tr><th scope="col">Fecha y hora</th><th scope="col">Persona</th><th scope="col">Evento</th><th scope="col">Módulo</th><th scope="col">Detalle</th></tr></thead>
                    <tbody id="auditRows"></tbody>
                </table>
            </div>
            <p class="audit-empty" id="auditEmpty" hidden>No hay eventos que coincidan con los filtros.</p>
        </section>
        <p class="audit-note"><i class="bx bx-info-circle" aria-hidden="true"></i> Estos registros se guardan en el almacenamiento local de este navegador; no son una bitácora central ni resistente a modificaciones.</p>
    `;

    const elements = {
        total: document.getElementById("auditTotal"),
        changes: document.getElementById("auditChanges"),
        denied: document.getElementById("auditDenied"),
        errors: document.getElementById("auditErrors"),
        rows: document.getElementById("auditRows"),
        empty: document.getElementById("auditEmpty"),
        results: document.getElementById("auditResults"),
        search: document.getElementById("auditSearch"),
        filter: document.getElementById("auditFilter")
    };

    const isChange = (event) => String(event.action || "").startsWith("Registro ");
    const isAccess = (event) => String(event.module || "").toLowerCase() === "acceso" || event.outcome === "denied";
    const isError = (event) => event.outcome === "error";

    function formatDate(value) {
        const date = new Date(value);
        return Number.isNaN(date.getTime()) ? "Fecha no disponible" : new Intl.DateTimeFormat("es-CO", { dateStyle: "medium", timeStyle: "short" }).format(date);
    }

    function visibleEvents(events) {
        const query = elements.search.value.trim().toLocaleLowerCase("es");
        const filter = elements.filter.value;
        return events.filter((event) => {
            const matchesType = filter === "all" || (filter === "changes" && isChange(event)) || (filter === "access" && isAccess(event)) || (filter === "errors" && isError(event));
            const text = [event.actor, event.email, event.action, event.module, event.entity, event.detail].join(" ").toLocaleLowerCase("es");
            return matchesType && (!query || text.includes(query));
        });
    }

    function render() {
        const events = window.MarquezaAudit.read();
        const filtered = visibleEvents(events);
        elements.total.textContent = String(events.length);
        elements.changes.textContent = String(events.filter(isChange).length);
        elements.denied.textContent = String(events.filter((event) => event.outcome === "denied").length);
        elements.errors.textContent = String(events.filter(isError).length);
        elements.results.textContent = `${filtered.length} ${filtered.length === 1 ? "evento" : "eventos"}`;
        elements.rows.replaceChildren();
        elements.empty.hidden = filtered.length > 0;

        filtered.forEach((event) => {
            const row = document.createElement("tr");
            const dateCell = document.createElement("td");
            dateCell.className = "audit-date";
            dateCell.textContent = formatDate(event.timestamp);

            const actorCell = document.createElement("td");
            actorCell.className = "audit-actor";
            actorCell.textContent = event.actor || "Sin identificar";
            const detail = String(event.detail || "").toLocaleLowerCase("es");
            const roleLabel = event.action === "Usuario no registrado" || detail.includes("usuario no registrado") || detail.includes("no hay usuarios registrados")
                ? "Usuario"
                : event.role;
            if (roleLabel) {
                const roleElement = document.createElement("small");
                roleElement.textContent = roleLabel;
                actorCell.appendChild(roleElement);
            }

            const eventCell = document.createElement("td");
            const badge = document.createElement("span");
            badge.className = `audit-badge audit-badge-${event.outcome || "success"}`;
            badge.textContent = event.action || "Actividad";
            eventCell.appendChild(badge);

            const moduleCell = document.createElement("td");
            moduleCell.textContent = event.module || "Sistema";
            const detailCell = document.createElement("td");
            detailCell.textContent = event.detail || event.entity || "Sin detalle";
            row.append(dateCell, actorCell, eventCell, moduleCell, detailCell);
            elements.rows.appendChild(row);
        });
    }

    function exportCsv() {
        const events = visibleEvents(window.MarquezaAudit.read());
        if (!events.length) return;
        const columns = ["timestamp", "actor", "email", "role", "action", "module", "entity", "detail", "outcome"];
        const quote = (value) => `"${String(value ?? "").replaceAll('"', '""')}"`;
        const content = [columns.join(","), ...events.map((event) => columns.map((column) => quote(event[column])).join(","))].join("\r\n");
        const url = URL.createObjectURL(new Blob(["\ufeff", content], { type: "text/csv;charset=utf-8" }));
        const link = document.createElement("a");
        link.href = url;
        link.download = "bitacora-marqueza.csv";
        link.click();
        URL.revokeObjectURL(url);
    }

    elements.search.addEventListener("input", render);
    elements.filter.addEventListener("change", render);
    document.getElementById("auditRefresh").addEventListener("click", render);
    document.getElementById("auditExport").addEventListener("click", exportCsv);
    window.addEventListener("storage", (event) => { if (event.key === "marqueza_bitacora") render(); });
    window.addEventListener("marqueza:audit", render);
    render();
})();