/* ============================================================
   inicio.js  —  MARQUEZA
   Maneja:
     • Toggle lateral (desktop ≥ 1025 px): Expande/colapsa la barra lateral.
     • Hamburger + menú desplegable (tablet / móvil ≤ 1024 px): Controla la barra superior responsive.
     • Drag lateral (solo desktop): Permite arrastrar la barra lateral para colapsarla.
     • Modo oscuro / claro: Cambia el tema visual de la aplicación.
     • Inicialización y redimensionamiento de gráficas ECharts.
   ============================================================ */

// Selecciona el elemento <body> del documento
const body = document.querySelector("body");
// Selecciona la barra lateral de navegación
const sidebar = body.querySelector(".barra_lateral");
// Selecciona el botón de toggle (flecha) para desktop
const toggle = body.querySelector(".toggle");
// Selecciona el botón de hamburguesa para el menú responsive
const hamburger = document.getElementById("hamburger");
// Selecciona el interruptor de modo oscuro/claro
const modeSwitch = body.querySelector(".toggle_switch");
// Selecciona el texto que indica el modo actual (Oscuro/Claro)
const modeText = body.querySelector(".modo_texto");

// Array para almacenar todas las instancias de gráficas ECharts y gestionarlas
let charts = [];

/* ─── Función de utilidad: detecta si la vista actual es de tablet/móvil (modo topbar) ─── */
const isTopbar = () => window.innerWidth <= 1024;

/* ─────────────────────────────────────────────────────────
   MODO OSCURO / CLARO
   ───────────────────────────────────────────────────────── */
// Agrega un event listener al interruptor de modo
modeSwitch.addEventListener("click", () => {
    // Alterna la clase 'dark' en el body para aplicar los estilos del modo oscuro
    body.classList.toggle("dark");
    // Actualiza el texto del modo según la clase 'dark'
    modeText.innerText = body.classList.contains("dark") ? "Claro" : "Oscuro";
    
    // Pequeño delay para asegurar que los colores CSS se apliquen antes de reinicializar las gráficas
    setTimeout(() => initCharts(), 100); 
});

// Función para redimensionar todas las gráficas
function resizeCharts() {
    // Ajuste inmediato de todas las gráficas para cambios bruscos de tamaño
    charts.forEach(chart => chart.resize());

    // Ajuste retardado para asegurar que las gráficas se redimensionen correctamente después de animaciones CSS
    setTimeout(() => {
        charts.forEach(chart => chart.resize());
    }, 600);
}

// Función para actualizar el layout del body (padding-left/padding-top) según el estado de la barra lateral
function updateLayout() {
    // Si estamos en modo topbar (tablet/móvil)
    if (isTopbar()) {
        // Elimina la clase 'sidebar-collapsed' y el padding-left
        body.classList.remove("sidebar-collapsed");
        body.style.paddingLeft = "0";
        // Usa requestAnimationFrame para leer el alto de la barra lateral DESPUÉS de que el DOM se haya actualizado
        requestAnimationFrame(() => {
            // Ajusta el padding-top del body al alto de la barra lateral
            body.style.paddingTop = `${sidebar.getBoundingClientRect().height}px`;
            resizeCharts();
        });
    // Si estamos en modo desktop
    } else {
        // Elimina el padding-top
        body.style.paddingTop = "0";
        // Si la barra lateral está colapsada
        if (sidebar.classList.contains("close")) {
            // Añade la clase 'sidebar-collapsed' y ajusta el padding-left
            body.classList.add("sidebar-collapsed");
            body.style.paddingLeft = "88px";
        // Si la barra lateral está expandida
        } else {
            // Elimina la clase 'sidebar-collapsed' y ajusta el padding-left
            body.classList.remove("sidebar-collapsed");
            body.style.paddingLeft = "250px";
        }
        resizeCharts();
    }
}

// Llama a updateLayout al cargar la página para establecer el estado inicial
updateLayout();

/* ─────────────────────────────────────────────────────────
   DESKTOP — toggle lateral (flecha)
   ───────────────────────────────────────────────────────── */
