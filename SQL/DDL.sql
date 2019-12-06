CREATE TABLE Administrador (
    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
    dni INTEGER UNIQUE NOT NULL,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    email TEXT,
    usuario TEXT UNIQUE NOT NULL,
    contrasena TEXT NOT NULL
);

CREATE TABLE Curso (
    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    carga_horaria INTEGER NOT NULL,
    lugar_dictado TEXT NOT NULL
);

CREATE TABLE Cursante (
    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
    dni INTEGER UNIQUE NOT NULL,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    email TEXT,
    telefono INTEGER,
    institucion TEXT NOT NULL
);

CREATE TABLE Inscripto (
    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_certificado TEXT,
    archivo BINARY,
    fecha_inscripcion DATE NOT NULL,
    cursante INTEGER NOT NULL REFERENCES Cursante(codigo),
    curso INTEGER NOT NULL REFERENCES Curso(codigo)
);

CREATE TABLE Asistencia ( 
    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha DATE NOT NULL,
    asistio BOOLEAN NOT NULL,
    inscripto INTEGER NOT NULL REFERENCES Inscripto(codigo),
    curso INTEGER NOT NULL REFERENCES Curso(codigo)
);

CREATE TABLE Docente ( 
    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
    dni INTEGER UNIQUE NOT NULL,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    email TEXT,
    telefono INTEGER,
    titulo TEXT NOT NULL
);

CREATE TABLE DocenteCurso (
    docente INTEGER NOT NULL REFERENCES Docente(codigo),
    curso INTEGER NOT NULL REFERENCES Curso(codigo)
);