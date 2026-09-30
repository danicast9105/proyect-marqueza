class MarquezaCrudPage {
    constructor({ storageKey, modalId, formId, fields, columns }) {
        this.storageKey = storageKey;
        this.resource = storageKey.replace(/^marqueza_/, "");
        this.modal = document.getElementById(modalId);
        this.form = document.getElementById(formId);
        this.body = document.querySelector(".cont_tabla tbody");
        this.searchInput = document.querySelector(".cont_busqueda input");
        this.fields = fields;
        this.columns = columns;
        this.editIndex = -1;
    }

    init() {
        if (!this.modal || !this.form || !this.body) return;
        document.querySelector(".agregar")?.addEventListener("click", () => this.openModal());
        document.getElementById("cerrarModal")?.addEventListener("click", () => this.closeModal());
        document.getElementById("btnCancelar")?.addEventListener("click", () => this.closeModal());
        document.getElementById("btnBuscar")?.addEventListener("click", () => this.render(this.searchInput?.value || ""));
        document.getElementById("btnExportPdf")?.addEventListener("click", () => this.exportRecords());
        this.form.addEventListener("submit", (event) => this.submit(event));
        this.body.addEventListener("click", (event) => this.handleRowAction(event));
        this.searchInput?.addEventListener("input", () => this.render(this.searchInput.value));
        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape" && this.modal.classList.contains("active")) this.closeModal();
        });
        this.modal.addEventListener("click", (event) => {
            if (event.target === this.modal) this.closeModal();
        });
        window.MarquezaRealtime?.subscribe(({ key }) => {
            if (key === this.storageKey) this.render(this.searchInput?.value || "");
        });
        this.render();
        this.refreshFromApi().catch((error) => {
            window.MarquezaApi.notifyError(error, "No se pudieron cargar los datos del servidor");
        });
    }

    async refreshFromApi() {
        await window.MarquezaApi.load(this.resource, this.storageKey);
        this.render(this.searchInput?.value || "");
    }

    readRecords() {
        try {
            return JSON.parse(localStorage.getItem(this.storageKey) || "[]");
        } catch {
            return [];
        }
    }

    writeRecords(records) {
        localStorage.setItem(this.storageKey, JSON.stringify(records));
    }

    notify(options) {
        if (window.Swal) return window.Swal.fire(options);
        return Promise.resolve();
    }

    exportRecords() {
        const records = this.readRecords();
        if (!records.length) {
            this.notify({ icon: "info", title: "Sin registros", text: "No hay datos para exportar." });
            return;
        }
        const headers = this.columns.join(",");
        const rows = records.map((record) => this.columns.map((column) => {
            const value = String(record[column] ?? "").replaceAll('"', '""');
            return `"${value}"`;
        }).join(","));
        const blob = new Blob([[headers, ...rows].join("\n")], { type: "text/csv;charset=utf-8" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = `${this.storageKey}.csv`;
        link.click();
        URL.revokeObjectURL(link.href);
        this.notify({ icon: "success", title: "Exportación lista", text: "El archivo se descargó correctamente.", timer: 1600, showConfirmButton: false });
    }

    collectForm() {
        return Object.fromEntries(this.fields.map((field) => [field, document.getElementById(field)?.value.trim() || ""]));
    }

    render(query = "") {
        const normalizedQuery = query.trim().toLowerCase();
        const records = this.readRecords().map((record, index) => ({ record, index })).filter(({ record }) => {
            return !normalizedQuery || JSON.stringify(record).toLowerCase().includes(normalizedQuery);
        });

        this.body.replaceChildren();
        records.forEach(({ record, index }) => {
            const row = document.createElement("tr");
            this.columns.forEach((column) => {
                const cell = document.createElement("td");
                cell.textContent = record[column] || "";
                row.appendChild(cell);
            });
            row.appendChild(this.createActionCell("Editar", "btn-editar", index));
            row.appendChild(this.createActionCell("Eliminar", "btn-eliminar", index));
            this.body.appendChild(row);
        });
    }

    createActionCell(label, className, index) {
        const cell = document.createElement("td");
        const button = document.createElement("button");
        const icon = document.createElement("i");
        button.type = "button";
        button.className = className;
        button.dataset.index = String(index);
        button.title = label;
        button.setAttribute("aria-label", label);
        icon.className = className === "btn-editar" ? "bx bx-pencil" : "bx bx-trash-alt";
        icon.setAttribute("aria-hidden", "true");
        button.appendChild(icon);
        cell.appendChild(button);
        return cell;
    }

    openModal(index = -1) {
        this.editIndex = index;
        const record = index >= 0 ? this.readRecords()[index] : {};
        this.fields.forEach((field) => {
            const input = document.getElementById(field);
            if (input) input.value = record[field] || "";
        });
        this.modal.classList.add("active");
        this.modal.setAttribute("aria-hidden", "false");
        this.modal.querySelector("input, select, textarea")?.focus();
    }

    closeModal() {
        this.modal.classList.remove("active");
        this.modal.setAttribute("aria-hidden", "true");
        this.form.reset();
        this.editIndex = -1;
    }

    async submit(event) {
        event.preventDefault();
        const records = this.readRecords();
        const record = this.collectForm();
        if (Object.values(record).some((value) => !value)) {
            this.notify({ icon: "warning", title: "Campos incompletos", text: "Completa todos los campos antes de guardar." });
            return;
        }
        const editing = this.editIndex >= 0;
        const currentRecord = editing ? records[this.editIndex] : null;
        try {
            if (editing && currentRecord.id !== undefined && currentRecord.id !== null) {
                await window.MarquezaApi.update(this.resource, currentRecord.id, record);
            } else {
                await window.MarquezaApi.create(this.resource, record);
                if (editing) window.MarquezaApi.consumeLegacy(this.storageKey, currentRecord.__localKey);
            }
        } catch (error) {
            window.MarquezaApi.notifyError(error, "No se pudo guardar el registro");
            return;
        }
        window.MarquezaAudit?.recordChange(editing ? "update" : "create", this.storageKey, record);
        this.closeModal();
        try {
            await this.refreshFromApi();
        } catch (error) {
            window.MarquezaApi.notifyError(error, "El cambio se guardó, pero no se pudo actualizar la lista");
        }
        this.notify({ icon: "success", title: editing ? "Registro actualizado" : "Registro guardado", text: editing ? "Los cambios se guardaron correctamente." : "El registro se agregó correctamente.", timer: 1600, showConfirmButton: false });
    }

    async handleRowAction(event) {
        const button = event.target.closest("button[data-index]");
        if (!button) return;
        const index = Number(button.dataset.index);
        if (button.classList.contains("btn-editar")) {
            this.openModal(index);
            return;
        }
        if (!button.classList.contains("btn-eliminar")) return;
        if (!window.Swal) return;
        const result = await window.Swal.fire({ icon: "warning", title: "¿Eliminar registro?", text: "Esta acción no se puede deshacer.", showCancelButton: true, confirmButtonText: "Eliminar", cancelButtonText: "Cancelar", confirmButtonColor: "#d4554d" });
        if (!result.isConfirmed) return;
        const record = this.readRecords()[index];
        try {
            if (record.id === undefined || record.id === null) {
                window.MarquezaApi.consumeLegacy(this.storageKey, record.__localKey);
            } else {
                await window.MarquezaApi.remove(this.resource, record.id);
            }
            window.MarquezaAudit?.recordChange("delete", this.storageKey, record);
        } catch (error) {
            window.MarquezaApi.notifyError(error, "No se pudo eliminar el registro");
            return;
        }
        try {
            await this.refreshFromApi();
        } catch (error) {
            window.MarquezaApi.notifyError(error, "El registro se eliminó, pero no se pudo actualizar la lista");
        }
        this.notify({ icon: "success", title: "Registro eliminado", text: "El registro se eliminó correctamente.", timer: 1600, showConfirmButton: false });
    }
}

window.MarquezaCrudPage = MarquezaCrudPage;
