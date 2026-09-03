USE MARQUEZA_C;

-- =====================================
-- Carga inicial de datos para MARQUEZA_C
-- =====================================

INSERT INTO T_ESTADO_TIPOS_CATEGORIAS (ETC_UUID, ETC_NOMBRE) VALUES
(uuid(), 'ACTIVO'),
(uuid(), 'INACTIVO'),
(uuid(), 'TELEFONO'),
(uuid(), 'EMAIL'),
(uuid(), 'CATEGORIA_PRODUCTO'),
(uuid(), 'CATEGORIA_INSUMO');

INSERT INTO T_PERSONA (PER_UUID, PER_NOMBRE, PER_SEG_NOMBRE, PER_PRI_APELLIDO, PER_SEG_APELLIDO, PER_CORREO, PER_DIRECCION, PER_IDENTIFICACION, PER_TELEFONO) VALUES
(uuid(), 'Laura', 'Marta', 'Gomez', 'Torres', 'laura.gomez@marqueza.com', 'Cra 12 #45-30', 1012345678, 3005001001),
(uuid(), 'Camilo', 'Andres', 'Ramirez', 'Perea', 'camilo.ramirez@marqueza.com', 'Clle 18 #20-15', 1023456789, 3014567789),
(uuid(), 'Sandra', 'Patricia', 'Lopez', 'Cruz', 'sandra.lopez@marqueza.com', 'Av 68 #24-10', 1034567890, 3021987654),
(uuid(), 'Diego', 'Fernando', 'Castro', 'Rojas', 'diego.castro@marqueza.com', 'Transversal 9 #11-45', 1045678901, 3037654321),
(uuid(), 'Marta', 'Lucia', 'Silva', 'Guerra', 'marta.silva@marqueza.com', 'Cra 30 #60-12', 1056789012, 3041122334),
(uuid(), 'Carlos', 'Eduardo', 'Muñoz', 'Estrada', 'carlos.munoz@marqueza.com', 'Calle 8 #17-80', 1067890123, 3053344556),
(uuid(), 'Valentina', 'Isabela', 'Fernandez', 'Rincon', 'valentina.fernandez@marqueza.com', 'Diagonal 15 #34-99', 1078901234, 3065566778),
(uuid(), 'Andres', 'Felipe', 'Diaz', 'Mora', 'andres.diaz@marqueza.com', 'Cra 52 #90-10', 1089012345, 3078899001),
(uuid(), 'Nicolas', 'Alejandro', 'Sanchez', 'Alvarez', 'nicolas.sanchez@marqueza.com', 'Kr 44 #77-14', 1090123456, 3089900112),
(uuid(), 'Juliana', 'Paola', 'Vargas', 'Mejia', 'juliana.vargas@marqueza.com', 'Calle 26 #13-45', 1101234567, 3091234567);

INSERT INTO T_DETALLES_ETC (DET_ETC_UUID, DET_ETC_NOMBRE, DET_ETC_ETC_ID, DET_ETC_PER_ID) VALUES
(uuid(), 'ADMINISTRADOR', 1, 1),
(uuid(), 'VENDEDOR', 1, 2),
(uuid(), 'AUXILIAR', 1, 3),
(uuid(), 'CLIENTE_PREFERENCIAL', 1, 4),
(uuid(), 'PROVEEDOR_MADERA', 5, 5),
(uuid(), 'PROVEEDOR_HERRAMIENTAS', 5, 6),
(uuid(), 'PROVEEDOR_ACCESORIOS', 6, 7),
(uuid(), 'PROVEEDOR_PINTURAS', 6, 8);

INSERT INTO T_CLIENTE (CLI_UUID, CLI_PER_ID) VALUES
(uuid(), 1),
(uuid(), 2),
(uuid(), 3),
(uuid(), 4);

INSERT INTO T_PROVEEDORES (PROV_UUID, PROV_PER_ID) VALUES
(uuid(), 5),
(uuid(), 6),
(uuid(), 7);

INSERT INTO T_USUARIOS (USUA_UUID, USUA_NOMBRE, USUA_CORREO, USUA_CONTRASEÑA, USUA_ESTADO, USUA_DET_ETC_ID) VALUES
(uuid(), 'admin', 'admin@marqueza.com', 'admin123', 'ACTIVO', 1),
(uuid(), 'camilo.vendedor', 'camilo.ramirez@marqueza.com', 'vendedor123', 'ACTIVO', 2),
(uuid(), 'sandra.auxiliar', 'sandra.lopez@marqueza.com', 'auxiliar123', 'ACTIVO', 3),
(uuid(), 'diego.cliente', 'diego.castro@marqueza.com', 'cliente123', 'ACTIVO', 4),
(uuid(), 'marta.prov', 'marta.silva@marqueza.com', 'prov123', 'ACTIVO', 5);

