from flask import Flask, render_template, request
from ollama import chat
import os
import base64

app = Flask(__name__)

IMAGE_UPLOAD_PATH = os.path.join('static', 'images')
if not os.path.exists(IMAGE_UPLOAD_PATH):
    os.makedirs(IMAGE_UPLOAD_PATH)

def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form.get("prompt")  # Get the prompt from the form
        image = request.files["image"]  # Get the image from the form

        # Save the uploaded image to disk
        image_path = os.path.join(IMAGE_UPLOAD_PATH, image.filename)
        image.save(image_path)

        # Encode the image to base64
        base64_image = encode_image(image_path)

        try:
            chat_completion = chat(
                model='llama3.2-vision',
                messages=[
                    {
                        'role': 'user',
                        'content': prompt,
                        'images': [base64_image],
                    }
                ],
            )

            # Extract the response text
            response_text = chat_completion.message.content
            print(response_text)
            
            # Pass the response_text to the template
            return render_template("index.html", response_text=response_text)

        except Exception as e:
            print(f"An error occurred: {e}")
            return render_template("index.html", error_message="An error occurred while processing the image.")
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)




# # Read image and convert to Base64
# path = Path(r'C:\Users\gurun\llama-local-wepapp\static\images\red-ballon-image.jpeg')

# with open(path, 'rb') as img_file:
#     base64_image = base64.b64encode(img_file.read()).decode('utf-8')

# response = chat(
#   model='llama3.2-vision',
#   messages=[
#     {
#       'role': 'user',
#       'content': 'What is in this image? Be concise.',
#       'images': [base64_image],
#     }
#   ],
# )

# print(response.message.content)