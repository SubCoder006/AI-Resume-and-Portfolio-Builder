"""
Optimized prompt templates for:
1. One-page ATS resume (concise, no descriptions)
2. Detailed portfolio PDF (elaborated, with image placeholders)
"""


def resume_summary_prompt(data: dict, role: str) -> str:
    """Generate a 2-3 line professional summary for resume."""
    return f"""You are an expert ATS resume writer.

Create a CONCISE professional summary (2-3 lines ONLY) for: {role}

Candidate:
- Name: {data['name']}
- Education: {data['education']}
- Key Skills: {data['skills']}
- Projects: {data['projects']}

RULES:
- 2-3 sentences maximum
- Mention target role: {role}
- Highlight 3-4 key technical skills
- No bullet points
- No emojis or special characters
- ATS-safe plain text

Return ONLY the summary."""


def project_bullets_prompt(data: dict, role: str) -> str:
    """Generate CONCISE project bullets for one-page resume."""
    return f"""You are an ATS resume expert.

Generate CONCISE project descriptions for ONE-PAGE resume targeting: {role}

Projects: {data['projects']}
Skills: {data['skills']}

STRICT RULES:
- Each project: Title | Tech Stack
- 2 bullet points maximum per project
- Each bullet: ONE line only
- Start with action verb (past tense)
- Focus on impact, not process
- No emojis, plain text only

FORMAT:
Project Name | Python, React, AWS
- Built X resulting in Y outcome
- Implemented Z feature with ABC impact

Return formatted projects ONLY."""


def full_resume_prompt(data: dict, role: str, summary: str, project_bullets: str) -> str:
    """Generate complete ONE-PAGE resume."""
    return f"""You are an expert ATS resume writer.

Create a STRICTLY ONE-PAGE resume for: {role}

CRITICAL RULES:
- ONE PAGE ONLY - be extremely concise
- Plain text, ATS-safe format
- No descriptions or explanations
- Bullet points must be single line
- No emojis, icons, or special characters

REQUIRED SECTIONS:

1. CONTACT (single line format)
{data['name']} | {data['email']} | {data.get('phone', '')} | {data.get('city', '')}
LinkedIn: {data.get('linkedin', '')} | GitHub: {data.get('github', '')}

2. PROFESSIONAL SUMMARY
{summary}

3. TECHNICAL SKILLS (categorized, comma-separated)
{data['skills']}

4. PROJECTS
{project_bullets}

5. EXPERIENCE (if provided, max 2 bullets per role)
{data.get('experience', 'SKIP if empty')}

6. EDUCATION (one line per degree)
{data['education']}

7. CERTIFICATIONS (if provided, one line each)
{data.get('certifications', 'SKIP if empty')}

8. ACHIEVEMENTS (if provided, max 3 bullets)
{data.get('achievements', 'SKIP if empty')}

STRICT FORMATTING:
- Section headers: ALL CAPS or Bold
- Bullets: single line, action verb + impact
- NO paragraphs except summary
- Skip empty sections
- Prioritize space efficiency

Return complete resume ONLY."""


def portfolio_content_prompt(data: dict, role: str, include_image_suggestions: bool = False) -> str:
    """Generate DETAILED portfolio content for PDF."""
    image_instruction = ""
    if include_image_suggestions:
        image_instruction = "\n- After each project, suggest what images would showcase it (using [Image: description] format)"
    
    return f"""You are a portfolio content specialist.

Create DETAILED portfolio content for: {data['name']} (targeting {role})

This is for a PORTFOLIO PDF (multi-page allowed), NOT a resume.
Be descriptive, elaborate, and showcase depth of work.{image_instruction}

CANDIDATE DATA:
Name: {data['name']}
Email: {data['email']}
Phone: {data.get('phone', '')}
Location: {data.get('city', '')}
LinkedIn: {data.get('linkedin', '')}
GitHub: {data.get('github', '')}

Education: {data['education']}
Skills: {data['skills']}
Projects: {data['projects']}
Experience: {data.get('experience', '')}
Certifications: {data.get('certifications', '')}
Achievements: {data.get('achievements', '')}

REQUIRED SECTIONS (in order):

1. ABOUT ME
Write a professional introduction (3-4 paragraphs):
- Background and education
- Technical interests and expertise areas
- Career goals and aspirations for {role}
- What makes them unique

2. TECHNICAL EXPERTISE
Organize skills into detailed categories:
- Programming Languages (with proficiency context)
- Frameworks & Libraries (mention use cases)
- Tools & Platforms (describe experience)
- Core Concepts & Methodologies

3. PROJECT SHOWCASE (DETAILED)
For EACH project:

Project Title
Technologies Used: [list all]

Problem Statement:
[Describe the problem or need this project addresses - 2-3 sentences]

Solution Approach:
[Explain the technical approach and architecture - 3-4 sentences]

Key Features:
- [Feature 1 with technical details]
- [Feature 2 with technical details]
- [Feature 3 with technical details]

Implementation Highlights:
- [Technical challenge solved]
- [Interesting algorithm or design pattern used]
- [Performance optimization or scalability consideration]

Outcomes & Learnings:
[Results, impact, what was learned - 2-3 sentences]

---

4. PROFESSIONAL EXPERIENCE (if provided)
For each role:
- Position Title | Organization | Duration
- Overview (2-3 sentences about role and responsibilities)
- Key Achievements:
  • [Achievement with metrics]
  • [Technical contribution]
  • [Impact on team/product]
- Technologies & Tools Used: [list]

5. EDUCATION & ACADEMIC BACKGROUND
- Degree details with CGPA
- Relevant coursework
- Academic projects or research
- Honors or distinctions

6. CERTIFICATIONS & CONTINUOUS LEARNING
For each certification:
- Certification Name | Issuing Organization | Year
- Brief description of what it covers
- Why it's relevant to {role}

7. ACHIEVEMENTS & RECOGNITION
List with context:
- Awards (what, when, why significant)
- Hackathons (problem solved, rank, team size)
- Leadership roles (organization, responsibilities, impact)
- Publications or talks (title, venue, topic)

8. CONTACT & LINKS
Professional contact information with all links

FORMATTING RULES:
- Use clear section headers (ALL CAPS)
- Use subsection headers (Title Case with colon)
- Write in professional but engaging tone
- Be descriptive and detailed
- Use bullet points for lists
- Use paragraphs for explanations

IMPORTANT:
- This is NOT a resume - be detailed and elaborate
- Explain HOW things were built, not just WHAT
- Include technical depth
- Show problem-solving process
- Demonstrate learning and growth
- Do NOT include image placeholders or references

Return complete portfolio content formatted as described."""


def project_image_suggestions_prompt(project_data: str) -> str:
    """Generate AI suggestions for project images/screenshots."""
    return f"""You are a technical portfolio advisor.

For the following project, suggest what images/screenshots would best showcase the work:

PROJECT:
{project_data}

Provide 2-3 specific image suggestions in this format:

[Screenshot Suggestion 1: Description]
Example: [Main Dashboard - showing data visualization with charts and metrics]

[Screenshot Suggestion 2: Description]
Example: [Architecture Diagram - system components and data flow]

[Screenshot Suggestion 3: Description]
Example: [Mobile Responsive View - application on different screen sizes]

Focus on:
- What would visually demonstrate the project's key features
- Technical architecture or design patterns
- User interface or user experience highlights
- Results or output visualization

Return ONLY the image placeholder suggestions."""