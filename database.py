import sqlite3
from sqlite3 import DatabaseError
from datetime import date

userID = None


def isValidEmail(email):
    connection = sqlite3.connect("CoffeeDatabase.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM coffeeUser WHERE email = ?", (email,))
    row = cursor.fetchone()
    if not row:
        raise DatabaseError
    connection.close()
    return row[0], row[2]








def validRegisterEmail(email):
    connection = sqlite3.connect("CoffeeDatabase.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM coffeeUser WHERE email = ?", (email,))
    row = cursor.fetchone()
    if not row:
        return email
    else:
        return -1












def registerUser():
    while True:
        con = sqlite3.connect("CoffeeDatabase.db")
        cursor = con.cursor()
        email = input("Skriv inn epostadresse: ")
        if validRegisterEmail(email) == -1:
            print("Denne mailen finnes, velg en annen")
            continue
        password = str(input("Skriv inn passordet du vil ha "))
        name = str(input("Skriv inn ditt fulle navn"))
        cursor.execute("INSERT INTO coffeeUser VALUES (?,?,?,?)",
                       (None, email, password, name,))
        con.commit()
        cursor.execute("SELECT userID FROM coffeeUser WHERE email = ?", (email,))
        row = cursor.fetchone()
        global userID
        userID = row[0]
        mainMenu()


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

    global userID
    userID = coffeeUserID
    mainMenu()


def findRoastery(roasteryName):
    connection = sqlite3.connect("CoffeeDatabase.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM coffeeRoastery WHERE roasteryName = ?", (roasteryName,))
    row = cursor.fetchone()
    if not row:
        raise DatabaseError
    connection.close()
    return row[0]




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




def makeReview(userID):
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




def userStory4(input):
    con = sqlite3.connect("CoffeeDatabase.db")
    cursor = con.cursor()
    cursor.execute(f'''SELECT roastedCoffee.description, coffeeRoastery.roasteryName 
                   FROM roastedCoffee NATURAL JOIN coffeeRoastery 
                   WHERE roastedCoffee.description LIKE '%{input}%' GROUP BY 
                   roastedCoffee.roastedCoffeeID 
                   UNION SELECT review.reviewNote, coffeeRoastery.roasteryName FROM review NATURAL JOIN roastedCoffee NATURAL JOIN coffeeRoastery WHERE reviewNote LIKE 
                   '%{input}%' GROUP BY roastedCoffeeID ''')
    rows = cursor.fetchall()
    print(f'''Hver kaffe som har en anmeldelse eller beskrivelse som er beskrevet som '{input}': \n ''')
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






def seeStatistics():
    active = True
    while active:
        print("Velkommen til statistikk! \n")
        valg = str(input("Trykk 'b' for å se hvilke brukere som er mest aktive!\n"
                         "Trykk 's' for å søke etter et ord kaffen har blitt beskrevet som \n"
                         "Trykk 'k' for å finne de kaffene brukere er mest fornøyd med tanke på pris! \n"
                         "Trykk 'm' for å gå tilbake til hovedmenyen \n"
                         "Trykk 'u' for å se Ukas kaffer: \n"
                         "Trykk 'q' for å gå tilbake:  "))
        if valg == 's':
            search = str(input("Hvilket ord vil du søke etter? \n"))
            userStory4(search)
        elif valg == 'b':
            userStory2()

        elif valg == 'k':
            userStory3()


        elif valg == 'm':
            mainMenu()

        elif valg == 'u':
            userStory5()

        elif valg == 'q':
            break

        else:
            print("Skjønte ikke, prøv igjen")


def userStories():
    while True:
        print("Velkommen til brukerhistoriene! \n")
        story = str(input((
                                "Trykk '2' for å utføre brukerhistorie 2 \n"
                                "Trykk '3' for å utføre brukerhistorie 3 \n"
                                "trykk '4' for å utføre brukerhistorie 4 \n"
                                "Trykk på '5' for å utføre brukerhistorie 5\n"
                                "Trykk på 'q' for å gå tilbake")))

        if story == '2':
            userStory2()
        elif story == '3':
            userStory3()
        elif story == '4':
            userStory4('Floral')
        elif story == '5':
            userStory5()
        elif story == 'q':
            break
        else:
            print("Skriv inn noe gyldig")
            continue





def mainMenu():
    while True:
        print("Velkommen til hovedmenyen! \n")
        storyInput = str(input(("Trykk 'o' for opprette nytt innlegg \n"
                                "Trykk 's' for å se statistikk, \n"
                                "Trykk 'u' for å se brukerhistoriene \n"
                                "trykk 'q' for å logge ut ")))
        if storyInput == 'o':
            makeReview(userID)
        elif storyInput == 's':
            seeStatistics()
        elif storyInput == 'u':
            userStories()
        elif storyInput == 'q':
            break

        else:
            print("Kunne ikke lese")


def main():
    while True:
        choice = str(input("Velkommen til kaffeapplikasjonen!\n"
                           "Skriv 'l' for å logge inn, skriv 'r' for å registrere en ny bruker eller 'q' for å avslutte:  "))
        if choice == 'l':
            logIn()
        elif choice == 'r':
            registerUser()
        elif choice == 'q':
            break
        else:
            print("Skriv inn et gyldig valg")

print(main())