// Agrega un event listener al botón de toggle (flecha)
toggle.addEventListener("click", () => {
    if (isTopbar()) return; // Si estamos en modo topbar, la flecha está oculta, así que ignoramos el click
    // Alterna la clase 'close' en la barra lateral
    sidebar.classList.toggle("close");
    // Actualiza el layout
    updateLayout();
});

/* ─────────────────────────────────────────────────────────
   TABLET / MÓVIL — hamburger → despliega/colapsa topbar
   ───────────────────────────────────────────────────────── */
// Función para alternar el menú móvil
function toggleMobileMenu() {
    // Alterna la clase 'open' en la barra lateral y guarda el estado
    const isOpen = sidebar.classList.toggle("open");

    /* Al abrir el menú móvil, se quita la clase 'close' para evitar conflictos con estilos de desktop.
       Al cerrar, se restaura la clase 'close' para mantener la consistencia. */
    if (isOpen) {
        sidebar.classList.remove("close");
    } else {
        sidebar.classList.add("close");
    }

    // Actualiza el layout
    updateLayout();

    // Recalcular paddingTop después de que termine la animación CSS (tran-04 = 0.4s) para asegurar la posición correcta
    setTimeout(() => {
        if (isTopbar()) {
            body.style.paddingTop = `${sidebar.getBoundingClientRect().height}px`;
            resizeCharts();
        }
    }, 450);
}

// Agrega un event listener al botón de hamburguesa para alternar el menú móvil
hamburger.addEventListener("click", toggleMobileMenu);

// Accesibilidad: permite activar el menú con las teclas Enter o Espacio
hamburger.addEventListener("keydown", (e) => {
    // Previene el comportamiento por defecto del navegador para estas teclas
    if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        toggleMobileMenu();
    }
});

/* Cerrar menú al hacer click en un link (útil en móvil) */
// Itera sobre todos los enlaces de navegación
sidebar.querySelectorAll(".nav_links a").forEach(link => {
    link.addEventListener("click", () => {
        // Si estamos en modo topbar y el menú está abierto, lo cierra
        if (isTopbar() && sidebar.classList.contains("open")) {
            toggleMobileMenu();
        }
    });
});

/* ─────────────────────────────────────────────────────────
   RESIZE — sincronizar estado al cambiar tamaño de ventana
   ───────────────────────────────────────────────────────── */
let resizeTimer;
// Agrega un event listener para el evento 'resize' de la ventana
window.addEventListener("resize", () => {
    // Limpia cualquier temporizador de redimensionamiento anterior para evitar ejecuciones excesivas
    clearTimeout(resizeTimer);
    // Establece un nuevo temporizador para ejecutar updateLayout después de un breve retraso
    resizeTimer = setTimeout(() => {
        if (!isTopbar()) {
            /* Si volvemos a modo desktop: limpiar clases del topbar */
            sidebar.classList.remove("open");
            /* Restaurar el estado colapsado por defecto en desktop si no lo está */
            if (!sidebar.classList.contains("close")) {
                sidebar.classList.add("close");
            }
            sidebar.style.left = ""; // Limpiar cualquier posición residual del drag
        }
        updateLayout();
    }, 100);
});

/* ─────────────────────────────────────────────────────────
   DESKTOP — arrastrar barra lateral con el mouse
   ───────────────────────────────────────────────────────── */
let isDragging = false;
// Variables para controlar el arrastre de la barra lateral
let dragStartX = 0; // Posición inicial X del mouse al empezar a arrastrar
let sidebarStartLeft = 0; // Posición inicial 'left' de la barra lateral

