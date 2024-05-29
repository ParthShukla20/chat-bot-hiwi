import os
import requests

def azure_api_details(conversation):
    azure_openai_key = 'f3b28a10a6d941bf94d1667cffc2e408'
    os.environ["OPENAI_API_KEY"] = azure_openai_key
    
    url = "https://hiwimobileapp-createopenai.openai.azure.com/openai/deployments/Hiwi-Mobile-App-Chatbot/extensions/chat/completions?api-version=2023-09-15-preview"  
    
    headers = {
        'Content-Type': 'application/json',
        'api-key': azure_openai_key
    }
    
  
    
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
        "max_tokens":150
    }
    
    # Sending the request
    # response = requests.post(url, headers=headers, json=body)
    
    return azure_openai_key,url,headers,body

