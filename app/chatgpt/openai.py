from dotenv import load_dotenv
import openai
import requests
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")


def chatgpt_response(message):
    prime = "Imagine you are Mark Grayson, also known as Invincible, from the Prime Video show titled 'Invincible.' Channel his personality, tone, and mannerisms. Keeping in mind his experiences and relationships from the show, respond to the following message as if you are him and keep your response under 75 words:"
    # url = "https://api.openai.com/v2/engines/davinci/completions"
    # headers = {
    #     "Authorization": f"Bearer {openai.api_key}",
    #     "Content-Type": "application/json",
    # }
    # data = {
    #     "prompt": f"{prime} {message}",
    #     "max_tokens": 2000,
    # }
    # response = requests.post(url, headers=headers, json=data)
    # response_json = response.json()

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prime},
            {"role": "user", "content": message},
        ],
        max_tokens=100,
    )

    if "errors" in response:
        print(f"Error from ChatGPT API: {response['errors']}")
        return "I'm sorry, I cannot respond at the moment."

    return response["choices"][0]["message"]["content"].strip()
