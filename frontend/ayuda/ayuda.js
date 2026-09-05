const body = document.querySelector("body");
const sidebar = body?.querySelector(".barra_lateral");
const toggle = body?.querySelector(".toggle");
const hamburger = document.getElementById("hamburger");
const modeSwitch = body?.querySelector(".toggle_switch");
const modeText = body?.querySelector(".modo_texto");

const isTopbar = () => window.innerWidth <= 1024;

function updateLayout() {
    if (!body || !sidebar) return;

    if (isTopbar()) {
        body.classList.remove("sidebar-collapsed");
        body.style.paddingLeft = "0";
        requestAnimationFrame(() => {
            body.style.paddingTop = `${sidebar.getBoundingClientRect().height}px`;
        });
    } else {
        body.style.paddingTop = "0";
        if (sidebar.classList.contains("close")) {
            body.classList.add("sidebar-collapsed");
            body.style.paddingLeft = "88px";
        } else {
            body.classList.remove("sidebar-collapsed");
            body.style.paddingLeft = "250px";
        }
    }
}

if (modeSwitch && modeText) {
    modeSwitch.addEventListener("click", () => {
        body.classList.toggle("dark");
        modeText.textContent = body.classList.contains("dark") ? "Claro" : "Oscuro";
    });
}

if (toggle) {
    toggle.addEventListener("click", () => {
        if (isTopbar()) return;
        sidebar.classList.toggle("close");
        updateLayout();
    });
}

function toggleMobileMenu() {
    if (!sidebar) return;

    const isOpen = sidebar.classList.toggle("open");
    sidebar.classList[isOpen ? "remove" : "add"]("close");
    updateLayout();

    setTimeout(() => {
        if (isTopbar()) {
            body.style.paddingTop = `${sidebar.getBoundingClientRect().height}px`;
        }
    }, 450);
}

hamburger?.addEventListener("click", toggleMobileMenu);

hamburger?.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        toggleMobileMenu();
    }
});

sidebar?.querySelectorAll(".nav_links a").forEach((link) => {
    link.addEventListener("click", () => {
        if (isTopbar() && sidebar.classList.contains("open")) {
            toggleMobileMenu();
        }
    });
});

let resizeTimer;
window.addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
        if (!isTopbar() && sidebar) {
            sidebar.classList.remove("open");
            if (!sidebar.classList.contains("close")) {
                sidebar.classList.add("close");
            }
            sidebar.style.left = "";
        }
        updateLayout();
    }, 100);
});

let isDragging = false;
let dragStartX = 0;
let sidebarStartLeft = 0;

sidebar?.addEventListener("mousedown", (event) => {
    if (isTopbar()) return;
    if (event.target.closest(".toggle")) return;
    if (event.target.closest("header")) {
        isDragging = true;
        dragStartX = event.clientX;
        sidebarStartLeft = sidebar.getBoundingClientRect().left;
        sidebar.classList.add("dragging");
    }
});

document.addEventListener("mousemove", (event) => {
    if (!isDragging || !sidebar) return;

    const deltaX = event.clientX - dragStartX;
    let nextLeft = sidebarStartLeft + deltaX;
    const sidebarWidth = sidebar.offsetWidth;
    const minLeft = -sidebarWidth + 40;
    const maxLeft = 0;

    nextLeft = Math.max(minLeft, Math.min(maxLeft, nextLeft));
    sidebar.style.left = `${nextLeft}px`;
});

document.addEventListener("mouseup", () => {
    if (!isDragging || !sidebar) return;

    isDragging = false;
    sidebar.classList.remove("dragging");

    if (sidebar.getBoundingClientRect().left < -sidebar.offsetWidth / 2) {
        sidebar.classList.add("close");
    } else {
        sidebar.classList.remove("close");
    }

    sidebar.style.left = "0";
    updateLayout();
});

sidebar?.addEventListener("mouseleave", () => {
    if (isDragging) {
        isDragging = false;
        sidebar.classList.remove("dragging");
        sidebar.style.left = "0";
    }
});

const searchInput = document.querySelector('.cont_busqueda input');
const searchButton = document.getElementById('btnBuscar');
const filterButtons = Array.from(document.querySelectorAll('.estado-btn'));
const helpCards = Array.from(document.querySelectorAll('.caja_ayuda'));
const noResultsMessage = document.createElement('p');

noResultsMessage.className = 'sin-resultados';
noResultsMessage.textContent = 'No se encontraron bloques de ayuda con esos filtros.';
noResultsMessage.style.display = 'none';
noResultsMessage.style.marginTop = '12px';
noResultsMessage.style.color = '#707070';

const containerAyuda = document.querySelector('.cont_ayuda');
if (containerAyuda) {
    containerAyuda.appendChild(noResultsMessage);
}

const getCategoryFromCard = (card) => card.dataset.category || 'General';

function filterHelpCards() {
    const query = searchInput?.value.trim().toLowerCase() || '';
    const selectedFilter = document.querySelector('.estado-btn.active')?.dataset.filter || 'Todos';
    let visibleCount = 0;

    helpCards.forEach((card) => {
        const text = card.textContent.toLowerCase();
        const matchesQuery = !query || text.includes(query);
        const matchesFilter = selectedFilter === 'Todos' || getCategoryFromCard(card) === selectedFilter;
        const shouldShow = matchesQuery && matchesFilter;

        card.style.display = shouldShow ? 'block' : 'none';
        if (shouldShow) visibleCount += 1;
    });

    if (noResultsMessage) {
        noResultsMessage.style.display = visibleCount === 0 ? 'block' : 'none';
    }
}

filterButtons.forEach((button) => {
    button.addEventListener('click', () => {
        filterButtons.forEach((btn) => btn.classList.remove('active'));
        button.classList.add('active');
        filterHelpCards();
    });
});

if (searchInput) {
    searchInput.addEventListener('input', filterHelpCards);
    searchInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            filterHelpCards();
        }
    });
}

if (searchButton) {
    searchButton.addEventListener('click', filterHelpCards);
}

filterHelpCards();
updateLayout();