INSERT INTO T_COTIZACIONES (COT_UUID, COT_PRO_CODIGO, COT_PRO_NOMBRE, COT_PRO_CANTIDAD, COT_PRO_PRECIO, COT_TOTAL_PAGAR, COT_USUA_ID, COT_CLI_ID) VALUES
(uuid(), 'PROD-001', 'Mesa de madera', 2, 650000, 1300000, 1, 1),
(uuid(), 'PROD-002', 'Silla de oficina', 5, 180000, 900000, 2, 2),
(uuid(), 'PROD-003', 'Escritorio modular', 1, 980000, 980000, 3, 3),
(uuid(), 'PROD-004', 'Archivador metalico', 3, 420000, 1260000, 1, 4);

INSERT INTO T_VENTAS (VENT_UUID, VENT_FECHA, VENT_USUA_ID, VENT_CLI_ID) VALUES
(uuid(), '2022-12-01', 1, 1),
(uuid(), '2023-07-03', 2, 2),
(uuid(), '2024-09-06', 3, 3),
(uuid(), '2025-10-08', 1, 4);

INSERT INTO T_PRODUCTOS (PROD_UUID, PROD_CODIGO, PROD_NOMBRE, PROD_CANTIDAD, PROD_PRECIO, PROD_ESTADO, PROD_USUA_ID, PROD_DET_ETC_ID) VALUES
(uuid(), 'PROD-001', 'Mesa de madera', 12, 650000, 'ACTIVO', 1, 1),
(uuid(), 'PROD-002', 'Silla de oficina', 30, 180000, 'ACTIVO', 2, 2),
(uuid(), 'PROD-003', 'Escritorio modular', 8, 980000, 'ACTIVO', 3, 3),
(uuid(), 'PROD-004', 'Archivador metalico', 15, 420000, 'ACTIVO', 1, 4),
(uuid(), 'PROD-005', 'Mueble para TV', 10, 540000, 'ACTIVO', 2, 5);

INSERT INTO T_CONTACTO (CONT_UUID, CONT_TIPO_DATO, CONT_CONTENIDO, CONT_PROV_ID) VALUES
(uuid(), 'TELEFONO', '3001112233', 1),
(uuid(), 'EMAIL', 'ventas@maderacol.com', 1),
(uuid(), 'TELEFONO', '3012233344', 2),
(uuid(), 'EMAIL', 'contacto@ferremetal.com', 2),
(uuid(), 'TELEFONO', '3023344455', 3),
(uuid(), 'EMAIL', 'accesorios@tornillosplus.com', 3);

INSERT INTO T_INSUMOS (INS_UUID, INS_CODIGO, INS_NOMBRE, INS_CANTIDAD, INS_PRECIO, INS_ESTADO, INS_USUA_ID, INS_DET_ETC_ID, INS_PROV_ID) VALUES
(uuid(), 'INS-001', 'Tablero MDF', 60, 35000, 'ACTIVO', 1, 1, 1),
(uuid(), 'INS-002', 'Pintura blanca', 40, 28000, 'ACTIVO', 2, 2, 2),
(uuid(), 'INS-003', 'Tornillos 5mm', 200, 1200, 'ACTIVO', 3, 3, 3),
(uuid(), 'INS-004', 'Bisagras metalicas', 90, 9500, 'ACTIVO', 1, 4, 2),
(uuid(), 'INS-005', 'Lija de madera', 75, 6000, 'ACTIVO', 2, 5, 1);

INSERT INTO T_VENT_PROD (VENPRO_UUID, VENPRO_CANTIDAD, VENPRO_VENT_ID, VENPRO_PROD_ID) VALUES
(uuid(), 2, 1, 1),
(uuid(), 3, 2, 2),
(uuid(), 1, 3, 3),
(uuid(), 2, 4, 4),
(uuid(), 1, 1, 5);

INSERT INTO T_PRODU_INSUM (PROINSU_UUID, PROINSU_CANTIDAD, PROINSU_PROD_ID, PROINSU_INS_ID) VALUES
(uuid(), 5, 1, 1),
(uuid(), 3, 2, 3),
(uuid(), 2, 3, 4),
(uuid(), 4, 4, 2),
(uuid(), 6, 5, 5);

SELECT 'Datos cargados correctamente en MARQUEZA_C' AS ESTADO;
