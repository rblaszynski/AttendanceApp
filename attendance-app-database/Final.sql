
CREATE TABLE [dbo].[Studenci](
	[nr] [int] IDENTITY(1,1) NOT NULL,
	[firstName] [varchar](25) NOT NULL,
	[lastName] [varchar](25) NOT NULL,
	[nr_indeksu] [int] NOT NULL,
	[id] [varchar](50) NOT NULL,
PRIMARY KEY (nr))

CREATE TABLE [dbo].[Przedmioty](
	[classID] [int] IDENTITY(1,1) NOT NULL,
	[className] [varchar](25) NOT NULL
PRIMARY KEY (classID))

CREATE TABLE [dbo].[Obecnosci](
	[nr] [int] IDENTITY(1,1) NOT NULL,
	[data] [varchar](25) NOT NULL,
	[classID] [int] NOT NULL,
	[group] [varchar](10) NOT NULL,
	[classStartDate] [varchar](5) NOT NULL,
	[classEndDate] [varchar](5) NOT NULL,
	[isPresent] [bit] NOT NULL,
	[id] [varchar](50) NOT NULL
PRIMARY KEY (nr)
FOREIGN KEY (classID) REFERENCES Przedmioty(classID))

INSERT INTO Przedmioty(className)
VALUES('PT-1')

INSERT INTO Przedmioty(className)
VALUES('PT-2')

INSERT INTO Przedmioty(className)
VALUES('TSM-1')

INSERT INTO Przedmioty(className)
VALUES('TSM-2')

INSERT INTO Studenci(firstName,lastName,nr_indeksu,id)
VALUES('Michal','Andrzejewski',131131,'013697D7')

INSERT INTO Studenci(firstName,lastName,nr_indeksu,id)
VALUES('Przemyslaw','Barlog',131123,'0136C21C')

INSERT INTO Studenci(firstName,lastName,nr_indeksu,id)
VALUES('Dominik','Blaszczyk',131733,'013697G8')

INSERT INTO Studenci(firstName,lastName,nr_indeksu,id)
VALUES('Robert','Blaszynski',131734,'0136C2T4')

INSERT INTO Studenci(firstName,lastName,nr_indeksu,id)
VALUES('Jan','Kowalski',131231,'01369891')

INSERT INTO Studenci(firstName,lastName,nr_indeksu,id)
VALUES('Piotr','Nowak',131198,'0136AB87')

INSERT INTO Studenci(firstName,lastName,nr_indeksu,id)
VALUES('Adam','Malysz',131112,'013697U2')

INSERT INTO Studenci(firstName,lastName,nr_indeksu,id)
VALUES('Mariusz','Pudzianowski',131199,'0136CZ73')

INSERT INTO Studenci(firstName,lastName,nr_indeksu,id)
VALUES('Robert','Kubica',131190,'013697F1')

INSERT INTO Studenci(firstName,lastName,nr_indeksu,id)
VALUES('Robert','Lewandowski',131195,'0136CZ75')

INSERT INTO Obecnosci([data],classID,[group],classStartDate, classEndDate, isPresent,id)
values('2019-06-05',1,'TI-1', '15:10','16:40',0,'013697D7')

INSERT INTO Obecnosci([data],classID,[group],classStartDate, classEndDate, isPresent,id)
values('2019-06-05',1,'TI-1', '15:10','16:40',1,'0136C21C')

INSERT INTO Obecnosci([data],classID,[group],classStartDate, classEndDate, isPresent,id)
values('2019-06-08',2,'TI-2', '08:00','09:30',1,'013697G8')

INSERT INTO Obecnosci([data],classID,[group],classStartDate, classEndDate, isPresent,id)
values('2019-06-08',2,'TI-2', '08:00','09:30',1,'0136C2T4')

INSERT INTO Obecnosci([data],classID,[group],classStartDate, classEndDate, isPresent,id)
values('2019-06-10',3,'TI-3', '09:45','11:15',0,'01369891')

INSERT INTO Obecnosci([data],classID,[group],classStartDate, classEndDate, isPresent,id)
values('2019-06-10',3,'TI-3', '09:45','11:15',1,'0136AB87')

INSERT INTO Obecnosci([data],classID,[group],classStartDate, classEndDate, isPresent,id)
values('2019-06-11',4,'TI-4', '15:10','16:40',1,'013697U2')

INSERT INTO Obecnosci([data],classID,[group],classStartDate, classEndDate, isPresent,id)
values('2019-06-05',4,'TI-4', '15:10','16:40',0,'0136CZ73')

INSERT INTO Obecnosci([data],classID,[group],classStartDate, classEndDate, isPresent,id)
values('2019-06-12',1,'TI-1', '15:10','16:40',0,'013697F1')

INSERT INTO Obecnosci([data],classID,[group],classStartDate, classEndDate, isPresent,id)
values('2019-06-12',2,'TI-1', '15:10','16:40',1,'0136CZ75')

SELECT * FROM Obecnosci

SELECT * FROM Studenci
