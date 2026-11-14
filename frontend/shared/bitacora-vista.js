(function () {
    const rootSelector = "[data-audit-view]";
    const columns = ["timestamp", "actor", "email", "role", "action", "module", "entity", "detail", "outcome"];
    const fieldLabels = ["Fecha y hora", "Persona", "Correo", "Rol", "Evento", "Módulo", "Registro", "Detalle", "Resultado"];
    const pad = (value) => String(value).padStart(2, "0");

    function localDateKey(value) {
        const date = new Date(value);
        if (Number.isNaN(date.getTime())) return "";
        return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
    }

    function normalizeEvent(event) {
        return {
            id: String(event.uuid || event.id || `${event.timestamp}-${event.action}`),
            timestamp: event.timestamp || event.fecha_hora || "",
            actor: event.actor || "Sin identificar",
            email: event.email || event.correo || "",
            role: event.role || event.rol || "",
            action: event.action || event.accion || "Actividad",
            module: event.module || event.modulo || "Sistema",
            entity: event.entity || event.entidad || "",
            detail: event.detail || event.detalle || "",
            outcome: event.outcome || event.resultado || "success"
        };
    }

    function monthLabel(date) {
        return new Intl.DateTimeFormat("es-CO", { month: "long", year: "numeric" }).format(date);
    }

    function displayDate(value) {
        const date = new Date(value);
        return Number.isNaN(date.getTime())
            ? "Fecha no disponible"
            : new Intl.DateTimeFormat("es-CO", { dateStyle: "medium", timeStyle: "short" }).format(date);
    }

    function mount(root) {
        const showTitle = root.dataset.showTitle === "true";
        const loginOnly = root.dataset.auditMode === "logins";
        root.innerHTML = `
            ${showTitle ? `
                <header class="audit-heading">
                    <div>
                        <span class="audit-eyebrow">Seguridad y seguimiento</span>
                        <h1>Registro de actividad</h1>
                        <p>Consulta los eventos de todos los módulos por fecha.</p>
                    </div>
                </header>
            ` : loginOnly ? `
                <header class="audit-heading audit-heading-compact">
                    <div>
                        <span class="audit-eyebrow">Acceso al sistema</span>
                        <h2>Inicios de sesión</h2>
                        <p>Accesos exitosos registrados para los usuarios.</p>
                    </div>
                </header>
            ` : ""}
            ${loginOnly ? "" : `
            <section class="audit-summary" aria-label="Resumen de actividad">
                <div class="audit-stat"><span>Eventos registrados</span><strong data-audit-total>0</strong><i class="bx bx-list-ul" aria-hidden="true"></i></div>
                <div class="audit-stat"><span>Cambios en registros</span><strong data-audit-changes>0</strong><i class="bx bx-edit-alt" aria-hidden="true"></i></div>
                <div class="audit-stat audit-stat-denied"><span>Accesos rechazados</span><strong data-audit-denied>0</strong><i class="bx bx-shield-x" aria-hidden="true"></i></div>
                <div class="audit-stat audit-stat-error"><span>Errores de aplicación</span><strong data-audit-errors>0</strong><i class="bx bx-error-circle" aria-hidden="true"></i></div>
            </section>
            `}
            ${loginOnly ? "" : `
            <section class="audit-calendar" aria-label="Calendario de actividad">
                <div class="audit-calendar-heading">
                    <div><span class="audit-eyebrow">Explorar por fecha</span><h2 data-audit-month></h2></div>
                    <div class="audit-calendar-navigation">
                        <button type="button" data-audit-refresh aria-label="Actualizar bitácora" title="Actualizar bitácora"><i class="bx bx-refresh"></i></button>
                        <button type="button" data-audit-previous aria-label="Mes anterior"><i class="bx bx-chevron-left"></i></button>
                        <button type="button" data-audit-next aria-label="Mes siguiente"><i class="bx bx-chevron-right"></i></button>
                    </div>
                </div>
                <div class="audit-calendar-grid audit-weekdays" aria-hidden="true">
                    <span>Dom</span><span>Lun</span><span>Mar</span><span>Mié</span><span>Jue</span><span>Vie</span><span>Sáb</span>
                </div>
                <div class="audit-calendar-grid" data-audit-days></div>
                <p class="audit-calendar-selection" data-audit-selection aria-live="polite"></p>
            </section>
            `}
            <section class="audit-toolbar" aria-label="Buscar y exportar actividades">
                <label class="audit-search"><i class="bx bx-search" aria-hidden="true"></i><input type="search" data-audit-search placeholder="Buscar persona, módulo o detalle" aria-label="Buscar en la actividad"></label>
                ${loginOnly ? "" : `
                <label class="audit-filter-label" for="auditFilter-${root.id || "default"}">Tipo de evento</label>
                <select id="auditFilter-${root.id || "default"}" data-audit-filter aria-label="Filtrar por tipo de evento">
                    <option value="all">Todos los eventos</option>
                    <option value="changes">Cambios de registros</option>
                    <option value="access">Accesos</option>
                    <option value="errors">Errores</option>
                </select>
                `}
                <span class="audit-results" data-audit-results aria-live="polite">0 eventos</span>
                <div class="audit-export-actions" aria-label="Exportar actividades">
                    <button type="button" data-audit-export="csv"><i class="bx bx-spreadsheet"></i> CSV</button>
                    <button type="button" data-audit-export="json"><i class="bx bx-code-alt"></i> JSON</button>
                    <button type="button" data-audit-export="pdf"><i class="bx bxs-file-pdf"></i> PDF</button>
                </div>
            </section>
            <section class="audit-table-section" aria-label="Actividades de la fecha seleccionada">
                <div class="audit-table-scroll">
                    <table class="audit-table">
                        <thead><tr>${loginOnly
                            ? "<th scope=\"col\">Fecha y hora</th><th scope=\"col\">Usuario</th><th scope=\"col\">Correo</th><th scope=\"col\">Rol</th>"
                            : "<th scope=\"col\">Fecha y hora</th><th scope=\"col\">Persona</th><th scope=\"col\">Evento</th><th scope=\"col\">Módulo</th><th scope=\"col\">Detalle</th>"}</tr></thead>
                        <tbody data-audit-rows></tbody>
                    </table>
                </div>
                <p class="audit-empty" data-audit-empty hidden>No hay actividades para esta fecha.</p>
                <nav class="audit-pagination" aria-label="Paginación del registro" data-audit-pagination hidden>
                    <button type="button" data-audit-page-previous aria-label="Página anterior"><i class="bx bx-chevron-left"></i><span>Anterior</span></button>
                    <span data-audit-page-label aria-live="polite"></span>
                    <button type="button" data-audit-page-next aria-label="Página siguiente"><span>Siguiente</span><i class="bx bx-chevron-right"></i></button>
                </nav>
            </section>
            <p class="audit-note" data-audit-status role="status"><i class="bx bx-info-circle" aria-hidden="true"></i><span>Cargando bitácora...</span></p>
        `;

        const elements = {
            total: root.querySelector("[data-audit-total]"),
            changes: root.querySelector("[data-audit-changes]"),
            denied: root.querySelector("[data-audit-denied]"),
            errors: root.querySelector("[data-audit-errors]"),
            month: root.querySelector("[data-audit-month]"),
            days: root.querySelector("[data-audit-days]"),
            selection: root.querySelector("[data-audit-selection]"),
            rows: root.querySelector("[data-audit-rows]"),
            empty: root.querySelector("[data-audit-empty]"),
            pagination: root.querySelector("[data-audit-pagination]"),
            previousPage: root.querySelector("[data-audit-page-previous]"),
            nextPage: root.querySelector("[data-audit-page-next]"),
            pageLabel: root.querySelector("[data-audit-page-label]"),
            results: root.querySelector("[data-audit-results]"),
            search: root.querySelector("[data-audit-search]"),
            filter: root.querySelector("[data-audit-filter]"),
            status: root.querySelector("[data-audit-status] span")
        };

        let events = window.MarquezaAudit.read().map(normalizeEvent);
        let currentPage = 1;
        const pageSize = 20;
        const today = new Date();
        let selectedDate = localDateKey(today);
        let month = new Date(today.getFullYear(), today.getMonth(), 1);

        const isChange = (event) => String(event.action).startsWith("Registro ");
        const isAccess = (event) => String(event.module).toLowerCase() === "acceso" || event.outcome === "denied";
        const isError = (event) => event.outcome === "error";
        const isLogin = (event) => String(event.action)
            .trim()
            .toLocaleLowerCase("es")
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "") === "inicio de sesion";

        function dayEvents() {
            const query = elements.search.value.trim().toLocaleLowerCase("es");
            const filter = elements.filter?.value || "all";
            return events.filter((event) => {
                if (loginOnly) {
                    if (!isLogin(event)) return false;
                } else if (localDateKey(event.timestamp) !== selectedDate) {
                    return false;
                }
                const matchesType = filter === "all" ||
                    (filter === "changes" && isChange(event)) ||
                    (filter === "access" && isAccess(event)) ||
                    (filter === "errors" && isError(event));
                const text = [event.actor, event.email, event.action, event.module, event.entity, event.detail].join(" ").toLocaleLowerCase("es");
                return matchesType && (!query || text.includes(query));
            });
        }

        function renderCalendar() {
            elements.month.textContent = monthLabel(month);
            elements.days.replaceChildren();
            const counts = new Map();
            events.forEach((event) => {
                const key = localDateKey(event.timestamp);
                if (key) counts.set(key, (counts.get(key) || 0) + 1);
            });

            const firstWeekday = new Date(month.getFullYear(), month.getMonth(), 1).getDay();
            const daysInMonth = new Date(month.getFullYear(), month.getMonth() + 1, 0).getDate();
            for (let index = 0; index < firstWeekday; index += 1) {
                const spacer = document.createElement("span");
                spacer.className = "audit-calendar-spacer";
                spacer.setAttribute("aria-hidden", "true");
                elements.days.appendChild(spacer);
            }
            for (let day = 1; day <= daysInMonth; day += 1) {
                const key = `${month.getFullYear()}-${pad(month.getMonth() + 1)}-${pad(day)}`;
                const count = counts.get(key) || 0;
                const button = document.createElement("button");
                button.type = "button";
                button.className = `audit-calendar-day${key === selectedDate ? " is-selected" : ""}${count ? " has-events" : ""}`;
                button.setAttribute("aria-pressed", String(key === selectedDate));
                button.setAttribute("aria-label", `${day} de ${monthLabel(month)}${count ? `, ${count} actividad${count === 1 ? "" : "es"}` : ", sin actividades"}`);
                const number = document.createElement("span");
                number.textContent = String(day);
                button.appendChild(number);
                if (count) {
                    const eventCount = document.createElement("small");
                    eventCount.textContent = String(count);
                    button.appendChild(eventCount);
                }
                button.addEventListener("click", () => {
                    selectedDate = key;
                    render();
                });
                elements.days.appendChild(button);
            }
            elements.selection.textContent = new Intl.DateTimeFormat("es-CO", {
                dateStyle: "full"
            }).format(new Date(`${selectedDate}T12:00:00`));
        }

        function renderRows(filtered) {
            elements.rows.replaceChildren();
            elements.empty.hidden = filtered.length > 0;
            const pageCount = Math.max(1, Math.ceil(filtered.length / pageSize));
            currentPage = Math.min(currentPage, pageCount);
            const start = (currentPage - 1) * pageSize;
            filtered.slice(start, start + pageSize).forEach((event) => {
                const row = document.createElement("tr");
                const dateCell = document.createElement("td");
                dateCell.className = "audit-date";
                dateCell.textContent = displayDate(event.timestamp);
                const actorCell = document.createElement("td");
                actorCell.className = "audit-actor";
                actorCell.textContent = event.actor || "Sin identificar";
                if (loginOnly) {
                    const emailCell = document.createElement("td");
                    emailCell.textContent = event.email || "Sin correo";
                    const roleCell = document.createElement("td");
                    roleCell.textContent = event.role || "Sin rol";
                    row.append(dateCell, actorCell, emailCell, roleCell);
                    elements.rows.appendChild(row);
                    return;
                }
                if (event.role) {
                    const role = document.createElement("small");
                    role.textContent = event.role;
                    actorCell.appendChild(role);
                }
                const eventCell = document.createElement("td");
                const badge = document.createElement("span");
                badge.className = `audit-badge audit-badge-${event.outcome}`;
                badge.textContent = event.action;
                eventCell.appendChild(badge);
                const moduleCell = document.createElement("td");
                moduleCell.textContent = event.module;
                const detailCell = document.createElement("td");
                detailCell.textContent = event.detail || event.entity || "Sin detalle";
                row.append(dateCell, actorCell, eventCell, moduleCell, detailCell);
                elements.rows.appendChild(row);
            });
            elements.pagination.hidden = filtered.length <= pageSize;
            elements.previousPage.disabled = currentPage === 1;
            elements.nextPage.disabled = currentPage === pageCount;
            elements.pageLabel.textContent = `Página ${currentPage} de ${pageCount} · ${filtered.length} ${filtered.length === 1 ? "registro" : "registros"}`;
        }

        function render() {
            if (!loginOnly) {
                elements.total.textContent = String(events.length);
                elements.changes.textContent = String(events.filter(isChange).length);
                elements.denied.textContent = String(events.filter((event) => event.outcome === "denied").length);
                elements.errors.textContent = String(events.filter(isError).length);
            }
            const filtered = dayEvents();
            currentPage = Math.min(currentPage, Math.max(1, Math.ceil(filtered.length / pageSize)));
            const countLabel = loginOnly
                ? (filtered.length === 1 ? "inicio de sesión" : "inicios de sesión")
                : (filtered.length === 1 ? "actividad" : "actividades");
            elements.results.textContent = `${filtered.length} ${countLabel}`;
            if (!loginOnly) renderCalendar();
            renderRows(filtered);
        }

        function changeMonth(offset) {
            const day = Number(selectedDate.slice(-2));
            month = new Date(month.getFullYear(), month.getMonth() + offset, 1);
            const lastDay = new Date(month.getFullYear(), month.getMonth() + 1, 0).getDate();
            selectedDate = `${month.getFullYear()}-${pad(month.getMonth() + 1)}-${pad(Math.min(day, lastDay))}`;
            render();
        }

        function download(content, type, extension) {
            const url = URL.createObjectURL(new Blob([content], { type }));
            const link = document.createElement("a");
            link.href = url;
            link.download = `bitacora-marqueza-${selectedDate}.${extension}`;
            link.click();
            setTimeout(() => URL.revokeObjectURL(url), 1000);
        }

        function exportEvents(format) {
            const filtered = dayEvents();
            if (!filtered.length) {
                elements.status.textContent = "No hay actividades para exportar en la fecha seleccionada.";
                return;
            }
            if (format === "pdf") {
                window.print();
                return;
            }
            if (format === "json") {
                download(JSON.stringify(filtered, null, 2), "application/json;charset=utf-8", "json");
                return;
            }
            const rows = [
                fieldLabels.map((label) => `"${label}"`).join(","),
                ...filtered.map((event) => columns.map((column) => {
                    let value = String(event[column] ?? "").replaceAll('"', '""');
                    if (/^[=+\-@]/.test(value)) value = `'${value}`;
                    return `"${value}"`;
                }).join(","))
            ];
            download(`\ufeff${rows.join("\r\n")}`, "text/csv;charset=utf-8", "csv");
        }

        async function refresh() {
            elements.status.textContent = "Actualizando bitácora central...";
            try {
                events = (await window.MarquezaAudit.loadAll()).map(normalizeEvent);
                elements.status.textContent = "Bitácora central actualizada.";
            } catch (error) {
                console.error("No se pudo actualizar la bitácora central.", error);
                events = window.MarquezaAudit.read().map(normalizeEvent);
                elements.status.textContent = `No se pudo consultar la bitácora central: ${error.message}. Se muestran los registros locales.`;
            }
            render();
        }

        root.querySelector("[data-audit-refresh]")?.addEventListener("click", refresh);
        root.querySelector("[data-audit-previous]")?.addEventListener("click", () => changeMonth(-1));
        root.querySelector("[data-audit-next]")?.addEventListener("click", () => changeMonth(1));
        elements.search.addEventListener("input", () => {
            currentPage = 1;
            render();
        });
        elements.filter?.addEventListener("change", () => {
            currentPage = 1;
            render();
        });
        elements.previousPage.addEventListener("click", () => {
            currentPage = Math.max(1, currentPage - 1);
            render();
        });
        elements.nextPage.addEventListener("click", () => {
            currentPage += 1;
            render();
        });
        root.querySelectorAll("[data-audit-export]").forEach((button) => {
            button.addEventListener("click", () => exportEvents(button.dataset.auditExport));
        });
        window.addEventListener("marqueza:audit", (event) => {
            if (event.detail) events = [normalizeEvent(event.detail), ...events.filter((item) => item.id !== event.detail.id)];
            render();
        });
        window.addEventListener("storage", (event) => {
            if (event.key === "marqueza_bitacora") {
                events = window.MarquezaAudit.read().map(normalizeEvent);
                render();
            }
        });
        render();
        void refresh();
    }

    document.querySelectorAll(rootSelector).forEach(mount);
})();
