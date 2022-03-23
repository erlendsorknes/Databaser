import sqlite3
from sqlite3 import DatabaseError
from datetime import date


def isValidEmail(email):
    connection = sqlite3.connect("CoffeeDatabase.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM coffeeUser WHERE email = ?", (email,))
    row = cursor.fetchone()
    if not row:
        raise DatabaseError
    connection.close()
    return row[0], row[2]


def logIn():
    while True:
        try:
            coffeeUserID, pw = isValidEmail(input("Skriv inn epostadresse: "))
        except DatabaseError:
            print("Denne epostadressen finnes ikke!")
            continue
        else:
            break
    while True:
        passordSkrevetInn = input("Skriv inn passord: ")
        if pw == passordSkrevetInn:
            break
        else:
            print("Dette passordet passer ikke til epostadressen!")
            continue

    return coffeeUserID


def findRoastery(roasteryName):
    connection = sqlite3.connect("CoffeeDatabase.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM coffeeRoastery WHERE roasteryName = ?", (roasteryName,))
    row = cursor.fetchone()
    if not row:
        raise DatabaseError
    connection.close()
    return row[0]


def makeReview():
    userID = logIn()
    while True:
        try:
            roasteryID = findRoastery(input("Skriv inn brenneriet kaffen er fra: "))
        except DatabaseError:
            print("Dette brenneriet finnes ikke")
            continue
        else:
            break
    while True:
        try:
            roastedCoffeeID = validCoffeeFromRoastery(input("Hva heter kaffen? "), roasteryID)
        except:
            print("Denne kaffen finnes ikke")
            continue
        else:
            break

    while True:
        con = sqlite3.connect("CoffeeDatabase.db")
        cursor = con.cursor()
        points = int(input("Hva vil du rangere kaffen? (1-10) "))
        note = str(input("Forklar kaffen: "))
        date = str(input("Hvilken dato smakte du kaffen? "))
        cursor.execute("INSERT INTO review VALUES (?,?,?,?,?,?)",
                       (None, points, note, roastedCoffeeID, userID, date,))
        print("Takk for anmeldelsen!")
        con.commit()
        con.close()
        break


def validCoffeeFromRoastery(coffee, roasteryID):
    connection = sqlite3.connect("CoffeeDatabase.db")
    cursor = connection.cursor()
    cursor.execute("SELECT roastedCoffeeID FROM roastedCoffee WHERE name = ? AND roastedCoffeeID = ? ",
                   (coffee, roasteryID))
    row = cursor.fetchone()
    if not row:
        raise DatabaseError
    connection.close()
    return row[0]


def userStory1():
    makeReview()


def userStory2():
    year = date.today().year
    con = sqlite3.connect("CoffeeDatabase.db")
    cursor = con.cursor()
    cursor.execute(f'''SELECT coffeeUser.fullname, COUNT(DISTINCT reviewID) as antall_typer FROM coffeeUser NATURAL JOIN 
                   review WHERE review.tastingDate LIKE '%{year}%' GROUP BY coffeeUser.userID ORDER BY antall_typer 
                   DESC''')
    rows = cursor.fetchall()
    print("Brukere som har anmeldt flest unike kaffer i synkende rekkefølge: \n")
    for row in rows:
        print(row)
    con.close()


def userStory3():
    con = sqlite3.connect("CoffeeDatabase.db")
    cursor = con.cursor()
    cursor.execute("SELECT roastedCoffee.name, coffeeRoastery.roasteryName, avg(points) as avergePoints, kiloPrice "
                   "FROM review NATURAL JOIN roastedCoffee NATURAL JOIN coffeeRoastery GROUP BY roastedCoffeeID ORDER "
                   "BY (avergePoints / roastedCoffee.kiloPrice) DESC ")
    rows = cursor.fetchall()
    print("Hver kaffe og dens brenneri med gjennomsnittspoeng delt på kilopris i synkende rekkefølge: \n  ")
    for row in rows:
        print(row)
    con.close()


def userStory4():
    con = sqlite3.connect("CoffeeDatabase.db")
    cursor = con.cursor()
    cursor.execute("SELECT roastedCoffee.description, coffeeRoastery.roasteryName "
                   "FROM roastedCoffee NATURAL JOIN coffeeRoastery "
                   "WHERE roastedCoffee.description LIKE '%floral%' GROUP BY "
                   "roastedCoffee.roastedCoffeeID "
                   "UNION SELECT review.reviewNote, coffeeRoastery.roasteryName FROM review NATURAL JOIN roastedCoffee NATURAL JOIN coffeeRoastery WHERE reviewNote LIKE "
                   "'%floral%' GROUP BY roastedCoffeeID " )
    rows = cursor.fetchall()
    print("Hver kaffe som har en anmeldelse eller beskrivelse som er beskrevet som 'Floral: \n ")
    for row in rows:
        print(row)
    con.close()


def userStory5():
    con = sqlite3.connect("CoffeeDatabase.db")
    cursor = con.cursor()
    cursor.execute("SELECT roastedCoffee.name, coffeeRoastery.roasteryName "
                   "FROM roastedCoffee NATURAL JOIN coffeeRoastery NATURAL JOIN batch JOIN farm f on batch.farmID = "
                   "f.farmID JOIN processingMethod pM on batch.processingMethodID = pM.processingMethodID WHERE(NOT("
                   "pM.name == 'Vasket')) AND (f.country == 'Colombia') OR (f.country == 'Rwanda') ")
    rows = cursor.fetchall()
    print("Kaffer og dens brennerier som ikke er 'Vasket', men kommmer fra Colombia eller Rwanda: \n")
    for row in rows:
        print(row)
    con.close()


def main():
    active = True
    while active:
        storyInput = str(input("Hvilken brukerhistorie vil du utføre? (1-5) Trykk 'q' for å stoppe. "))
        if storyInput == '1':
            userStory1()
        elif storyInput == '2':
            userStory2()
        elif storyInput == '3':
            userStory3()
        elif storyInput == '4':
            userStory4()
        elif storyInput == '5':
            userStory5()
        elif storyInput == 'q':
            active = False
        else:
            print("Kunne ikke lese")


print(main())
