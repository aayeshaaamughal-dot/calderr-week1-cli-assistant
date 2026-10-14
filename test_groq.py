
import os
from dotenv import load_dotenv
from groq import Groq

# Load API key from .env
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY .env file mein nahi mili.")

client = Groq(api_key=api_key)

response = client.chat.completions.create(
   model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": "Introduce yourself in one short sentence."
        }
    ],
)

print("Groq AI Response:")
print(response.choices[0].message.content)
