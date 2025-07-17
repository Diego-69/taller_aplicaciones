--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

-- Started on 2025-07-16 20:02:19

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = on;

DROP DATABASE IF EXISTS "correo_yury";
--
-- TOC entry 4885 (class 1262 OID 16638)
-- Name: correo_yury; Type: DATABASE; Schema: -; Owner: -
--

CREATE DATABASE "correo_yury" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Spain.1252';


\connect "correo_yury"

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = on;

--
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA "public";


--
-- TOC entry 220 (class 1259 OID 16649)
-- Name: areas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."areas" (
    "id" integer NOT NULL,
    "nombre_area" character varying(100) NOT NULL
);


--
-- TOC entry 219 (class 1259 OID 16648)
-- Name: areas_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."areas_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4886 (class 0 OID 0)
-- Dependencies: 219
-- Name: areas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."areas_id_seq" OWNED BY "public"."areas"."id";


--
-- TOC entry 229 (class 1259 OID 16719)
-- Name: cargas_familiares; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."cargas_familiares" (
    "id" integer NOT NULL,
    "rut_carga" character varying(12) NOT NULL,
    "trabajador_rut" character varying(12) NOT NULL,
    "nombre_completo" character varying(200) NOT NULL,
    "parentesco" character varying(50) NOT NULL,
    "sexo" character varying(10) NOT NULL,
    CONSTRAINT "cargas_familiares_sexo_check" CHECK ((("sexo")::"text" = ANY ((ARRAY['Masculino'::character varying, 'Femenino'::character varying, 'Otro'::character varying])::"text"[])))
);


--
-- TOC entry 228 (class 1259 OID 16718)
-- Name: cargas_familiares_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."cargas_familiares_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4887 (class 0 OID 0)
-- Dependencies: 228
-- Name: cargas_familiares_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."cargas_familiares_id_seq" OWNED BY "public"."cargas_familiares"."id";


--
-- TOC entry 224 (class 1259 OID 16670)
-- Name: cargos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."cargos" (
    "id" integer NOT NULL,
    "nombre_cargo" character varying(100) NOT NULL
);


--
-- TOC entry 223 (class 1259 OID 16669)
-- Name: cargos_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."cargos_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4888 (class 0 OID 0)
-- Dependencies: 223
-- Name: cargos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."cargos_id_seq" OWNED BY "public"."cargos"."id";


--
-- TOC entry 231 (class 1259 OID 16734)
-- Name: contactos_emergencia; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."contactos_emergencia" (
    "id" integer NOT NULL,
    "trabajador_rut" character varying(12) NOT NULL,
    "nombre_completo" character varying(200) NOT NULL,
    "relacion" character varying(50) NOT NULL,
    "telefono" character varying(20) NOT NULL
);


--
-- TOC entry 230 (class 1259 OID 16733)
-- Name: contactos_emergencia_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."contactos_emergencia_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4889 (class 0 OID 0)
-- Dependencies: 230
-- Name: contactos_emergencia_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."contactos_emergencia_id_seq" OWNED BY "public"."contactos_emergencia"."id";


--
-- TOC entry 222 (class 1259 OID 16658)
-- Name: departamentos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."departamentos" (
    "id" integer NOT NULL,
    "nombre_departamento" character varying(100) NOT NULL,
    "id_area" integer NOT NULL
);


--
-- TOC entry 221 (class 1259 OID 16657)
-- Name: departamentos_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."departamentos_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4890 (class 0 OID 0)
-- Dependencies: 221
-- Name: departamentos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."departamentos_id_seq" OWNED BY "public"."departamentos"."id";


--
-- TOC entry 218 (class 1259 OID 16640)
-- Name: perfiles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."perfiles" (
    "id" integer NOT NULL,
    "nombre_perfil" character varying(50) NOT NULL
);


--
-- TOC entry 217 (class 1259 OID 16639)
-- Name: perfiles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."perfiles_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4891 (class 0 OID 0)
-- Dependencies: 217
-- Name: perfiles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."perfiles_id_seq" OWNED BY "public"."perfiles"."id";


