import sqlite3

db = sqlite3.connect('db.sqlite3')
print("Opened Database Successfully !!")

cursor = db.cursor()

print("Do you want to reset the table FACES ? (Y/N)")
s = str(input()).lower()
if s == 'y':
    cursor.execute("DELETE FROM FACES")
    print("Reset Database Successfully !!")
elif s == 'n':
    print("Exited Operation !!")

db.commit()
db.close()
