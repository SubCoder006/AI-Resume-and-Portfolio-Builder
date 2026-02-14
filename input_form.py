import streamlit as st
from typing import Optional

_SESSION_KEYS = (
    "name", "phone", "email", "city", "linkedin", "github",
    "education", "skills", "projects", "experience", 
    "certifications", "achievements"
)


def _load_defaults() -> dict:
    return {k: st.session_state.get(f"form_{k}", "") for k in _SESSION_KEYS}


def student_input_form() -> Optional[dict]:
    """
    Renders the comprehensive student-details form with all ATS-required fields.
    Returns the data dict once saved; None before that.
    """
    defaults = _load_defaults()

    st.markdown("""
    <div class="glass-card">
      <div class="card-header">
        <div class="card-icon">&#128104;</div>
        <div>
          <p class="card-title">Student Details</p>
          <p class="card-subtitle">Complete all sections for ATS-optimized resume</p>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("student_form", border=False):
        # ── CONTACT INFORMATION ───────────────────────────────────────
        st.markdown("**Contact Information**")
        col1, col2 = st.columns(2, gap="medium")
        with col1:
            name = st.text_input(
                "Full Name *",
                value=defaults["name"],
                placeholder="e.g. John Doe",
            )
            email = st.text_input(
                "Email *",
                value=defaults["email"],
                placeholder="e.g. xyz@email.com",
            )
            linkedin = st.text_input(
                "LinkedIn URL",
                value=defaults["linkedin"],
                placeholder="https://linkedin.com/in/yourprofile",
            )
        with col2:
            phone = st.text_input(
                "Phone Number *",
                value=defaults["phone"],
                placeholder="e.g. +91 98765 43210",
            )
            city = st.text_input(
                "City, State, Country *",
                value=defaults["city"],
                placeholder="e.g. Durgapur, West Bengal, India",
            )
            github = st.text_input(
                "GitHub / Portfolio URL",
                value=defaults["github"],
                placeholder="https://github.com/yourusername",
            )

        st.markdown("---")

        # ── EDUCATION ─────────────────────────────────────────────────
        st.markdown("**Education**")
        education = st.text_area(
            "Education Details *",
            value=defaults["education"],
            placeholder=(
                "B.Tech in Computer Science Engineering\n"
                "College Name, Location | 2024-2028 | CGPA : 8.7/10 \n"
            ),
            height=90,
        )

        st.markdown("---")

        # ── TECHNICAL SKILLS ──────────────────────────────────────────
        st.markdown("**Technical Skills**")
        skills = st.text_area(
            "Skills (categorize if possible) *",
            value=defaults["skills"],
            placeholder=(
                "Programming Languages: Python, C++, JavaScript\n"
                "Frameworks: React, Django, TensorFlow\n"
                "Tools: Git, Docker, AWS"
            ),
            height=100,
        )

        st.markdown("---")

        # ── PROJECTS ──────────────────────────────────────────────────
        st.markdown("**Projects**")
        projects = st.text_area(
            "Projects (one per line) *",
            value=defaults["projects"],
            placeholder=(
                "Project Name | Tech Stack | Description\n"
                "Project A | Python, Flask | Developed a web app for XYZ\n"
                "Project B | React, Node.js | Created a real-time chat application"
            ),
            height=120,
        )

        st.markdown("---")

        # ── EXPERIENCE ─────────────────────────────────────
        st.markdown("**Experience**")
        experience = st.text_area(
            "Work Experience / Internships",
            value=defaults["experience"],
            placeholder=(
                "Software Engineering Intern | ABC Company | June 2023 – Aug 2026\n"
                "- Developed feature X using Y, resulting in Z outcome\n"
                "Research Assistant | NIT Durgapur | Jan 2023 – May 2025\n"
            ),
            height=100,
        )

        st.markdown("---")

        # ── CERTIFICATIONS ─────────────────────────────────
        st.markdown("**Certifications**")
        certifications = st.text_area(
            "Certifications",
            value=defaults["certifications"],
            placeholder=(
                "AWS Certified Solutions Architect | Amazon Web Services | 2026\n"
                "Machine Learning Specialization | Coursera | 2025"
            ),
            height=80,
        )

        st.markdown("---")

        # ── ACHIEVEMENTS ───────────────────────────────────
        st.markdown("**Achievements / Responsibilities**")
        achievements = st.text_area(
            "Achievements, Awards, Leadership",
            value=defaults["achievements"],
            placeholder=(
                "1st Place - Smart India Hackathon 2023\n"
                "Technical Lead - College Coding Club (2025–2026)\n"
                "Published research paper in IEEE conference"
            ),
            height=80,
        )

        # Submit button
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        submit = st.form_submit_button("💾  Save Details", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── persist on submit ─────────────────────────────────────────────
    if submit:
        for key, val in [
            ("name", name), ("phone", phone), ("email", email), ("city", city),
            ("linkedin", linkedin), ("github", github), ("education", education),
            ("skills", skills), ("projects", projects), ("experience", experience),
            ("certifications", certifications), ("achievements", achievements),
        ]:
            st.session_state[f"form_{key}"] = val
        st.session_state["form_saved"] = True
        st.success("✅  Details saved successfully!")

    if st.session_state.get("form_saved"):
        return {k: st.session_state[f"form_{k}"] for k in _SESSION_KEYS}
    return None