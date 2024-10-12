from flask import Blueprint,request,jsonify, render_template, redirect, url_for
from firebase_admin import firestore

db = firestore.client()
dbCollection = db.collection("employees")
chatbotAPI = Blueprint('chatbotAPI', __name__)

# chatbotAPI.py
import openai

# Set your OpenAI API key here
openai.api_key = "your-api-key-here"

# System message to set the context for the chatbot
system_message = """
You are a mental health support assistant. 
Your goal is to only answer questions related to mental health, emotional well-being, 
self-care, and coping strategies. Always be supportive and provide advice on seeking professional help when needed.
"""

def get_openai_response(user_input):
    """
    Sends the user input to OpenAI's GPT-4 model and returns the response.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use GPT-4
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input}
        ],
        max_tokens=150  # Adjust based on response length
    )
    return response.choices[0].message["content"].strip()


@chatbotAPI.route('/', methods=['GET'])
def show_form():
    return render_template('chatbot.html')