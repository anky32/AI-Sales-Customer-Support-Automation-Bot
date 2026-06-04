from groq import Groq
from dotenv import load_dotenv

import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def ask_bot(question):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "system",

                "content":
                """
                You are an AI Sales and Customer Support Agent.

                Help customers professionally.
                """
            },

            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.choices[0].message.content