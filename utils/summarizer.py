from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()   


client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Split text into manageable chunks
def chunk_text(text, chunk_size=2500):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks


def summarize_text(text):
    chunks = chunk_text(text)

    partial_summaries = []

    # Step 1: Summarize chunks
    for chunk in chunks[:3]:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a financial research analyst. Extract key insights from earnings transcripts."
                },
                {
                    "role": "user",
                    "content": f"Summarize this transcript section:\n\n{chunk}"
                }
            ],
            temperature=0.3,
            max_tokens=600
        )

        partial_summaries.append(response.choices[0].message.content)

    combined_text = "\n\n".join(partial_summaries)

    # Step 2: Create FINAL structured output
    final_response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": """You are a financial research analyst.
Generate structured output in this exact format:

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
        max_tokens=1200
    )

    return final_response.choices[0].message.content

