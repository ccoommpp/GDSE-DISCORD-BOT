import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GOOGLE_TOKEN=os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GOOGLE_TOKEN)
model = genai.GenerativeModel("gemini-2.0-flash")

def get_response(user_input: str):
    
    if not user_input.strip():
        return "Please enter a valid message."

    try:
        response = model.generate_content([user_input])

        # Ensure response is not empty
        if hasattr(response, "text") and response.text and response.text.strip():
            return response.text.strip()
        else:
            return "I'm not sure what to say. Try asking something else!"

    except Exception as e:
        print(f"Error fetching response from Gemini API: {e}")
        return "Error: Unable to process your request."
