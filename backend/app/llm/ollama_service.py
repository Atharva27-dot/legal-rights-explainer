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

                "num_predict": 190,

                "num_ctx": 3072

            }

        )

        return response["message"]["content"]