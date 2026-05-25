import requests


def analyse_risks(vendor_info):
    prompt = f"""
You are an IT cybersecurity risk analyst.

You are given a combined context containing:
- RAG findings from uploaded assurance documents
- follow-up questions
- user/vendor answers

IMPORTANT:
The user/vendor answers are the most recent and most trusted information.
If a user/vendor answer clarifies an issue, do not keep describing it as missing.

Your task:
Create a final cybersecurity risk assessment.

Rules:
- Return ONLY valid JSON.
- Do not include markdown.
- Maximum 10 risks.
- Do not duplicate risks.
- Use the user/vendor answers to update the risk descriptions.
- If a control exists but evidence is still needed, describe it as an assurance or documentation gap.
- If a control is planned but not implemented, describe it as an implementation gap.
- Do not overstate severity.
- Documentation or evidence gaps should usually be Medium risk.
- Use Critical only for severe confirmed risks.

Use this exact JSON structure:
[
  {{
    "risk_id": "R001",
    "risk_category": "",
    "risk_description": "",
    "cause": "",
    "consequence": "",
    "likelihood": "",
    "impact": "",
    "risk_rating": "",
    "existing_controls": "",
    "recommended_controls": "",
    "risk_treatment": "",
    "residual_risk": "",
    "evidence_source": "",
    "follow_up_question": ""
  }}
]

Allowed categories:
- Access Control
- Data Protection
- Privacy and Compliance
- Business Continuity
- Monitoring and Logging
- Vendor Risk
- Network Security
- Confidentiality
- Integrity
- Availability

Category guide:
- MFA, password, authentication = Access Control
- Encryption, key rotation, data deletion = Data Protection
- Data residency, Privacy Act, GDPR, PIA = Privacy and Compliance
- Backup, RTO, RPO, disaster recovery = Business Continuity
- Logs, SIEM, monitoring = Monitoring and Logging
- Vendors, subcontractors, employee training, audits = Vendor Risk
- Vulnerability scanning, penetration testing, firewall = Network Security

Important examples:
- If data is stored in Australia and Singapore, do not say "data residency not provided".
  Instead say "cross-border data residency compliance should be formally evidenced".
- If training is provided, do not say "training not mentioned".
  Instead say "training completion evidence should be reviewed".
- If vendors are listed, do not say "subcontractors not disclosed".
  Instead say "vendor assurance evidence should be assessed".
- If RTO is 4 hours, do not say "RTO missing".
  Instead say "RTO documentation should be confirmed".
- If SIEM is planned within 12 months, say "SIEM integration is planned but not yet operational".

Use only:
- likelihood: Low, Medium, High
- impact: Low, Medium, High, Critical
- risk_rating: Low, Medium, High, Critical
- risk_treatment: Accept, Mitigate, Transfer, Avoid

Risk rating guide:
- Low + Low/Medium = Low
- Medium + Medium = Medium
- Medium + High = High
- High + Medium = High
- High + High/Critical = Critical
- Documentation/evidence gaps normally = Medium
- Planned but not implemented controls normally = Medium

Existing controls:
Only include controls directly relevant to the risk.

Examples:
- Encryption risk: AES-256, TLS, 90-day key rotation
- MFA risk: MFA using authenticator apps
- Data residency risk: Australia and Singapore
- RTO/DR risk: 4-hour RTO, annual DR testing
- Logging risk: 12-month log retention
- SIEM risk: Microsoft Sentinel planned
- Vendor risk: AWS, Azure, Cloudflare, SendGrid
- Training risk: onboarding and annual refresher training
- PIA risk: PIA conducted within last 12 months

If no relevant control exists, use "Not specified".

Context:
{vendor_info}

Return ONLY the JSON array.
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
