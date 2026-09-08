from groq import Groq
from dotenv import load_dotenv

import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_email(name, requirement):

    prompt = f"""
Write a professional sales email to a potential client.

Client Name: {name}
Client Requirement: {requirement}

The email should:
- Have a compelling subject line (prefix it with "Subject:")
- Be warm, professional and concise
- Highlight how we can solve their requirement
- Include a clear call to action
- End with a professional sign-off from "The Sales Team"
    """.strip()

    try:

        response = client.chat.completions.create(

            model="groq/compound-mini",

            messages=[
                {
                    "role": "system",
                    "content": "You are an expert sales copywriter. Write persuasive, professional sales emails."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error generating email: {str(e)}"
