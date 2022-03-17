import sqlite3

def createUser():
    fullname = str(input("What is your full name? "))
    email = str(input("Write your email: "))
    password = str(input("Write your password: "))
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM sqlite_master")
    cursor.execute("INSERT INTO coffeeUser VALUES (?,?,?,?)", (None,email, password, fullname))
    con.commit()
    con.close()

def main():

    newUser = str(input("Do you want to create a new user?"))
    if newUser == "y":
        createUser()
    else:
        print("Did not understand")

print(main())


