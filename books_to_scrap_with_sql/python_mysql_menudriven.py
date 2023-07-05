import datetime

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="actowiz",
  database="new"
)
mycursor = mydb.cursor()
def insert(mycurser):
    while True:
        try:
            a = int(input("enter roll no"))
            break
        except ValueError:
            print("please  enter corect input")
    b=input("enter your first name")
    c=input("enter your last name")
    while True:
        try:
            d= input("Enter your dob (YYYY-MM-DD): ")
            d= datetime.datetime.strptime(d, "%Y-%m-%d").date()
            break
        except ValueError:
            print("please  enter corect input")

    while True:
        try:
            e=input("enter your standard")
            break
        except ValueError:
            print("please  enter corect input")

    sql = "INSERT INTO student2 (roll_no, first_name, last_name,dateofbirth, standard) VALUES (%s, %s,%s,%s,%s)"
    val = (a,b,c, d, e)
    mycursor.execute(sql, val)
    mydb.commit()


def retrive(mycursor):
    mycursor.execute("SELECT * FROM student2")
    for row in mycursor.fetchall():
        date_str = row[3].strftime("%Y-%m-%d")
        print(*row[:3], date_str, row[4])


def update(mycursor):
    k=int(input("enter roll_no to update"))
    c=int(input("press 1 to update roll_no \n"
          "press 2 to update first_name  \n"
          "press 3 to update last_name \n"
          "press 4 to update dob \n"
          "press 5 to update standard: "))
    new_value = input("Enter the new value: ")
    column_name = ""
    if c == 1:
        column_name = "roll_no"
    elif c == 2:
        column_name = "first_name"
    elif c == 3:
         column_name = "last_name"
    elif c == 4:
        column_name = "dateofbirth"
    elif c == 5:
        column_name = "standard"
    else:
        print("Invalid choice")
        return

    sql = f"UPDATE student2 SET {column_name} = %s WHERE roll_no = %s"
    val = (new_value, k)

    mycursor.execute(sql, val)
    mydb.commit()

    print(mycursor.rowcount, "record updated")

    mycursor.execute("SELECT * FROM student2 WHERE roll_no = %s", (k,))
    r = mycursor.fetchone()
    print(r)

while True:
    p=input(("press i for insert and r for retrive u for update any other to quit : "))
    if p.lower()=="i":
        insert(mycursor)
    elif p.lower()=="r":
        retrive(mycursor)
    elif p.lower()=="u":
        update(mycursor)
    else:
        break




