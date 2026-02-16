from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

# HARD LIMITS
MAX_TOTAL_CHARS = 8000
CHUNK_SIZE = 2000
MAX_CHUNKS = 3


def get_client():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is not set")

    return Groq(api_key=api_key)


def chunk_text(text):
    text = text[:MAX_TOTAL_CHARS]
    chunks = []

    for i in range(0, len(text), CHUNK_SIZE):
        if len(chunks) >= MAX_CHUNKS:
            break
        chunks.append(text[i:i+CHUNK_SIZE])

    return chunks


def summarize_text(text):
    client = get_client()   # ✅ client created safely here

    chunks = chunk_text(text)
    partial_summaries = []

    for chunk in chunks:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a financial research analyst. Extract key insights strictly from the given transcript. Do not fabricate information."
                },
                {
                    "role": "user",
                    "content": f"Summarize this transcript section:\n\n{chunk}"
                }
            ],
            temperature=0.3,
            max_tokens=500
        )

        partial_summaries.append(response.choices[0].message.content)

    combined_text = "\n\n".join(partial_summaries)

    final_response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": """You are a financial research analyst.

Strictly rely only on the provided transcript.
If something is not mentioned, write:
'Not explicitly discussed in transcript.'

Generate output in this exact format:

Management Tone:
Confidence Level:
3-5 Key Positives:
3-5 Key Concerns:
Forward Guidance:
Capacity Utilization Trends:
2-3 New Growth Initiatives:
"""
            },
            {
                "role": "user",
                "content": combined_text
            }
        ],
        temperature=0.2,
        max_tokens=900
    )

    return final_response.choices[0].message.content
