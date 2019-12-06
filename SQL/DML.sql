-- SQLite
INSERT INTO Cursante(codigo, dni, nombre, apellido, email, telefono, institucion)
VALUES (NULL, 38738347, 'Agustín',  'González',   NULL, 15678124, 'UNTDF'),
       (NULL, 43164843, 'María',    'Pérez',      NULL, 15789451, 'UTN'  ),
       (NULL, 36522250, 'José',     'Rigoni',     NULL, 15354987, 'UNTDF'),
       (NULL, 42060158, 'Federico', 'Suar',       NULL, 15215497, 'UNTDF'),
       (NULL, 40775983, 'Micaela',  'Kloster',    NULL, 15487951, 'UTN'  ),
       (NULL, 43478724, 'Rocío',    'Pereyra',    NULL, 15459781, 'OTRO' ),
       (NULL, 41422400, 'Hernesto', 'Domínguez',  NULL, 15345874, 'OTRO' ),
       (NULL, 42030416, 'Sabrina',  'Garay',      NULL, 15459574, 'OTRO' ),
       (NULL, 41822685, 'Santiago', 'Maciel',     NULL, 15598791, 'UNTDF'),
       (NULL, 43702214, 'Lorena',   'López',      NULL, 15321654, 'UTN'  ),
       (NULL, 40217391, 'Raúl',     'Palacios',   NULL, 15657987, 'UTN'  ),
       (NULL, 40628805, 'Brian',    'Villanueva', NULL, 15135457, 'UTN'  ),
       (NULL, 37204882, 'Camila',   'Gonzalez',   NULL, 15548975, 'UNTDF'),
       (NULL, 36057843, 'Gabriel',  'Sanchez',    NULL, 15654987, 'OTRO' ),
       (NULL, 39672258, 'Iván',     'Álvarez',    NULL, 15645498, 'OTRO' );


INSERT INTO Docente(codigo, dni, nombre, apellido, email, telefono, titulo)
VALUES (NULL, 32164549, 'Esteban',  'García',    NULL, 15456787, 'Lic. en Economía'),
       (NULL, 21645987, 'Tomás',    'Espíndola', NULL, 15212647, 'Máster en Informática'),
       (NULL, 12315648, 'Elisa',    'Gómez',     NULL, 15216547, 'Lic. en Historia'),
       (NULL, 15454987, 'Milagros', 'Pereyra',   NULL, 15324654, 'Lic. en Psicología'),
       (NULL, 24564896, 'Alicia',   'Nizovoy',   NULL, 15456781, 'Doctorado en Geología'),
       (NULL, 32465487, 'Valeria',  'Ferrer',    NULL, 15123575, 'Lic. Ciencias Ambientales'),
       (NULL, 16548594, 'Verónica', 'Lozano',    NULL, 15123454, 'Analísta técnico contable'),
       (NULL, 26548787, 'Mirta',    'Giménez',   NULL, 15235478, 'Lic. en Sistemas'),
       (NULL, 35548971, 'Agustina', 'Legrand',   NULL, 15126457, 'Lic. en Turismo'),
       (NULL, 34687954, 'Juana',    'Rizzo',     NULL, 15548754, 'Doctorado en Pediatría');


INSERT INTO Curso(codigo, nombre, fecha_inicio, fecha_fin, carga_horaria, lugar_dictado)
VALUES (NULL, 'Taller de Ciberseguridad',         '2019-10-28', '2019-10-31', 5, 'Kuanip 557'),
       (NULL, 'Taller de Desarrollo Sustentable', '2019-12-09', '2019-12-12', 8, 'San Martín 745'); 


INSERT INTO Administrador(codigo, dni, nombre, apellido, email, usuario, contrasena) 
VALUES (NULL, 37261933, "Kevin Edgardo", "Juarez Desch", NULL, "Admin", 1234);

