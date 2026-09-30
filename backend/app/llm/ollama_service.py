"""
ollama_service.py

Optimized Ollama Service
"""

from ollama import chat


class OllamaService:

    def __init__(self, model="llama3.2:3b"):
        self.model = model

    def generate(self, prompt: str):

        response = chat(
            model=self.model,
            keep_alive="10m",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0.0,
                "top_p": 0.9,

                # Keep answers concise
                "num_predict": 140,

                # Smaller context = less processing
                "num_ctx": 2048,
            }
        )

        return response["message"]["content"]