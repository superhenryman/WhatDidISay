from flask import Flask, render_template, request, jsonify
from ai_handler import *
from ocr_handler import *

app = Flask(__name__)

@app.route("/")
def home(): return render_template("index.html")

@app.route("/what", methods=["POST"])
def jack_black(): # i fucking love you jack black
    # finally, main
    data = request.get_json()
    is_photo = data.get("is_photo")
    mode = data.get("mode")
    if is_photo:
        # if it is photo, we have to process it with ocr_handler, then we have to use ai and send back a response
        image = data.get("image")
        if not image:
            return jsonify({"response": "No image provided"}), 400
        try:
            image_string = return_image_string(image=image)
            if not image_string:
                return jsonify({"error": "No text found in the image"}), 400
            # print(image_string) # debugging
            response = generate_response(prompt=image_string, mode=mode)
            return jsonify({"response": response}), 200
        except Exception as e:
            print(generate_debug_response(e))
            print(f"Error: {e}")
            return jsonify({"response": "An error occurred while processing the image"}), 500
    elif not is_photo:
        # easier job
        text = data.get("text") 
        if not text:
            return jsonify({"response": "No text provided"}), 400
        
        try:
            response = generate_response(prompt=text, mode=mode)
            return jsonify({"response": response}), 200
        except Exception as e:
            print(generate_debug_response(e))
            print(f"Error: {e}")
            return jsonify({"response": "An error occurred while processing the text"}), 500
        
    else:
        return jsonify({"response": "Invalid request"}), 400


if __name__ == "__main__":
    app.run(debug=True)