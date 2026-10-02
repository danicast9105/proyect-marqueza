-- =============================================================================
-- BASE DE DATOS: MARQUEZA — CONFECCIONES QUE INSPIRAN
-- Sistema de Gestión Integral de Confecciones (ERP / Pyme)
-- Archivo: database_marqueza.sql
-- Generado tras el análisis exhaustivo de todos los módulos del Frontend:
--   - frontend/inicio          (Dashboard, métricas ejecutivas y gráficos)
--   - frontend/clientes        (Directorio de clientes y contactos)
--   - frontend/proveedores     (Aliados comerciales y personas de contacto)
--   - frontend/productos       (Catálogo, stock, precios y categorías)
--   - frontend/insumos         (Materia prima, inventario, unidades y proveedores)
--   - frontend/ventas          (Operaciones comerciales, pedidos e ingresos)
--   - frontend/cotizaciones    (Propuestas comerciales, estados y líneas de productos)
--   - frontend/usuarios        (Cuentas, roles y control de acceso)
--   - frontend/inicio_sesion   (Autenticación de usuarios)
--   - frontend/olvido_contrasena (Recuperación y registro de usuarios)
--   - frontend/log_errores     (Bitácora de actividad, trazabilidad y errores)
-- Compatible con Backend Flask (backend/API/Models & Services) y MySQL / MariaDB
-- Motor: InnoDB | Codificación: UTF-8 (utf8mb4)
-- =============================================================================

CREATE DATABASE IF NOT EXISTS `marqueza_db`
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE `marqueza_db`;

-- Desactivar temporalmente revisión de claves foráneas para reconstrucción limpia
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `T_BITACORA_AUDITORIA`;
DROP TABLE IF EXISTS `T_RECUPERACION_CONTRASENA`;
DROP TABLE IF EXISTS `T_DETALLE_COTIZACION`;
DROP TABLE IF EXISTS `T_COTIZACIONES`;
DROP TABLE IF EXISTS `T_VENT_PROD`;
DROP TABLE IF EXISTS `T_VENTAS`;
DROP TABLE IF EXISTS `T_PRODU_INSUM`;
DROP TABLE IF EXISTS `T_PRODUCTOS`;
DROP TABLE IF EXISTS `T_INSUMOS`;
DROP TABLE IF EXISTS `T_CONTACTO`;
DROP TABLE IF EXISTS `T_PROVEEDORES`;
DROP TABLE IF EXISTS `T_CLIENTE`;
DROP TABLE IF EXISTS `T_USUARIOS`;
DROP TABLE IF EXISTS `T_DETALLES_ETC`;
DROP TABLE IF EXISTS `T_ESTADO_TIPOS_CATEGORIAS`;
DROP TABLE IF EXISTS `T_PERSONA`;

SET FOREIGN_KEY_CHECKS = 1;

