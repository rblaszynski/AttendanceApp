create database AttendanceApp_db

GO

use AttendanceApp_db

create table Studenci
(id int PRIMARY KEY NOT NULL,
imie varchar(25) NOT NULL,
nazwisko varchar(25) NOT NULL,
nr_indeksu int NOT NULL,
nr_legitymacji varchar(50) NOT NULL)

GO

create table Obecnosci
(id int PRIMARY KEY NOT NULL,
data DATE NOT NULL,
lokalizacja varchar(25) NOT NULL,
nr_legitymacji varchar(50) NOT NULL)

GO

create table Obecnosci_Studentow
(id int PRIMARY KEY NOT NULL,
id_studenta int NOT NULL,
id_obecnosci int NOT NULL,
FOREIGN KEY (id_studenta) REFERENCES Studenci(id),
FOREIGN KEY (id_obecnosci) REFERENCES Obecnosci(id))
