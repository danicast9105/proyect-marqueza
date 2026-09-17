const body = document.body;
const sidebar = document.querySelector(".barra_lateral");
const charts = [];
const read = (key) => {
    try {
        const value = JSON.parse(localStorage.getItem(key) || "[]");
        return Array.isArray(value) ? value : [];
    } catch {
        return [];
    }
};

const number = (value) => Number(value || 0).toLocaleString("es-CO");
const money = (value) => Number(value || 0).toLocaleString("es-CO", { style: "currency", currency: "COP", maximumFractionDigits: 0 });
const sum = (records, field) => records.reduce((total, record) => total + Number(record[field] || 0), 0);
const isTopbar = () => window.innerWidth <= 1024;

function updateLayout() {
    if (isTopbar()) {
        body.classList.remove("sidebar-collapsed");
        body.style.paddingLeft = "0";
        requestAnimationFrame(() => { body.style.paddingTop = `${sidebar.getBoundingClientRect().height}px`; resizeCharts(); });
        return;
    }
    body.style.paddingTop = "0";
    const collapsed = sidebar.classList.contains("close");
    body.classList.toggle("sidebar-collapsed", collapsed);
    body.style.paddingLeft = collapsed ? "88px" : "250px";
    resizeCharts();
}

function getDashboardData() {
    const insumos = read("marqueza_insumos");
    const productos = read("marqueza_productos");
    const ventas = read("marqueza_ventas");
    const clientes = read("marqueza_clientes");
    const proveedores = read("marqueza_proveedores");
    const usuarios = read("marqueza_usuarios");
    const cotizaciones = read("marqueza_cotizaciones");
    const stock = sum(productos, "cantidad");
    const inventoryValue = productos.reduce((total, item) => total + Number(item.cantidad || 0) * Number(item.precio || 0), 0);
    const supplyValue = insumos.reduce((total, item) => total + Number(item.cantidad || 0) * Number(item.precioUnitario || 0), 0);
    return { insumos, productos, ventas, clientes, proveedores, usuarios, cotizaciones, stock, inventoryValue, supplyValue };
}

function updateMetrics(data) {
    const openQuotes = data.cotizaciones.filter(item => item.estado !== "Rechazada").length;
    document.getElementById("metricStock").textContent = number(data.stock);
    document.getElementById("metricStockDetail").textContent = `${number(data.productos.length)} productos registrados`;
    document.getElementById("metricInventory").textContent = money(data.inventoryValue + data.supplyValue);
    document.getElementById("metricInventoryDetail").textContent = `${money(data.supplyValue)} en insumos`;
    document.getElementById("metricSales").textContent = money(sum(data.ventas, "total"));
    document.getElementById("metricSalesDetail").textContent = `${number(data.ventas.length)} operaciones registradas`;
    document.getElementById("metricClients").textContent = number(data.clientes.length);
    document.getElementById("metricClientsDetail").textContent = `${number(openQuotes)} cotizaciones abiertas`;
    document.getElementById("ultimaActualizacion").textContent = new Date().toLocaleTimeString("es-CO", { hour: "2-digit", minute: "2-digit" });
}

function monthData(records, field) {
    const labels = Array.from({ length: 6 }, (_, index) => {
        const date = new Date();
        date.setMonth(date.getMonth() - (5 - index));
        return date.toLocaleDateString("es-CO", { month: "short" }).replace(".", "");
    });
    const values = labels.map(() => 0);
    records.forEach(record => {
        const date = new Date(record.fecha);
        if (Number.isNaN(date.getTime())) return;
        const now = new Date();
        const age = (now.getFullYear() - date.getFullYear()) * 12 + now.getMonth() - date.getMonth();
        if (age >= 0 && age < 6) values[5 - age] += Number(record[field] || 0);
    });
    return { labels, values };
}

const palette = ["#1f7a8c", "#f28f6b", "#efc45b", "#6c9f8d", "#56758f", "#c96b54"];
const textColor = () => body.classList.contains("dark") ? "#dceaf1" : "#526474";
const axis = () => ({ axisLabel: { color: textColor() }, axisLine: { lineStyle: { color: body.classList.contains("dark") ? "#405361" : "#d8e1e6" } }, splitLine: { lineStyle: { color: body.classList.contains("dark") ? "#2d414e" : "#edf1f3" } } });

