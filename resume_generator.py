"""
AI-powered resume content generation using Google Gemini.

Compatible with google-genai >= 0.3.0
Fixes: Ensures complete generation, no truncation
"""

import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

_client = None
DEFAULT_MODEL = "gemini-2.5-flash"


def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set. Add it to .env file.")
        _client = genai.Client(api_key=api_key)
    return _client


def resume_summary_prompt(data: dict, role: str, job_description: str = None) -> str:
    jd_section = f"\nJob Description:\n{job_description}\n" if job_description else ""

    return f"""
You are an expert ATS resume writer.

Create a professional summary (2-3 sentences) for: {role}

Candidate:
Name: {data['name']}
Education: {data['education']}
Skills: {data['skills']}
Projects: {data['projects']}

RULES:
- Exactly 2-3 complete sentences
- Mention role: {role}
- Highlight key technical skills
- NO truncation or abbreviations
- Full sentences only

{jd_section}

Return the complete summary.
"""


def project_bullets_prompt(data: dict, role: str) -> str:
    return f"""
Generate ATS-optimized project descriptions for: {role}

PROJECT DATA:
{data['projects']}

SKILLS:
{data['skills']}

STRICT RULES:
- Format: Project Name | Technologies
- Then 1 bullets per project
- Each bullet ONE complete sentence
- Past tense action verbs
- NO truncation - write full sentences
- NO abbreviations like "This pro..." or "The trad..."

EXAMPLE:
E-commerce Platform | React, Node.js, MongoDB
- Built full-stack web application with secure payment integration serving 500+ users ,(summurise as per new trend)

Generate first 3 projects completely.
Return formatted text only.
"""


def full_resume_prompt(
    data: dict,
    role: str,
    summary: str,
    project_bullets: str,
    job_description: str = None
) -> str:
    # Build sections conditionally
    exp_section = ""
    if data.get('experience', '').strip():
        exp_section = f"""
PROFESSIONAL EXPERIENCE
{data['experience'].strip()}
"""

    cert_section = ""
    if data.get('certifications', '').strip():
        cert_section = f"""
CERTIFICATIONS
{data['certifications'].strip()}
"""

    ach_section = ""
    if data.get('achievements', '').strip():
        ach_section = f"""
ACHIEVEMENTS
{data['achievements'].strip()}
"""

    return f"""
Generate a COMPLETE one-page ATS resume for: {role}

CRITICAL RULES:
- Write ALL sections COMPLETELY - NO truncation
- NO abbreviations or "..." ellipsis
- Use full sentences
- Complete all sections before stopping
- Skip only if no data provided

CONTACT
{data['name']}
{data['email']} | {data.get('phone', '')} | {data.get('city', '')}
LinkedIn: {data.get('linkedin', '')}
GitHub: {data.get('github', '')}

PROFESSIONAL SUMMARY
{summary}

CORE SKILLS
Organize these skills by category (Languages, Frameworks, Tools, Databases, Concepts):
{data['skills']}

PROJECTS
{project_bullets}

{exp_section}

EDUCATION
{data['education']}

CERTIFICATIONS
{cert_section}

ACHIEVEMENTS
{ach_section}

FORMATTING:
- Section headers in ALL CAPS
- Bullets start with •
- One line per bullet
- Be concise but COMPLETE

Generate the FULL resume. Do NOT stop early.
Return formatted text only.
"""


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
            temperature=0.3,
            max_output_tokens=400,
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
            temperature=0.3,
            max_output_tokens=1500,
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
            temperature=0.2,  # Very stable
            max_output_tokens=4000,  # Increased for complete generation
            stop_sequences=None,  # Don't stop early
        ),
    )
    
    result = response.text.strip()
    
    # Validation: Check if resume seems complete
    required_sections = ["CONTACT", "PROFESSIONAL SUMMARY", "CORE SKILLS", "PROJECTS", "EDUCATION"]
    missing = [s for s in required_sections if s not in result.upper()]
    
    if missing:
        print(f"Warning: Resume may be incomplete. Missing sections: {missing}")
    
    return result