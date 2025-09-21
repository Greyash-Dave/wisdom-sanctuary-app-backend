import google.generativeai as genai

class GeminiResponder:
    def __init__(self, api_key):
        """Initialize the Gemini responder with API key"""
        if not api_key:
            raise ValueError("API key is required")
        
        genai.configure(api_key=api_key)
        
        # Configure the model with safety settings to be less restrictive
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
        
        # Safety settings to reduce blocking
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
        ]
        
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )
    
    def get_response(self, prompt):
        """Get response from Gemini with proper error handling"""
        try:
            response = self.model.generate_content(prompt)
            
            # Check if response was blocked
            if response.candidates and response.candidates[0].finish_reason != 1:
                return response.text
            else:
                # Handle blocked responses
                finish_reason = response.candidates[0].finish_reason if response.candidates else "unknown"
                
                if finish_reason == 1:  # STOP (normal completion)
                    return response.text if hasattr(response, 'text') else "I'm reflecting on your words..."
                elif finish_reason == 2:  # MAX_TOKENS
                    return response.text if hasattr(response, 'text') else "Let me pause here and continue this thought..."
                elif finish_reason == 3:  # SAFETY
                    return "I sense your question touches on sensitive ground. Let me guide you with wisdom while being mindful of our conversation's direction. Could you perhaps share more context about what you're truly seeking?"
                elif finish_reason == 4:  # RECITATION
                    return "I notice our conversation may be echoing familiar patterns. Let me offer you fresh perspective and original guidance instead."
                else:
                    return "I'm taking a moment to gather my thoughts. Please share more about what weighs on your mind."
                    
        except ValueError as e:
            if "response.text" in str(e) and "finish_reason" in str(e):
                return "I understand you're seeking guidance, but I need to approach this topic more carefully. Could you help me understand what specific aspect of wisdom you're looking for?"
            else:
                raise e
        except Exception as e:
            # Log the error for debugging
            print(f"Error in get_response: {e}", file=sys.stderr)
            return "I'm experiencing some difficulty accessing my deeper wisdom at this moment. Let me try to help you in a different way - what specific challenge are you facing today?"