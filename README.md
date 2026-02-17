# Earnings Call Analyzer – Option B

## Developed By
Vyshnavi Kakarla

---

## Overview

This application analyzes earnings call transcripts and generates structured financial insights including:

- Management Tone
- Confidence Level
- 3–5 Key Positives
- 3–5 Key Concerns
- Forward Guidance
- Capacity Utilization Trends
- 2–3 New Growth Initiatives

The system is designed to process long transcripts reliably while respecting API token limits.

---

##  How It Works

### 1.Document Processing
- User uploads an earnings call transcript (PDF).
- The system extracts text from the document.
- If the document is large, it is split into manageable chunks.

### 2. Hierarchical Summarization
To handle long transcripts efficiently:

- Step 1: Each chunk is summarized individually.
- Step 2: Partial summaries are combined.
- Step 3: A final structured financial analysis is generated.

This prevents token overflow and improves output coherence.

---

##  Output Structure

The system generates output in the following structured format:

- Management Tone
- Confidence Level
- 3–5 Key Positives
- 3–5 Key Concerns
- Forward Guidance (Revenue / Margin / Capex outlook if mentioned)
- Capacity Utilization Trends
- 2–3 New Growth Initiatives

---

##  Management Tone Assessment

Tone is determined using model-based interpretation of:

- Forward-looking statements
- Defensive or corrective language
- Growth commentary
- Risk disclosures
- Clarifications and transparency in responses

---

##  Hallucination Prevention

The model is explicitly instructed to:

- Rely strictly on transcript content
- Avoid adding assumptions
- Avoid fabricating financial metrics
- Mark missing sections as:

  "Not explicitly discussed in transcript."

This ensures research-grade reliability.

---

##  Limitations

- Due to free-tier API token constraints, only the initial transcript sections may be analyzed.
- Very large files may experience slight processing latency.
- OCR functionality may not be supported in deployed environments.
- Output depends entirely on the quality and clarity of the provided transcript.

## Deployment Constraints

This application is deployed on Render Free Tier, which has limited memory and CPU resources.

To ensure stability:
- Maximum PDF upload size: 4MB
- Extracted text is truncated before sending to OpenAI API

These constraints prevent Gunicorn worker crashes and optimize memory usage.


---

## Deployment

The application is built using:

- Flask (Backend)
- Groq API (LLM inference)
- Chunk-based summarization logic
- Structured output formatting

Environment variable required:

GROQ_API_KEY=your_api_key_here

---

##  Live Deployment Link

Render
https://earnings-call-summary.onrender.com

---

## Scope Completion

This tool supports:

- Document upload
- Transcript processing
- End-to-end research analysis
- Structured and usable output

The system prioritizes reliability, clarity, and structured financial insight generation over performance.

---
