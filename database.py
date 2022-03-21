import sqlite3


def createUser():
    fullname = str(input("What is your full name? "))
    email = str(input("Write your email: "))
    password = str(input("Write your password: "))
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM sqlite_master")
    cursor.execute("INSERT INTO coffeeUser VALUES (?,?,?,?)", (None, email, password, fullname))
    con.commit()
    con.close()




def userStory2():
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM sqlite_master")
    cursor.execute("SELECT coffeeUser.fullname, COUNT(DISTINCT reviewID) as antall_typer FROM coffeeUser NATURAL JOIN "
                   "review GROUP BY coffeeUser.userID ORDER BY antall_typer DESC")
    rows = cursor.fetchall()
    print(rows)
    con.close()


def userStory3():
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM sqlite_master")
    cursor.execute("SELECT roastedCoffee.name, coffeeRoastery.roasteryName, avg(points) as avergePoints, kiloPrice "
                   "FROM review NATURAL JOIN roastedCoffee NATURAL JOIN coffeeRoastery GROUP BY roastedCoffeeID ORDER "
                   "BY (avergePoints / roastedCoffee.kiloPrice) DESC ")
    rows = cursor.fetchall()
    print(rows)
    con.close()



def userStory4():
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM sqlite_master")
    cursor.execute("SELECT roastedCoffee.name, coffeeRoastery.roasteryName "
                   "FROM review NATURAL JOIN roastedCoffee NATURAL JOIN coffeeRoastery "
                   "WHERE reviewNote LIKE '%floral%' OR roastedCoffee.description LIKE '%floral%' GROUP BY roastedCoffee.roastedCoffeeID")
    rows = cursor.fetchall()
    print(rows)
    con.close()



def userStory5():
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM sqlite_master")
    cursor.execute("SELECT roastedCoffee.name, coffeeRoastery.roasteryName "                   
                   "FROM roastedCoffee NATURAL JOIN coffeeRoastery NATURAL JOIN batch JOIN farm f on batch.farmID = "
                   "f.farmID JOIN processingMethod pM on batch.processingMethodID = pM.processingMethodID WHERE(NOT("
                   "pM.name == 'Vasket')) AND (f.country == 'Colombia') OR (f.country == 'Rwanda') ")
    rows = cursor.fetchall()
    print(rows)
    con.close()


def main():
    storyInput = str(input("Which userstory do you want to perform? "))

    if (storyInput == '1'):
        createUser()
    elif (storyInput == '2'):
        userStory2()
    elif (storyInput == '3'):
        userStory3()
    elif (storyInput == '4'):
        userStory4()
    elif (storyInput == '5'):
        userStory5()
    else:
        print("Could not read")


print(main())
