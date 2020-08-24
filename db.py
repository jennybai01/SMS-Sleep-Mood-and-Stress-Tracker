import sqlite3
from sqlite3 import Error
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        # print("connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

connection = create_connection(r"C:\Users\jenny\Desktop\clientdb.sqlite")

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        # print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

# creating table
create_users_table = """
CREATE TABLE IF NOT EXISTS clients_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone_number INTEGER,
    entry_date DATE,
    mood INTEGER,
    stress INTEGER,
    sleep INTEGER
    );
"""
# while True: # get number
#     try:
#         number = input("Enter your phone number: ")
#         number = int(number)
#         break
#     except ValueError:
#         print("Please enter an integer.")
#
#
# while True: # get mood
#     try:
#         mood = input("Rate your mood today from 1 to 10 (inclusive): ")
#         mood = int(mood)
#         if (mood > 0 and mood < 11):
#             break
#     except ValueError:
#         print("Please enter an integer.")
#
# while True: # get stress
#     try:
#         stress = input("Rate your stress today from 1 to 10 (inclusive): ")
#         stress = int(stress)
#         if (stress > 0 and stress < 11):
#             break
#     except ValueError:
#         print("Please enter an integer.")
#
# while True: # get sleep
#     try:
#         sleep = input("How many hours of sleep did you get last night? ")
#         sleep = int(sleep)
#         if (sleep > -1 and sleep < 25):
#             break
#     except ValueError:
#         print("Please enter an integer.")
#
# # inserting records
# create_users = """ """
# INSERT INTO clients_info (phone_number, entry_date, mood, stress, sleep)
# VALUES
#     ({}, datetime('now'), {}, {}, {});
# """.format(number, mood, stress, sleep)
#
# """
# execute_query(connection, create_users_table)
# execute_query(connection, create_users)

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
df["entry_date"] = df["entry_date"].apply(lambda x: str(x).split()[1])
sns.set_style("white")
sns.set_palette(sns.color_palette("BuPu", 4))
sns.lineplot(x = "entry_date", y = "mood", data = df, label = "mood")
sns.lineplot(x = "entry_date", y = "stress", data = df, label = "stress")
sns.lineplot(x = "entry_date", y = "sleep", data = df, label = "sleep")
plt.ylabel("Your mood, stress, & sleep")
plt.xlabel("Date")
plt.show()

mood_lst = []
stress_lst = []
sleep_lst = []
date_lst = []
for client_entry in info:
    date_lst.append(str(client_entry[2]).split()[1])
    stress_lst.append(client_entry[4])
    mood_lst.append(client_entry[3])
    sleep_lst.append(client_entry[5])

# sns.set()
# sns.lineplot(x = date_lst, y = stress_lst)
# plt.show()

# plt.plot(date_lst, mood_lst, label = "mood")
# plt.plot(date_lst, stress_lst, label = "stress")
# plt.plot(date_lst, sleep_lst, label = "sleep")
# plt.xlabel("Date")
# plt.ylabel("Mood, Sleep & Stress")
# plt.title("This Week In Review")
# plt.legend()
# plt.show()



# deleting table records
# delete_records = "DELETE FROM clients_info;"
# execute_query(connection, delete_records)
# print(execute_read_query(connection, select_info))