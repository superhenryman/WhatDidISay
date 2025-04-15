import google.generativeai as genai
import os
from typing import Literal
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API key for Google Generative AI is not set.")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

class AIError(Exception):
    pass

def generate_debug_response(error:str) -> str:
    try:
        response = model.generate_content(contents=f"Please explain what happened, how can we debug it? {error}")
        return response.text.strip().replace('*', '')
    
    except Exception as e:
        raise AIError() from e
    
def generate_response(prompt: str, mode: Literal["Serious", "Normal", "Sarcastic"]) -> str:
    try:
        response = ""
        if mode == "Serious":
            response = model.generate_content(f"With this prompt, I need you to be as serious as you can: {prompt}")
        elif mode == "Normal":
            response = model.generate_content(f"With this prompt, I need you to be as normal as you can: {prompt}")
        elif mode == "Sarcastic":
            response = model.generate_content(f"With this prompt, I need you to be as sarcastic as you can: {prompt}")
        else:
            raise RuntimeError("Invalid mode. Please choose 'Serious', 'Normal', or 'Sarcastic'.")
        print(f"Response: {response.text.strip().replace('*', '')}") # debugging
        return response.text.strip().replace("*", "")
    except Exception as e:
        print(f"Error generating response: {e}")
        print(generate_debug_response(e))
        return "Sorry, I couldn't generate a response."