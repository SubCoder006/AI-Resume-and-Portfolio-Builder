"""
AI Resume & Portfolio Builder — Optimized Version

Features:
- One-page ATS resume (concise, small fonts)
- Detailed portfolio PDF (elaborate descriptions with image placeholders)
- Clean, modern UI

Run: streamlit run app.py
"""

import os
import streamlit as st
from dotenv import load_dotenv

from styles import inject_styles
from input_form import student_input_form
from role_selector import role_selector
from resume_generator import (
    generate_resume_summary,
    generate_project_bullets,
    generate_full_resume,
)
from pdf_generator import generate_pdf_resume
from portfolio_generator import generate_portfolio_content
from portfolio_pdf_generator import generate_portfolio_pdf

# ─── Bootstrap ────────────────────────────────────────────────────────────
load_dotenv()
os.makedirs("output/resumes", exist_ok=True)
os.makedirs("output/portfolios", exist_ok=True)

st.set_page_config(
    page_title="AI Resume & Portfolio Builder",
    layout="centered",
    initial_sidebar_state="collapsed",
)

inject_styles()

# ─── Session State Defaults ───────────────────────────────────────────────
st.session_state.setdefault("summary", "")
st.session_state.setdefault("bullets", "")
st.session_state.setdefault("full_resume", "")
st.session_state.setdefault("resume_pdf_path", "")
st.session_state.setdefault("portfolio_content", "")
st.session_state.setdefault("portfolio_pdf_path", "")


