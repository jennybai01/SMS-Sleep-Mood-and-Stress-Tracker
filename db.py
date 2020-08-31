import sqlite3
from sqlite3 import Error
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import seaborn as sns

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

connection = create_connection(r"C:\Users\jenny\Desktop\clientdb.sqlite")

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")

# creating table
create_db = """
CREATE TABLE IF NOT EXISTS clients_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone_number INTEGER,
    entry_date DATE,
    mood INTEGER,
    stress INTEGER,
    sleep INTEGER
    );
"""
execute_query(connection, create_db)

# get entry data
while True: # get number
    try:
        number = input("Enter your phone number: ")
        number = int(number)
        break
    except ValueError:
        print("Please enter an integer.")


while True: # get mood
    try:
        mood = input("Rate your mood today from 1 to 10 (inclusive): ")
        mood = int(mood)
        if (mood > 0 and mood < 11):
            break
    except ValueError:
        print("Please enter an integer.")

while True: # get stress
    try:
        stress = input("Rate your stress today from 1 to 10 (inclusive): ")
        stress = int(stress)
        if (stress > 0 and stress < 11):
            break
    except ValueError:
        print("Please enter an integer.")

while True: # get sleep
    try:
        sleep = input("How many hours of sleep did you get last night? ")
        sleep = int(sleep)
        if (sleep > -1 and sleep < 25):
            break
    except ValueError:
        print("Please enter an integer.")

# inserting records
entry = (number, datetime.datetime.now(), mood, stress, sleep)
c = connection.cursor()
c.execute("INSERT INTO clients_info(phone_number, entry_date, mood, stress, sleep) VALUES (?, ?, ?, ?, ?)", entry)
connection.commit()

#execute_query(connection, add_entry)

# selecting records
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

select_number = input("Enter the client's number who you wish to observe: ")
# select_info will get the top 7 most recent entries (sorted in ascending order by date) for a specified phone number
select_info = """
WITH top7 AS (
    SELECT * FROM clients_info
    WHERE phone_number = {}
    ORDER BY entry_date DESC
    LIMIT 7
)
SELECT * FROM
top7
ORDER BY entry_date ASC""".format(select_number)

#select_info = "SELECT * FROM clients_info"

info = execute_read_query(connection, select_info)

df = pd.read_sql_query(select_info, connection)
# print(df)
df["entry_date"] = df["entry_date"].apply(lambda x: str(x).split()[1][:8]) # fix this to represent dates, not times
sns.set_style("white")
sns.set_palette(sns.color_palette("BuPu", 2))
sns.lineplot(x = "entry_date", y = "mood", data = df, label = "mood")
sns.lineplot(x = "entry_date", y = "stress", data = df, label = "stress")
sns.barplot(x = "entry_date", y = "sleep", data = df, label = "sleep", color="lavender").set_title("This Week's Mood, Stress & Sleep")
plt.ylabel("Your mood, stress, & sleep")
plt.xlabel("Date")
plt.show()

# deleting table records
# delete_records = "DELETE FROM clients_info;"
# execute_query(connection, delete_records)
# print(execute_read_query(connection, select_info))