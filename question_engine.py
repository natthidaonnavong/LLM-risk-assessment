import requests


def generate_followup_questions(rag_findings):

    prompt = f"""
You are an experienced IT cybersecurity risk analyst.

Based on the missing or unclear controls below, generate targeted follow-up questions for clarification.

GOAL:
Ask ONLY the most important questions needed to improve confidence in the final risk assessment.

STRICT RULES:
- Generate a maximum of 6 follow-up questions.
- Prioritise High or Medium risk issues.
- Prioritise:
  - Access control
  - Privacy and compliance
  - Business continuity
  - Monitoring and logging
  - Vendor risk
- Ask only questions that materially improve assurance.
- Avoid duplicate or overlapping questions.
- Do NOT ask questions if the issue is already sufficiently clear.
- Avoid low-value or unnecessary clarification questions.
- Return ONLY numbered questions.
- One question per line.
- No explanations.
- No headings.
- No introductory text.
- No summary sentence.

GOOD QUESTION EXAMPLES:
1. What is the Recovery Time Objective (RTO) for critical systems and applications?
2. Are MFA controls enabled for non-administrative accounts?
3. What are the data residency locations for sensitive organisational data?

BAD QUESTION EXAMPLES:
❌ Here is the list of targeted follow-up questions:
❌ Please answer the following:
❌ Can you elaborate more?
❌ Generic low-value questions

Missing or unclear controls:
{rag_findings}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.1:8b",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]
