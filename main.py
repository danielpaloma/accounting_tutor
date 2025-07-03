import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
import app.prompts as prompts



def chat(message, history):
    # Initialize
    openai = OpenAI()
    MODEL = 'gpt-4o-mini'

    system_message = prompts.system_message

    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]

    stream = openai.chat.completions.create(model=MODEL, messages=messages, stream=True)

    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        yield response

def main():
    
    print("Hello from accounting-tutor!")

    load_dotenv(override=True)
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if openai_api_key:
        print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
    else:
        print("OpenAI API Key not set")

    #Render app using Gradio, calling function 'chat'
    gr.ChatInterface(fn=chat, type="messages").launch()
    


if __name__ == "__main__":
    main()