// Agrega un event listener para el evento 'mousedown' en la barra lateral
sidebar.addEventListener("mousedown", (event) => {
    if (isTopbar()) return; // Desactivar el arrastre en modo topbar
    if (event.target.closest(".toggle")) return; // Ignorar si el click es en el botón de toggle
    // Si el click es en el header de la barra lateral
    if (event.target.closest("header")) {
        isDragging = true;
        dragStartX = event.clientX;
        sidebarStartLeft = sidebar.getBoundingClientRect().left;
        sidebar.classList.add("dragging");
    }
});
// Agrega un event listener para el evento 'mousemove' en todo el documento
document.addEventListener("mousemove", (event) => {
    if (!isDragging) return;

    // Calcula el desplazamiento del mouse
    const deltaX = event.clientX - dragStartX;
    let nextLeft = sidebarStartLeft + deltaX;
    
    // Define los límites de arrastre para la barra lateral
    const sidebarWidth = sidebar.offsetWidth;
    const minLeft = -sidebarWidth + 40;
    const maxLeft = 0;

    nextLeft = Math.max(minLeft, Math.min(maxLeft, nextLeft));
    sidebar.style.left = `${nextLeft}px`;
});

// Agrega un event listener para el evento 'mouseup' en todo el documento
document.addEventListener("mouseup", () => {
    if (!isDragging) return;
    isDragging = false;
    sidebar.classList.remove("dragging");

    // Decide si la barra lateral debe colapsarse o expandirse según la posición final
    if (sidebar.getBoundingClientRect().left < -sidebar.offsetWidth / 2) {
        sidebar.classList.add("close");
    } else {
        sidebar.classList.remove("close");
    }

    // Restablece la posición 'left' a 0 y actualiza el layout
    sidebar.style.left = "0";
    updateLayout();
});

sidebar.addEventListener("mouseleave", () => {
    if (isDragging) {
        isDragging = false;
        sidebar.classList.remove("dragging");
        sidebar.style.left = "0";
    }
});



/* ─────────────────────────────────────────────────────────
   CONFIGURACIÓN DE GRÁFICAS (ECharts)
   ───────────────────────────────────────────────────────── */

// Opciones para la Gráfica 1 (Área apilada)
const getOptionsGrafica1 = () => ({
    color: ['#27B7F5', '#695cfe', '#67F9D8', '#FF917C'],
  title: {
    textStyle: { color: body.classList.contains("dark") ? '#ccc' : '#333' }
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross',
      label: {
        backgroundColor: '#6a7985'
      }
    }
  },
  legend: {
    data: ['Camisas', 'Pantalones', 'Chaquetas', 'Accesorios'] // Leyenda de las series
  },
  toolbox: {
    feature: { // Herramientas disponibles (ej. guardar como imagen)
      saveAsImage: {}
    }
  },
  xAxis: [
    {
      type: 'category',
      boundaryGap: false,
      data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'] // Datos del eje X
    }
  ],
  yAxis: [
    { type: 'value', axisLabel: { color: body.classList.contains("dark") ? '#ccc' : '#666' } } // Eje Y de valores
  ],
  series: [
    {
      name: 'Camisas',
      type: 'line',
      stack: 'Total',
      smooth: true,
      lineStyle: {
        width: 0
      },
      showSymbol: false,
      areaStyle: {
        opacity: 0.8,
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          {
            offset: 0,
            color: 'rgb(128, 255, 165)'
          },
          {
            offset: 1,
            color: 'rgb(1, 191, 236)'
          }
        ])
      },
      emphasis: {
        focus: 'series'
      },
      data: [140, 232, 101, 264, 90, 340, 250]
    },
    {
      name: 'Pantalones',
      type: 'line',
      stack: 'Total',
      smooth: true,
      lineStyle: {
        width: 0
      },
      showSymbol: false,
      areaStyle: {
        opacity: 0.8,
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          {
            offset: 0,
            color: 'rgb(0, 221, 255)'
          },
          {
            offset: 1,
            color: 'rgb(77, 119, 255)'
          }
        ])
      },
      emphasis: {
        focus: 'series'
      },
      data: [120, 282, 111, 234, 220, 340, 310]
    },
    {
      name: 'Chaquetas',
      type: 'line',
      stack: 'Total',
      smooth: true,
      lineStyle: {
        width: 0
      },
      showSymbol: false,
      areaStyle: {
        opacity: 0.8,
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          {
            offset: 0,
            color: 'rgb(55, 162, 255)'
          },
          {
            offset: 1,
            color: 'rgb(116, 21, 219)'
          }
        ])
      },
      emphasis: {
        focus: 'series'
      },
      data: [320, 132, 201, 334, 190, 130, 220]
    },
    {
      name: 'Accesorios',
      type: 'line',
      stack: 'Total',
      smooth: true,
      lineStyle: {
        width: 0
      },
      showSymbol: false,
      areaStyle: {
        opacity: 0.8,
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          {
            offset: 0,
            color: 'rgb(255, 0, 135)'
          },
          {
            offset: 1,
            color: 'rgb(135, 0, 157)'
          }
        ])
      },
      emphasis: {
        focus: 'series'
      },
      data: [220, 302, 181, 234, 210, 290, 150]
    }
  ]
});

