import sqlite3
from sqlite3 import Error
import datetime
import time
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request, session
from creds import *

app = Flask(__name__)

client = Client(ACC_SID, AUTH_TOKEN)

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

# Prompt user for input
message = client.messages.create(body="Hey there! Checking in for today",
                from_=twilio_num,
                to=from_number)
message = client.messages.create(body="Rate your mood today from 1 to 10 (inclusive): ",
                from_=twilio_num,
                to=from_number)

# time delay to get next day's message
while True:
        # 30 second delay
        time.sleep(60)
        message = client.messages.create(body="Hey there! Checking in for today",
                from_=twilio_num,
                to=from_number)
        message = client.messages.create(body="Rate your mood today from 1 to 10 (inclusive): ",
                from_=twilio_num,
                to=from_number)


# while True: # get number
#     try:
#         number = input("Enter your phone number: ")
#         number = int(number)
#         print("Your number is: " + number)
#         break
#     except ValueError:
#         print("Please enter an integer.")



#############################################################
@app.route("/", methods=['GET', 'POST'])
def respond():
    # Get incoming phone number
    from_number = request.values.get('From')

    # Check cookies for the incoming phone number
    counter = session.get(from_number, 0)
    counter = (counter + 1) % 3
    session[from_number] = counter

    if (counter == 1):
        # get mood 
        try:
            mood = request.values.get('Body')
            mood = int(mood)
            if (mood < 0 or mood > 10):
                # invalid range 
                message = client.messages.create(body="Invalid mood range. Please enter a number from 1 to 10",
                from_=twilio_num,
                to=from_number)
                session[from_number] = counter - 1
        except ValueError:
            # invalid type
            message = client.messages.create(body="Invalid mood type. Please enter a number from 1 to 10",
                from_=twilio_num,
                to=from_number)
            session[from_number] = counter - 1

        # store mood
        session[from_number][mood] = mood

        # prompt next question
        message = client.messages.create(body="Rate your stress today from 1 to 10 (inclusive): ",
            from_=twilio_num,
            to=from_number)


    if (counter == 2):
        # get stress

        try:
            stress = request.values.get('Body')
            stress = int(mood)
            if (stress < 0 or stress > 10):
                # invalid range 
                message = client.messages.create(body="Invalid stress range. Please enter a number from 1 to 10",
                from_=twilio_num,
                to=from_number)
                session[from_number] = counter - 1
        except ValueError:
            # invalid type
            message = client.messages.create(body="Invalid stress type. Please enter a number from 1 to 10",
                from_=twilio_num,
                to=from_number)
            session[from_number] = counter - 1
        
        # store stress
        session[from_number][stress] = mood
        
        # prompt next question
        message = client.messages.create(body="How many hours of sleep did you get last night? ",
            from_=twilio_num,
            to=from_number)

    if (counter == 0):
        # get sleep
        try:
            sleep = request.values.get('Body')
            sleep = int(mood)
            if (sleep < 0 or sleep > 24):
                # invalid range 
                message = client.messages.create(body="Invalid sleep range. Please enter a number from 1 to 24",
                from_=twilio_num,
                to=from_number)
                session[from_number] = counter - 1
        except ValueError:
            # invalid type
            message = client.messages.create(body="Invalid sleep type. Please enter a number from 1 to 24",
                from_=twilio_num,
                to=from_number)
            session[from_number] = counter - 1

        # last entry, make db entry
        insertRecord(from_number, session[from_number][mood], session[from_number][stress], sleep)
    
   


def insertRecord(number, mood, stress, sleep):
    # inserting records
    create_users = """
    INSERT INTO clients_info (phone_number, entry_date, mood, stress, sleep)
    VALUES
        ({}, datetime('now'), {}, {}, {});
    """.format(number, mood, stress, sleep)

    execute_query(connection, create_users_table)
    execute_query(connection, create_users)

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
WITH top7 as (
    SELECT * FROM clients_info 
    WHERE phone_number = {} 
    ORDER BY entry_date DESC
    LIMIT 7
    )
AS top7
SELECT * FROM
top7
ORDER BY entry_date
.format(select_number)"""

#select_info = "SELECT * FROM clients_info"

info = execute_read_query(connection, select_info)
for client in info:
    print(client)

# deleting table records
# delete_records = "DELETE FROM clients_info;"
# execute_query(connection, delete_records)
# print(execute_read_query(connection, select_info))

if __name__ == "__main__":
    app.run(debug=True)