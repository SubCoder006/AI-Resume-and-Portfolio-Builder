"""
AI-powered resume content generation using Google Gemini.

Compatible with google-genai >= 0.3.0
Uses correct model names that are actually available.

Functions (DO NOT RENAME):
  - generate_resume_summary
  - generate_project_bullets
  - generate_full_resume
"""

import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# -------------------------------------------------------------------
# Singleton client
# -------------------------------------------------------------------
_client = None

AVAILABLE_MODELS = [
    "gemini-2.5-flash"
]

DEFAULT_MODEL = "gemini-2.5-flash"


def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set. Add it to .env file.")
        _client = genai.Client(api_key=api_key)
    return _client


# -------------------------------------------------------------------
# PROMPTS
# -------------------------------------------------------------------

def resume_summary_prompt(data: dict, role: str, job_description: str = None) -> str:
    jd_section = f"\nJob Description:\n{job_description}\n" if job_description else ""

    return f"""
You are a senior recruiter and ATS optimization expert.

TASK: Write a PROFESSIONAL SUMMARY.

STRICT RULES:
- Exactly 1-2 sentences
- No bullet points
- No emojis or symbols
- ATS-safe language
- Professional and concise
- Role-specific

Candidate Information:
Name: {data['name']}
Target Role: {role}
Key Skills: {data['skills']}
Projects: {data['projects']}
Experience: {data.get('experience', 'Entry-level / student')}

{jd_section}

Return ONLY the summary text.
"""


def project_bullets_prompt(data: dict, role: str) -> str:
    return f"""
You are a senior technical recruiter.

TASK: Generate ATS-optimized PROJECT DESCRIPTIONS.

STRICT RULES:
- Plain text only
- Past tense action verbs
- 1-2 bullets per project
- No emojis
- No special symbols except "-"
- Concise, impact-focused

REQUIRED FORMAT (EXACT):

Project Name | Technologies Used
- Bullet point
- Bullet point

PROJECT DATA:
{data['projects']}

SKILLS:
{data['skills']}

TARGET ROLE:
{role}

Return ONLY the formatted project section.
"""


def full_resume_prompt(
    data: dict,
    role: str,
    summary: str,
    project_bullets: str,
    job_description: str = None
) -> str:
    return f"""
You are a senior recruiter generating a COMPLETE, PROFESSIONAL, ATS-OPTIMIZED resume.

ABSOLUTE RULES (MANDATORY):
- DO NOT stop early
- DO NOT summarize
- DO NOT omit any section
- ALL section headers MUST appear
- Plain text only
- ATS compatible
- Professional resume tone
- Resume length: up to 3 pages

==================================================
HEADER
==================================================
{data['name']}
{data['email']} | {data.get('phone', '')} | {data.get('city', '')}
LinkedIn: {data.get('linkedin', '')}
GitHub: {data.get('github', '')}

==================================================
PROFESSIONAL SUMMARY
==================================================
{"Keep it exact to the point in 2-3 lines."}
{summary}

==================================================
CORE SKILLS
==================================================
Intelligently group the following skills by category:
- Programming Languages
- Frameworks & Libraries
- Tools & Platforms
- Other relevant categories

Use only the skills below:
{data['skills']}

==================================================
PROJECTS
==================================================
{"Explain each project in 1-2 lines, try to be precise in short."}
{project_bullets}

==================================================
PROFESSIONAL EXPERIENCE
==================================================
{"Use the experience provided below. And finish in 1-2 sentence. Try to summarise in 1 line if possible." if data.get("experience") else
"Convert the most relevant projects above into experience-style bullet points."}

{data.get("experience", "")}

==================================================
EDUCATION
==================================================
{data['education']}

==================================================
CERTIFICATIONS 
==================================================
{"One line each,don't over explain keep simple understandable."}
{data.get("certifications", "")}

==================================================
ACHIEVEMENTS
==================================================
{"One line each,don't over explain keep simple understandable."}
{data.get("achievements", "")}


FINAL INSTRUCTION:
End ONLY after the EDUCATION section.
Do NOT add explanations or notes.
"""


# -------------------------------------------------------------------
# GENERATORS (FUNCTION NAMES UNCHANGED)
# -------------------------------------------------------------------

def generate_resume_summary(
    data: dict,
    role: str,
    job_description: str = None,
    model: str = None
) -> str:
    client = _get_client()
    model = model or DEFAULT_MODEL

    response = client.models.generate_content(
        model=model,
        contents=resume_summary_prompt(data, role, job_description),
        config=types.GenerateContentConfig(
            temperature=0.35,
            max_output_tokens=300,
        ),
    )
    return response.text.strip()


def generate_project_bullets(
    data: dict,
    role: str,
    model: str = None
) -> str:
    client = _get_client()
    model = model or DEFAULT_MODEL

    response = client.models.generate_content(
        model=model,
        contents=project_bullets_prompt(data, role),
        config=types.GenerateContentConfig(
            temperature=0.35,
            max_output_tokens=1000,
        ),
    )
    return response.text.strip()


def generate_full_resume(
    data: dict,
    role: str,
    summary: str,
    project_bullets: str,
    job_description: str = None,
    model: str = None
) -> str:
    client = _get_client()
    model = model or DEFAULT_MODEL

    response = client.models.generate_content(
        model=model,
        contents=full_resume_prompt(
            data,
            role,
            summary,
            project_bullets,
            job_description,
        ),
        config=types.GenerateContentConfig(
            temperature=0.25,  # very stable formatting
            max_output_tokens=3500,
        ),
    )
    return response.text.strip()