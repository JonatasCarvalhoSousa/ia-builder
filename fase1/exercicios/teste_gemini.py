from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()
client = genai.Client() # lê GEMINI_API_KEY sozinho
MODELO = "gemini-3.5-flash-lite"
r = client.models.generate_content(
model=MODELO,
contents="Liste 3 cenários de teste para um campo de CEP.",
config=types.GenerateContentConfig(
system_instruction="Você é um analista de QA sênior. Responda em português, de forma objetiva.",
temperature=0.2,
max_output_tokens=500,
),
)
print(r.text)
print("Tokens:", r.usage_metadata.prompt_token_count, "entrada /",
r.usage_metadata.candidates_token_count, "saída")