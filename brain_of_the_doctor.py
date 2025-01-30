import os
import base64
from dotenv import load_dotenv
from groq import Groq



# Setup GROQ API KEY
GROQ_API_KEY = "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"
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set. Please ensure it is defined in the .env file.")

client = Groq(api_key=GROQ_API_KEY)

# Setup: Convert image to required format
image_path = "/Users/arnavvasishtsharma/Desktop/Medical-Chatbot/images/acne.jpg"
with open(image_path, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

# Setup: Multimodal LLM
query = "what is wrong with my face?"
model = "llama-3.2-90b-vision-preview"
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": query
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encoded_image}",
                },
            },
        ],
    }
]

# Perform chat completion request
chat_completion = client.chat.completions.create(
    messages=messages,
    model=model
)

# Print the result
print(chat_completion.choices[0].message.content)