// Opciones para la Gráfica 2 (Barras horizontales)
const getOptionsGrafica2 = () => ({
    title: {
        textStyle: { color: body.classList.contains("dark") ? '#ccc' : '#333' }
    },
    tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'shadow' }
  },
  legend: {
    textStyle: { color: body.classList.contains("dark") ? '#ccc' : '#666' }, // Estilo del texto de la leyenda
    top: '10%' // Posición de la leyenda
  },
  xAxis: { 
    type: 'value',
    axisLabel: { color: body.classList.contains("dark") ? '#ccc' : '#666' } // Estilo de las etiquetas del eje X
  },
  yAxis: {
    type: 'category',
    data: ['Telas', 'Hilos', 'Botones', 'Cierres', 'Etiquetas'], // Categorías del eje Y
    axisLabel: { color: body.classList.contains("dark") ? '#ccc' : '#666' } // Estilo de las etiquetas del eje Y
  },
  series: [
    {
      name: 'Stock Actual',
      type: 'bar',
      color: '#27B7F5',
      label: {
        show: true // Mostrar etiquetas de valor en las barras
      },
      emphasis: {
        focus: 'series'
      },
      data: [320, 302, 301, 334, 390, 330, 320]
    },
    {
      name: 'Demanda Estimada',
      type: 'bar',
      color: '#695cfe',
      label: {
        show: true // Mostrar etiquetas de valor en las barras
      },
      emphasis: {
        focus: 'series'
      },
      data: [220, 182, 191, 234, 290]
    }
  ]
});

/* Gráfica 3: Configurada como un Donut Chart minimalista. Se han quitado tooltips y etiquetas para un diseño más limpio. */
const getOptionsGrafica3 = () => ({
    title: {
        left: 'center',
        textStyle: {
            color: body.classList.contains("dark") ? '#ccc' : '#333',
            fontSize: 18
        }
    },
    tooltip: { show: false }, // Tooltip deshabilitado
    legend: {
        bottom: '5%',
        left: 'center',
        textStyle: {
            color: body.classList.contains("dark") ? '#ccc' : '#666' // Color del texto de la leyenda
        }
    },
    series: [
        {
            name: 'Insumos',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: true, // Evita que las etiquetas se superpongan
            itemStyle: {
                borderRadius: 10,
                borderColor: body.classList.contains("dark") ? '#18191a' : '#fff', // Borde entre las secciones
                borderWidth: 2
            },
            label: {
                show: false,
                color: body.classList.contains("dark") ? '#ccc' : '#444'
            },
            emphasis: {
                label: {
                    show: true,
                    fontSize: 16,
                    fontWeight: 'bold'
                },
                itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            },
            data: [
                { value: 1048, name: 'Telas Algodón', itemStyle: { color: '#27B7F5' } },
                { value: 735, name: 'Hilos Poliéster', itemStyle: { color: '#695cfe' } },
                { value: 580, name: 'Botones Lujo', itemStyle: { color: '#67F9D8' } },
                { value: 484, name: 'Cierres Metálicos', itemStyle: { color: '#FFE434' } },
                { value: 300, name: 'Otros', itemStyle: { color: '#FF917C' } }
            ]
        }
    ]
});

