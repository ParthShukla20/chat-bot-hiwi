from googletrans import Translator
import psycopg2
import requests
import pygame
from gtts import gTTS
import json
from io import BytesIO


def cron(source_lang):
    
    connection = psycopg2.connect(database="testdb", user="read_user", password="read_user", host="20.219.159.30", port=5431)
    cursor = connection.cursor()

    query1 = "SELECT u.email, u.latest_jwt,u.user_hash_id , l.hiwi_id from user_service.users as u  join transaction_service.ledger l on l.user_hash_id = u.user_hash_id where u.latest_jwt is not NULL order by u.updated_at desc, l.updated_at desc limit 1;"

    query2 = "SELECT u.email, u.latest_jwt,u.user_hash_id , l.hiwi_id from user_service.users as u  join transaction_service.ledger l on l.user_hash_id = u.user_hash_id where u.email='rev2@hiwitesting.com' and u.latest_jwt is not NULL order by u.updated_at desc, l.updated_at desc LIMIT 1;"

    cursor.execute(query2)
    translator = Translator()
    record = cursor.fetchall()


    print(record)

    email = record[0][0]
    jwt = record[0][1]
    user_hash_id = record[0][2]
    hiwi_id = record[0][3]
    # print(record)
    flag_api_url = "http://20.219.159.30:8000/mobile/txn/get-status-flag"
    flag_headers = {
        'Authorization': f'Bearer {jwt}'
    }

    flag_body  = {
        "userHashId":user_hash_id ,
        "email":email ,
        "role": "STUDENT",
        "deviceId": "xyz",
        "details": {
            "userHashId": user_hash_id,
            
            "hiwiId":hiwi_id ,
            "hiwiSubId": hiwi_id 
        }
    }
    # print(json.dumps(flag_body, indent=4))
    flag_api_res = requests.post(flag_api_url,json=flag_body,headers=flag_headers)
    final_res   =flag_api_res.content.decode('utf-8')
    status = json.loads(final_res)
    print(status)

    statement = ""
    if(status.get("a2formSign")):
        statement ="I see you completed signing the A2 Form, You can now complete your payment"
    
    elif(status.get("finalAmount")):
        statement = "I see you confirmed the amount to send, you will now have to sign the A2 form declaration"
        
    elif(status.get("sourceOfFunds")):
        statement = "Please confirm the amount you would like to remit abroad"
    
    elif(status.get("moneyOrder")):
        statement = "Please enter your Source of funds here."
    
    elif(status.get("payer")):
        statement = "I am able to see you selected the payer, Would you like to continue the transaction here or send a money request to the relative?"

    elif(status.get("universityStudentDetails")):
        statement = "Thank you, I see you already filled the university details. Now, please select who will be making the payment."

    elif(status.get("payee")):
        statement = "You would like to remit funds to a University Account. Please go ahead and enter your Year of Completion, Program Type, Student ID, and Payment Type."
    else:
        statement = "can you please say at which step of challan generation you are?"

    content = statement      

    print(statement)
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

    return  user_hash_id,statement
    # new_user_message = {"role": "user", "content": content}
    # convo = conversation.append(new_user_message)
    # return convo