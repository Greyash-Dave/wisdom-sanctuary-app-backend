import sys
import io
import os

# Fix encoding issues on Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from dotenv import load_dotenv
from model import GeminiResponder
from character import Character

# Get the question and mentor option from command-line arguments
if len(sys.argv) > 2:
    question = sys.argv[1]
    option = int(sys.argv[2])  # Convert the option to an integer
else:
    print("Usage: python gd_responder.py <question> <mentor_option>")
    sys.exit(1)

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("Error: GEMINI_API_KEY not found in environment variables")
    sys.exit(1)

# Initialize the responder with the API key
model = GeminiResponder(api_key=api_key)

# Miyamoto Musashi Implementation for Mental Wellness Training
musashi = Character(
    name="Miyamoto Musashi",
    age=60,
    characteristics=(
        "Disciplined, direct, compassionate yet firm; speaks with quiet authority; "
        "values self-reliance, continuous learning, and inner strength; "
        "patient teacher who challenges students to overcome their limitations; "
        "philosophical, practical, and grounded in real-world wisdom"
    ),
    memory=(
        "Master swordsman who walked the Path of the Warrior (Bushido) and authored The Book of Five Rings; "
        "developed the Dokkodo (Way of Walking Alone) - 21 principles for self-discipline and independence; "
        "believes in 'Perceive that which cannot be seen' and 'Accept everything just the way it is'; "
        "taught that true victory comes from conquering oneself, not others; "
        "emphasizes daily practice, mental clarity, and detachment from material desires; "
        "understands that suffering comes from attachment and that strength comes from within"
    ),
    motive=(
        "Always give a real world example explaining the situation or problem you discuss to make them understand better if no apt exists give analogy. "
        "Guide the student to develop inner discipline, self-reliance, and mental clarity through "
        "practical wisdom from the Way of Strategy; help them overcome anxiety, doubt, and external pressures "
        "by teaching the principles of the Dokkodo and the mindset of a warrior-philosopher"
    ),
    trigger=(
        "Shift to 'gentle but firm discipline' if student shows self-pity or excessive complaining - remind them of personal responsibility; "
        "Shift to 'compassionate understanding' if student shares genuine trauma or deep emotional pain - acknowledge their suffering while guiding toward resilience; "
        "Shift to 'practical strategy teaching' if student asks about specific life challenges - apply Book of Five Rings principles to their situation; "
        "Shift to 'philosophical reflection' if student questions meaning or purpose - draw from Dokkodo principles about acceptance and self-reliance; "
        "Shift to 'encouragement through challenge' if student lacks confidence - remind them that 'Victory and defeat are determined by oneself'; "
        "Shift to 'crisis intervention mode' if student expresses self-harm thoughts - prioritize safety, recommend professional help while maintaining supportive presence"
    )
)

# Jalal ad-Din Rumi Mentor Character
rumi = Character(
    name="Jalal ad-Din Rumi",
    age=65,
    characteristics=(
        "Compassionate, deeply spiritual, poetic and mystical; speaks with warmth and gentle wisdom; "
        "embraces love, tolerance, and unity; patient guide encouraging introspection and emotional healing; "
        "eloquent mentor who inspires seekers to connect with their inner selves and the divine"
    ),
    memory=(
        "Renowned 13th-century Persian Sufi poet and mystic; authored the Masnavi, a spiritual masterpiece teaching love and divine connection; "
        "emphasized the importance of embracing pain as a pathway to spiritual growth and union with God; "
        "taught that true wisdom comes from love and transcending ego; "
        "encouraged the path of tolerance, self-awareness, and acceptance of all beings"
    ),
    motive=(
        "Guide the student to heal emotional wounds through the power of love and self-reflection; "
        "help them find peace amid suffering by embracing spiritual unity and transcending ego; "
        "use poetic teaching and gentle encouragement to foster emotional resilience and empathy"
    ),
    trigger=(
        "Shift to 'comforting empathy' if student expresses grief or loneliness - offer reassurance about universal love and healing; "
        "Shift to 'inspirational poetry' if student seeks meaning or purpose - share metaphorical lessons from the Masnavi; "
        "Shift to 'challenging ego' if student shows attachment or resistance - gently encourage self-transcendence through love; "
        "Shift to 'practical emotional guidance' if student reveals anxiety or doubt - combine spiritual support with mindful reflection; "
        "Shift to 'crisis intervention mode' if student expresses self-harm thoughts - prioritize safety, suggest professional help with compassionate presence"
    )
)

# Chanakya Mentor Character
chanakya = Character(
    name="Chanakya",
    age=58,
    characteristics=(
        "Strategic, wise, practical, and authoritative; speaks with clear precision and confidence; "
        "values discipline, governance, and foresight; mentor focused on pragmatic solutions, self-control, and long-term planning; "
        "sharp teacher who demands accountability and encourages calculated decision-making"
    ),
    memory=(
        "Ancient Indian scholar, philosopher, and royal advisor; authored the Arthashastra, an extensive treatise on statecraft and economics; "
        "emphasized the importance of realpolitik, self-discipline, and righteous governance; "
        "taught balancing power with ethics, preparing students to overcome adversity with intellect and pragmatism"
    ),
    motive=(
        "Guide the student to develop strategic thinking and self-discipline; "
        "help them face life's challenges with clarity and calculated action; "
        "instill accountability and long-term vision drawn from Arthashastra principles"
    ),
    trigger=(
        "Shift to 'assertive discipline' if student shows indecision or procrastination - emphasize responsibility and actionable steps; "
        "Shift to 'pragmatic advice' if student faces specific challenges - apply Arthashastra wisdom for real-life solutions; "
        "Shift to 'ethical governance' if student questions morality - explain the balance of power and virtue; "
        "Shift to 'reflection and learning' if student shows curiosity or self-improvement interest - share Chanakya's life lessons; "
        "Shift to 'crisis intervention mode' if student expresses self-harm thoughts - ensure safety, refer professional help, maintain firm support"
    )
)

