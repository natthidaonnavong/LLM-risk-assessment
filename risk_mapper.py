def generate_risks_from_answers(context):
    text = context.lower()
    risks = []

    def contains_any(words):
        return any(word in text for word in words)

    counter = 1

    def next_id():
        nonlocal counter
        rid = f"R{counter:03d}"
        counter += 1
        return rid

    def add_risk(
        category,
        description,
        cause,
        consequence,
        likelihood,
        impact,
        rating,
        controls,
        recommendation,
        treatment="Mitigate",
        residual="Low"
    ):
        risks.append({
            "risk_id": next_id(),
            "risk_category": category,
            "risk_description": description,
            "cause": cause,
            "consequence": consequence,
            "likelihood": likelihood,
            "impact": impact,
            "risk_rating": rating,
            "existing_controls": controls,
            "recommended_controls": recommendation,
            "risk_treatment": treatment,
            "residual_risk": residual,
            "evidence_source":
                "RAG findings and user/vendor follow-up answers",
            "follow_up_question": ""
        })

    # ------------------------------------------------
    # MFA
    # ------------------------------------------------
    if contains_any([
        "mfa",
        "authenticator",
        "one-time password",
        "multi-factor authentication"
    ]):

        add_risk(
            "Access Control",
            "MFA enforcement evidence should be validated",
            "MFA is enabled using authenticator-based one-time passwords, but implementation evidence should be confirmed.",
            "Without evidence of MFA enforcement, there may be reduced assurance that account access controls are consistently applied.",
            "Medium",
            "Medium",
            "Medium",
            "MFA enabled for non-administrative accounts using authenticator app-based one-time passwords",
            "Review MFA configuration evidence and verify enforcement across relevant systems."
        )

    # ------------------------------------------------
    # Encryption
    # ------------------------------------------------
    if contains_any([
        "key rotation",
        "90 days",
        "encryption keys",
        "key management"
    ]):

        add_risk(
            "Data Protection",
            "Encryption key governance evidence should be reviewed",
            "Encryption keys rotate every 90 days under a documented key management process.",
            "If encryption governance documentation is incomplete, the organisation may have reduced assurance over long-term key protection.",
            "Medium",
            "Medium",
            "Medium",
            "AES-256 encryption, TLS encryption and 90-day key rotation policy",
            "Review key management procedures and recent key rotation records."
        )

    # ------------------------------------------------
    # Data residency
    # ------------------------------------------------
    if contains_any([
        "australia",
        "singapore",
        "data residency"
    ]):

        add_risk(
            "Privacy and Compliance",
            "Cross-border data residency compliance should be evidenced",
            "Sensitive information is stored across Australia and Singapore, creating jurisdiction-specific privacy obligations.",
            "If cross-border handling requirements are not formally evidenced, privacy and regulatory compliance risks may increase.",
            "Medium",
            "High",
            "High",
            "Sensitive data stored in Australia and Singapore with encryption at rest and in transit",
            "Review data residency agreements and validate regulatory compliance obligations."
        )

    # ------------------------------------------------
    # RTO
    # ------------------------------------------------
    if contains_any([
        "rto",
        "recovery time objective",
        "4 hours",
        "4-hour"
    ]):

        add_risk(
            "Business Continuity",
            "Recovery Time Objective evidence should be confirmed",
            "A 4-hour RTO exists for critical systems, but supporting continuity evidence should be reviewed.",
            "If recovery procedures are not fully evidenced, service restoration delays may occur during outages.",
            "Medium",
            "Medium",
            "Medium",
            "RTO for critical systems is 4 hours",
            "Review continuity documentation and recovery testing evidence."
        )

    # ------------------------------------------------
    # DR Testing
    # ------------------------------------------------
    if contains_any([
        "disaster recovery",
        "failover",
        "backup restoration",
        "last 12 months"
    ]):

        add_risk(
            "Business Continuity",
            "Disaster recovery testing effectiveness should be evidenced",
            "Disaster recovery testing occurs annually and within the last 12 months.",
            "Without documented evidence of outcomes and remediation tracking, recovery preparedness may be difficult to validate.",
            "Medium",
            "Medium",
            "Medium",
            "Annual disaster recovery testing and recovery exercises",
            "Review disaster recovery test reports and remediation actions."
        )

    # ------------------------------------------------
    # Logs
    # ------------------------------------------------
    if contains_any([
        "log retention",
        "logs retained",
        "12 months"
    ]):

        add_risk(
            "Monitoring and Logging",
            "Log retention and review evidence should be confirmed",
            "System logs are retained for 12 months and reviewed regularly.",
            "Weak evidence of logging practices may reduce incident investigation and compliance assurance.",
            "Medium",
            "Medium",
            "Medium",
            "12-month log retention and regular IT security reviews",
            "Review log retention policy and evidence of log review procedures."
        )

    # ------------------------------------------------
    # SIEM
    # ------------------------------------------------
    if contains_any([
        "siem",
        "sentinel",
        "microsoft sentinel"
    ]):

        add_risk(
            "Monitoring and Logging",
            "SIEM integration is planned but not operational",
            "Microsoft Sentinel implementation is planned within the next 12 months.",
            "Until SIEM deployment is completed, visibility over security events and incident detection may remain limited.",
            "Medium",
            "Medium",
            "Medium",
            "Microsoft Sentinel planned for deployment",
            "Review implementation roadmap and interim monitoring controls."
        )

    # ------------------------------------------------
    # Vendors
    # ------------------------------------------------
    if contains_any([
        "aws",
        "azure",
        "cloudflare",
        "sendgrid",
        "vendors",
        "subcontractors"
    ]):

        add_risk(
            "Vendor Risk",
            "Third-party assurance evidence should be reviewed",
            "Third-party vendors support hosting, identity, communication and security services.",
            "If vendor assurance evidence is incomplete, supply chain, compliance and confidentiality risks may increase.",
            "Medium",
            "High",
            "High",
            "AWS, Azure, Cloudflare and SendGrid with vendor reviews and questionnaires",
            "Review vendor assurance evidence, contracts and security responsibilities."
        )

    # ------------------------------------------------
    # Training
    # ------------------------------------------------
    if contains_any([
        "training",
        "phishing",
        "annual refresher",
        "security awareness"
    ]):

        add_risk(
            "Vendor Risk",
            "Employee cybersecurity awareness evidence should be reviewed",
            "Cybersecurity training is provided during onboarding and annually.",
            "Without evidence of completion and effectiveness, employee-related security exposure may remain.",
            "Low",
            "Medium",
            "Low",
            "Mandatory onboarding and annual cybersecurity training",
            "Review training completion reports and awareness programme effectiveness."
        )

    # ------------------------------------------------
    # Audits
    # ------------------------------------------------
    if contains_any([
        "audit",
        "internal audits",
        "external audits"
    ]):

        add_risk(
            "Vendor Risk",
            "Security audit evidence should be reviewed",
            "Internal audits occur annually and external audits occur every two years.",
            "Without audit evidence, assurance over security control effectiveness may be reduced.",
            "Low",
            "Medium",
            "Low",
            "Annual internal audits and biennial external audits",
            "Review recent audit findings and remediation evidence."
        )

    # ------------------------------------------------
    # PIA
    # ------------------------------------------------
    if contains_any([
        "privacy impact assessment",
        "pia"
    ]):

        add_risk(
            "Privacy and Compliance",
            "Privacy Impact Assessment evidence should be reviewed",
            "PIAs have been conducted for high-risk systems and processes.",
            "Without supporting privacy assessment evidence, assurance over privacy risk management may be reduced.",
            "Medium",
            "High",
            "High",
            "Privacy Impact Assessments conducted for high-risk systems",
            "Review recent PIA findings and mitigation actions."
        )

    return risks[:10]
