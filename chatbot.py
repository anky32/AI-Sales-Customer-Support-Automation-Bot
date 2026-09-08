from groq import Groq
from dotenv import load_dotenv
from faq import FAQS

import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Build FAQ context string for system prompt
faq_context = "\n".join(
    [f"- {key.capitalize()}: {value}" for key, value in FAQS.items()]
)

SYSTEM_PROMPT = f"""
You are an AI Sales and Customer Support Agent.
Help customers professionally and politely.

Here is important company information you must use when answering:

{faq_context}

Always answer based on the above information when relevant.
If you don't know something, say you will connect them with a human agent.
""".strip()

# Try primary model, fall back to secondary
PRIMARY_MODEL   = "compound-beta"
FALLBACK_MODEL  = "groq/compound-mini"


def ask_bot(question):

    for model in [PRIMARY_MODEL, FALLBACK_MODEL]:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": question}
                ]
            )
            return response.choices[0].message.content

        except Exception as e:
            error_msg = str(e)
            # If it's a service error and we have a fallback, try next
            if model == PRIMARY_MODEL and ("503" in error_msg or "unavailable" in error_msg.lower()):
                continue
            return f"Sorry, I'm unable to process your request right now. Please try again later.\n\nError: {error_msg}"

    return "Sorry, the AI service is currently unavailable. Please try again in a few minutes."
