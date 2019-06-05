
ALTER TABLE Obecnosci 
DROP COLUMN "isPresent"

SP_RENAME 'Obecnosci.lokalizacja','przedmiot'

ALTER TABLE Obecnosci
ADD "grupa" varchar(4)

ALTER TABLE Obecnosci
ADD "startZajec" varchar(5)

ALTER TABLE Obecnosci
ADD "koniecZajec" varchar(5)

ALTER TABLE Obecnosci 
ADD "isPresent" bit


INSERT INTO Obecnosci(id,data,nr_legitymacji,przedmiot,grupa, startZajec, koniecZajec,isPresent)
values(1,'2019-06-05', '013697D7','Podstawy teleinformatyki','TI-1', '15:10','16:40',0)
INSERT INTO Obecnosci(id,data,nr_legitymacji,przedmiot,grupa, startZajec, koniecZajec,isPresent)
values(2,'2019-06-05', '0136C21C','Podstawy teleinformatyki','TI-1', '15:10','16:40',0)

select * from Obecnosci
