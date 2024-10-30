import json
from openai import OpenAI
from config import OPENAI_API_KEY

class AIHelper:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def process_query(self, query: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant specializing in blockchain technology."},
                    {"role": "user", "content": query}
                ],
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error processing query: {str(e)}"
