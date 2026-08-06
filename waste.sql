SQL STATEMENTS:

-- DROP TABLES--
DROP TABLE Collection_Event;
DROP TABLE Collection_Bin;
DROP TABLE Staff;
DROP TABLE Waste;
DROP TABLE Building;


-- STAFF TABLE -- 
CREATE TABLE Staff (
    staffID NUMBER PRIMARY KEY,
    staffName VARCHAR2(50)
);

-- BUILDING TABLE --
CREATE TABLE Building (
    buildingName VARCHAR2(100) PRIMARY KEY,
    buildingPfx VARCHAR2(10),
    currentShift VARCHAR2(20),
    staffID NUMBER,
    FOREIGN KEY(staffID) REFERENCES Staff(staffID)
);

-- WASTE TABLE -- 
CREATE TABLE Waste (
    wasteTypeID INT PRIMARY KEY,
    wasteName VARCHAR2(50)
);

-- COLLECTION BIN TABLE -- 
CREATE TABLE Collection_Bin (
    binID NUMBER PRIMARY KEY,
    binLocation VARCHAR2(100),
    buildingName VARCHAR2(100),
    wasteTypeID INT,
    FOREIGN KEY(buildingName) REFERENCES Building(buildingName),
    FOREIGN KEY(wasteTypeID) REFERENCES Waste(wasteTypeID)
);


-- COLLECTION EVENT TABLE -- 
CREATE TABLE Collection_Event (
    collectionID NUMBER PRIMARY KEY,
    collectionDate DATE,
    collectionWeight NUMBER(10,3),
    binID NUMBER,
    staffID NUMBER,
    buildingName VARCHAR2(100),
    FOREIGN KEY (binID) REFERENCES Collection_Bin(binID),
    FOREIGN KEY (staffID) REFERENCES Staff(staffID),
    FOREIGN KEY (buildingName) REFERENCES Building(buildingName)
);


INSERT INTO Building (buildingName, buildingPfx,currentShift,staffID ) VALUES ('Murchie Science Building','MSB','Night',17211);
INSERT INTO Building (buildingName, buildingPfx,currentShift,staffID) VALUES ('University Pavilion', 'UPAV','Morning',17212);
INSERT INTO Building (buildingName, buildingPfx,currentShift,staffID) VALUES ('Harding Mott University Center','UCEN','Night',17213);
INSERT INTO Building (buildingName, buildingPfx,currentShift,staffID) VALUES ('Recreation Center', 'REC','Morning',17215);
INSERT INTO Building (buildingName, buildingPfx,currentShift,staffID) VALUES ('Frances Willson Thompson Library','FWTL','Morning',17214);
INSERT INTO Building (buildingName, buildingPfx,currentShift,staffID) VALUES ('French Hall', 'FHall','Night',17216);
INSERT INTO Building (buildingName, buildingPfx,currentShift,staffID) VALUES ('Riverfront Conference Center', 'RCC','Night',17217);
INSERT INTO Building (buildingName, buildingPfx,currentShift,staffID) VALUES ('Willam S White Building','WSWB','Morning',17218);
INSERT INTO Building (buildingName, buildingPfx,currentShift,staffID) VALUES ('NorthBank Center Building','NCB','Night',17219);
INSERT INTO Building (buildingName, buildingPfx,currentShift,staffID) VALUES ('First Street Residence Hall','FSRH','Night',17220);


INSERT INTO Staff (staffID, staffName)
VALUES (17211, 'Alice Johnson');

INSERT INTO Staff (staffID, staffName)
VALUES (17212, 'Michael Smith');

INSERT INTO Staff (staffID, staffName)
VALUES (17213, 'Fatima Ali');

INSERT INTO Staff (staffID, staffName)
VALUES (17214, 'David Kwame');

INSERT INTO Staff (staffID, staffName)
VALUES (17215, 'Joyce Mitchual');

INSERT INTO Staff (staffID, staffName)
VALUES (17216, 'Alice Johnson');

INSERT INTO Staff (staffID, staffName)
VALUES (17217, 'Oluchi Obadoni');

INSERT INTO Staff (staffID, staffName)
VALUES (17218, 'Frank Stewart');

INSERT INTO Staff (staffID, staffName)
VALUES (17219, 'Manuella Kroger');

INSERT INTO Staff (staffID, staffName)
VALUES (17220, 'Webber Merilyn');


INSERT INTO Waste (wasteTypeID, wasteName) VALUES (1, 'Landfill');
INSERT INTO Waste (wasteTypeID, wasteName) VALUES (2, 'Recyclables');
INSERT INTO Waste (wasteTypeID, wasteName) VALUES (3, 'Cardboard');
INSERT INTO Waste (wasteTypeID, wasteName) VALUES (4, 'Electronic Waste');

    
INSERT INTO Collection_Bin (binID, binLocation, buildingName, wasteTypeID)
VALUES (101, 'Ground Floor Lobby', 'Murchie Science Building', 1);

INSERT INTO Collection_Bin (binID, binLocation, buildingName, wasteTypeID)
VALUES (102, 'Second Floor Corridor', 'University Pavilion', 2);

INSERT INTO Collection_Bin (binID, binLocation, buildingName, wasteTypeID)
VALUES (103, 'Main Entrance', 'Harding Mott University Center', 2);

INSERT INTO Collection_Bin (binID, binLocation, buildingName, wasteTypeID)
VALUES (104, 'Basement', 'Recreation Center', 3);


-- INSERT COLLECTION EVENTS --
INSERT INTO Collection_Event (collectionID, collectionDate, collectionWeight, binID, staffID, buildingName)
VALUES (1, TO_DATE('2025-10-20', 'YYYY-MM-DD'), 23.45, 101, 17211, 'Murchie Science Building');

INSERT INTO Collection_Event (collectionID, collectionDate, collectionWeight, binID, staffID, buildingName)
VALUES (2, TO_DATE('2025-10-20', 'YYYY-MM-DD'), 23.45, 101, 17214, 'Murchie Science Building');

INSERT INTO Collection_Event (collectionID, collectionDate, collectionWeight, binID, staffID, buildingName)
VALUES (3, TO_DATE('2025-10-21', 'YYYY-MM-DD'), 15.20, 102, 17212, 'University Pavilion');

INSERT INTO Collection_Event (collectionID, collectionDate, collectionWeight, binID, staffID, buildingName)
VALUES (4, TO_DATE('2025-10-22', 'YYYY-MM-DD'), 18.75, 103, 17213, 'Harding Mott University Center');

INSERT INTO Collection_Event (collectionID, collectionDate, collectionWeight, binID, staffID, buildingName)
VALUES (5, TO_DATE('2025-10-22', 'YYYY-MM-DD'), 25.60, 104, 17215, 'Recreation Center');

COMMIT;


