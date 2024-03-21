import requests
import pyttsx3

def ulca_config():

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 138)         
    engine.say("Hello I am Emmma , I am here to help you. Please select your conversational language")
    engine.runAndWait()

    config_url = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"
    model = {'telugu': 'te', 'tamil': 'ta', 'hindi': 'hi', 'gujarati': 'gu', 'marathi': 'mr', 'english': 'en'}

    source_lang = model[input("Enter the language you want to talk : ").lower()]

    print(source_lang)

    ulca_header_config = {
        "userID": "e143f6eaa3b344d681cf183673608a4d",
        "ulcaApiKey": "178685922a-a901-4916-9c13-2bed6eeeedb7"
    }
    
    ulca_body_config = {
        "pipelineTasks": [
            {
                "taskType": "asr",
                "config": {
                    "language": {
                        "sourceLanguage": source_lang
                    }
                }
            }
        ],
        "pipelineRequestConfig": {
            "pipelineId": "64392f96daac500b55c543cd"
        }
    }

    response = requests.post(config_url, headers=ulca_header_config, json=ulca_body_config)
    task_type_to_find = "asr"
    service_id =None
    data=None
    if response.status_code == 200:
        # Successful API call
        data = response.json()
        print("API call successful. Response:")
        

        for config in data.get("pipelineResponseConfig", []):
            if config.get("taskType") == task_type_to_find:
                service_id = config.get("config", [{}])[0].get("serviceId")
                break

        print("Service ID for task type 'asr':", service_id)
    else:
        # API call failed
        print(f"API call failed with status code: {response.status_code}")
        print(response.text)

    return config_url, ulca_header_config, ulca_body_config, source_lang, service_id,data


def ulca_compute(encoded_audio,source_lang,service_id,data,conversation,azure_openai_url,headers,body):
    ulca_body_compute= { "pipelineTasks": [
            {
                "taskType": "asr",
                "config": {
                    "language": {
                        "sourceLanguage": source_lang
                    },
                    "serviceId": service_id,
                    "audioFormat": "wav",
                    "samplingRate": 16000
                }
            }
        ],
        "inputData": {
            "audio": [
                {
                    "audioContent": encoded_audio }]
                    }
        }
    ulca_header_compute = {
                "Authorization" : data['pipelineInferenceAPIEndPoint']['inferenceApiKey']['value']
            }
    ulca_compute_url = data['pipelineInferenceAPIEndPoint']['callbackUrl']
    compute_response = requests.post(ulca_compute_url, headers=ulca_header_compute, json=ulca_body_compute)
    response_data = compute_response.json()
        # print(response_data)
    source_value =response_data["pipelineResponse"][0]["output"][0]["source"]
    print(source_value)
    new_user_message = {"role": "user", "content": source_value}
    conversation.append(new_user_message)
    body ={
        "dataSources": [
            {
                "type": "AzureCognitiveSearch",
                "parameters": {
                    "endpoint": "https://azure-search-service-hiwi-chatbot.search.windows.net",
                    "indexName": "chatindex02022024-01-index",
                    "semanticConfiguration": "default",
                    "queryType": "simple",
                    "fieldsMapping": {},
                    "inScope": 'true',
                    "roleInformation": "You are an AI assistant that helps people find information.",
                    "strictness": 3,
                    "topNDocuments": 5,
                    "key": "ynt3y4kryQb5XQjSOesRzzcqPGKk6mn803SbhSYVXfAzSeByVqSc"
                }
            }
        ],
        "messages": conversation,
        "temperature": 0.3,
        "top_p": 0.95,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "max_tokens": 200
    }
    
   
        
    response = requests.post(azure_openai_url, headers=headers, json=body)

    new_generated_text = response.json().get('choices', [])[0].get('messages', [])[1].get('content', '')

    return new_generated_text ,conversation, body
