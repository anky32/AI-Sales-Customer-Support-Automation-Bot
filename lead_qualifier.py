from groq import Groq
from dotenv import load_dotenv

import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def qualify_lead(budget, requirement=""):
    """
    Score a lead from 0-100 using AI analysis.
    Falls back to budget-only scoring if AI call fails.
    """

    if not requirement:
        return _budget_score(budget)

    prompt = f"""
You are a sales lead qualification expert.

Score this lead from 0 to 100 based on:
- Budget size (higher budget = higher score)
- Clarity and seriousness of the requirement
- Overall sales potential

Lead Details:
- Budget: ${budget}
- Requirement: {requirement}

Rules:
- Return ONLY a single integer number between 0 and 100
- No explanation, no text, just the number
    """.strip()

    try:

        response = client.chat.completions.create(

            model="groq/compound-mini",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        raw = response.choices[0].message.content.strip()

        # Extract first number found in response
        import re
        numbers = re.findall(r'\d+', raw)

        if numbers:
            score = int(numbers[0])
            return max(0, min(100, score))  # clamp to 0-100

        return _budget_score(budget)

    except Exception:
        return _budget_score(budget)


def _budget_score(budget):
    """Fallback: simple budget-based scoring."""
    budget = int(budget)

    if budget >= 5000:
        return 90
    elif budget >= 2000:
        return 70
    else:
        return 40
