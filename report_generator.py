from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib import styles


def generate_pdf_report(risks, output_path="risk_assessment_report.pdf"):

    doc = SimpleDocTemplate(output_path)

    story = []

    style_sheet = styles.getSampleStyleSheet()

    title_style = style_sheet["Title"]
    heading_style = style_sheet["Heading2"]
    body_style = style_sheet["BodyText"]

    story.append(
        Paragraph(
            "LLM-Assisted Cybersecurity Risk Assessment Report",
            title_style
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Generated using Llama 3.1 + LlamaIndex RAG",
            body_style
        )
    )

    story.append(Spacer(1, 20))

    for risk in risks:

        story.append(
            Paragraph(
                f"{risk['risk_id']} - {risk['risk_description']}",
                heading_style
            )
        )

        story.append(
            Paragraph(
                f"<b>Risk Category:</b> {risk['risk_category']}",
                body_style
            )
        )

        story.append(
            Paragraph(
                f"<b>Cause:</b> {risk['cause']}",
                body_style
            )
        )

        story.append(
            Paragraph(
                f"<b>Consequence:</b> {risk['consequence']}",
                body_style
            )
        )

        story.append(
            Paragraph(
                f"<b>Likelihood:</b> {risk['likelihood']}",
                body_style
            )
        )

        story.append(
            Paragraph(
                f"<b>Impact:</b> {risk['impact']}",
                body_style
            )
        )

        story.append(
            Paragraph(
                f"<b>Risk Rating:</b> {risk['risk_rating']}",
                body_style
            )
        )

        story.append(
            Paragraph(
                f"<b>Existing Controls:</b> {risk['existing_controls']}",
                body_style
            )
        )

        story.append(
            Paragraph(
                f"<b>Recommended Controls:</b> {risk['recommended_controls']}",
                body_style
            )
        )

        story.append(
            Paragraph(
                f"<b>Risk Treatment:</b> {risk['risk_treatment']}",
                body_style
            )
        )

        story.append(
            Paragraph(
                f"<b>Residual Risk:</b> {risk['residual_risk']}",
                body_style
            )
        )

        story.append(
            Paragraph(
                f"<b>Evidence Source:</b> {risk['evidence_source']}",
                body_style
            )
        )

        story.append(
            Paragraph(
                f"<b>Follow-Up Question:</b> {risk['follow_up_question']}",
                body_style
            )
        )

        story.append(Spacer(1, 20))

    doc.build(story)

    return output_path
