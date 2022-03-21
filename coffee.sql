CREATE TABLE coffeeUser( 
userID INTEGER PRIMARY KEY AUTOINCREMENT ,
email UNIQUE NOT NULL, 
pw NOT NULL, 
fullName NOT NULL);


CREATE TABLE coffeeRoastery(
coffeeRoasteryID INTEGER PRIMARY KEY AUTOINCREMENT ,
roasteryName VARCHAR(30));


CREATE TABLE roastedCoffee( 
roastedCoffeeID INTEGER PRIMARY KEY AUTOINCREMENT,
name VARCHAR(30),
degreeOfBurning VARCHAR(15), 
kiloPrice INT, 
description VARCHAR(100), 
roastDate TEXT DEFAULT(date('now')), 
coffeeRoasteryID INT NOT NULL,
batchID INT NOT NULL, 
FOREIGN KEY(coffeeRoasteryID) REFERENCES coffeeRoastery(coffeeRoasteryID) ON DELETE CASCADE,
FOREIGN KEY(batchID) REFERENCES batch(batchID) ON DELETE CASCADE);


CREATE TABLE review(
reviewID INTEGER PRIMARY KEY AUTOINCREMENT ,
points INT,
reviewNote VARCHAR(200),
coffeeID INT NOT NULL,
userID INT NOT NULL,
tastingDate TEXT DEFAULT(date('now')),
FOREIGN KEY(roastedCoffeeID) REFERENCES roastedCoffee(roastedCoffeeID) ON DELETE CASCADE,
FOREIGN KEY(userID) REFERENCES coffeeUser(userID) ON DELETE CASCADE,
CHECK (points > -1 AND points < 11));



CREATE TABLE batch( 
batchID INTEGER PRIMARY KEY AUTOINCREMENT,
kgPrice INT, 
harvestYear TEXT DEFAULT (strftime('%Y','now')), 
farmID INT NOT NULL, 
processingMethodID INT NOT NULL, 
FOREIGN KEY(farmID) REFERENCES farm(farmID) ON DELETE CASCADE, 
FOREIGN KEY(processingMethodID) REFERENCES processingMethod(processingMethodID) ON DELETE CASCADE);

CREATE TABLE farmedBy( 
farmID INTEGER,
coffeeBeanID INT, 
PRIMARY KEY(farmID, coffeeBeanID),
FOREIGN KEY(coffeeBeanID) REFERENCES coffeeBean(coffeeBeanID) ON DELETE CASCADE, 
FOREIGN KEY(farmID) REFERENCES farm(farmID) ON DELETE CASCADE);


CREATE TABLE processingMethod( 
processingMethodID INTEGER PRIMARY KEY AUTOINCREMENT,
name VARCHAR(20),
description VARCHAR(500)); 

CREATE TABLE coffeeBean( 
coffeeBeanID INTEGER PRIMARY KEY AUTOINCREMENT,
name VARCHAR(30), 
species VARCHAR(30));


CREATE TABLE farm( 
farmID INTEGER PRIMARY KEY AUTOINCREMENT,
name VARCHAR(30), 
country VARCHAR(20), 
region VARCHAR(20), 
height INT); 

CREATE TABLE contains(
coffeeBeanID INT,
batchID INT,
PRIMARY KEY(batchID, coffeeBeanID),
FOREIGN KEY(batchID) REFERENCES batch(batchID) ON DELETE CASCADE,
FOREIGN KEY(coffeeBeanID) REFERENCES coffeeBean(coffeeBeanID) ON DELETE CASCADE);


