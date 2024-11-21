import requests

def get_ai_response(messages, model, client):
    
    params = {
        "model": model,
        "messages": messages,
    }
        
    response = client.chat.completions.create(**params)
    return response.choices[0].message.content.strip()

def send_answer(api_key, report_url, task, answer):
    
    pyload = {
        "task": task,
        "apikey": api_key,
        "answer": answer
    }

    try:
        response = requests.post(report_url, json=pyload)
        result = response.json()

        if result.get('code')==0:
            print("Success:", result.get('message'))
            return True
        else:
            print("Error:", result.get('message'))
            return False
        
    except requests.RequestException as e:
        print(f"Error sending answer: {e}")
        return False