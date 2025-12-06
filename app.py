import streamlit as st
from pypdf import PdfReader
from ats_scanner import calculate_match


# ------------ PDF Extraction ------------
def extract_text_from_pdf(file) -> str:
    text = ""
    try:
        pdf = PdfReader(file)
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    except Exception:
        return ""
    return text.strip()


def classify_match(score: float) -> str:
    if score >= 85:
        return "Excellent Match"
    elif score >= 70:
        return "Strong Match"
    elif score >= 50:
        return "Moderate Match"
    else:
        return "Weak Match"


def get_status_badge(score: float) -> str:
    if score >= 70:
        return '<span class="badge badge-green">LIKELY SHORTLISTED</span>'
    elif score >= 50:
        return '<span class="badge badge-amber">MAY PASS FILTER</span>'
    else:
        return '<span class="badge badge-red">LOW CHANCE</span>'


# ------------ Page Config ------------
st.set_page_config(
    page_title="ATS Resume Scanner | Shivam Kumar",
    page_icon="📝",
    layout="wide"
)


# ------------ Modern Dark Mode Styling (Black + Orange) ------------
st.markdown("""
<style>

    /* PAGE BACKGROUND */
    .stApp {
        background: #000000;
        color: #e6e6e6;
        font-family: 'Segoe UI', sans-serif;
    }

    .block-container {
        padding-top: 1.5rem;
        max-width: 1100px;
    }

    /* HEADER CARD */
    .hero {
        background: linear-gradient(135deg, #111111, #1a1a1a);
        border: 1px solid #ff88008f;
        border-radius: 18px;
        padding: 1.8rem 2rem;
        box-shadow: 0 0 28px rgba(255,128,0,0.25);
    }

    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #ff8800;
        margin-bottom: 0.3rem;
    }

    .hero-sub {
        font-size: 1rem;
        color: #bbbbbb;
        line-height: 1.5;
    }

    .tag {
        padding: 6px 12px;
        border-radius: 20px;
        background: #2b2b2b;
        border: 1px solid #ff8800;
        font-size: 0.75rem;
        color: #f3f3f3;
    }

    /* INPUT FIELDS */
    textarea, input {
        background-color: #0e0e0e !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        border: 1px solid #444444 !important;
    }

    textarea:focus, input:focus {
        border: 1px solid #ff8800 !important;
        background-color: #141414 !important;
    }

    /* BUTTON */
    .stButton > button {
        width: 100%;
        background: #ff8800;
        color: black;
        border-radius: 30px;
        font-weight: bold;
        padding: 0.7rem;
        transition: 0.2s;
        border: none;
        box-shadow: 0 0 15px rgba(255,136,0,0.55);
    }

    .stButton > button:hover {
        background: #ffaa33;
        box-shadow: 0 0 25px rgba(255,136,0,0.9);
        color: black;
    }

    /* BADGES */
    .badge {
        padding: 6px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
        letter-spacing: 0.05em;
        display: inline-block;
        margin-top: 8px;
    }
    .badge-green {background: rgba(0,200,100,0.2); color: #00ff6f; border:1px solid #00ff6f;}
    .badge-amber {background: rgba(255,170,0,0.2); color: #ffbb33; border:1px solid #ffbb33;}
    .badge-red {background: rgba(255,0,0,0.2); color: #ff5f5f; border:1px solid #ff5f5f;}

    /* CARDS */
    .card {
        background: #111111;
        border-radius: 14px;
        padding: 1.2rem;
        border: 1px solid #333333;
    }

    .footer {
        margin-top: 2rem;
        text-align: center;
        color: #888;
        font-size: 0.85rem;
    }

</style>
""", unsafe_allow_html=True)



# ------------ UI Layout ------------
st.markdown(f"""
<div class='hero'>
    <div class='hero-title'>ATS Resume Scanner</div>
    <div class='hero-sub'>
        Compare your resume against a job description using AI scoring, keyword matching, 
        and ATS filtering insights — styled clean, minimal and professional.
    </div>
    <br>
    <span class="tag">Resume vs Job Description Match</span>
    <span class="tag">AI Assistance</span>
    <span class="tag">ATS Optimization</span>
    <p style="margin-top:10px; color:#777;">Developed by <strong style="color:#ff8800;">Shivam Kumar</strong></p>
</div>
""", unsafe_allow_html=True)


st.write("")
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Job Description")
    job_description = st.text_area("", height=250, placeholder="Paste the job description here...")

with col2:
    st.subheader("📁 Upload Resume (PDF)")
    uploaded_file = st.file_uploader("", type="pdf")


st.write("")
center = st.columns([1,1,1])[1]
with center:
    submit = st.button("Analyze Resume")


# ------------ Run Analysis ------------
if submit:
    if not uploaded_file or not job_description.strip():
        st.warning("⚠ Please provide both resume and job description.")
    else:
        resume_text = extract_text_from_pdf(uploaded_file)

        if not resume_text:
            st.error("⚠ Could not extract text. Resume might be scanned. Use a text-based PDF.")
            st.stop()

        score = calculate_match(resume_text, job_description)
        rounded_score = int(round(score))

        st.subheader("📊 Match Result")
        st.progress(rounded_score, text=f"{rounded_score}% Match Score")

        st.markdown(f"""
        <p style='font-size:1.2rem; margin-top:10px;'>
            <strong>{classify_match(score)}</strong><br>
            {get_status_badge(score)}
        </p>
        """, unsafe_allow_html=True)

        st.write("")
        st.markdown("### Suggestions")
        st.markdown("""
        - Ensure required skills appear clearly in your resume  
        - Use similar wording as the job post  
        - Add missing tools or frameworks (if relevant)  
        """)


st.markdown("<div class='footer'>© 2025 · Designed by Shivam Kumar · All Rights Reserved</div>", unsafe_allow_html=True)
