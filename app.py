import time
from flask import Flask, request, redirect
from flask_ngrok import run_with_ngrok
from twilio_client import TwilioClient
from twilio.twiml.messaging_response import MessagingResponse
from collections import defaultdict

from db import tracker_entry

app = Flask(__name__)
run_with_ngrok(app)
client = TwilioClient()


# datatype for storing message and response logs
def list_2d():
    """
    [0] - User's messages
    [1] - Bot's messages
    [2] - Message flag
    [3] - Last messaged time
    :return: new datatype
    """
    return [[], [], False, time.time()]
hist = defaultdict(list_2d)

_user = 0
_bot = 1
_flag = 2
_time = 3
MESSAGE_DELAY = 60 * 60 * 24 # 24 hours


@app.route('/')
def home():
    """
    Home page
    :return: Server status
    """
    return 'Twilio Server Status: Working!'


@app.route('/sms', methods=['GET', 'POST'])
def receive_sms():
    """
    Receives sms
    """
    # user phone number
    user_num = request.values.get('From', None)
    # message
    body = request.values.get('Body', None)

    # instantiate MessagingResponse object
    resp = MessagingResponse()

    # log user's texts
    hist[user_num][_user].append(str(body))
    hist[user_num][_time] = time.time()

    if body.lower() == 'start':
        if hist[user_num][_flag]:
            resp.message(f'Your status will be collected in {((60 * 60 * 24) - (time.time() - hist[user_num][_time])) / 60**2 :.0f}'
                         f' hours.')
        else:
            # clear message log
            hist[user_num][_user] = [str(body)]
            message = 'What is your email?'
            hist[user_num][_bot] = [message]
            resp.message(message)
            hist[user_num][_flag] = True

    elif hist[user_num][_bot][-1] == 'What is your email?' or hist[user_num][_bot][-1].startswith('Hi! I\'m here to take your'):
        message = 'Enter your current level of stress (1-10):'
        hist[user_num][_bot].append(message)
        resp.message(message)

    elif hist[user_num][_bot][-1] == 'Enter your current level of stress (1-10):':
        message = 'Enter your current mood (1-10):'
        hist[user_num][_bot].append(message)
        resp.message(message)

    elif hist[user_num][_bot][-1] == 'Enter your current mood (1-10):':
        message = 'Enter your level of sleep (0-12):'
        hist[user_num][_bot].append(message)
        resp.message(message)

    elif hist[user_num][_bot][-1] == 'Enter your level of sleep (0-12):':
        resp.message('Thank you! Your next status update will be collected in 24 hours.')
        print(hist[user_num][_user][-4:])
        if hist[user_num][_user][-5].lower() == 'start':
            email = hist[user_num][_user][-4]
        else:
            email = 'optional'
        tracker_entry(user_num,
                      email=email,
                      stress=int(hist[user_num][_user][-3]),
                      mood=int(hist[user_num][_user][-2]),
                      sleep=int(hist[user_num][_user][-1]))

    return str(resp)


def ask_for_status(user_num):
    message = 'Hi! I\'m here to take your weekly status checks. First, what is your current level of stress (1-10):'
    client.send_message(message, to=user_num)
    hist[user_num][_bot].append(message)


if __name__ == '__main__':
    app.run()
    while True:
        for key in hist.keys():
            if time.time() - hist[key][_time] >= MESSAGE_DELAY:
                elapsed = time.time() - hist[key][_time]
                print(f'Time elapsed: {elapsed} - {key}')
                ask_for_status(key)
                hist[key][_time] = time.time()
