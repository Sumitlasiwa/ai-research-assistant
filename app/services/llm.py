from google import genai
from app.config import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_MODEL_STRONG
from google.genai import types

client = genai.Client(api_key=GEMINI_API_KEY,
                      http_options = types.HttpOptions(
                          retry_options=types.HttpRetryOptions(
                          attempts=5,
                          initial_delay=1.0,
                          max_delay=10.0,
                          exp_base=2.0,
                          jitter=0.5,
                          http_status_codes=[408, 429, 500, 502, 503, 504]
                      ),
                      timeout=60_000
                      )
)


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

def generate_response_reviewer(prompt: str) -> str:
    response = client.models.generate_content(
        model=GEMINI_MODEL_STRONG,
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            temperature=0,
            thinking_config=genai.types.ThinkingConfig(
                thinking_level=genai.types.ThinkingLevel.HIGH 
            )
        )
    )
    if not response.text:
        raise RuntimeError("Gemini returned an empty response")

    return response.text

if __name__ == "__main__":
    test_prompt = "Write a short poem about the beauty of nature."
    print(repr(generate_response(test_prompt)))