function chartOptions(data) {
    const sales = monthData(data.ventas, "total");
    const quotes = monthData(data.cotizaciones.filter(item => item.estado !== "Rechazada"), "total");
    const categories = [...data.insumos, ...data.productos].reduce((result, item) => {
        const category = item.categoria || "Sin categoría";
        result[category] = (result[category] || 0) + Number(item.cantidad || 0);
        return result;
    }, {});
    const categoryNames = Object.keys(categories).slice(0, 7);
    const activity = [data.insumos.length, data.productos.length, data.ventas.length, data.cotizaciones.length, data.clientes.length, data.proveedores.length, data.usuarios.length];
    const activityNames = ["Insumos", "Productos", "Ventas", "Cotizaciones", "Clientes", "Proveedores", "Usuarios"];
    const quoteStatuses = ["Pendiente", "Enviada", "Aprobada", "Rechazada"].map(status => ({ name: status, value: data.cotizaciones.filter(item => item.estado === status).length }));
    return [
        { color: [palette[0], palette[1]], tooltip: { trigger: "axis", valueFormatter: value => money(value) }, legend: { data: ["Ventas", "Cotizaciones"], textStyle: { color: textColor() } }, grid: { left: 48, right: 24, top: 35, bottom: 30 }, xAxis: { type: "category", data: sales.labels, ...axis() }, yAxis: { type: "value", ...axis() }, series: [{ name: "Ventas", type: "line", smooth: true, symbol: "circle", data: sales.values, areaStyle: { opacity: .12 }, lineStyle: { width: 3 } }, { name: "Cotizaciones", type: "line", smooth: true, data: quotes.values, lineStyle: { width: 3, type: "dashed" } }] },
        { color: [palette[0]], tooltip: { trigger: "axis" }, grid: { left: 45, right: 20, top: 20, bottom: 35 }, xAxis: { type: "category", data: categoryNames.length ? categoryNames : ["Sin datos"], axisLabel: { color: textColor(), rotate: categoryNames.length > 4 ? 25 : 0 } }, yAxis: { type: "value", ...axis() }, series: [{ type: "bar", barMaxWidth: 32, data: categoryNames.length ? categoryNames.map(name => categories[name]) : [0], itemStyle: { borderRadius: [6, 6, 0, 0] }, label: { show: true, position: "top", color: textColor() } }] },
        { tooltip: { trigger: "item", valueFormatter: value => money(value) }, color: [palette[0], palette[1]], series: [{ type: "pie", radius: ["45%", "72%"], center: ["50%", "48%"], label: { color: textColor(), formatter: "{b}\n{d}%" }, data: [{ value: data.inventoryValue, name: "Productos" }, { value: data.supplyValue, name: "Insumos" }] }] },
        { tooltip: { trigger: "axis" }, grid: { left: 68, right: 20, top: 15, bottom: 25 }, xAxis: { type: "value", ...axis() }, yAxis: { type: "category", data: activityNames, axisLabel: { color: textColor() } }, series: [{ type: "bar", data: activity, barMaxWidth: 18, itemStyle: { color: palette[1], borderRadius: [0, 6, 6, 0] }, label: { show: true, position: "right", color: textColor() } }] },
        { tooltip: { trigger: "item" }, color: ["#2a9d8f", "#27b7f5", "#1f7a8c", "#e76f51"], series: [{ type: "pie", radius: ["42%", "70%"], center: ["50%", "50%"], label: { color: textColor(), formatter: "{b}\n{c}" }, data: quoteStatuses }] }
    ];
}

function initCharts() {
    charts.splice(0).forEach(chart => chart.dispose());
    const data = getDashboardData();
    updateMetrics(data);
    const options = chartOptions(data);
    ["grafica_1", "grafica_2", "grafica_3", "grafica_4", "grafica_5"].forEach((id, index) => {
        const element = document.getElementById(id);
        if (!element) return;
        const chart = echarts.init(element);
        chart.setOption(options[index]);
        charts.push(chart);
    });
    ["mini_1", "mini_2", "mini_3", "mini_4"].forEach((id, index) => {
        const element = document.getElementById(id);
        if (!element) return;
        const chart = echarts.init(element);
        const values = [data.stock, data.inventoryValue, sum(data.ventas, "total"), data.clientes.length];
        chart.setOption({ grid: { left: 0, right: 0, top: 4, bottom: 0 }, xAxis: { show: false, type: "category", data: [1, 2, 3, 4, 5] }, yAxis: { show: false, type: "value" }, series: [{ type: "line", smooth: true, showSymbol: false, data: [0, values[index] * .55, values[index] * .76, values[index] * .9, values[index]], lineStyle: { color: palette[index], width: 2 }, areaStyle: { color: palette[index], opacity: .12 } }] });
        charts.push(chart);
    });
}

function resizeCharts() { charts.forEach(chart => chart.resize()); }

document.querySelector(".toggle_switch")?.addEventListener("click", () => setTimeout(initCharts, 120));
document.querySelector(".toggle")?.addEventListener("click", () => setTimeout(resizeCharts, 550));
document.getElementById("hamburger")?.addEventListener("click", () => setTimeout(resizeCharts, 450));
document.addEventListener("DOMContentLoaded", () => new MarquezaAppShell().init());
updateLayout();
window.addEventListener("resize", () => { clearTimeout(window.dashboardResize); window.dashboardResize = setTimeout(updateLayout, 120); });
window.addEventListener("storage", initCharts);
window.addEventListener("load", initCharts);
