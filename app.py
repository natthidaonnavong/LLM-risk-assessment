import streamlit as st
import tempfile
import os
import re

from llm_engine import analyse_risks
from rag_engine import query_uploaded_documents
from report_generator import generate_pdf_report
from ppt_generator import generate_ppt_report
from question_engine import generate_followup_questions
from risk_mapper import generate_risks_from_answers
from utils import extract_json_array, risks_to_dataframe


st.set_page_config(
    page_title="LLM-Assisted Risk Assessment",
    page_icon="🛡️",
    layout="wide"
)


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.title("🛡️ System Information")
st.sidebar.write("**LLM:** Llama 3.1 8B")
st.sidebar.write("**RAG Framework:** LlamaIndex")
st.sidebar.write("**Embedding Model:** nomic-embed-text")
st.sidebar.write("**Runtime:** Ollama")
st.sidebar.write("**Vector Store:** ChromaDB")
st.sidebar.write("**Deployment:** Local")
st.sidebar.markdown("---")
st.sidebar.success(
    "Privacy-Preserving Local Deployment\n\n"
    "No external cloud AI services are used."
)
st.sidebar.caption(
    "Prototype system for IT Security, Governance, Risk and Compliance review."
)


# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.title("🛡️ LLM-Assisted Risk Assessment")

st.write(
    "Local cybersecurity risk assessment prototype using Streamlit, "
    "LlamaIndex RAG, Ollama, Llama 3.1 8B and deterministic risk mapping."
)

st.info("""
### Workflow

Upload documents → RAG evidence retrieval → Interactive follow-up questions →  
User/vendor answers → Deterministic risk mapping → Risk register → PDF/PPT export
""")

st.caption(
    "Prototype system: AI-generated and rule-based risk assessments "
    "should be reviewed by human analysts before approval decisions."
)


# ---------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------
def parse_questions(question_text):
    questions = []
    lines = question_text.splitlines()

    for line in lines:
        clean_line = line.strip()

        if not clean_line:
            continue

        lower_line = clean_line.lower()

        if "follow-up questions" in lower_line:
            continue
        if "targeted questions" in lower_line:
            continue
        if "here is" in lower_line:
            continue
        if "below are" in lower_line:
            continue
        if lower_line == "questions:":
            continue

        match = re.match(r"^\d+[\).\s-]*(.+)", clean_line)

        if match:
            question = match.group(1).strip()

            if len(question) > 5:
                questions.append(question)

    return questions


def show_outputs_from_risks(risks):
    st.subheader("📌 Final Risk Assessment")

    total = len(risks)
    high = len([r for r in risks if r["risk_rating"] == "High"])
    medium = len([r for r in risks if r["risk_rating"] == "Medium"])
    low = len([r for r in risks if r["risk_rating"] == "Low"])
    critical = len([r for r in risks if r["risk_rating"] == "Critical"])

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Risks", total)
    col2.metric("Critical / High", critical + high)
    col3.metric("Medium", medium)
    col4.metric("Low", low)

    df = risks_to_dataframe(risks)

    def highlight_risk(row):
        rating = row["risk_rating"]

        if rating == "Critical":
            return ["background-color: #f4cccc"] * len(row)
        elif rating == "High":
            return ["background-color: #fce5cd"] * len(row)
        elif rating == "Medium":
            return ["background-color: #fff2cc"] * len(row)
        elif rating == "Low":
            return ["background-color: #d9ead3"] * len(row)
        else:
            return [""] * len(row)

    st.subheader("📊 Risk Register")

    st.dataframe(
        df.style.apply(highlight_risk, axis=1),
        use_container_width=True
    )

    with st.expander("View Structured JSON Output", expanded=False):
        st.json(risks)

    st.subheader("📤 Export Reports")

    col1, col2 = st.columns(2)

    with col1:
        pdf_path = generate_pdf_report(risks)

        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_file,
                file_name="risk_assessment_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    with col2:
        ppt_path = generate_ppt_report(risks)

        with open(ppt_path, "rb") as ppt_file:
            st.download_button(
                label="📊 Download PowerPoint",
                data=ppt_file,
                file_name="risk_assessment_presentation.pptx",
                mime=(
                    "application/vnd.openxmlformats-"
                    "officedocument.presentationml.presentation"
                ),
                use_container_width=True
            )


def display_risk_output(result):
    st.subheader("AI Risk Assessment Output")

    with st.expander("View Raw AI Output"):
        st.code(result)

    try:
        risks = extract_json_array(result)
        show_outputs_from_risks(risks)

    except Exception as e:
        st.error("The AI output was not valid JSON.")
        st.write("Error:", e)


# ---------------------------------------------------
# MODE SELECTOR
# ---------------------------------------------------
mode = st.radio(
    "Choose assessment mode",
    [
        "Manual Vendor Input",
        "Upload Documents with RAG + Follow-Up"
    ]
)