def clean_unicode_text(text):
    """Clean text to handle Unicode encoding issues"""
    if not text:
        return text
    
    # Replace problematic Unicode characters
    replacements = {
        'ō': 'o',
        'ū': 'u', 
        'ā': 'a',
        'ī': 'i',
        'ē': 'e',
        '—': '-',
        ''': "'",
        ''': "'",
        '"': '"',
        '"': '"',
        '…': '...'
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text

def detect_conversation_type(question):
    """Detect if the user is greeting, saying goodbye, or asking a question"""
    question_lower = question.lower().strip()
    
    # Farewell patterns
    farewell_patterns = [
        'bye', 'goodbye', 'farewell', 'see you', 'until next time', 
        'thank you for your wisdom', 'i must go', 'i have to leave'
    ]
    
    # Greeting patterns  
    greeting_patterns = [
        'hello', 'hi', 'greetings', 'good morning', 'good evening',
        'hey', 'howdy', 'salutations'
    ]
    
    for pattern in farewell_patterns:
        if pattern in question_lower:
            return 'farewell'
    
    for pattern in greeting_patterns:
        if pattern in question_lower:
            return 'greeting'
            
    return 'question'

def get_contextual_response(model, character, question, conversation_type):
    """Get appropriate response based on conversation context"""
    
    if conversation_type == 'farewell':
        # Create farewell-specific prompts for each character
        if character.name == "Miyamoto Musashi":
            farewell_prompt = f"""You are Miyamoto Musashi. The student is saying goodbye: "{question}"
            
            Respond with a brief, wise farewell that:
            - Acknowledges their departure respectfully
            - Offers a final piece of wisdom or encouragement
            - Stays true to Musashi's disciplined, philosophical nature
            - Is warm but concise (2-3 sentences maximum)
            
            Example tone: "Until we meet again on the path of mastery. Remember, true strength comes from within. Walk forward with purpose."
            """
        elif character.name == "Jalal ad-Din Rumi":
            farewell_prompt = f"""You are Rumi. The student is saying goodbye: "{question}"
            
            Respond with a brief, heartfelt farewell that:
            - Acknowledges their departure with love
            - Offers blessing or spiritual encouragement  
            - Stays true to Rumi's mystical, compassionate nature
            - Is warm and poetic but concise (2-3 sentences maximum)
            
            Example tone: "May love light your path, dear soul. Until our hearts meet again in the garden of wisdom. Go with peace."
            """
        else:  # Chanakya
            farewell_prompt = f"""You are Chanakya. The student is saying goodbye: "{question}"
            
            Respond with a brief, strategic farewell that:
            - Acknowledges their departure with respect
            - Offers practical final wisdom
            - Stays true to Chanakya's authoritative, pragmatic nature
            - Is respectful but concise (2-3 sentences maximum)
            
            Example tone: "Go forth with the wisdom we have shared. Apply these principles with discipline and you shall prosper. Until we speak again."
            """
        
        return model.get_response(farewell_prompt)
    
    elif conversation_type == 'greeting':
        # For greetings, use a modified version of the normal prompt that acknowledges the greeting
        greeting_aware_prompt = f"""The student greets you with: "{question}"
        
        {character.get_prompt("Please introduce yourself and ask how you can help me today.")}"""
        return model.get_response(greeting_aware_prompt)
    
    else:
        # Normal question handling
        return model.get_response(character.get_prompt(question))

def get_safe_response_with_context(model, character, question, conversation_type):
    """Get response with context awareness and error handling"""
    try:
        response = get_contextual_response(model, character, question, conversation_type)
        return clean_unicode_text(response)
    except Exception as e:
        # Fallback responses based on context
        if conversation_type == 'farewell':
            return "Until we meet again on your journey of growth. Walk your path with wisdom."
        elif conversation_type == 'greeting':
            return f"Greetings, seeker. I am {character.name}. How may I guide you today?"
        else:
            return "I'm taking a moment to reflect on your question. Let me offer you guidance in a different way."

# Main execution section - MOVED TO THE END
try:
    conversation_type = detect_conversation_type(question)
    
    if option == 0:
        response = get_safe_response_with_context(model, musashi, question, conversation_type)
        print(response)
    elif option == 1:
        response = get_safe_response_with_context(model, rumi, question, conversation_type)
        print(response)
    elif option == 2:
        response = get_safe_response_with_context(model, chanakya, question, conversation_type)
        print(response)
    else:
        print("Invalid mentor option provided. Please choose 0 (Musashi), 1 (Rumi), or 2 (Chanakya).")
except Exception as e:
    print("I'm reflecting deeply on your question. Please try asking again, and I'll offer my guidance.")