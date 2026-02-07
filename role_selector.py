import streamlit as st


PREDEFINED_ROLES = [
    "AI / ML Engineer",
    "Data Scientist",
    "Software Engineer",
    "Web Developer",
    "Frontend Developer",
    "Backend Developer",
    "DevOps / Cloud Engineer",
    "Cybersecurity Analyst",
    "UI / UX Designer",
    "Other",
]


def role_selector() -> str:
    """
    Renders the target-role card.
    Returns the selected role string (or custom text when "Other").
    """
    st.markdown("""
    <div class="glass-card">
      <div class="card-header">
        <div class="card-icon">&#127919;</div>
        <div>
          <p class="card-title">Target Job Role</p>
          <p class="card-subtitle">Pick the role that matches your application</p>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    role = st.selectbox(
        "Role",
        PREDEFINED_ROLES,
        label_visibility="hidden",
    )

    if role == "Other":
        custom = st.text_input(
            "Custom Role",
            placeholder="e.g. Embedded Systems Engineer",
            key="custom_role_input",
            label_visibility="hidden",
        )
        role = custom.strip() if custom.strip() else "Other"

    return role