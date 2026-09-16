class MarquezaCrudPage {
    constructor({ storageKey, modalId, formId, fields, columns }) {
        this.storageKey = storageKey;
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
        this.form.addEventListener("submit", (event) => this.submit(event));
        this.body.addEventListener("click", (event) => this.handleRowAction(event));
        this.searchInput?.addEventListener("input", () => this.render(this.searchInput.value));
        this.render();
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
        button.type = "button";
        button.className = className;
        button.dataset.index = String(index);
        button.textContent = label;
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
    }

    closeModal() {
        this.modal.classList.remove("active");
        this.form.reset();
        this.editIndex = -1;
    }

    submit(event) {
        event.preventDefault();
        const records = this.readRecords();
        const record = this.collectForm();
        if (this.editIndex >= 0) records[this.editIndex] = record;
        else records.push(record);
        this.writeRecords(records);
        this.closeModal();
        this.render(this.searchInput?.value || "");
    }

    handleRowAction(event) {
        const button = event.target.closest("button[data-index]");
        if (!button) return;
        const index = Number(button.dataset.index);
        if (button.classList.contains("btn-editar")) {
            this.openModal(index);
            return;
        }
        if (button.classList.contains("btn-eliminar") && confirm("¿Eliminar registro?")) {
            const records = this.readRecords();
            records.splice(index, 1);
            this.writeRecords(records);
            this.render(this.searchInput?.value || "");
        }
    }
}

window.MarquezaCrudPage = MarquezaCrudPage;
