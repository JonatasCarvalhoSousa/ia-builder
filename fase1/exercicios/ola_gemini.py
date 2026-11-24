from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

r = client.models.generate_content(model="gemini-3.5-flash", contents="Estou bem, o que você pode fazer por mim")
print(r.text)