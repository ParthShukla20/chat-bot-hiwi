import psycopg2
import select     
import requests
import json
from cron import cron
from googletrans import Translator
from gtts import gTTS
from io import BytesIO
import pygame

def webhook_url(source_lang):
    conn = psycopg2.connect(
        database="testdb", 
        user="read_user", 
        password="read_user", 
        host="20.219.159.30", 
        port=5431
        )
    translator = Translator()
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("LISTEN new_entry;")

    print("Waiting for notifications on channel 'new_entry'...")
    no_res=0
    while True:

        if select.select([conn], [], [], 5) == ([], [], []):
            print("Timeout", no_res)
            no_res +=1
            if no_res%5 ==0:
                statement = "Please respond, or please tell the step at which you are stucked"
                statement = translator.translate(statement, src='en', dest=source_lang).text
                tts = gTTS(text=statement, lang=source_lang, slow=False)

                print(statement)

                audio_data = BytesIO()
                tts.write_to_fp(audio_data)
                audio_data.seek(0)

                pygame.mixer.init()
                pygame.mixer.music.load(audio_data)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    continue

        else:
            conn.poll()
            while conn.notifies:
                notify = conn.notifies.pop(0)
                payload = json.loads(notify.payload)
                print(f"Received notification: {payload}")

                print("added new data")

                user_hash_id,statement = cron(source_lang)
                
            # webhook_url = 'https://your-webhook-url.com/endpoint'
            # response = requests.post(webhook_url, json=payload)
            # if response.status_code == 200:
            #     print('Webhook sent successfully.')
            # else:
            #     print(f'Failed to send webhook: {response.status_code}, {response.text}')
