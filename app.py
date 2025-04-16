from flask import Flask, render_template, request, jsonify
from flask import jsonify
from ai_handler import *
from ocr_handler import *
import base64
import binascii

app = Flask(__name__)

@app.route("/")
def home(): return render_template("index.html")

@app.route("/what", methods=["POST"])
def jack_black():
    """Handle both text and image processing requests with validation"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        valid_modes = ["Serious", "Normal", "Sarcastic"]
        mode = data.get("mode")
        if mode not in valid_modes:
            return jsonify({"error": f"Invalid mode. Valid options: {', '.join(valid_modes)}"}), 400

        is_photo = data.get("is_photo", False)
        
        if is_photo:
            return handle_image_request(data, mode)
        return handle_text_request(data, mode)
        
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        debug_info = generate_debug_response(str(e))
        print(f"Critical Error: {error_msg}\nDebug Info: {debug_info}")
        return jsonify({"error": "Internal server error", "debug": debug_info}), 500


def handle_image_request(data, mode):
    """Process image-based requests"""
    try:
        image_b64 = data.get("image")
        if not image_b64:
            return jsonify({"error": "No image data provided"}), 400

        try:
            image_bytes = base64.b64decode(image_b64)
        except (binascii.Error, ValueError) as e:
            return jsonify({"error": "Invalid base64 encoding"}), 400

        image_string = return_image_string(image_bytes)
        if not image_string.strip():
            return jsonify({"error": "No text found in image"}), 400

        return jsonify({
            "response": generate_response(image_string, mode)
            }), 200
        
    except Exception as e:
        debug_info = generate_debug_response(str(e))
        return jsonify({"error": "Image processing failed", "debug": debug_info}), 400

def handle_text_request(data, mode):
    """Process text-based requests"""
    text = data.get("text")
    if not text or not text.strip():
        return jsonify({"error": "No text provided"}), 400
    
    if len(text) > 10000:
        return jsonify({"error": "Text exceeds 10,000 character limit"}), 400

    return jsonify({
        "response": generate_response(text, mode)
        }), 200


if __name__ == "__main__":
    app.run(debug=True)