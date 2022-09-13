-- sql scripts to create the tsp database

-- create the location table
create table if not exists location (
    id integer primary key AUTOINCREMENT,
    name varchar(255) not null,
    x_coord int not null,
    y_coord int not null
);

