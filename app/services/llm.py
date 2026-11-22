from google import genai
from app.config import GEMINI_API_KEY, GEMINI_MODEL

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_response(prompt: str) -> str:
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            temperature=0 # research planning should be deterministic, not random
        )
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response")

    return response.text

if __name__ == "__main__":
    test_prompt = "Write a short poem about the beauty of nature."
    print(repr(generate_response(test_prompt)))