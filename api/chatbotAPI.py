import openai
from flask import Blueprint, request, jsonify, render_template

# Create the chatbotAPI Blueprint
chatbotAPI = Blueprint('chatbotAPI', __name__)

# Set your OpenAI API key
openai.api_key = "sk-9SnSdZNt5k646FZLmaLRd75FlQmgMn4DOM5K1gwRlXT3BlbkFJz7LlzH4eYULgxBoxQBJvITNmjsyjjNEieQ972tlQgA"

# Define the system message to restrict the bot's responses to mental health topics
system_message = """
You are a mental health support assistant. Your goal is to answer questions related to mental health,
emotional well-being, coping strategies, stress management, and self-care. Politely refuse to answer any questions that are not related to mental health.
"""

# Route to serve the chatbot HTML form
@chatbotAPI.route('/', methods=['GET'])
def show_chatbot():
    return render_template('chatbot.html')

# Route to handle user input and return the bot response
@chatbotAPI.route('/get_response', methods=['POST'])
def get_bot_response():
    # Get the user's message from the request
    user_message = request.json.get("message")
    
    print(f"Received message: {user_message}")  # Log the received message

    if not user_message:
        return jsonify({"response": "Please ask me something about mental health."})

    try:
        # Use the new OpenAI API (openai>=1.0.0) interface
        response = openai.completions.create(
            model="gpt-4",
            prompt=f"{system_message}\nUser: {user_message}\nAssistant:",
            max_tokens=150  # Adjust token limit as necessary
        )
        
        # Get the bot's response from the OpenAI API response
        bot_message = response.choices[0].text.strip()  # Extract the bot's response from the 'text' field
        print(f"Bot response: {bot_message}")  # Log the bot response

        return jsonify({"response": bot_message})

    except Exception as e:
        # Log the error and return a default error message
        print(f"Error calling OpenAI API: {e}")
        return jsonify({"response": "Sorry, I couldn't process your request right now. Please try again later."})
