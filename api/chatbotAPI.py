import openai
from flask import Blueprint, request, jsonify, render_template

chatbotAPI = Blueprint('chatbotAPI', __name__)

# OpenAI API Key
openai.api_key = "your-openai-api-key-here"

@chatbotAPI.route('/get_response', methods=['POST'])
def get_bot_response():
    # Get the user message from the frontend
    user_message = request.json.get("message")
    
    # Log the received message for debugging
    print(f"Received message: {user_message}")

    if not user_message:
        return jsonify({"response": "Please enter a valid message."})

    try:
        # Call OpenAI GPT-4 API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a mental health support chatbot."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150
        )

        bot_message = response.choices[0].message["content"]

        # Log the bot response for debugging
        print(f"Bot response: {bot_message}")

        return jsonify({"response": bot_message})

    except Exception as e:
        # Log any errors that occur during API call
        print(f"Error calling OpenAI API: {e}")
        return jsonify({"response": "There was an error generating a response."})