--
-- TOC entry 227 (class 1259 OID 16693)
-- Name: trabajadores; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."trabajadores" (
    "rut" character varying(12) NOT NULL,
    "id_usuario" integer,
    "nombre_completo" character varying(200) NOT NULL,
    "sexo" character varying(10) NOT NULL,
    "direccion" character varying(255),
    "telefono" character varying(20),
    "fecha_ingreso" "date" NOT NULL,
    "id_cargo" integer NOT NULL,
    "id_departamento" integer NOT NULL,
    CONSTRAINT "trabajadores_sexo_check" CHECK ((("sexo")::"text" = ANY ((ARRAY['Masculino'::character varying, 'Femenino'::character varying, 'Otro'::character varying])::"text"[])))
);


--
-- TOC entry 226 (class 1259 OID 16679)
-- Name: usuarios; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."usuarios" (
    "id" integer NOT NULL,
    "nombre_usuario" character varying(50) NOT NULL,
    "contrasena_hash" character varying(255) NOT NULL,
    "id_perfil" integer NOT NULL,
    "activo" boolean DEFAULT true
);


--
-- TOC entry 225 (class 1259 OID 16678)
-- Name: usuarios_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."usuarios_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4892 (class 0 OID 0)
-- Dependencies: 225
-- Name: usuarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."usuarios_id_seq" OWNED BY "public"."usuarios"."id";


--
-- TOC entry 4676 (class 2604 OID 16652)
-- Name: areas id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."areas" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."areas_id_seq"'::"regclass");


--
-- TOC entry 4681 (class 2604 OID 16722)
-- Name: cargas_familiares id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."cargas_familiares" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."cargas_familiares_id_seq"'::"regclass");


--
-- TOC entry 4678 (class 2604 OID 16673)
-- Name: cargos id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."cargos" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."cargos_id_seq"'::"regclass");


--
-- TOC entry 4682 (class 2604 OID 16737)
-- Name: contactos_emergencia id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."contactos_emergencia" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."contactos_emergencia_id_seq"'::"regclass");


--
-- TOC entry 4677 (class 2604 OID 16661)
-- Name: departamentos id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."departamentos" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."departamentos_id_seq"'::"regclass");


--
-- TOC entry 4675 (class 2604 OID 16643)
-- Name: perfiles id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."perfiles" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."perfiles_id_seq"'::"regclass");


--
-- TOC entry 4679 (class 2604 OID 16682)
-- Name: usuarios id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."usuarios" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."usuarios_id_seq"'::"regclass");


--
-- TOC entry 4868 (class 0 OID 16649)
-- Dependencies: 220
-- Data for Name: areas; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO "public"."areas" ("id", "nombre_area") VALUES (1, 'Tecnología') ON CONFLICT DO NOTHING;
INSERT INTO "public"."areas" ("id", "nombre_area") VALUES (2, 'Operaciones') ON CONFLICT DO NOTHING;
INSERT INTO "public"."areas" ("id", "nombre_area") VALUES (3, 'Administración') ON CONFLICT DO NOTHING;


--
-- TOC entry 4877 (class 0 OID 16719)
-- Dependencies: 229
-- Data for Name: cargas_familiares; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 4872 (class 0 OID 16670)
-- Dependencies: 224
-- Data for Name: cargos; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO "public"."cargos" ("id", "nombre_cargo") VALUES (1, 'Desarrollador Senior') ON CONFLICT DO NOTHING;
INSERT INTO "public"."cargos" ("id", "nombre_cargo") VALUES (2, 'Jefe de RRHH') ON CONFLICT DO NOTHING;
INSERT INTO "public"."cargos" ("id", "nombre_cargo") VALUES (3, 'Asistente de Logística') ON CONFLICT DO NOTHING;
INSERT INTO "public"."cargos" ("id", "nombre_cargo") VALUES (4, 'Analista de Soporte') ON CONFLICT DO NOTHING;


--
-- TOC entry 4879 (class 0 OID 16734)
-- Dependencies: 231
-- Data for Name: contactos_emergencia; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 4870 (class 0 OID 16658)
-- Dependencies: 222
-- Data for Name: departamentos; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO "public"."departamentos" ("id", "nombre_departamento", "id_area") VALUES (1, 'Desarrollo de Software', 1) ON CONFLICT DO NOTHING;
INSERT INTO "public"."departamentos" ("id", "nombre_departamento", "id_area") VALUES (2, 'Soporte TI', 1) ON CONFLICT DO NOTHING;
INSERT INTO "public"."departamentos" ("id", "nombre_departamento", "id_area") VALUES (3, 'Logística', 2) ON CONFLICT DO NOTHING;
INSERT INTO "public"."departamentos" ("id", "nombre_departamento", "id_area") VALUES (4, 'Recursos Humanos', 3) ON CONFLICT DO NOTHING;


