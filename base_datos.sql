-- ===========================
-- CREACIÓN DE TABLAS
-- ===========================

-- 1. Área
CREATE TABLE area (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

-- 2. Departamento ligado a un área
CREATE TABLE departamento (
    id SERIAL PRIMARY KEY,
    area_id INTEGER NOT NULL REFERENCES area(id) ON DELETE RESTRICT,
    nombre VARCHAR(100) NOT NULL,
    UNIQUE(area_id, nombre)
);

-- 3. Trabajador (datos personales)
CREATE TABLE trabajador (
    rut VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    sexo VARCHAR(15) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    fecha_nacimiento DATE,
    email VARCHAR(100) UNIQUE
);

-- 4. Datos laborales (uno por trabajador)
CREATE TABLE datos_laborales (
    id SERIAL PRIMARY KEY,
    rut_trabajador VARCHAR(20) NOT NULL REFERENCES trabajador(rut) ON DELETE CASCADE,
    cargo VARCHAR(50) NOT NULL,
    fecha_de_ingreso DATE NOT NULL,
    area_id INTEGER NOT NULL REFERENCES area(id) ON DELETE RESTRICT,
    departamento_id INTEGER NOT NULL REFERENCES departamento(id) ON DELETE RESTRICT,
    estado VARCHAR(20) NOT NULL DEFAULT 'activo',
    UNIQUE(rut_trabajador)
);

-- 5. Contactos de emergencia (varios por trabajador)
CREATE TABLE contactos_emergencia (
    id SERIAL PRIMARY KEY,
    rut_trabajador VARCHAR(20) NOT NULL REFERENCES trabajador(rut) ON DELETE CASCADE,
    nombre_contacto VARCHAR(100) NOT NULL,
    relacion VARCHAR(50) NOT NULL,
    telefono_contacto VARCHAR(20) NOT NULL
);

-- 6. Cargas familiares (varias por trabajador)
CREATE TABLE cargas_familiares (
    id SERIAL PRIMARY KEY,
    rut_trabajador VARCHAR(20) NOT NULL REFERENCES trabajador(rut) ON DELETE CASCADE,
    nombre VARCHAR(100) NOT NULL,
    parentesco VARCHAR(50) NOT NULL,
    sexo VARCHAR(15) NOT NULL,
    rut VARCHAR(20) NOT NULL
);

-- 7. Rol/perfil de usuario
CREATE TABLE rol (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(200)
);

-- 8. Usuario para login
CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(200) NOT NULL,
    rol_id INTEGER NOT NULL REFERENCES rol(id) ON DELETE RESTRICT,
    rut_trabajador VARCHAR(20) REFERENCES trabajador(rut),
    fecha_creacion TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

-- 9. Log de accesos/login
CREATE TABLE log_acceso (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuario(id) ON DELETE SET NULL,
    fecha TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    exito BOOLEAN NOT NULL,
    ip_origen VARCHAR(50)
);

-- 10. Historial de cambios en datos personales
CREATE TABLE historial_cambios (
    id SERIAL PRIMARY KEY,
    rut_trabajador VARCHAR(20) NOT NULL REFERENCES trabajador(rut) ON DELETE CASCADE,
    campo VARCHAR(50) NOT NULL,
    valor_anterior TEXT,
    valor_nuevo TEXT,
    fecha TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    usuario_id INTEGER REFERENCES usuario(id) ON DELETE SET NULL
);

-- 11. Asistencia diaria
CREATE TABLE asistencia (
    id SERIAL PRIMARY KEY,
    rut_trabajador VARCHAR(20) NOT NULL REFERENCES trabajador(rut) ON DELETE CASCADE,
    fecha DATE NOT NULL,
    hora_entrada TIME,
    hora_salida TIME,
    estado VARCHAR(20) NOT NULL DEFAULT 'presente',
    UNIQUE(rut_trabajador, fecha)
);

-- 12. Vacaciones / permisos
CREATE TABLE vacaciones (
    id SERIAL PRIMARY KEY,
    rut_trabajador VARCHAR(20) NOT NULL REFERENCES trabajador(rut) ON DELETE CASCADE,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'pendiente'
);

-- 13. Evaluaciones de desempeño
CREATE TABLE evaluacion_desempeno (
    id SERIAL PRIMARY KEY,
    rut_trabajador VARCHAR(20) NOT NULL REFERENCES trabajador(rut) ON DELETE CASCADE,
    fecha_evaluacion DATE NOT NULL,
    evaluador VARCHAR(100) NOT NULL,
    puntuacion INTEGER NOT NULL CHECK (puntuacion BETWEEN 1 AND 10),
    comentarios TEXT
);

-- 14. Capacitaciones / cursos
CREATE TABLE capacitacion (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    lugar VARCHAR(100)
);

-- 15. Relación trabajador <-> capacitacion
CREATE TABLE trabajador_capacitacion (
    id SERIAL PRIMARY KEY,
    rut_trabajador VARCHAR(20) NOT NULL REFERENCES trabajador(rut) ON DELETE CASCADE,
    capacitacion_id INTEGER NOT NULL REFERENCES capacitacion(id) ON DELETE CASCADE,
    estado VARCHAR(20) NOT NULL DEFAULT 'inscrito',
    UNIQUE(rut_trabajador, capacitacion_id)
);

-- 16. Beneficios disponibles
CREATE TABLE beneficio (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- 17. Relación trabajador <-> beneficio
CREATE TABLE trabajador_beneficio (
    id SERIAL PRIMARY KEY,
    rut_trabajador VARCHAR(20) NOT NULL REFERENCES trabajador(rut) ON DELETE CASCADE,
    beneficio_id INTEGER NOT NULL REFERENCES beneficio(id) ON DELETE CASCADE,
    fecha_asignacion DATE NOT NULL DEFAULT CURRENT_DATE,
    estado VARCHAR(20) NOT NULL DEFAULT 'activo',
    UNIQUE(rut_trabajador, beneficio_id)
);

-- ===========================
-- INSERCIÓN DE DATOS
-- ===========================

-- Áreas
INSERT INTO area(nombre) VALUES
    ('Tecnologías de la Información'),
    ('Recursos Humanos'),
    ('Finanzas'),
    ('Operaciones'),
    ('Marketing');

-- Departamentos
INSERT INTO departamento(area_id, nombre) VALUES
    (1, 'Desarrollo'),
    (1, 'Infraestructura'),
    (2, 'Selección'),
    (2, 'Capacitación'),
    (3, 'Contabilidad'),
    (3, 'Tesorería'),
    (4, 'Logística'),
    (4, 'Producción'),
    (5, 'Digital'),
    (5, 'Publicidad');

-- Roles
INSERT INTO rol(nombre, descripcion) VALUES
    ('trabajador', 'Empleado con acceso a sus datos personales'),
    ('rrhh', 'Personal de Recursos Humanos'),
    ('jefe_rrhh', 'Jefe de Recursos Humanos'),
    ('admin', 'Administrador del sistema');

-- Trabajadores
INSERT INTO trabajador(rut, nombre, sexo, direccion, telefono, fecha_nacimiento, email) VALUES
    ('11111111-1', 'Ana Gómez', 'Femenino', 'Av. Siempre Viva 100', '+56911111111', '1990-03-15', 'ana.gomez@example.com'),
    ('22222222-2', 'Pedro Ruiz', 'Masculino', 'Calle Luna 200', '+56922222222', '1985-07-20', 'pedro.ruiz@example.com'),
    ('33333333-3', 'Laura Fernández', 'Femenino', 'Calle Sol 300', '+56933333333', '1992-11-05', 'laura.fernandez@example.com'),
    ('44444444-4', 'Miguel Torres', 'Masculino', 'Av. Central 400', '+56944444444', '1988-02-28', 'miguel.torres@example.com'),
    ('55555555-5', 'Sofía Martínez', 'Femenino', 'Calle Norte 500', '+56955555555', '1991-06-10', 'sofia.martinez@example.com');

-- Datos laborales
INSERT INTO datos_laborales(rut_trabajador, cargo, fecha_de_ingreso, area_id, departamento_id, estado) VALUES
    ('11111111-1', 'Desarrolladora', '2024-01-10', 1, 1, 'activo'),
    ('22222222-2', 'Analista RRHH', '2023-06-01', 2, 3, 'activo'),
    ('33333333-3', 'Contadora', '2022-09-15', 3, 5, 'activo'),
    ('44444444-4', 'Técnico Infraestructura', '2023-11-20', 1, 2, 'activo'),
    ('55555555-5', 'Especialista Marketing', '2024-03-05', 5, 9, 'activo');

-- Contactos de emergencia
INSERT INTO contactos_emergencia(rut_trabajador, nombre_contacto, relacion, telefono_contacto) VALUES
    ('11111111-1', 'Carlos Gómez', 'Cónyuge', '+56999999991'),
    ('11111111-1', 'María López', 'Madre', '+56999999992'),
    ('22222222-2', 'Juan Ruiz', 'Hermano', '+56988888882'),
    ('33333333-3', 'Sofía Fernández', 'Hermana', '+56977777773'),
    ('44444444-4', 'Paula Torres', 'Esposa', '+56966666664'),
    ('55555555-5', 'Martín Martínez', 'Padre', '+56955555000');

-- Cargas familiares
INSERT INTO cargas_familiares(rut_trabajador, nombre, parentesco, sexo, rut) VALUES
    ('11111111-1', 'Lucía Gómez', 'Hija', 'Femenino', '66666666-6'),
    ('22222222-2', 'Sara Ruiz', 'Hija', 'Femenino', '77777777-7'),
    ('33333333-3', 'Diego Fernández', 'Hijo', 'Masculino', '88888888-8'),
    ('44444444-4', 'Laura Torres', 'Hija', 'Femenino', '99999999-9');

-- Usuarios
INSERT INTO usuario(username, password_hash, rol_id, rut_trabajador) VALUES
    ('ana.g', '<HASH_ANA>', 1, '11111111-1'),
    ('pedro.r', '<HASH_PEDRO>', 1, '22222222-2'),
    ('laura.f', '<HASH_LAURA>', 1, '33333333-3'),
    ('rrhh.user', '<HASH_RRHH>', 2, NULL),
    ('jefe.rrhh', '<HASH_JEFE>', 3, NULL),
    ('admin', '<HASH_ADMIN>', 4, NULL);

-- Logs de acceso
INSERT INTO log_acceso(usuario_id, fecha, exito, ip_origen) VALUES
    (1, NOW() - INTERVAL '5 days', TRUE, '192.168.1.10'),
    (1, NOW() - INTERVAL '4 days', FALSE, '192.168.1.10'),
    (4, NOW() - INTERVAL '2 days', TRUE, '192.168.1.20'),
    (5, NOW() - INTERVAL '1 day', TRUE, '192.168.1.30');

-- Historial de cambios
INSERT INTO historial_cambios(rut_trabajador, campo, valor_anterior, valor_nuevo, fecha, usuario_id) VALUES
    ('11111111-1', 'direccion', 'Av. Vieja 50', 'Av. Siempre Viva 100', NOW() - INTERVAL '30 days', 4),
    ('22222222-2', 'telefono', '+56977777777', '+56922222222', NOW() - INTERVAL '15 days', 4),
    ('33333333-3', 'email', 'laura.old@example.com', 'laura.fernandez@example.com', NOW() - INTERVAL '10 days', 4);

-- Asistencia
INSERT INTO asistencia(rut_trabajador, fecha, hora_entrada, hora_salida, estado) VALUES
    ('11111111-1', CURRENT_DATE - INTERVAL '3 days', '09:00', '18:00', 'presente'),
    ('11111111-1', CURRENT_DATE - INTERVAL '2 days', '09:15', '18:05', 'presente'),
    ('22222222-2', CURRENT_DATE - INTERVAL '3 days', NULL, NULL, 'ausente'),
    ('33333333-3', CURRENT_DATE - INTERVAL '1 day', '08:55', '17:50', 'presente'),
    ('44444444-4', CURRENT_DATE - INTERVAL '1 day', '09:10', '18:10', 'presente'),
    ('55555555-5', CURRENT_DATE - INTERVAL '2 days', '09:05', '18:00', 'presente');

-- Vacaciones / permisos
INSERT INTO vacaciones(rut_trabajador, fecha_inicio, fecha_fin, tipo, estado) VALUES
    ('11111111-1', '2025-01-05', '2025-01-20', 'vacaciones anuales', 'aprobado'),
    ('22222222-2', '2025-02-10', '2025-02-12', 'licencia médica', 'pendiente'),
    ('33333333-3', '2025-03-01', '2025-03-05', 'vacaciones anuales', 'aprobado');

-- Evaluaciones de desempeño
INSERT INTO evaluacion_desempeno(rut_trabajador, fecha_evaluacion, evaluador, puntuacion, comentarios) VALUES
    ('11111111-1', '2024-12-01', 'Jefe TI', 8, 'Buen desempeño general.'),
    ('22222222-2', '2024-11-15', 'Jefe RRHH', 7, 'Cumple con expectativas.'),
    ('33333333-3', '2024-10-20', 'Jefe Finanzas', 9, 'Excelente atención al detalle.');

-- Capacitaciones
INSERT INTO capacitacion(nombre, descripcion, fecha_inicio, fecha_fin, lugar) VALUES
    ('Curso Python Básico', 'Introducción a Python para empleados', '2024-08-01', '2024-08-05', 'Sala 101'),
    ('Taller Liderazgo', 'Desarrollo de habilidades de liderazgo', '2024-09-10', '2024-09-12', 'Centro RRHH'),
    ('Seminario Finanzas Avanzadas', 'Profundización en análisis financiero', '2024-10-15', '2024-10-17', 'Sala Finanzas');

-- Relación trabajador <-> capacitacion
INSERT INTO trabajador_capacitacion(rut_trabajador, capacitacion_id, estado) VALUES
    ('11111111-1', 1, 'completado'),
    ('22222222-2', 2, 'inscrito'),
    ('33333333-3', 3, 'inscrito');

-- Beneficios
INSERT INTO beneficio(nombre, descripcion) VALUES
    ('Seguro Médico', 'Cobertura de salud para el empleado'),
    ('Caja de Compensación', 'Descuento en Caja de Compensación'),
    ('Ticket Restaurante', 'Beneficio de alimentación');

-- Relación trabajador <-> beneficio
INSERT INTO trabajador_beneficio(rut_trabajador, beneficio_id, fecha_asignacion, estado) VALUES
    ('11111111-1', 1, '2024-01-15', 'activo'),
    ('33333333-3', 2, '2024-06-01', 'activo'),
    ('55555555-5', 3, '2024-07-01', 'activo');

-- ===========================
-- ÍNDICES
-- ===========================

CREATE INDEX idx_datos_laborales_area ON datos_laborales(area_id);
CREATE INDEX idx_datos_laborales_depto ON datos_laborales(departamento_id);
CREATE INDEX idx_asistencia_fecha ON asistencia(fecha);
CREATE INDEX idx_vacaciones_estado ON vacaciones(estado);
