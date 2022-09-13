
-- import from ddl.sql to create tables if needed 
.read ./resources/ddl.sql

-- insert data into the location table
insert into location (name, x_coord, y_coord) values 
    ('A', 4, 4),
    ('B', 2, 0),
    ('C', 8, 0),
    ('D', 0, 1),
    ('E', 1, 1),
    ('F', 5, 2),
    ('G', 7, 2),
    ('H', 3, 3),
    ('I', 5, 5),
    ('J', 8, 5),
    ('K', 1, 6),
    ('L', 2, 6),
    ('M', 6, 7),
    ('N', 3, 8),
    ('O', 6, 9),
    ('P', 0, 10),
    ('Q', 7, 10);