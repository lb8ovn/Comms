import datetime
import pytz
import schedule
import time

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google_auth_httplib2 import AuthorizedHttp
from googleapiclient.discovery import build

# Replace with your girlfriend's phone number
your_girlfriends_number = "+11234567890"

# List of good morning and good night texts
good_morning_texts = [
    "Rise and shine, beautiful! Hope you have an amazing day ahead.",
    "Good morning, sweetheart! Just wanted to remind you that you're the first thing on my mind today.",
    "Morning, love! I hope your day is as wonderful as you are.",
    "Hey gorgeous, just wanted to say good morning and let you know how grateful I am to have you in my life.",
    "Good morning, babe! Remember, today is a new day with endless possibilities. Go seize it!",
    "Morning! Let's make today an awesome day, just like us!",
    "Waking up is so much better when I get to say good morning to you, my love.",
    "Hey sunshine, sending you all the positive vibes and love to kickstart your day.",
    "Good morning, my love! I'm so lucky to have you. I can't wait to see you later today.",
    "Rise and sparkle, my queen! Wishing you a day full of joy, laughter, and love.",

]

good_night_texts = [
    "Sleep tight, my love! I'll be dreaming of you tonight.",
    "Good night, beautiful. Can't wait to see you in my dreams.",
    "Sweet dreams, sweetheart! Rest well and know that you're loved.",
    "Good night, babe. Just wanted to say I love you and I'm grateful for every moment we share.",
    "Wishing you a peaceful night's sleep, my love. I'll be here waiting for you in the morning.",
    "Nighty night, my queen! Sleep well and let the stars guide your dreams.",
    "Sweet dreams, gorgeous! Looking forward to our next adventure together.",
    "Good night, love. I hope you drift off to sleep knowing how much you mean to me.",
    "As you fall asleep, remember that you are the best thing that ever happened to me. Good night, sweetheart.",
    "Close your eyes and rest, my love. Tomorrow is a new day, and I can't wait to spend it with you.",

]

# Load Google Fi API credentials
creds = None
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json")
if not creds or not creds.valid:
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", ["https://www.googleapis.com/auth/fi"])
    creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
        token.write(creds.to_json())

# Create an authorized HTTP object and build the API client
authed_http = AuthorizedHttp(creds)
fi = build("fi", "v1", http=authed_http)


# Function to send a random text from a list
def send_text(texts, phone_number):
    text = random.choice(texts)
    body = {
        "text": text,
        "phoneNumber": phone_number,
    }
    fi.sendText().execute(body)


# Schedule good morning and good night texts
def schedule_texts():
    schedule.every().day.at("06:00").do(send_text, good_morning_texts, your_girlfriends_number)
    schedule.every().day.at("22:00").do(send_text, good_night_texts, your_girlfriends_number)

    while True:
        schedule.run_pending()
        time.sleep(60)


# Convert current local time to PST
def to_pst(dt):
    local = pytz.timezone("America/Los_Angeles")
    return dt.astimezone(local)


# Main function
if __name__ == "__main__":
    now = datetime.datetime.now()
    pst_now = to_pst(now)

    if 6 <= pst_now.hour < 22:
        send_text(good_morning_texts, your_girlfriends_number)
    else:
        send_text(good_night_texts, your_girlfriends_number)

    schedule_texts()