--
-- TOC entry 4866 (class 0 OID 16640)
-- Dependencies: 218
-- Data for Name: perfiles; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO "public"."perfiles" ("id", "nombre_perfil") VALUES (1, 'Admin') ON CONFLICT DO NOTHING;
INSERT INTO "public"."perfiles" ("id", "nombre_perfil") VALUES (2, 'RRHH') ON CONFLICT DO NOTHING;
INSERT INTO "public"."perfiles" ("id", "nombre_perfil") VALUES (3, 'Trabajador') ON CONFLICT DO NOTHING;


--
-- TOC entry 4875 (class 0 OID 16693)
-- Dependencies: 227
-- Data for Name: trabajadores; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO "public"."trabajadores" ("rut", "id_usuario", "nombre_completo", "sexo", "direccion", "telefono", "fecha_ingreso", "id_cargo", "id_departamento") VALUES ('21056391-1', 17, 'Diego Ignacio Castillo', 'Masculino', 'ciudad gotica540', '925439525', '2025-07-16', 1, 1) ON CONFLICT DO NOTHING;


--
-- TOC entry 4874 (class 0 OID 16679)
-- Dependencies: 226
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO "public"."usuarios" ("id", "nombre_usuario", "contrasena_hash", "id_perfil", "activo") VALUES (1, 'admin_rrhh', '$2b$12$KASaDn1VOC7lfYMPai7D..4gd2VEEigKztBdhS3rXa6kWYedrz/KO', 2, true) ON CONFLICT DO NOTHING;
INSERT INTO "public"."usuarios" ("id", "nombre_usuario", "contrasena_hash", "id_perfil", "activo") VALUES (17, 'diego', '$2b$12$8JBJl3sGDr39YeAlvafaX.BEWP3benNxS1xU8B/noSOUnrZsbtWHm', 3, true) ON CONFLICT DO NOTHING;


--
-- TOC entry 4893 (class 0 OID 0)
-- Dependencies: 219
-- Name: areas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."areas_id_seq"', 3, true);


--
-- TOC entry 4894 (class 0 OID 0)
-- Dependencies: 228
-- Name: cargas_familiares_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."cargas_familiares_id_seq"', 1, false);


--
-- TOC entry 4895 (class 0 OID 0)
-- Dependencies: 223
-- Name: cargos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."cargos_id_seq"', 4, true);


--
-- TOC entry 4896 (class 0 OID 0)
-- Dependencies: 230
-- Name: contactos_emergencia_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."contactos_emergencia_id_seq"', 1, false);


--
-- TOC entry 4897 (class 0 OID 0)
-- Dependencies: 221
-- Name: departamentos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."departamentos_id_seq"', 4, true);


--
-- TOC entry 4898 (class 0 OID 0)
-- Dependencies: 217
-- Name: perfiles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."perfiles_id_seq"', 3, true);


--
-- TOC entry 4899 (class 0 OID 0)
-- Dependencies: 225
-- Name: usuarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."usuarios_id_seq"', 17, true);


--
-- TOC entry 4690 (class 2606 OID 16656)
-- Name: areas areas_nombre_area_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."areas"
    ADD CONSTRAINT "areas_nombre_area_key" UNIQUE ("nombre_area");


--
-- TOC entry 4692 (class 2606 OID 16654)
-- Name: areas areas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."areas"
    ADD CONSTRAINT "areas_pkey" PRIMARY KEY ("id");


--
-- TOC entry 4708 (class 2606 OID 16725)
-- Name: cargas_familiares cargas_familiares_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."cargas_familiares"
    ADD CONSTRAINT "cargas_familiares_pkey" PRIMARY KEY ("id");


--
-- TOC entry 4710 (class 2606 OID 16727)
-- Name: cargas_familiares cargas_familiares_rut_carga_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."cargas_familiares"
    ADD CONSTRAINT "cargas_familiares_rut_carga_key" UNIQUE ("rut_carga");


--
-- TOC entry 4696 (class 2606 OID 16677)
-- Name: cargos cargos_nombre_cargo_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."cargos"
    ADD CONSTRAINT "cargos_nombre_cargo_key" UNIQUE ("nombre_cargo");


