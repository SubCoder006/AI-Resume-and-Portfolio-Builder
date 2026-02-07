"""
Optimized prompt templates - FIXED VERSION
Prevents truncation and ensures complete generation
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
- COMPLETE sentences only - no truncation

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
- Each bullet: ONE complete sentence
- Start with action verb (past tense)
- Focus on impact, not process
- No emojis, plain text only
- NO truncation or abbreviations

FORMAT:
Project Name | Python, React, AWS
- Built X resulting in Y outcome
- Implemented Z feature with ABC impact

Generate ALL projects completely.
Return formatted projects ONLY."""


def full_resume_prompt(data: dict, role: str, summary: str, project_bullets: str) -> str:
    """Generate complete ONE-PAGE resume."""
    
    # Build conditional sections
    exp_section = ""
    if data.get('experience', '').strip():
        exp_section = f"""
5. EXPERIENCE
Format each role as:
Role | Organization | Duration
- Bullet 1
- Bullet 2

Experience data:
{data['experience']}
"""
    
    cert_section = ""
    if data.get('certifications', '').strip():
        cert_section = f"""
{6 if exp_section else 5}. CERTIFICATIONS (one line each)
{data['certifications']}
"""
    
    ach_section = ""
    if data.get('achievements', '').strip():
        ach_section = f"""
{7 if exp_section and cert_section else 6 if exp_section or cert_section else 5}. ACHIEVEMENTS (one line each)
{data['achievements']}
"""
    
    return f"""You are an expert ATS resume writer.

Create a STRICTLY ONE-PAGE resume for: {role}

CRITICAL RULES:
- ONE PAGE ONLY - be extremely concise
- Plain text, ATS-safe format
- No descriptions or explanations
- Bullet points must be single line
- No emojis, icons, or special characters
- COMPLETE ALL SECTIONS - no truncation
- NO abbreviations like "This proj..." or incomplete words

REQUIRED SECTIONS:

1. CONTACT (single line format)
{data['name']} | {data['email']} | {data.get('phone', '')} | {data.get('city', '')}
LinkedIn: {data.get('linkedin', '')} | GitHub: {data.get('github', '')}

2. PROFESSIONAL SUMMARY
{summary}

3. CORE SKILLS (categorized, comma-separated)
Organize these skills into categories:
- Programming Languages
- Frameworks & Libraries
- Tools & Platforms
- Databases
- Core Concepts

Skills: {data['skills']}

4. PROJECTS
{project_bullets}

{exp_section}

{4 if not exp_section else 6 if not cert_section and not ach_section else 6}. EDUCATION (one line per degree)
{data['education']}

{cert_section}

{ach_section}

STRICT FORMATTING:
- Section headers: ALL CAPS or Bold
- Bullets: single line, action verb + impact
- NO paragraphs except summary
- Skip sections only if no data
- Prioritize space efficiency
- COMPLETE all sections

Generate the COMPLETE resume. Return formatted text ONLY."""


def portfolio_content_prompt(data: dict, role: str, include_image_suggestions: bool = False) -> str:
    """Generate DETAILED portfolio content for PDF - FIXED to prevent truncation."""
    
    return f"""You are a portfolio content specialist.

Create DETAILED portfolio content for: {data['name']} (targeting {role})

This is for a PORTFOLIO PDF (multi-page allowed), NOT a resume.
Be descriptive, elaborate, and showcase depth of work.

CRITICAL INSTRUCTIONS:
- Write COMPLETE sentences and paragraphs
- NO truncation or abbreviations
- NO incomplete words like "trad" or "pro"  
- NO ellipsis (...)
- Write everything out FULLY
- Complete ALL sections before stopping

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
Write a professional introduction (4-5 complete paragraphs):
- Background and education (full paragraph)
- Technical interests and expertise areas (full paragraph)
- Career goals and aspirations for {role} (full paragraph)
- What makes them unique (full paragraph)
- Specific skills and technologies mastered (full paragraph)

IMPORTANT: Write COMPLETE paragraphs. Do NOT use abbreviations.

2. TECHNICAL EXPERTISE
Organize skills into detailed categories with explanations:
- Programming Languages (explain proficiency and use cases)
- Frameworks & Libraries (describe experience with each)
- Tools & Platforms (detail what you've built with them)
- Databases (mention projects using each)
- Core Concepts & Methodologies (explain understanding)

3. PROJECT SHOWCASE (DETAILED)
For EACH project, write COMPLETE sections:

Project Title
Technologies Used: [list all]

Problem Statement:
[Write 3-4 COMPLETE sentences describing the problem. NO truncation.]

Solution Approach:
[Write 4-5 COMPLETE sentences explaining the technical approach. Be specific.]

Key Features:
- [Feature 1 - COMPLETE description with technical details]
- [Feature 2 - COMPLETE description with technical details]
- [Feature 3 - COMPLETE description with technical details]
- [Feature 4 if applicable]

Implementation Highlights:
- [Technical challenge solved - FULL sentence]
- [Algorithm or design pattern - FULL explanation]
- [Performance optimization - COMPLETE description]
- [Scalability consideration - FULL details]

Outcomes & Learnings:
[Write 3-4 COMPLETE sentences about results, impact, and learning. NO truncation.]

---

4. PROFESSIONAL EXPERIENCE (if provided)
For each role:
- Position Title | Organization | Duration
- Overview (3-4 COMPLETE sentences about role)
- Key Achievements:
  • [Achievement 1 with metrics - COMPLETE sentence]
  • [Achievement 2 - technical contribution - COMPLETE]
  • [Achievement 3 - impact - COMPLETE sentence]
- Technologies & Tools Used: [comprehensive list]

5. EDUCATION & ACADEMIC BACKGROUND
- Degree details with CGPA (full information)
- Relevant coursework (if applicable)
- Academic projects or research (if any)
- Honors or distinctions (if any)

6. CERTIFICATIONS & CONTINUOUS LEARNING (if provided)
For each certification:
- Certification Name | Issuing Organization | Year
- Brief description of coverage (2-3 sentences)
- Relevance to {role} (1-2 sentences)

7. ACHIEVEMENTS & RECOGNITION (if provided)
List with context:
- Awards (what, when, why significant - COMPLETE sentences)
- Hackathons (problem solved, rank, team size - FULL details)
- Leadership roles (organization, responsibilities, impact - COMPLETE)
- Publications or talks (title, venue, topic - FULL information)

8. CONTACT & LINKS
Professional contact information with all links

FORMATTING RULES:
- Use clear section headers (ALL CAPS)
- Use subsection headers (Title Case with colon)
- Write in professional but engaging tone
- Be descriptive and detailed
- Use bullet points for lists
- Use COMPLETE paragraphs for explanations
- NO abbreviations or incomplete words

FINAL VALIDATION:
Before finishing, check that:
- All sentences are COMPLETE
- No truncated words or phrases
- No "..." ellipsis
- All sections are FULLY written
- Everything is explained in FULL

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