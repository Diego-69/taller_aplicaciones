-- Script para crear la estructura de la base de datos para "El correo de Yury"
-- Usar PostgreSQL

-- Tabla para los perfiles de usuario (Roles)
CREATE TABLE perfiles (
    id SERIAL PRIMARY KEY,
    nombre_perfil VARCHAR(50) UNIQUE NOT NULL -- Ej: 'Admin', 'RRHH', 'Trabajador'
);

CREATE TABLE areas (
    id SERIAL PRIMARY KEY,
    nombre_area VARCHAR(100) UNIQUE NOT NULL
);

-- Tabla para los departamentos, asociados a un área
CREATE TABLE departamentos (
    id SERIAL PRIMARY KEY,
    nombre_departamento VARCHAR(100) NOT NULL,
    id_area INTEGER NOT NULL,
    FOREIGN KEY (id_area) REFERENCES areas(id)
);

-- Tabla para los cargos de los trabajadores
CREATE TABLE cargos (
    id SERIAL PRIMARY KEY,
    nombre_cargo VARCHAR(100) UNIQUE NOT NULL
);

-- Tabla de usuarios para el login
-- La contraseña se debe almacenar como un hash (ej: bcrypt)
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre_usuario VARCHAR(50) UNIQUE NOT NULL,
    contrasena_hash VARCHAR(255) NOT NULL,
    id_perfil INTEGER NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_perfil) REFERENCES perfiles(id)
);

-- Tabla principal de trabajadores
CREATE TABLE trabajadores (
    rut VARCHAR(12) PRIMARY KEY, -- RUT como PK, ej: '12345678-9'
    id_usuario INTEGER UNIQUE, -- Un trabajador puede tener un usuario para login
    nombre_completo VARCHAR(200) NOT NULL,
    sexo VARCHAR(10) NOT NULL CHECK (sexo IN ('Masculino', 'Femenino', 'Otro')),
    direccion VARCHAR(255),
    telefono VARCHAR(20),
    fecha_ingreso DATE NOT NULL,
    id_cargo INTEGER NOT NULL,
    id_departamento INTEGER NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY (id_cargo) REFERENCES cargos(id),
    FOREIGN KEY (id_departamento) REFERENCES departamentos(id)
);

-- Tabla para cargas familiares
CREATE TABLE cargas_familiares (
    id SERIAL PRIMARY KEY,
    rut_carga VARCHAR(12) UNIQUE NOT NULL,
    trabajador_rut VARCHAR(12) NOT NULL,
    nombre_completo VARCHAR(200) NOT NULL,
    parentesco VARCHAR(50) NOT NULL,
    sexo VARCHAR(10) NOT NULL CHECK (sexo IN ('Masculino', 'Femenino', 'Otro')),
    FOREIGN KEY (trabajador_rut) REFERENCES trabajadores(rut) ON DELETE CASCADE
);

-- Tabla para contactos de emergencia
CREATE TABLE contactos_emergencia (
    id SERIAL PRIMARY KEY,
    trabajador_rut VARCHAR(12) NOT NULL,
    nombre_completo VARCHAR(200) NOT NULL,
    relacion VARCHAR(50) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    FOREIGN KEY (trabajador_rut) REFERENCES trabajadores(rut) ON DELETE CASCADE
);

-- Inserción de datos iniciales para empezar a operar
INSERT INTO perfiles (nombre_perfil) VALUES ('Admin'), ('RRHH'), ('Trabajador');
INSERT INTO areas (nombre_area) VALUES ('Tecnología'), ('Operaciones'), ('Administración');
INSERT INTO departamentos (nombre_departamento, id_area) VALUES 
    ('Desarrollo de Software', 1),
    ('Soporte TI', 1),
    ('Logística', 2),
    ('Recursos Humanos', 3);
INSERT INTO cargos (nombre_cargo) VALUES 
    ('Desarrollador Senior'), 
    ('Jefe de RRHH'), 
    ('Asistente de Logística'),
    ('Analista de Soporte');

-- Creación de un usuario de RRHH para el primer login
-- La contraseña es 'admin123'. En una aplicación real, esto se haría desde un formulario de registro seguro.
-- El hash corresponde a 'admin123' usando bcrypt.
INSERT INTO usuarios (nombre_usuario, contrasena_hash, id_perfil) VALUES 
('admin_rrhh', '$2b$12$DwtS.I3V5/vT4T5E5aH.IuW2hJjGPLX.2v3w.YgIeZgY.U.V.mZ.q', 2);

-- Creación de un trabajador asociado a ese usuario de RRHH
INSERT INTO trabajadores (rut, id_usuario, nombre_completo, sexo, direccion, telefono, fecha_ingreso, id_cargo, id_departamento) VALUES
('11222333-4', (SELECT id FROM usuarios WHERE nombre_usuario = 'admin_rrhh'), 'Juan Perez Gonzalez', 'Masculino', 'Av. Siempre Viva 123', '+56912345678', '2024-01-15', 2, 4);

COMMIT;