--
-- TOC entry 4698 (class 2606 OID 16675)
-- Name: cargos cargos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."cargos"
    ADD CONSTRAINT "cargos_pkey" PRIMARY KEY ("id");


--
-- TOC entry 4712 (class 2606 OID 16739)
-- Name: contactos_emergencia contactos_emergencia_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."contactos_emergencia"
    ADD CONSTRAINT "contactos_emergencia_pkey" PRIMARY KEY ("id");


--
-- TOC entry 4694 (class 2606 OID 16663)
-- Name: departamentos departamentos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."departamentos"
    ADD CONSTRAINT "departamentos_pkey" PRIMARY KEY ("id");


--
-- TOC entry 4686 (class 2606 OID 16647)
-- Name: perfiles perfiles_nombre_perfil_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."perfiles"
    ADD CONSTRAINT "perfiles_nombre_perfil_key" UNIQUE ("nombre_perfil");


--
-- TOC entry 4688 (class 2606 OID 16645)
-- Name: perfiles perfiles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."perfiles"
    ADD CONSTRAINT "perfiles_pkey" PRIMARY KEY ("id");


--
-- TOC entry 4704 (class 2606 OID 16702)
-- Name: trabajadores trabajadores_id_usuario_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."trabajadores"
    ADD CONSTRAINT "trabajadores_id_usuario_key" UNIQUE ("id_usuario");


--
-- TOC entry 4706 (class 2606 OID 16700)
-- Name: trabajadores trabajadores_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."trabajadores"
    ADD CONSTRAINT "trabajadores_pkey" PRIMARY KEY ("rut");


--
-- TOC entry 4700 (class 2606 OID 16687)
-- Name: usuarios usuarios_nombre_usuario_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."usuarios"
    ADD CONSTRAINT "usuarios_nombre_usuario_key" UNIQUE ("nombre_usuario");


--
-- TOC entry 4702 (class 2606 OID 16685)
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."usuarios"
    ADD CONSTRAINT "usuarios_pkey" PRIMARY KEY ("id");


--
-- TOC entry 4718 (class 2606 OID 16728)
-- Name: cargas_familiares cargas_familiares_trabajador_rut_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."cargas_familiares"
    ADD CONSTRAINT "cargas_familiares_trabajador_rut_fkey" FOREIGN KEY ("trabajador_rut") REFERENCES "public"."trabajadores"("rut") ON DELETE CASCADE;


--
-- TOC entry 4719 (class 2606 OID 16740)
-- Name: contactos_emergencia contactos_emergencia_trabajador_rut_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."contactos_emergencia"
    ADD CONSTRAINT "contactos_emergencia_trabajador_rut_fkey" FOREIGN KEY ("trabajador_rut") REFERENCES "public"."trabajadores"("rut") ON DELETE CASCADE;


--
-- TOC entry 4713 (class 2606 OID 16664)
-- Name: departamentos departamentos_id_area_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."departamentos"
    ADD CONSTRAINT "departamentos_id_area_fkey" FOREIGN KEY ("id_area") REFERENCES "public"."areas"("id");


--
-- TOC entry 4715 (class 2606 OID 16708)
-- Name: trabajadores trabajadores_id_cargo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."trabajadores"
    ADD CONSTRAINT "trabajadores_id_cargo_fkey" FOREIGN KEY ("id_cargo") REFERENCES "public"."cargos"("id");


--
-- TOC entry 4716 (class 2606 OID 16713)
-- Name: trabajadores trabajadores_id_departamento_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."trabajadores"
    ADD CONSTRAINT "trabajadores_id_departamento_fkey" FOREIGN KEY ("id_departamento") REFERENCES "public"."departamentos"("id");


--
-- TOC entry 4717 (class 2606 OID 16703)
-- Name: trabajadores trabajadores_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."trabajadores"
    ADD CONSTRAINT "trabajadores_id_usuario_fkey" FOREIGN KEY ("id_usuario") REFERENCES "public"."usuarios"("id");


--
-- TOC entry 4714 (class 2606 OID 16688)
-- Name: usuarios usuarios_id_perfil_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."usuarios"
    ADD CONSTRAINT "usuarios_id_perfil_fkey" FOREIGN KEY ("id_perfil") REFERENCES "public"."perfiles"("id");


-- Completed on 2025-07-16 20:02:19

--
-- PostgreSQL database dump complete
--

