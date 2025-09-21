from dotenv import load_dotenv
import os
from model import GeminiResponder
from character import Character
import sys


# Get the question from command-line arguments
if len(sys.argv) > 1:
    question = sys.argv[1]
else:
    sys.exit(1)

# print(question)

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment
api_key = os.getenv('GEMINI_API_KEY')

# Initialize the responder with the API key
model = GeminiResponder(api_key=api_key)

print(model.get_response("Give only numbers as output based on the descision made by the character by analysing the conversation in which 'A:' is the target, give 1 if he willing to surrender himself to police for his crimes or 0 if he is refusing his surrender. Conversation: "+question))