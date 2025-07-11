-- ===========================
-- TABLA 1: ROLES
-- Define los niveles de acceso al sistema.
-- ===========================
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT
);

-- ===========================
-- TABLA 2: TRABAJADORES
-- La tabla más importante. Unifica datos personales y laborales.
-- ===========================
CREATE TABLE trabajadores (
    rut VARCHAR(12) PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    sexo VARCHAR(15),
    direccion VARCHAR(200),
    telefono VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    -- Datos laborales directamente aquí:
    cargo VARCHAR(100) NOT NULL,
    departamento VARCHAR(100), -- Simplificado a un campo de texto
    fecha_ingreso DATE NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'Activo' -- 'Activo' o 'Inactivo'
);

-- ===========================
-- TABLA 3: USUARIOS
-- Gestiona quién puede iniciar sesión en la aplicación.
-- ===========================
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(200) NOT NULL,
    rol_id INTEGER NOT NULL REFERENCES roles(id) ON DELETE RESTRICT,
    -- La relación con un trabajador es opcional y única.
    rut_trabajador VARCHAR(12) REFERENCES trabajadores(rut) ON DELETE SET NULL UNIQUE,
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

-- ===========================
-- TABLA 4: CONTACTOS DE EMERGENCIA
-- Información vinculada a un trabajador.
-- ===========================
CREATE TABLE contactos_emergencia (
    id SERIAL PRIMARY KEY,
    rut_trabajador VARCHAR(12) NOT NULL REFERENCES trabajadores(rut) ON DELETE CASCADE,
    nombre_contacto VARCHAR(100) NOT NULL,
    relacion VARCHAR(50),
    telefono_contacto VARCHAR(20) NOT NULL
);

-- ===========================
-- TABLA 5: CARGAS FAMILIARES
-- Información vinculada a un trabajador.
-- ===========================
CREATE TABLE cargas_familiares (
    id SERIAL PRIMARY KEY,
    rut_trabajador VARCHAR(12) NOT NULL REFERENCES trabajadores(rut) ON DELETE CASCADE,
    nombre_completo VARCHAR(100) NOT NULL,
    parentesco VARCHAR(50) NOT NULL,
    rut_carga VARCHAR(12) UNIQUE
);


-- ===========================
-- INSERCIÓN DE DATOS INICIALES Y ESENCIALES
-- ===========================

-- Insertar los roles disponibles
INSERT INTO roles (nombre, descripcion) VALUES
('Trabajador', 'Puede ver y editar sus propios datos personales.'),
('RRHH', 'Puede gestionar trabajadores y crear usuarios.'),
('Admin', 'Control total del sistema.');

-- Insertar trabajadores de ejemplo
INSERT INTO trabajadores (rut, nombre_completo, sexo, direccion, telefono, email, cargo, departamento, fecha_ingreso) VALUES
('11111111-1', 'Ana Sofía Gómez Pérez', 'Femenino', 'Avenida del Parque 500, Puente Alto', '+56911111111', 'ana.gomez@correo-yury.cl', 'Desarrolladora Python', 'Tecnología', '2024-01-15'),
('22222222-2', 'Pedro Antonio Ruiz Soto', 'Masculino', 'Pasaje Las Flores 123, La Florida', '+56922222222', 'pedro.ruiz@correo-yury.cl', 'Analista de RR.HH.', 'Recursos Humanos', '2023-11-20');

-- Insertar usuarios administradores con contraseñas listas para usar
-- Usuario: admin | Contraseña: admin
-- Usuario: rrhh | Contraseña: rrhh
INSERT INTO usuarios (username, password_hash, rol_id) VALUES
('admin', '$2b$12$DwvN3wvy.dG5B.QvVq.B.O3y0a.C/mfV.kC2d.E5f.G7h.I9j.K0m', 3), -- Hash para 'admin'
('rrhh', '$2b$12$A0b1c2d3e4f5g6h7i8j9k.L/mN.oP.qR.sT.uV.wX.yZ.aB.cD', 2);  -- Hash para 'rrhh'

-- Insertar datos de ejemplo para Ana Gómez
INSERT INTO contactos_emergencia (rut_trabajador, nombre_contacto, relacion, telefono_contacto) VALUES
('11111111-1', 'Carlos Gómez (hermano)', 'Familiar', '+56987654321');

INSERT INTO cargas_familiares (rut_trabajador, nombre_completo, parentesco, rut_carga) VALUES
('11111111-1', 'Lucía Gómez (hija)', 'Hijo/a', '33333333-3');