# ---------------------------------------------------
# MANUAL MODE
# ---------------------------------------------------
if mode == "Manual Vendor Input":

    st.subheader("Manual Vendor Input")

    vendor_info = st.text_area(
        "Enter vendor/security information",
        height=300,
        placeholder="Paste vendor/security information here..."
    )

    if st.button("Analyse Manual Input", use_container_width=True):

        if not vendor_info.strip():
            st.warning(
                "Please enter vendor/security information first."
            )

        else:
            with st.spinner("Analysing vendor information..."):
                result = analyse_risks(vendor_info)

            display_risk_output(result)


# ---------------------------------------------------
# DOCUMENT RAG + FOLLOW-UP MODE
# ---------------------------------------------------
if mode == "Upload Documents with RAG + Follow-Up":

    st.subheader("📂 Document-Based Risk Assessment")

    st.write(
        "Upload assurance artefacts such as HECVAT questionnaires, "
        "SOC2 summaries, Murdoch policies and vendor questionnaires."
    )

    uploaded_files = st.file_uploader(
        "Upload assurance documents",
        type=["txt", "pdf", "docx", "xlsx","csv"],
        accept_multiple_files=True
    )

    if uploaded_files:
        st.success(f"{len(uploaded_files)} file(s) uploaded successfully.")

    rag_question = """
You are a cybersecurity evidence extractor.

ONLY return missing, unclear, undocumented, or contradictory cybersecurity controls.

STRICT RULES:
- Return concise bullet points only
- No explanations
- No categories
- No summaries
- No paragraphs
- No recommendations
- No structured risk assessment
- No reasoning
- Do not mention controls that are already implemented

Example output:
- MFA for standard users not mentioned
- Backup frequency not documented
- Data residency unclear
- Log retention period not specified

Return findings only.
"""

    if st.button(
        "Step 1: Retrieve Evidence and Generate Questions",
        use_container_width=True
    ):

        if not uploaded_files:
            st.warning("Please upload at least one document.")

        else:
            with tempfile.TemporaryDirectory() as temp_dir:

                for uploaded_file in uploaded_files:

                    file_path = os.path.join(
                        temp_dir,
                        uploaded_file.name
                    )

                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                with st.spinner("Retrieving evidence using LlamaIndex RAG..."):
                    rag_findings = query_uploaded_documents(
                        temp_dir,
                        rag_question
                    )

                with st.spinner("Generating targeted follow-up questions..."):
                    followup_questions_text = generate_followup_questions(
                        rag_findings
                    )

                questions = parse_questions(followup_questions_text)

                if not questions:
                    st.warning(
                        "Could not parse numbered questions clearly. "
                        "Please try again."
                    )
                    st.write(followup_questions_text)

                else:
                    st.session_state["rag_findings"] = rag_findings
                    st.session_state["questions"] = questions
                    st.session_state["answers"] = []
                    st.session_state["current_question_index"] = 0

    if "rag_findings" in st.session_state:

        with st.expander(
            "🔎 View Retrieved Security Evidence (RAG)",
            expanded=True
        ):
            st.success(st.session_state["rag_findings"])

    if "questions" in st.session_state:

        questions = st.session_state["questions"]
        current_index = st.session_state["current_question_index"]

        st.subheader("💬 Interactive Follow-Up Questions")

        if current_index < len(questions):

            st.progress((current_index + 1) / len(questions))

            current_question = questions[current_index]

            with st.chat_message("assistant"):
                st.write(
                    f"Follow-Up Question "
                    f"{current_index + 1} of {len(questions)}"
                )
                st.write(current_question)

            answer = st.chat_input(
                "Type your answer and press Enter..."
            )

            if answer:
                st.session_state["answers"].append(
                    {
                        "question": current_question,
                        "answer": answer
                    }
                )

                st.session_state["current_question_index"] += 1
                st.rerun()

        else:
            st.success("✓ Clarification phase completed.")

            answer_text = ""

            with st.expander(
                "📝 View Collected User/Vendor Answers",
                expanded=False
            ):
                for item in st.session_state["answers"]:
                    st.write(f"**Q:** {item['question']}")
                    st.write(f"**A:** {item['answer']}")
                    st.markdown("---")

                    answer_text += f"Q: {item['question']}\n"
                    answer_text += f"A: {item['answer']}\n\n"

            if st.button(
                "Step 2: Generate Final Risk Assessment",
                use_container_width=True
            ):

                combined_context = f"""
Retrieved RAG Findings:
{st.session_state["rag_findings"]}

User/Vendor Follow-Up Answers:
{answer_text}
"""

                with st.spinner(
                    "Generating final structured risk assessment "
                    "using deterministic risk mapping..."
                ):
                    risks = generate_risks_from_answers(
                        combined_context
                    )

                show_outputs_from_risks(risks)
