from dotenv import load_dotenv
import os
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

import openai
openai.api_key = OPENAI_API_KEY

class OpenAIEmbedding:
    def __init__(self, model="text-embedding-ada-002"):
        self.model = model

    def encode(self, text):
        response = openai.embeddings.create(input=[text], model=self.model)
        # print(response)
        return response.data[0].embedding

# Create an instance just like SentenceTransformer
# model = OpenAIEmbedding()
# embedding = model.encode("Hello, world!")
# print("Embedding:", embedding)