# ═══════════════════════════════════════════════════════════════════════════
# HELPER: Render animated 4-step stepper
# ═══════════════════════════════════════════════════════════════════════════
def _render_stepper(data_saved: bool, has_resume: bool, has_resume_pdf: bool, has_portfolio: bool):
    steps = [
        ("1", "Details", data_saved),
        ("2", "Resume", has_resume),
        ("3", "Resume PDF", has_resume_pdf),
        ("4", "Portfolio PDF", has_portfolio),
    ]

    active_idx = len(steps)
    for i, (_, _, done) in enumerate(steps):
        if not done:
            active_idx = i
            break

    html_parts = ['<div class="stepper">']
    for i, (num, label, done) in enumerate(steps):
        if i < active_idx:
            state = "done"
        elif i == active_idx:
            state = "active"
        else:
            state = "pending"

        connector = '<div class="step-connector"></div>' if i < len(steps) - 1 else ""
        html_parts.append(f"""
            <div class="step {state}">
                <div class="step-circle">{num if state == 'pending' else '&#10003;' if state == 'done' else num}</div>
                <span class="step-label">{label}</span>
                {connector}
            </div>
        """)
    html_parts.append('</div>')
    st.markdown("".join(html_parts), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# HELPER: Render output card for resume preview
# ═══════════════════════════════════════════════════════════════════════════
def _output_card_resume(text: str):
    escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    formatted = escaped.replace("\n", "<br>")
    
    st.markdown(f"""
    <div class="output-card">
      <div class="output-label">One-Page ATS Resume (Preview)</div>
      <div class="output-text" style="font-family: 'Courier New', monospace; font-size: 0.85rem; line-height: 1.5;">
        {formatted}
      </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE LAYOUT
# ═══════════════════════════════════════════════════════════════════════════

# ── Hero Banner ───────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-mesh-orb"></div>
  <h1>AI Resume &amp; Portfolio Builder</h1>
  <p class="subtitle">One-page ATS resume + Detailed portfolio PDF — powered by Google Gemini</p>
</div>
""", unsafe_allow_html=True)

# ── Step 1: Role + Student Details ────────────────────────────────────────
role = role_selector()
student_data = student_input_form()

# ── Stepper ───────────────────────────────────────────────────────────────
_render_stepper(
    data_saved=student_data is not None,
    has_resume=bool(st.session_state["full_resume"]),
    has_resume_pdf=bool(st.session_state["resume_pdf_path"]),
    has_portfolio=bool(st.session_state["portfolio_pdf_path"]),
)

# ── Step 2: AI Resume Generation ──────────────────────────────────────────
st.markdown("""
<div class="glass-card">
  <div class="card-header">
    <div class="card-icon">&#128196;</div>
    <div>
      <p class="card-title">One-Page ATS Resume</p>
      <p class="card-subtitle">Concise, optimized resume with small fonts to fit one page</p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

if not student_data:
    st.info("💡 Save your details above to unlock AI generation.")
else:
    st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
    if st.button("✨ Generate One-Page Resume", use_container_width=True):
        with st.spinner("Generating concise resume components…"):
            summary = generate_resume_summary(student_data, role)
            st.session_state["summary"] = summary
            
            bullets = generate_project_bullets(student_data, role)
            st.session_state["bullets"] = bullets
            
        with st.spinner("Assembling one-page ATS resume…"):
            full_resume = generate_full_resume(student_data, role, summary, bullets)
            st.session_state["full_resume"] = full_resume
            
        st.success("✅ One-page resume generated!")
    st.markdown('</div>', unsafe_allow_html=True)

# Display resume preview
if st.session_state["full_resume"]:
    _output_card_resume(st.session_state["full_resume"])

# ── Step 3: Resume PDF Export ─────────────────────────────────────────────
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="glass-card">
  <div class="card-header">
    <div class="card-icon">&#128190;</div>
    <div>
      <p class="card-title">Resume PDF Export</p>
      <p class="card-subtitle">Download your one-page ATS resume as PDF (optimized fonts)</p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

if not student_data:
    st.info("💡 Save your details first.")
elif not st.session_state["full_resume"]:
    st.warning("⚠️ Generate the resume first.")
else:
    st.markdown('<div class="btn-export">', unsafe_allow_html=True)
    if st.button("📄 Export Resume PDF", use_container_width=True):
        with st.spinner("Creating one-page PDF with optimized formatting…"):
            st.session_state["resume_pdf_path"] = generate_pdf_resume(
                st.session_state["full_resume"]
            )
        st.success("✅ Resume PDF created!")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state["resume_pdf_path"] and os.path.exists(st.session_state["resume_pdf_path"]):
        st.markdown('<div class="btn-download">', unsafe_allow_html=True)
        with open(st.session_state["resume_pdf_path"], "rb") as f:
            st.download_button(
                label="⬇️ Download Resume PDF",
                data=f,
                file_name="resume.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

# ── Step 4: Portfolio PDF ─────────────────────────────────────────────────
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="glass-card">
  <div class="card-header">
    <div class="card-icon">&#128188;</div>
    <div>
      <p class="card-title">Detailed Portfolio PDF</p>
      <p class="card-subtitle">AI-generated detailed portfolio with comprehensive project descriptions</p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

if not student_data:
    st.info("💡 Save your details first.")
else:
    st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
    if st.button("🎨 Generate Portfolio PDF", use_container_width=True):
        with st.spinner("AI is creating detailed portfolio content…"):
            # Generate text-only portfolio (no image placeholders)
            portfolio_content = generate_portfolio_content(student_data, role, include_images=False)
            st.session_state["portfolio_content"] = portfolio_content
        
        with st.spinner("Building portfolio PDF…"):
            # Generate PDF without image placeholders
            st.session_state["portfolio_pdf_path"] = generate_portfolio_pdf(
                portfolio_content,
                student_data["name"],
                include_image_placeholders=False
            )
        
        st.success("✅ Portfolio PDF generated!")
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state["portfolio_pdf_path"] and os.path.exists(st.session_state["portfolio_pdf_path"]):
    st.markdown('<div class="btn-download">', unsafe_allow_html=True)
    with open(st.session_state["portfolio_pdf_path"], "rb") as f:
        st.download_button(
            label="⬇️ Download Portfolio PDF",
            data=f,
            file_name="portfolio.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show preview of portfolio content
    if st.session_state["portfolio_content"]:
        with st.expander("📄 Preview Portfolio Content"):
            st.text(st.session_state["portfolio_content"][:2000] + "..." if len(st.session_state["portfolio_content"]) > 2000 else st.session_state["portfolio_content"])

# ── Footer ────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #718096; font-size: 0.9rem; padding: 1rem;">
    <p>Built with ❤️ using Streamlit and Google Gemini AI</p>
    <p style="font-size: 0.8rem; margin-top: 0.5rem;">
        Resume: One-page ATS optimized | Portfolio: Detailed multi-page showcase
    </p>
</div>
""", unsafe_allow_html=True)