-- =============================================================================
-- 1. TABLA MAESTRA DE CONFIGURACIÓN Y METADATOS: ETC
-- (Estados, Tipos y Categorías)
-- Mapea los catálogos del sistema (Roles, Categorías de producto, Insumos, etc.)
-- =============================================================================
CREATE TABLE `T_ESTADO_TIPOS_CATEGORIAS` (
    `ETC_ID` INT AUTO_INCREMENT PRIMARY KEY,
    `ETC_UUID` CHAR(36) NOT NULL UNIQUE,
    `ETC_NOMBRE` VARCHAR(100) NOT NULL COMMENT 'Nombre del grupo: ROLES, CAT_PRODUCTOS, CAT_INSUMOS, UNIDADES, ESTADOS_COTIZACION, etc.',
    `ETC_DESCRIPCION` VARCHAR(255) NULL,
    `ETC_FECHA_CREACION` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Grupos principales de tipos y clasificaciones';

-- =============================================================================
-- 2. TABLA DETALLES DE ETC
-- Registra los elementos individuales de cada categoría/estado/tipo
-- =============================================================================
CREATE TABLE `T_DETALLES_ETC` (
    `DET_ETC_ID` INT AUTO_INCREMENT PRIMARY KEY,
    `DET_ETC_UUID` CHAR(36) NOT NULL UNIQUE,
    `DET_ETC_NOMBRE` VARCHAR(100) NOT NULL COMMENT 'Ej: Administrador, Empleado, Camisetas, Pantalones, Telas, etc.',
    `DET_ETC_ETC_ID` INT NOT NULL COMMENT 'Referencia al grupo en T_ESTADO_TIPOS_CATEGORIAS',
    `DET_ETC_PER_ID` INT NULL COMMENT 'Persona creadora/asociada opcional',
    `DET_ETC_DESCRIPCION` VARCHAR(255) NULL,
    `DET_ETC_FECHA_CREACION` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `FK_DET_ETC_GRUPO` FOREIGN KEY (`DET_ETC_ETC_ID`) 
        REFERENCES `T_ESTADO_TIPOS_CATEGORIAS` (`ETC_ID`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Valores detallados de configuraciones, tipos y clasificaciones';

-- =============================================================================
-- 3. TABLA PERSONA
-- Contiene los datos personales unificados tanto para Clientes como para Contactos de Proveedores
-- =============================================================================
CREATE TABLE `T_PERSONA` (
    `PER_ID` INT AUTO_INCREMENT PRIMARY KEY,
    `PER_UUID` CHAR(36) NOT NULL UNIQUE,
    `PER_NOMBRE` VARCHAR(60) NOT NULL COMMENT 'Primer nombre o nombre completo',
    `PER_SEG_NOMBRE` VARCHAR(60) NULL COMMENT 'Segundo nombre opcional',
    `PER_PRI_APELLIDO` VARCHAR(60) NULL COMMENT 'Primer apellido',
    `PER_SEG_APELLIDO` VARCHAR(60) NULL COMMENT 'Segundo apellido',
    `PER_CORREO` VARCHAR(150) NULL COMMENT 'Correo electrónico de contacto',
    `PER_DIRECCION` VARCHAR(255) NULL COMMENT 'Dirección física o de entrega',
    `PER_IDENTIFICACION` VARCHAR(50) NOT NULL UNIQUE COMMENT 'Cédula, NIT, pasaporte o documento de identidad',
    `PER_TELEFONO` VARCHAR(30) NULL COMMENT 'Teléfono fijo o móvil de contacto',
    `PER_FECHA_CREACION` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `PER_FECHA_ACTUALIZACION` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `IDX_PERSONA_IDENTIFICACION` (`PER_IDENTIFICACION`),
    INDEX `IDX_PERSONA_CORREO` (`PER_CORREO`),
    INDEX `IDX_PERSONA_NOMBRE` (`PER_NOMBRE`, `PER_PRI_APELLIDO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Entidad central para datos biográficos y de contacto';

-- =============================================================================
-- 4. TABLA USUARIOS (Control de acceso, login, registro y roles)
-- Módulo: frontend/usuarios, frontend/inicio_sesion, frontend/olvido_contrasena
-- =============================================================================
CREATE TABLE `T_USUARIOS` (
    `USUA_ID` INT AUTO_INCREMENT PRIMARY KEY,
    `USUA_UUID` CHAR(36) NOT NULL UNIQUE,
    `USUA_NOMBRE` VARCHAR(100) NOT NULL UNIQUE COMMENT 'Nombre de usuario o nombre completo para iniciar sesión',
    `USUA_CORREO` VARCHAR(150) NOT NULL UNIQUE COMMENT 'Correo electrónico para autenticación y recuperación',
    `USUA_CONTRASENA` VARCHAR(255) NOT NULL COMMENT 'Contraseña encriptada o hash de seguridad',
    `USUA_ESTADO` ENUM('Activo', 'Inactivo') NOT NULL DEFAULT 'Activo' COMMENT 'Estado de la cuenta en el sistema',
    `USUA_DET_ETC_ID` INT NOT NULL COMMENT 'Rol del usuario (Administrador, Empleado, etc.) ref a T_DETALLES_ETC',
    `USUA_ULTIMO_ACCESO` DATETIME NULL COMMENT 'Fecha y hora del último inicio de sesión',
    `USUA_FECHA_CREACION` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `USUA_FECHA_ACTUALIZACION` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `FK_USUARIO_ROL` FOREIGN KEY (`USUA_DET_ETC_ID`) 
        REFERENCES `T_DETALLES_ETC` (`DET_ETC_ID`) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX `IDX_USUARIO_CORREO` (`USUA_CORREO`),
    INDEX `IDX_USUARIO_ESTADO` (`USUA_ESTADO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Usuarios del sistema con roles y accesos';

-- =============================================================================
-- 5. TABLA CLIENTES
-- Módulo: frontend/clientes
-- =============================================================================
CREATE TABLE `T_CLIENTE` (
    `CLI_ID` INT AUTO_INCREMENT PRIMARY KEY,
    `CLI_UUID` CHAR(36) NOT NULL UNIQUE,
    `CLI_PER_ID` INT NOT NULL UNIQUE COMMENT 'Relación biunívoca con T_PERSONA',
    `CLI_ESTADO` ENUM('Activo', 'Inactivo') NOT NULL DEFAULT 'Activo',
    `CLI_NOTAS` TEXT NULL COMMENT 'Observaciones o condiciones comerciales',
    `CLI_FECHA_CREACION` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `CLI_FECHA_ACTUALIZACION` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `FK_CLIENTE_PERSONA` FOREIGN KEY (`CLI_PER_ID`) 
        REFERENCES `T_PERSONA` (`PER_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX `IDX_CLIENTE_ESTADO` (`CLI_ESTADO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Registro de clientes comerciales';

-- =============================================================================
-- 6. TABLA PROVEEDORES
-- Módulo: frontend/proveedores
-- =============================================================================
CREATE TABLE `T_PROVEEDORES` (
    `PROV_ID` INT AUTO_INCREMENT PRIMARY KEY,
    `PROV_UUID` CHAR(36) NOT NULL UNIQUE,
    `PROV_EMPRESA` VARCHAR(150) NOT NULL COMMENT 'Razón social o nombre comercial de la empresa proveedora',
    `PROV_PER_ID` INT NULL COMMENT 'Persona de contacto principal referenciada en T_PERSONA',
    `PROV_DIRECCION` VARCHAR(255) NULL COMMENT 'Dirección de la empresa proveedora',
    `PROV_TELEFONO` VARCHAR(50) NULL COMMENT 'Teléfono de contacto de la empresa',
    `PROV_CORREO` VARCHAR(150) NULL COMMENT 'Correo empresarial',
    `PROV_ESTADO` ENUM('Activo', 'Inactivo') NOT NULL DEFAULT 'Activo',
    `PROV_FECHA_CREACION` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `PROV_FECHA_ACTUALIZACION` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `FK_PROVEEDOR_PERSONA` FOREIGN KEY (`PROV_PER_ID`) 
        REFERENCES `T_PERSONA` (`PER_ID`) ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX `IDX_PROVEEDOR_EMPRESA` (`PROV_EMPRESA`),
    INDEX `IDX_PROVEEDOR_ESTADO` (`PROV_ESTADO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Aliados comerciales y proveedores de materiales';

-- =============================================================================
-- 7. TABLA CONTACTOS ADICIONALES DE PROVEEDORES
-- Permite registrar múltiples canales de contacto (Móvil, WhatsApp, PBX, etc.)
-- =============================================================================
CREATE TABLE `T_CONTACTO` (
    `CONT_ID` INT AUTO_INCREMENT PRIMARY KEY,
    `CONT_UUID` CHAR(36) NOT NULL UNIQUE,
    `CONT_TIPO_DATO` VARCHAR(50) NOT NULL COMMENT 'Teléfono, Correo, Celular, WhatsApp, Asesor comercial',
    `CONT_CONTENIDO` VARCHAR(200) NOT NULL COMMENT 'El valor del canal de contacto',
    `CONT_PROV_ID` INT NOT NULL COMMENT 'Proveedor al cual pertenece el contacto',
    `CONT_FECHA_CREACION` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `FK_CONTACTO_PROVEEDOR` FOREIGN KEY (`CONT_PROV_ID`) 
        REFERENCES `T_PROVEEDORES` (`PROV_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX `IDX_CONTACTO_PROV` (`CONT_PROV_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Canales adicionales de comunicación para proveedores';

-- =============================================================================
-- 8. TABLA INSUMOS (Materiales de confección)
-- Módulo: frontend/insumos
-- =============================================================================
CREATE TABLE `T_INSUMOS` (
    `INS_ID` INT AUTO_INCREMENT PRIMARY KEY,
    `INS_UUID` CHAR(36) NOT NULL UNIQUE,
    `INS_CODIGO` VARCHAR(50) NOT NULL UNIQUE COMMENT 'Código único del insumo (ej: INS-001)',
    `INS_NOMBRE` VARCHAR(150) NOT NULL COMMENT 'Nombre del insumo (ej: Tela dril, Botón nacarado)',
    `INS_CANTIDAD` DECIMAL(12, 2) NOT NULL DEFAULT 0.00 COMMENT 'Existencias actuales en inventario',
    `INS_UNIDAD` VARCHAR(50) NOT NULL DEFAULT 'metros' COMMENT 'Unidad de medida: metros, piezas, rollos, conos, etc.',
    `INS_PRECIO` DECIMAL(14, 2) NOT NULL DEFAULT 0.00 COMMENT 'Precio o costo unitario en COP',
    `INS_ESTADO` ENUM('Disponible', 'Agotado', 'Pedido') NOT NULL DEFAULT 'Disponible' COMMENT 'Estado operativo del insumo',
    `INS_STOCK_MINIMO` DECIMAL(12, 2) NOT NULL DEFAULT 10.00 COMMENT 'Umbral para alertas de stock bajo',
    `INS_USUA_ID` INT NULL COMMENT 'Usuario que registró o modificó el insumo',
    `INS_PROV_ID` INT NULL COMMENT 'Proveedor del insumo',
    `INS_DET_ETC_ID` INT NULL COMMENT 'Categoría del insumo en T_DETALLES_ETC (Telas, Hilos, etc.)',
    `INS_FECHA_CREACION` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `INS_FECHA_ACTUALIZACION` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `FK_INSUMO_USUARIO` FOREIGN KEY (`INS_USUA_ID`) 
        REFERENCES `T_USUARIOS` (`USUA_ID`) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT `FK_INSUMO_PROVEEDOR` FOREIGN KEY (`INS_PROV_ID`) 
        REFERENCES `T_PROVEEDORES` (`PROV_ID`) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT `FK_INSUMO_CATEGORIA` FOREIGN KEY (`INS_DET_ETC_ID`) 
        REFERENCES `T_DETALLES_ETC` (`DET_ETC_ID`) ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX `IDX_INSUMO_CODIGO` (`INS_CODIGO`),
    INDEX `IDX_INSUMO_NOMBRE` (`INS_NOMBRE`),
    INDEX `IDX_INSUMO_ESTADO` (`INS_ESTADO`),
    INDEX `IDX_INSUMO_CANTIDAD` (`INS_CANTIDAD`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Inventario de insumos y materias primas de confección';

-- =============================================================================
-- 9. TABLA PRODUCTOS (Prendas terminadas y catálogo)
-- Módulo: frontend/productos
-- =============================================================================
CREATE TABLE `T_PRODUCTOS` (
    `PROD_ID` INT AUTO_INCREMENT PRIMARY KEY,
    `PROD_UUID` CHAR(36) NOT NULL UNIQUE,
    `PROD_CODIGO` VARCHAR(50) NOT NULL UNIQUE COMMENT 'Código comercial de la prenda (ej: P001, P002)',
    `PROD_NOMBRE` VARCHAR(150) NOT NULL COMMENT 'Nombre de la prenda (ej: Camiseta básica, Pantalón jean)',
    `PROD_CANTIDAD` INT NOT NULL DEFAULT 0 COMMENT 'Unidades disponibles en stock',
    `PROD_PRECIO` DECIMAL(14, 2) NOT NULL DEFAULT 0.00 COMMENT 'Precio de venta al público en COP',
    `PROD_ESTADO` ENUM('Activo', 'Inactivo') NOT NULL DEFAULT 'Activo' COMMENT 'Estado en el catálogo',
    `PROD_STOCK_MINIMO` INT NOT NULL DEFAULT 5 COMMENT 'Umbral para semáforo: <= 5 Bajo, 6-20 Medio, > 20 Bueno',
    `PROD_USUA_ID` INT NULL COMMENT 'Usuario creador / administrador',
    `PROD_DET_ETC_ID` INT NULL COMMENT 'Categoría de producto en T_DETALLES_ETC (Camisetas, Pantalones, etc.)',
    `PROD_FECHA_CREACION` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `PROD_FECHA_ACTUALIZACION` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `FK_PRODUCTO_USUARIO` FOREIGN KEY (`PROD_USUA_ID`) 
        REFERENCES `T_USUARIOS` (`USUA_ID`) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT `FK_PRODUCTO_CATEGORIA` FOREIGN KEY (`PROD_DET_ETC_ID`) 
        REFERENCES `T_DETALLES_ETC` (`DET_ETC_ID`) ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX `IDX_PRODUCTO_CODIGO` (`PROD_CODIGO`),
    INDEX `IDX_PRODUCTO_NOMBRE` (`PROD_NOMBRE`),
    INDEX `IDX_PRODUCTO_ESTADO` (`PROD_ESTADO`),
    INDEX `IDX_PRODUCTO_CANTIDAD` (`PROD_CANTIDAD`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Catálogo de prendas terminadas y existencias';

-- =============================================================================
-- 10. TABLA FICHA TÉCNICA / RELACIÓN PRODUCTO-INSUMO (BOM - Bill of Materials)
-- Define la cantidad de insumos consumidos para fabricar una prenda terminada
-- =============================================================================
CREATE TABLE `T_PRODU_INSUM` (
    `PROINSU_ID` INT AUTO_INCREMENT PRIMARY KEY,
    `PROINSU_UUID` CHAR(36) NOT NULL UNIQUE,
    `PROINSU_CANTIDAD` DECIMAL(12, 2) NOT NULL COMMENT 'Cantidad de insumo consumida por unidad de producto terminado',
    `PROINSU_PROD_ID` INT NOT NULL COMMENT 'Prenda terminada',
    `PROINSU_INS_ID` INT NOT NULL COMMENT 'Insumo requerido',
    `PROINSU_FECHA_CREACION` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `FK_BOM_PRODUCTO` FOREIGN KEY (`PROINSU_PROD_ID`) 
        REFERENCES `T_PRODUCTOS` (`PROD_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `FK_BOM_INSUMO` FOREIGN KEY (`PROINSU_INS_ID`) 
        REFERENCES `T_INSUMOS` (`INS_ID`) ON DELETE RESTRICT ON UPDATE CASCADE,
    UNIQUE KEY `UQ_PROD_INSUMO` (`PROINSU_PROD_ID`, `PROINSU_INS_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Estructura de materiales por prenda (Ficha técnica)';

-- =============================================================================
-- 11. TABLA VENTAS (Encabezado de pedidos u operaciones comerciales)
-- Módulo: frontend/ventas
-- =============================================================================
CREATE TABLE `T_VENTAS` (
    `VENT_ID` INT AUTO_INCREMENT PRIMARY KEY,
    `VENT_UUID` CHAR(36) NOT NULL UNIQUE,
    `VENT_NUMERO_FACTURA` VARCHAR(50) NULL UNIQUE COMMENT 'Número consecutivo de venta/remisión (ej: VNT-2026-001)',
    `VENT_FECHA` DATE NOT NULL COMMENT 'Fecha de la transacción',
    `VENT_TOTAL` DECIMAL(14, 2) NOT NULL DEFAULT 0.00 COMMENT 'Valor total acumulado de la venta en COP',
    `VENT_ESTADO` ENUM('Completada', 'Pendiente', 'Cancelada') NOT NULL DEFAULT 'Completada',
    `VENT_USUA_ID` INT NULL COMMENT 'Usuario/Vendedor que procesó la venta',
    `VENT_CLI_ID` INT NOT NULL COMMENT 'Cliente que realiza la compra',
    `VENT_OBSERVACIONES` VARCHAR(255) NULL,
    `VENT_FECHA_CREACION` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `VENT_FECHA_ACTUALIZACION` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `FK_VENTA_USUARIO` FOREIGN KEY (`VENT_USUA_ID`) 
        REFERENCES `T_USUARIOS` (`USUA_ID`) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT `FK_VENTA_CLIENTE` FOREIGN KEY (`VENT_CLI_ID`) 
        REFERENCES `T_CLIENTE` (`CLI_ID`) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX `IDX_VENTA_FECHA` (`VENT_FECHA`),
    INDEX `IDX_VENTA_CLIENTE` (`VENT_CLI_ID`),
    INDEX `IDX_VENTA_ESTADO` (`VENT_ESTADO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Encabezado de transacciones de venta y pedidos';

-- =============================================================================
-- 12. TABLA DETALLE DE VENTAS (Items vendidos por pedido)
-- Permite asociar uno o más productos a cada venta
-- =============================================================================
CREATE TABLE `T_VENT_PROD` (
    `VENTPRO_ID` INT AUTO_INCREMENT PRIMARY KEY,
    `VENTPRO_UUID` CHAR(36) NOT NULL UNIQUE,
    `VENTPRO_CANTIDAD` INT NOT NULL DEFAULT 1 COMMENT 'Cantidad de unidades vendidas',
    `VENTPRO_PRECIO_UNITARIO` DECIMAL(14, 2) NOT NULL DEFAULT 0.00 COMMENT 'Precio unitario aplicado en el momento de la venta',
    `VENTPRO_SUBTOTAL` DECIMAL(14, 2) NOT NULL DEFAULT 0.00 COMMENT 'Subtotal = Cantidad * Precio Unitario',
    `VENTPRO_VENT_ID` INT NOT NULL COMMENT 'Venta a la que pertenece',
    `VENTPRO_PROD_ID` INT NOT NULL COMMENT 'Producto comercializado',
    `VENTPRO_FECHA_CREACION` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `FK_DETALLE_VENTA` FOREIGN KEY (`VENTPRO_VENT_ID`) 
        REFERENCES `T_VENTAS` (`VENT_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `FK_DETALLE_PRODUCTO` FOREIGN KEY (`VENTPRO_PROD_ID`) 
        REFERENCES `T_PRODUCTOS` (`PROD_ID`) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX `IDX_VENT_PROD_VENTA` (`VENTPRO_VENT_ID`),
    INDEX `IDX_VENT_PROD_PRODUCTO` (`VENTPRO_PROD_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Líneas de detalle de productos por transacción de venta';

-- =============================================================================
-- 13. TABLA COTIZACIONES (Encabezado de propuestas comerciales)
-- Módulo: frontend/cotizaciones
-- =============================================================================
CREATE TABLE `T_COTIZACIONES` (
    `COT_ID` INT AUTO_INCREMENT PRIMARY KEY,
    `COT_UUID` CHAR(36) NOT NULL UNIQUE,
    `COT_NUMERO` VARCHAR(50) NULL UNIQUE COMMENT 'Número consecutivo de cotización (ej: COT-2026-001)',
    `COT_FECHA` DATE NOT NULL COMMENT 'Fecha de expedición de la propuesta',
    `COT_TOTAL_PAGAR` DECIMAL(14, 2) NOT NULL DEFAULT 0.00 COMMENT 'Valor total cotizado en COP',
    `COT_ESTADO` ENUM('Pendiente', 'Enviada', 'Aprobada', 'Rechazada') NOT NULL DEFAULT 'Pendiente',
    `COT_NOTAS` TEXT NULL COMMENT 'Condiciones comerciales, forma de pago o entrega',
    `COT_USUA_ID` INT NULL COMMENT 'Asesor comercial que genera la propuesta',
    `COT_CLI_ID` INT NOT NULL COMMENT 'Cliente destinatario',
    -- Campos de compatibilidad directa con servicio legacy:
    `COT_PRO_CODIGO` VARCHAR(50) NULL COMMENT 'Código de producto principal (opcional)',
    `COT_PRO_NOMBRE` VARCHAR(150) NULL COMMENT 'Nombre de producto principal (opcional)',
    `COT_PRO_CANTIDAD` INT NULL DEFAULT 0,
    `COT_PRO_PRECIO` DECIMAL(14, 2) NULL DEFAULT 0.00,
    `COT_FECHA_CREACION` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `COT_FECHA_ACTUALIZACION` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `FK_COTIZACION_USUARIO` FOREIGN KEY (`COT_USUA_ID`) 
        REFERENCES `T_USUARIOS` (`USUA_ID`) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT `FK_COTIZACION_CLIENTE` FOREIGN KEY (`COT_CLI_ID`) 
        REFERENCES `T_CLIENTE` (`CLI_ID`) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX `IDX_COTIZACION_FECHA` (`COT_FECHA`),
    INDEX `IDX_COTIZACION_ESTADO` (`COT_ESTADO`),
    INDEX `IDX_COTIZACION_CLIENTE` (`COT_CLI_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Encabezado de cotizaciones y propuestas comerciales';

-- =============================================================================
-- 14. TABLA DETALLE DE COTIZACIÓN (Múltiples productos por cotización)
-- Implementa la grilla dinámica de productos de frontend/cotizaciones/cotizaciones.js
-- =============================================================================
CREATE TABLE `T_DETALLE_COTIZACION` (
    `DETCOT_ID` INT AUTO_INCREMENT PRIMARY KEY,
    `DETCOT_UUID` CHAR(36) NOT NULL UNIQUE,
    `DETCOT_COT_ID` INT NOT NULL COMMENT 'Cotización a la que pertenece',
    `DETCOT_PROD_ID` INT NULL COMMENT 'Producto del catálogo (opcional si es personalizado)',
    `DETCOT_CODIGO` VARCHAR(50) NULL COMMENT 'Código del producto',
    `DETCOT_NOMBRE` VARCHAR(150) NOT NULL COMMENT 'Descripción de la prenda cotizada',
    `DETCOT_CANTIDAD` INT NOT NULL DEFAULT 1 COMMENT 'Cantidad de unidades cotizadas',
    `DETCOT_PRECIO_UNITARIO` DECIMAL(14, 2) NOT NULL DEFAULT 0.00 COMMENT 'Precio unitario propuesto',
    `DETCOT_SUBTOTAL` DECIMAL(14, 2) NOT NULL DEFAULT 0.00 COMMENT 'Subtotal = Cantidad * Precio',
    `DETCOT_FECHA_CREACION` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `FK_DETALLE_COTIZACION` FOREIGN KEY (`DETCOT_COT_ID`) 
        REFERENCES `T_COTIZACIONES` (`COT_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `FK_DETCOT_PRODUCTO` FOREIGN KEY (`DETCOT_PROD_ID`) 
        REFERENCES `T_PRODUCTOS` (`PROD_ID`) ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX `IDX_DETCOT_COTIZACION` (`DETCOT_COT_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Partidas o productos incluidos en una cotización';

-- =============================================================================
-- 15. TABLA RECUPERACIÓN DE CONTRASEÑA
-- Módulo: frontend/olvido_contrasena/recuperar.js
-- =============================================================================
CREATE TABLE `T_RECUPERACION_CONTRASENA` (
    `REC_ID` INT AUTO_INCREMENT PRIMARY KEY,
    `REC_UUID` CHAR(36) NOT NULL UNIQUE,
    `REC_USUA_ID` INT NOT NULL COMMENT 'Usuario que solicitó el restablecimiento',
    `REC_CORREO` VARCHAR(150) NOT NULL COMMENT 'Correo de destino',
    `REC_TOKEN` VARCHAR(255) NOT NULL UNIQUE COMMENT 'Token o enlace temporal de recuperación',
    `REC_CREADO_EN` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `REC_EXPIRA_EN` DATETIME NOT NULL COMMENT 'Tiempo límite de validez (ej: 24 horas)',
    `REC_USADO` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '0: No usado, 1: Utilizado',
    CONSTRAINT `FK_RECUPERACION_USUARIO` FOREIGN KEY (`REC_USUA_ID`) 
        REFERENCES `T_USUARIOS` (`USUA_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX `IDX_RECUPERACION_TOKEN` (`REC_TOKEN`),
    INDEX `IDX_RECUPERACION_CORREO` (`REC_CORREO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Tokens y solicitudes de recuperación de contraseña';

-- =============================================================================
-- 16. TABLA BITÁCORA DE AUDITORÍA Y REGISTRO DE ACTIVIDAD / ERRORES
-- Módulo: frontend/shared/auditoria.js y frontend/log_errores
-- =============================================================================
CREATE TABLE `T_BITACORA_AUDITORIA` (
    `AUD_ID` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `AUD_UUID` VARCHAR(80) NOT NULL UNIQUE COMMENT 'Identificador único del evento (timestamp-hash)',
    `AUD_FECHA_HORA` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Momento exacto del suceso',
    `AUD_ACTOR` VARCHAR(100) NOT NULL DEFAULT 'Sin identificar' COMMENT 'Nombre del usuario que realizó la acción',
    `AUD_CORREO` VARCHAR(150) NULL COMMENT 'Correo de la sesión activa',
    `AUD_ROL` VARCHAR(50) NULL COMMENT 'Rol de quien ejecutó la acción',
    `AUD_ACCION` VARCHAR(100) NOT NULL COMMENT 'Registro creado, Registro actualizado, Registro eliminado, Inicio de sesión, Acceso denegado, Error de aplicación',
    `AUD_MODULO` VARCHAR(80) NOT NULL COMMENT 'Clientes, Insumos, Productos, Ventas, Cotizaciones, Usuarios, Acceso, Sistema',
    `AUD_ENTIDAD` VARCHAR(150) NULL COMMENT 'Identificador o nombre del registro modificado',
    `AUD_DETALLE` TEXT NULL COMMENT 'Descripción pormenorizada del cambio o traza del error',
    `AUD_RESULTADO` ENUM('success', 'denied', 'error') NOT NULL DEFAULT 'success' COMMENT 'Resultado de la operación',
    INDEX `IDX_AUD_FECHA` (`AUD_FECHA_HORA`),
    INDEX `IDX_AUD_MODULO` (`AUD_MODULO`),
    INDEX `IDX_AUD_RESULTADO` (`AUD_RESULTADO`),
    INDEX `IDX_AUD_ACTOR` (`AUD_ACTOR`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Trazabilidad y auditoría de eventos, accesos y errores del sistema';

-- =============================================================================
-- VISTAS OPTIMIZADAS (VIEWS)
-- Facilitan el consumo desde el Frontend y Dashboard sin consultas complejas
-- =============================================================================

-- Vista 1: Resumen Completo de Clientes
CREATE OR REPLACE VIEW `V_CLIENTES_COMPLETO` AS
SELECT 
    c.CLI_ID AS id,
    c.CLI_UUID AS uuid,
    TRIM(CONCAT_WS(' ', p.PER_NOMBRE, p.PER_SEG_NOMBRE, p.PER_PRI_APELLIDO, p.PER_SEG_APELLIDO)) AS nombre,
    p.PER_IDENTIFICACION AS documento,
    COALESCE(p.PER_TELEFONO, '') AS telefono,
    COALESCE(p.PER_CORREO, '') AS correo,
    COALESCE(p.PER_DIRECCION, '') AS direccion,
    c.CLI_ESTADO AS estado,
    c.CLI_FECHA_CREACION AS fecha_creacion
FROM `T_CLIENTE` c
INNER JOIN `T_PERSONA` p ON c.CLI_PER_ID = p.PER_ID;

-- Vista 2: Directorio Completo de Proveedores
CREATE OR REPLACE VIEW `V_PROVEEDORES_COMPLETO` AS
SELECT 
    pr.PROV_ID AS id,
    pr.PROV_UUID AS uuid,
    pr.PROV_EMPRESA AS empresa,
    COALESCE(TRIM(CONCAT_WS(' ', p.PER_NOMBRE, p.PER_SEG_NOMBRE, p.PER_PRI_APELLIDO, p.PER_SEG_APELLIDO)), 'Sin contacto asignado') AS contacto,
    COALESCE(pr.PROV_TELEFONO, p.PER_TELEFONO, '') AS telefono,
    COALESCE(pr.PROV_CORREO, p.PER_CORREO, '') AS correo,
    COALESCE(pr.PROV_DIRECCION, p.PER_DIRECCION, '') AS direccion,
    pr.PROV_ESTADO AS estado,
    pr.PROV_FECHA_CREACION AS fecha_creacion
FROM `T_PROVEEDORES` pr
LEFT JOIN `T_PERSONA` p ON pr.PROV_PER_ID = p.PER_ID;

-- Vista 3: Catálogo de Productos con Semáforo de Stock
CREATE OR REPLACE VIEW `V_CATALOGO_PRODUCTOS` AS
SELECT 
    pr.PROD_ID AS id,
    pr.PROD_UUID AS uuid,
    pr.PROD_CODIGO AS codigo,
    pr.PROD_NOMBRE AS nombre,
    pr.PROD_CANTIDAD AS cantidad,
    pr.PROD_PRECIO AS precio,
    (pr.PROD_CANTIDAD * pr.PROD_PRECIO) AS valor_inventario,
    pr.PROD_ESTADO AS estado,
    COALESCE(d.DET_ETC_NOMBRE, 'General') AS categoria,
    CASE 
        WHEN pr.PROD_CANTIDAD <= 5 THEN 'Bajo'
        WHEN pr.PROD_CANTIDAD <= 20 THEN 'Medio'
        ELSE 'Bueno'
    END AS nivel_stock,
    CASE 
        WHEN pr.PROD_CANTIDAD <= 5 THEN 'estado-rojo'
        WHEN pr.PROD_CANTIDAD <= 20 THEN 'estado-amarillo'
        ELSE 'estado-verde'
    END AS clase_badge
FROM `T_PRODUCTOS` pr
LEFT JOIN `T_DETALLES_ETC` d ON pr.PROD_DET_ETC_ID = d.DET_ETC_ID;

-- Vista 4: Inventario de Insumos con Proveedor y Categoría
CREATE OR REPLACE VIEW `V_INVENTARIO_INSUMOS` AS
SELECT 
    i.INS_ID AS id,
    i.INS_UUID AS uuid,
    i.INS_CODIGO AS codigo,
    i.INS_NOMBRE AS nombre,
    COALESCE(d.DET_ETC_NOMBRE, 'General') AS categoria,
    COALESCE(p.PROV_EMPRESA, 'Sin asignar') AS proveedor,
    i.INS_CANTIDAD AS cantidad,
    i.INS_UNIDAD AS unidad,
    i.INS_PRECIO AS precioUnitario,
    (i.INS_CANTIDAD * i.INS_PRECIO) AS valor_estimado,
    i.INS_ESTADO AS estado,
    CASE 
        WHEN i.INS_CANTIDAD <= i.INS_STOCK_MINIMO THEN 'Bajo'
        WHEN i.INS_CANTIDAD <= (i.INS_STOCK_MINIMO * 2) THEN 'Medio'
        ELSE 'Bueno'
    END AS nivel_stock
FROM `T_INSUMOS` i
LEFT JOIN `T_PROVEEDORES` p ON i.INS_PROV_ID = p.PROV_ID
LEFT JOIN `T_DETALLES_ETC` d ON i.INS_DET_ETC_ID = d.DET_ETC_ID;

-- Vista 5: Historial Comercial de Ventas
CREATE OR REPLACE VIEW `V_HISTORIAL_VENTAS` AS
SELECT 
    v.VENT_ID AS id,
    v.VENT_UUID AS uuid,
    v.VENT_NUMERO_FACTURA AS factura,
    v.VENT_FECHA AS fecha,
    TRIM(CONCAT_WS(' ', per.PER_NOMBRE, per.PER_PRI_APELLIDO)) AS cliente,
    per.PER_IDENTIFICACION AS cliente_documento,
    COALESCE(GROUP_CONCAT(CONCAT(prod.PROD_NOMBRE, ' (x', vp.VENTPRO_CANTIDAD, ')') SEPARATOR ', '), 'Sin detalle') AS productos_resumen,
    COALESCE(SUM(vp.VENTPRO_CANTIDAD), 0) AS unidades_totales,
    v.VENT_TOTAL AS total,
    v.VENT_ESTADO AS estado,
    u.USUA_NOMBRE AS vendedor
FROM `T_VENTAS` v
INNER JOIN `T_CLIENTE` c ON v.VENT_CLI_ID = c.CLI_ID
INNER JOIN `T_PERSONA` per ON c.CLI_PER_ID = per.PER_ID
LEFT JOIN `T_USUARIOS` u ON v.VENT_USUA_ID = u.USUA_ID
LEFT JOIN `T_VENT_PROD` vp ON v.VENT_ID = vp.VENTPRO_VENT_ID
LEFT JOIN `T_PRODUCTOS` prod ON vp.VENTPRO_PROD_ID = prod.PROD_ID
GROUP BY v.VENT_ID, v.VENT_UUID, v.VENT_NUMERO_FACTURA, v.VENT_FECHA, cliente, per.PER_IDENTIFICACION, v.VENT_TOTAL, v.VENT_ESTADO, u.USUA_NOMBRE;

-- Vista 6: Resumen de Cotizaciones
CREATE OR REPLACE VIEW `V_RESUMEN_COTIZACIONES` AS
SELECT 
    cot.COT_ID AS id,
    cot.COT_UUID AS uuid,
    cot.COT_NUMERO AS numero,
    cot.COT_FECHA AS fecha,
    TRIM(CONCAT_WS(' ', per.PER_NOMBRE, per.PER_PRI_APELLIDO)) AS cliente,
    per.PER_CORREO AS cliente_correo,
    cot.COT_TOTAL_PAGAR AS total,
    cot.COT_ESTADO AS estado,
    COALESCE(cot.COT_NOTAS, '') AS notas,
    COALESCE(COUNT(dc.DETCOT_ID), 0) AS cantidad_items,
    u.USUA_NOMBRE AS asesor
FROM `T_COTIZACIONES` cot
INNER JOIN `T_CLIENTE` c ON cot.COT_CLI_ID = c.CLI_ID
INNER JOIN `T_PERSONA` per ON c.CLI_PER_ID = per.PER_ID
LEFT JOIN `T_USUARIOS` u ON cot.COT_USUA_ID = u.USUA_ID
LEFT JOIN `T_DETALLE_COTIZACION` dc ON cot.COT_ID = dc.DETCOT_COT_ID
GROUP BY cot.COT_ID, cot.COT_UUID, cot.COT_NUMERO, cot.COT_FECHA, cliente, per.PER_CORREO, cot.COT_TOTAL_PAGAR, cot.COT_ESTADO, cot.COT_NOTAS, u.USUA_NOMBRE;

-- Vista 7: Métricas para el Dashboard de Inicio (frontend/inicio/inicio.js)
CREATE OR REPLACE VIEW `V_DASHBOARD_METRICAS` AS
SELECT 
    (SELECT COALESCE(SUM(PROD_CANTIDAD), 0) FROM `T_PRODUCTOS` WHERE PROD_ESTADO = 'Activo') AS stock_total_unidades,
    (SELECT COUNT(*) FROM `T_PRODUCTOS` WHERE PROD_ESTADO = 'Activo') AS productos_registrados,
    (SELECT COALESCE(SUM(PROD_CANTIDAD * PROD_PRECIO), 0) FROM `T_PRODUCTOS` WHERE PROD_ESTADO = 'Activo') AS valor_productos,
    (SELECT COALESCE(SUM(INS_CANTIDAD * INS_PRECIO), 0) FROM `T_INSUMOS`) AS valor_insumos,
    (
        (SELECT COALESCE(SUM(PROD_CANTIDAD * PROD_PRECIO), 0) FROM `T_PRODUCTOS` WHERE PROD_ESTADO = 'Activo')
        + (SELECT COALESCE(SUM(INS_CANTIDAD * INS_PRECIO), 0) FROM `T_INSUMOS`)
    ) AS valor_inventario_total,
    (SELECT COALESCE(SUM(VENT_TOTAL), 0) FROM `T_VENTAS` WHERE VENT_ESTADO = 'Completada') AS total_ventas,
    (SELECT COUNT(*) FROM `T_VENTAS` WHERE VENT_ESTADO = 'Completada') AS operaciones_ventas,
    (SELECT COUNT(*) FROM `T_CLIENTE` WHERE CLI_ESTADO = 'Activo') AS clientes_totales,
    (SELECT COUNT(*) FROM `T_COTIZACIONES` WHERE COT_ESTADO != 'Rechazada') AS cotizaciones_abiertas,
    (SELECT COALESCE(SUM(COT_TOTAL_PAGAR), 0) FROM `T_COTIZACIONES` WHERE COT_ESTADO != 'Rechazada') AS ingresos_proyectados;

-- =============================================================================
-- DISPARADORES (TRIGGERS)
-- Automatización de stock e integridad transaccional
-- =============================================================================

DELIMITER $$

-- Trigger 1: Al registrar un detalle de venta, descontar stock de productos automáticamente
CREATE TRIGGER `TRG_VENT_PROD_AFTER_INSERT`
AFTER INSERT ON `T_VENT_PROD`
FOR EACH ROW
BEGIN
    UPDATE `T_PRODUCTOS`
    SET `PROD_CANTIDAD` = GREATEST(0, `PROD_CANTIDAD` - NEW.VENTPRO_CANTIDAD)
    WHERE `PROD_ID` = NEW.VENTPRO_PROD_ID;
END$$

-- Trigger 2: Si se cancela o elimina un detalle de venta, restaurar el stock del producto
CREATE TRIGGER `TRG_VENT_PROD_AFTER_DELETE`
AFTER DELETE ON `T_VENT_PROD`
FOR EACH ROW
BEGIN
    UPDATE `T_PRODUCTOS`
    SET `PROD_CANTIDAD` = `PROD_CANTIDAD` + OLD.VENTPRO_CANTIDAD
    WHERE `PROD_ID` = OLD.VENTPRO_PROD_ID;
END$$

-- Trigger 3: Auditoría automática tras crear un producto
CREATE TRIGGER `TRG_PRODUCTO_AFTER_INSERT`
AFTER INSERT ON `T_PRODUCTOS`
FOR EACH ROW
BEGIN
    INSERT INTO `T_BITACORA_AUDITORIA` (
        `AUD_UUID`, `AUD_FECHA_HORA`, `AUD_ACTOR`, `AUD_ACCION`, `AUD_MODULO`, `AUD_ENTIDAD`, `AUD_DETALLE`, `AUD_RESULTADO`
    ) VALUES (
        CONCAT(UNIX_TIMESTAMP(), '-', SUBSTRING(MD5(RAND()), 1, 6)),
        NOW(),
        'Sistema Automático',
        'Registro creado',
        'Productos',
        NEW.PROD_NOMBRE,
        CONCAT('Producto registrado: Código ', NEW.PROD_CODIGO, ', Stock: ', NEW.PROD_CANTIDAD, ', Precio: $', NEW.PROD_PRECIO),
        'success'
    );
END$$

-- Trigger 4: Auditoría automática tras eliminar un producto
CREATE TRIGGER `TRG_PRODUCTO_AFTER_DELETE`
AFTER DELETE ON `T_PRODUCTOS`
FOR EACH ROW
BEGIN
    INSERT INTO `T_BITACORA_AUDITORIA` (
        `AUD_UUID`, `AUD_FECHA_HORA`, `AUD_ACTOR`, `AUD_ACCION`, `AUD_MODULO`, `AUD_ENTIDAD`, `AUD_DETALLE`, `AUD_RESULTADO`
    ) VALUES (
        CONCAT(UNIX_TIMESTAMP(), '-', SUBSTRING(MD5(RAND()), 1, 6)),
        NOW(),
        'Sistema Automático',
        'Registro eliminado',
        'Productos',
        OLD.PROD_NOMBRE,
        CONCAT('Producto eliminado: Código ', OLD.PROD_CODIGO),
        'success'
    );
END$$

DELIMITER ;

-- =============================================================================
-- PROCEDIMIENTOS ALMACENADOS (STORED PROCEDURES)
-- Facilitan operaciones atómicas frecuentes
-- =============================================================================

DELIMITER $$

-- Procedimiento 1: Crear o registrar cliente con transacción atómica
DROP PROCEDURE IF EXISTS `SP_REGISTRAR_CLIENTE`$$
CREATE PROCEDURE `SP_REGISTRAR_CLIENTE`(
    IN p_nombre VARCHAR(60),
    IN p_identificacion VARCHAR(50),
    IN p_telefono VARCHAR(30),
    IN p_correo VARCHAR(150),
    OUT p_cliente_id INT
)
BEGIN
    DECLARE v_per_id INT;
    DECLARE v_per_uuid CHAR(36);
    DECLARE v_cli_uuid CHAR(36);

    START TRANSACTION;
        SET v_per_uuid = UUID();
        SET v_cli_uuid = UUID();

        -- Verificar si la persona ya existe por identificación
        SELECT PER_ID INTO v_per_id FROM `T_PERSONA` WHERE `PER_IDENTIFICACION` = p_identificacion LIMIT 1;

        IF v_per_id IS NULL THEN
            INSERT INTO `T_PERSONA` (
                `PER_UUID`, `PER_NOMBRE`, `PER_IDENTIFICACION`, `PER_TELEFONO`, `PER_CORREO`
            ) VALUES (
                v_per_uuid, p_nombre, p_identificacion, p_telefono, p_correo
            );
            SET v_per_id = LAST_INSERT_ID();
        ELSE
            UPDATE `T_PERSONA`
            SET `PER_NOMBRE` = p_nombre,
                `PER_TELEFONO` = p_telefono,
                `PER_CORREO` = p_correo
            WHERE `PER_ID` = v_per_id;
        END IF;

        -- Insertar en T_CLIENTE si no está registrado
        INSERT INTO `T_CLIENTE` (`CLI_UUID`, `CLI_PER_ID`, `CLI_ESTADO`)
        VALUES (v_cli_uuid, v_per_id, 'Activo')
        ON DUPLICATE KEY UPDATE `CLI_ESTADO` = 'Activo';

        SELECT CLI_ID INTO p_cliente_id FROM `T_CLIENTE` WHERE `CLI_PER_ID` = v_per_id;
    COMMIT;
END$$

-- Procedimiento 2: Registrar una venta simple desde el frontend
DROP PROCEDURE IF EXISTS `SP_REGISTRAR_VENTA_SIMPLE`$$
CREATE PROCEDURE `SP_REGISTRAR_VENTA_SIMPLE`(
    IN p_fecha DATE,
    IN p_cliente_nombre VARCHAR(150),
    IN p_producto_codigo VARCHAR(50),
    IN p_cantidad INT,
    IN p_total DECIMAL(14, 2),
    OUT p_venta_id INT
)
BEGIN
    DECLARE v_cli_id INT;
    DECLARE v_prod_id INT;
    DECLARE v_prod_precio DECIMAL(14, 2);
    DECLARE v_vent_uuid CHAR(36);
    DECLARE v_ventpro_uuid CHAR(36);

    START TRANSACTION;
        SET v_vent_uuid = UUID();
        SET v_ventpro_uuid = UUID();

        -- Localizar cliente por nombre aproximado
        SELECT c.CLI_ID INTO v_cli_id 
        FROM `T_CLIENTE` c
        INNER JOIN `T_PERSONA` p ON c.CLI_PER_ID = p.PER_ID
        WHERE p.PER_NOMBRE LIKE CONCAT('%', p_cliente_nombre, '%')
        LIMIT 1;

        -- Localizar producto
        SELECT PROD_ID, PROD_PRECIO INTO v_prod_id, v_prod_precio 
        FROM `T_PRODUCTOS` 
        WHERE PROD_CODIGO = p_producto_codigo OR PROD_NOMBRE = p_producto_codigo
        LIMIT 1;

        IF v_cli_id IS NOT NULL AND v_prod_id IS NOT NULL THEN
            -- Insertar encabezado de venta
            INSERT INTO `T_VENTAS` (`VENT_UUID`, `VENT_FECHA`, `VENT_TOTAL`, `VENT_ESTADO`, `VENT_CLI_ID`)
            VALUES (v_vent_uuid, p_fecha, p_total, 'Completada', v_cli_id);

            SET p_venta_id = LAST_INSERT_ID();

            -- Insertar detalle de venta (el trigger descontará el stock)
            INSERT INTO `T_VENT_PROD` (
                `VENTPRO_UUID`, `VENTPRO_CANTIDAD`, `VENTPRO_PRECIO_UNITARIO`, `VENTPRO_SUBTOTAL`, `VENTPRO_VENT_ID`, `VENTPRO_PROD_ID`
            ) VALUES (
                v_ventpro_uuid, p_cantidad, v_prod_precio, p_total, p_venta_id, v_prod_id
            );
        END IF;
    COMMIT;
END$$

DELIMITER ;

-- =============================================================================
-- DATOS SEMILLA INICIALES (SEED DATA)
-- Precarga de datos coincidentes con los mocks y valores por defecto del Frontend
-- =============================================================================

-- 1. Grupos ETC (Categorías y Estados Maestros)
INSERT INTO `T_ESTADO_TIPOS_CATEGORIAS` (`ETC_ID`, `ETC_UUID`, `ETC_NOMBRE`, `ETC_DESCRIPCION`) VALUES
(1, UUID(), 'ROLES_USUARIO', 'Roles de acceso y permisos para el personal'),
(2, UUID(), 'CATEGORIAS_PRODUCTOS', 'Categorías de prendas y catálogo terminado'),
(3, UUID(), 'CATEGORIAS_INSUMOS', 'Clasificación de materiales e insumos de costura'),
(4, UUID(), 'UNIDADES_MEDIDA', 'Unidades de inventario para materiales'),
(5, UUID(), 'ESTADOS_COTIZACION', 'Fases de propuestas comerciales'),
(6, UUID(), 'ESTADOS_INSUMO', 'Disponibilidad operativa de materias primas');

-- 2. Detalles de ETC
INSERT INTO `T_DETALLES_ETC` (`DET_ETC_ID`, `DET_ETC_UUID`, `DET_ETC_NOMBRE`, `DET_ETC_ETC_ID`) VALUES
-- Roles de usuario (frontend/usuarios/usuarios.html)
(1, UUID(), 'Administrador', 1),
(2, UUID(), 'Empleado', 1),
-- Categorías de Productos (frontend/productos/productos.js)
(3, UUID(), 'Camisetas', 2),
(4, UUID(), 'Pantalones', 2),
(5, UUID(), 'Chaquetas', 2),
(6, UUID(), 'Vestidos', 2),
(7, UUID(), 'General', 2),
-- Categorías de Insumos (frontend/insumos/insumos.js)
(8, UUID(), 'Tela', 3),
(9, UUID(), 'Hilo', 3),
(10, UUID(), 'Botones', 3),
(11, UUID(), 'Cremalleras', 3),
(12, UUID(), 'Marquillas', 3),
-- Unidades de Medida
(13, UUID(), 'metros', 4),
(14, UUID(), 'piezas', 4),
(15, UUID(), 'conos', 4),
(16, UUID(), 'rollos', 4),
-- Estados de Cotización (frontend/cotizaciones/cotizaciones.html)
(17, UUID(), 'Pendiente', 5),
(18, UUID(), 'Enviada', 5),
(19, UUID(), 'Aprobada', 5),
(20, UUID(), 'Rechazada', 5),
-- Estados de Insumos
(21, UUID(), 'Disponible', 6),
(22, UUID(), 'Agotado', 6),
(23, UUID(), 'Pedido', 6);

-- 3. Usuarios iniciales (frontend/usuarios/usuarios.js)
-- Admin usa 'admin1234'; Operador conserva '1234'.
INSERT INTO `T_USUARIOS` (`USUA_ID`, `USUA_UUID`, `USUA_NOMBRE`, `USUA_CORREO`, `USUA_CONTRASENA`, `USUA_ESTADO`, `USUA_DET_ETC_ID`) VALUES
(1, UUID(), 'Admin', 'admin@example.com', '$2b$12$0itqw.nGyuQPKnZ7ttOY2.u./mq.iXfpp1DnnqFL7jJRdOg43CYKW', 'Activo', 1),
(2, UUID(), 'Operador', 'operador@marqueza.com', '$2b$12$ku06o8bUReFjufv.3HM26uvzApCXqrWDhJl26B.k/zoOaw3x57eJW', 'Activo', 2);

DELIMITER $$
CREATE TRIGGER `TRG_PROTEGER_ADMIN_USUARIO`
BEFORE DELETE ON `T_USUARIOS`
FOR EACH ROW
BEGIN
    IF OLD.`USUA_NOMBRE` = 'Admin' OR OLD.`USUA_CORREO` = 'admin@example.com' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La cuenta principal de Administrador no se puede eliminar';
    END IF;
END$$
DELIMITER ;

-- 4. Personas (Clientes y Contactos de Proveedores)
INSERT INTO `T_PERSONA` (`PER_ID`, `PER_UUID`, `PER_NOMBRE`, `PER_PRI_APELLIDO`, `PER_CORREO`, `PER_DIRECCION`, `PER_IDENTIFICACION`, `PER_TELEFONO`) VALUES
(1, UUID(), 'Carlos Andrés', 'Mendoza', 'carlos.mendoza@email.com', 'Calle 45 # 23-10, Bogotá', '1020304050', '3104567890'),
(2, UUID(), 'Mariana Lucía', 'Gómez', 'mariana.gomez@email.com', 'Carrera 15 # 85-30, Medellín', '1098765432', '3157891234'),
(3, UUID(), 'Alejandro', 'Rojas', 'ventas@textilesandinos.com', 'Zona Industrial Montevideo, Bogotá', '900123456-1', '6017894561'),
(4, UUID(), 'Beatriz', 'Herrera', 'contacto@hilosdelvalle.com', 'Calle 10 # 50-20, Cali', '900987654-2', '6024561234');

-- 5. Clientes vinculados a T_PERSONA (frontend/clientes/clientes.js)
INSERT INTO `T_CLIENTE` (`CLI_ID`, `CLI_UUID`, `CLI_PER_ID`, `CLI_ESTADO`) VALUES
(1, UUID(), 1, 'Activo'),
(2, UUID(), 2, 'Activo');

-- 6. Proveedores vinculados (frontend/proveedores/proveedores.js)
INSERT INTO `T_PROVEEDORES` (`PROV_ID`, `PROV_UUID`, `PROV_EMPRESA`, `PROV_PER_ID`, `PROV_DIRECCION`, `PROV_TELEFONO`, `PROV_CORREO`, `PROV_ESTADO`) VALUES
(1, UUID(), 'Textiles Andinos S.A.S.', 3, 'Zona Industrial Montevideo, Bogotá', '6017894561', 'ventas@textilesandinos.com', 'Activo'),
(2, UUID(), 'Distribuidora Hilos del Valle', 4, 'Calle 10 # 50-20, Cali', '6024561234', 'contacto@hilosdelvalle.com', 'Activo');

-- 7. Contactos de proveedores (T_CONTACTO)
INSERT INTO `T_CONTACTO` (`CONT_ID`, `CONT_UUID`, `CONT_TIPO_DATO`, `CONT_CONTENIDO`, `CONT_PROV_ID`) VALUES
(1, UUID(), 'Teléfono PBX', '6017894561 Ext 101', 1),
(2, UUID(), 'WhatsApp Comercial', '+57 312 987 6543', 1),
(3, UUID(), 'Correo Pedidos', 'pedidos@hilosdelvalle.com', 2);

-- 8. Productos iniciales del frontend (frontend/productos/productos.js)
-- Iniciales: P001 Camiseta básica (20 u, $35.000, Activo, Camisetas)
--            P002 Pantalón jean (8 u, $85.000, Activo, Pantalones)
INSERT INTO `T_PRODUCTOS` (`PROD_ID`, `PROD_UUID`, `PROD_CODIGO`, `PROD_NOMBRE`, `PROD_CANTIDAD`, `PROD_PRECIO`, `PROD_ESTADO`, `PROD_STOCK_MINIMO`, `PROD_USUA_ID`, `PROD_DET_ETC_ID`) VALUES
(1, UUID(), 'P001', 'Camiseta básica', 20, 35000.00, 'Activo', 5, 1, 3),
(2, UUID(), 'P002', 'Pantalón jean', 8, 85000.00, 'Activo', 5, 1, 4),
(3, UUID(), 'P003', 'Chaqueta impermeable', 4, 120000.00, 'Activo', 5, 1, 5),
(4, UUID(), 'P004', 'Vestido casual de verano', 15, 65000.00, 'Activo', 5, 1, 6);

-- 9. Insumos iniciales (frontend/insumos/insumos.js)
INSERT INTO `T_INSUMOS` (`INS_ID`, `INS_UUID`, `INS_CODIGO`, `INS_NOMBRE`, `INS_CANTIDAD`, `INS_UNIDAD`, `INS_PRECIO`, `INS_ESTADO`, `INS_STOCK_MINIMO`, `INS_USUA_ID`, `INS_PROV_ID`, `INS_DET_ETC_ID`) VALUES
(1, UUID(), 'INS-001', 'Tela algodón jersey 180g', 150.00, 'metros', 14500.00, 'Disponible', 20.00, 1, 1, 8),
(2, UUID(), 'INS-002', 'Tela índigo rígido 12oz', 85.00, 'metros', 22000.00, 'Disponible', 15.00, 1, 1, 8),
(3, UUID(), 'INS-003', 'Hilo poliéster 120 calibre azul', 40.00, 'conos', 6800.00, 'Disponible', 10.00, 1, 2, 9),
(4, UUID(), 'INS-004', 'Botón metálico para jean 17mm', 500.00, 'piezas', 350.00, 'Disponible', 100.00, 1, 2, 10),
(5, UUID(), 'INS-005', 'Cremallera de cobre 18cm', 300.00, 'piezas', 1200.00, 'Disponible', 50.00, 1, 2, 11);

-- 10. Ficha Técnica / Receta Producto-Insumo (BOM)
INSERT INTO `T_PRODU_INSUM` (`PROINSU_ID`, `PROINSU_UUID`, `PROINSU_CANTIDAD`, `PROINSU_PROD_ID`, `PROINSU_INS_ID`) VALUES
(1, UUID(), 1.20, 1, 1), -- Camiseta básica requiere 1.2 metros de tela algodón
(2, UUID(), 0.10, 1, 3), -- y 0.1 cono de hilo
(3, UUID(), 1.50, 2, 2), -- Pantalón jean requiere 1.5 metros de índigo
(4, UUID(), 1.00, 2, 4), -- 1 botón metálico
(5, UUID(), 1.00, 2, 5); -- 1 cremallera

-- 11. Ventas iniciales (frontend/ventas/ventas.js)
INSERT INTO `T_VENTAS` (`VENT_ID`, `VENT_UUID`, `VENT_NUMERO_FACTURA`, `VENT_FECHA`, `VENT_TOTAL`, `VENT_ESTADO`, `VENT_USUA_ID`, `VENT_CLI_ID`) VALUES
(1, UUID(), 'VNT-001', '2026-09-15', 175000.00, 'Completada', 1, 1),
(2, UUID(), 'VNT-002', '2026-09-20', 170000.00, 'Completada', 1, 2);

-- Detalle de productos vendidos en ventas iniciales
INSERT INTO `T_VENT_PROD` (`VENTPRO_ID`, `VENTPRO_UUID`, `VENTPRO_CANTIDAD`, `VENTPRO_PRECIO_UNITARIO`, `VENTPRO_SUBTOTAL`, `VENTPRO_VENT_ID`, `VENTPRO_PROD_ID`) VALUES
(1, UUID(), 5, 35000.00, 175000.00, 1, 1), -- 5 camisetas
(2, UUID(), 2, 85000.00, 170000.00, 2, 2); -- 2 pantalones

-- 12. Cotizaciones iniciales (frontend/cotizaciones/cotizaciones.js)
INSERT INTO `T_COTIZACIONES` (`COT_ID`, `COT_UUID`, `COT_NUMERO`, `COT_FECHA`, `COT_TOTAL_PAGAR`, `COT_ESTADO`, `COT_NOTAS`, `COT_USUA_ID`, `COT_CLI_ID`, `COT_PRO_CODIGO`, `COT_PRO_NOMBRE`, `COT_PRO_CANTIDAD`, `COT_PRO_PRECIO`) VALUES
(1, UUID(), 'COT-001', '2026-09-22', 1050000.00, 'Enviada', 'Propuesta de dotación empresarial. Entrega en 10 días hábiles.', 1, 1, 'P001', 'Camiseta básica', 30, 35000.00),
(2, UUID(), 'COT-002', '2026-09-25', 850000.00, 'Pendiente', 'Cotización por 10 pantalones jean para personal operativo.', 1, 2, 'P002', 'Pantalón jean', 10, 85000.00);

-- Detalle de productos de las cotizaciones
INSERT INTO `T_DETALLE_COTIZACION` (`DETCOT_ID`, `DETCOT_UUID`, `DETCOT_COT_ID`, `DETCOT_PROD_ID`, `DETCOT_CODIGO`, `DETCOT_NOMBRE`, `DETCOT_CANTIDAD`, `DETCOT_PRECIO_UNITARIO`, `DETCOT_SUBTOTAL`) VALUES
(1, UUID(), 1, 1, 'P001', 'Camiseta básica institucional bordada', 30, 35000.00, 1050000.00),
(2, UUID(), 2, 2, 'P002', 'Pantalón jean clásico resistente', 10, 85000.00, 850000.00);

-- 13. Bitácora de Auditoría inicial (frontend/shared/auditoria.js)
INSERT INTO `T_BITACORA_AUDITORIA` (`AUD_UUID`, `AUD_FECHA_HORA`, `AUD_ACTOR`, `AUD_CORREO`, `AUD_ROL`, `AUD_ACCION`, `AUD_MODULO`, `AUD_ENTIDAD`, `AUD_DETALLE`, `AUD_RESULTADO`) VALUES
(CONCAT(UNIX_TIMESTAMP(), '-001'), NOW(), 'Admin', 'admin@example.com', 'Administrador', 'Inicio de sesión', 'Acceso', 'Sistema', 'Inicio de sesión autorizado desde frontend.', 'success'),
(CONCAT(UNIX_TIMESTAMP(), '-002'), NOW(), 'Admin', 'admin@example.com', 'Administrador', 'Registro creado', 'Productos', 'Camiseta básica', 'Registro inicial del producto P001 en inventario.', 'success'),
(CONCAT(UNIX_TIMESTAMP(), '-003'), NOW(), 'Admin', 'admin@example.com', 'Administrador', 'Registro creado', 'Insumos', 'Tela algodón jersey 180g', 'Ingreso inicial de lote de materia prima INS-001.', 'success');

-- =============================================================================
-- FIN DEL ARCHIVO DE BASE DE DATOS MARQUEZA
-- =============================================================================
