from flask import Flask, request, jsonify
from subprocess import run, PIPE, TimeoutExpired
import sys
import json
import os
from flask_cors import CORS

# Define the Flask application
app = Flask(__name__)
CORS(app)

@app.route('/respond', methods=['POST'])
def respond_to_user():
    """
    Receives a user query and mentor option, and then executes a Python script
    to generate a character-based response.
    """
    try:
        # Get data from the incoming JSON request
        data = request.get_json()
        
        print(f"=== DEBUG: Received data: {data}")
        
        if not data:
            print("ERROR: No JSON data provided")
            return jsonify({"error": "No JSON data provided"}), 400
            
        question = data.get('question', '').strip()
        mentor_option = data.get('mentor_option')

        print(f"=== DEBUG: Extracted - Question: '{question}', Mentor Option: {mentor_option}")

        # Validate that the necessary data is present
        if not question:
            print("ERROR: Missing or empty question")
            return jsonify({"error": "Missing or empty 'question' in request body"}), 400
            
        if mentor_option is None:
            print("ERROR: Missing mentor_option")
            return jsonify({"error": "Missing 'mentor_option' in request body"}), 400
            
        # Validate mentor_option is a valid integer
        try:
            mentor_option = int(mentor_option)
            if mentor_option not in [0, 1, 2]:
                print(f"ERROR: Invalid mentor_option: {mentor_option}")
                return jsonify({"error": "Invalid mentor_option. Must be 0, 1, or 2"}), 400
        except (ValueError, TypeError):
            print(f"ERROR: mentor_option not valid integer: {mentor_option}")
            return jsonify({"error": "mentor_option must be a valid integer"}), 400

        print(f"=== DEBUG: Validated inputs - Question: '{question}', Mentor Option: {mentor_option}")

        # Check if gd_responder.py exists
        script_path = "gd_responder.py"
        if not os.path.exists(script_path):
            print(f"ERROR: Script not found at {script_path}")
            return jsonify({"error": f"Script file '{script_path}' not found"}), 500

        print(f"=== DEBUG: Found script at {script_path}")

        # Execute the gd_responder.py script as a subprocess
        try:
            print(f"=== DEBUG: Executing command: {sys.executable} {script_path} '{question}' {mentor_option}")
            
            process = run(
                [sys.executable, script_path, question, str(mentor_option)],
                stdout=PIPE,
                stderr=PIPE,
                text=True,
                timeout=30
            )
            
            print(f"=== DEBUG: Script completed with return code: {process.returncode}")
            print(f"=== DEBUG: Script stdout: '{process.stdout}'")
            print(f"=== DEBUG: Script stderr: '{process.stderr}'")

        except TimeoutExpired:
            print("ERROR: Script execution timed out")
            return jsonify({"error": "Request timed out. The mentor is taking too long to respond."}), 508
        except FileNotFoundError as e:
            print(f"ERROR: FileNotFoundError: {e}")
            return jsonify({"error": f"Could not execute script: {e}"}), 500

        # Check for errors from the subprocess
        if process.returncode != 0:
            error_msg = process.stderr if process.stderr else "Unknown error occurred in gd_responder.py"
            print(f"ERROR: Script failed with error: {error_msg}")
            return jsonify({"error": f"Script execution failed: {error_msg}"}), 500

        response_text = process.stdout.strip()
        print(f"=== DEBUG: Final response text: '{response_text}'")
        
        if not response_text:
            print("ERROR: Empty response from script")
            return jsonify({"error": "Empty response from mentor script"}), 500

        # Return the output from the script
        print(f"=== DEBUG: Returning successful response")
        return jsonify({"response": response_text})

    except Exception as e:
        print(f"=== ERROR: Unexpected exception: {str(e)}")
        print(f"=== ERROR: Exception type: {type(e).__name__}")
        import traceback
        print(f"=== ERROR: Traceback: {traceback.format_exc()}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "healthy", "message": "Mentor API is running"}), 200

@app.route('/test-script', methods=['GET'])
def test_script():
    """Test if gd_responder.py can be executed"""
    try:
        # Test with simple parameters
        process = run(
            [sys.executable, "gd_responder.py", "test question", "0"],
            stdout=PIPE,
            stderr=PIPE,
            text=True,
            timeout=10
        )
        
        return jsonify({
            "script_exists": os.path.exists("gd_responder.py"),
            "return_code": process.returncode,
            "stdout": process.stdout,
            "stderr": process.stderr,
            "python_executable": sys.executable
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Mentor Backend API...")
    print("Available endpoints:")
    print("- POST /respond - Get mentor response")
    print("- GET /health - Health check")
    print("- GET /test-script - Test gd_responder.py")
    print(f"Python executable: {sys.executable}")
    print(f"Working directory: {os.getcwd()}")
    print(f"gd_responder.py exists: {os.path.exists('gd_responder.py')}")
    app.run(debug=True, host='0.0.0.0', port=5000)