// Opciones para la Gráfica 4 (Radar Chart)
const getOptionsGrafica4 = () => ({
    color: ['#695cfe'],
  title: {
    left: 'center',
    textStyle: { color: body.classList.contains("dark") ? '#ccc' : '#333' }
  },
  radar: {
    indicator: [ // Indicadores del radar (ejes)
      { text: 'Calidad', max: 100 },
      { text: 'Velocidad', max: 100 },
      { text: 'Eficiencia', max: 100 },
      { text: 'Desperdicio', max: 100 },
      { text: 'Puntualidad', max: 100 }
    ],
    center: ['50%', '50%'], // Centro del radar
    radius: 80,
    axisName: {
      color: body.classList.contains("dark") ? '#ccc' : '#666'
    },
    splitArea: {
      areaStyle: {
        color: body.classList.contains("dark") ? ['#242526', '#18191a'] : ['#f6f5ff', '#fff'],
        shadowColor: 'rgba(0, 0, 0, 0.2)', // Sombra del área
        shadowBlur: 10
      }
    },
    splitLine: { lineStyle: { color: body.classList.contains("dark") ? '#3a3b3c' : '#ddd' } } // Estilo de las líneas de división
  },
  series: [
    {
      type: 'radar',
      data: [
        {
          value: [80, 90, 70, 85, 75],
          name: 'Datos Actuales'
        }
      ]
    }
  ]
});

/* Generador de opciones para mini-gráficas (Sparklines) que se muestran en las tarjetas superiores (cont_info) */
const getOptionsMini = (color) => ({
    grid: { left: 0, right: 0, top: 5, bottom: 5 }, // Ajusta el grid para ocupar el mínimo espacio
    xAxis: { type: 'category', show: false }, // Oculta el eje X
    yAxis: { type: 'value', show: false }, // Oculta el eje Y
    series: [{
        data: [15, 23, 18, 35, 28, 45, 40, 55], // Datos de ejemplo para la mini-gráfica
        type: 'line', // Tipo de gráfica de línea
        smooth: true, // Línea suavizada
        showSymbol: false, // No muestra los puntos de datos
        lineStyle: { width: 2, color: color }, // Estilo de la línea
        areaStyle: { opacity: 0.1, color: color }, // Área sombreada debajo de la línea
        animationDuration: 2000 // Duración de la animación al cargar
    }]
});

/* Inicialización principal de todas las gráficas del dashboard */
const initCharts = () => {
    // Eliminar instancias previas para evitar duplicados y fugas de memoria
    charts.forEach(chart => chart.dispose());
    charts = []; // Reinicia el array de instancias de gráficas

    // Define los contenedores de las gráficas y sus opciones correspondientes
    const containers = [
        { id: "grafica_1", options: getOptionsGrafica1 },
        { id: "grafica_2", options: getOptionsGrafica2 },
        { id: "grafica_3", options: getOptionsGrafica3 },
        { id: "grafica_4", options: getOptionsGrafica4 },
        // Mini-gráficas (sparklines) para las tarjetas de información (cont_info)
        { id: "mini_1", options: () => getOptionsMini('#27B7F5') },
        { id: "mini_2", options: () => getOptionsMini('#695cfe') },
        { id: "mini_3", options: () => getOptionsMini('#67F9D8') },
        { id: "mini_4", options: () => getOptionsMini('#FF917C') }
    ];

    // Itera sobre los contenedores para inicializar cada gráfica
    containers.forEach(container => {
        const el = document.getElementById(container.id);
        if (el) {
            const chart = echarts.init(el);
            chart.setOption(container.options());
            charts.push(chart);

            // Utiliza ResizeObserver para redimensionar la gráfica automáticamente cuando su contenedor cambia de tamaño
            new ResizeObserver(() => chart.resize()).observe(el);
        }
    });
};

// Agrega un event listener para inicializar todas las gráficas cuando la página ha cargado completamente
window.addEventListener("load", () => {
    initCharts();
});