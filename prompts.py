"""
Optimized prompt templates - ALL SECTIONS MANDATORY
All sections will be generated even if data is empty
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
- 2 sentences maximum
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
    """Generate complete ONE-PAGE resume with ALL SECTIONS MANDATORY."""
    
    return f"""You are an expert ATS resume writer.

Create a STRICTLY ONE-PAGE resume for: {role}

CRITICAL RULES:
- ONE PAGE ONLY - be extremely concise
- Plain text, ATS-safe format
- ALL SECTIONS ARE MANDATORY - include every section below
- If no data provided for a section, write "Not provided" or skip gracefully
- Bullet points must be single line
- No emojis, icons, or special characters
- COMPLETE ALL SECTIONS - no truncation

REQUIRED SECTIONS (ALL MANDATORY):

1. CONTACT (single line format)
{data['name']} | {data['email']} | {data.get('phone', 'Not provided')} | {data.get('city', 'Not provided')}
LinkedIn: {data.get('linkedin', 'Not provided')} | GitHub: {data.get('github', 'Not provided')}

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

5. PROFESSIONAL EXPERIENCE (MANDATORY - include this section)
{data.get('experience', 'Currently seeking professional opportunities')}

If no experience provided, write:
"Seeking entry-level opportunities to apply technical skills in a professional environment"

6. EDUCATION (MANDATORY)
{data['education']}

7. CERTIFICATIONS (MANDATORY - include this section)
{data.get('certifications', 'Currently pursuing relevant certifications')}

If no certifications, write:
"Actively pursuing industry-recognized certifications in [relevant field based on role]"

8. ACHIEVEMENTS (MANDATORY - include this section)
{data.get('achievements', 'Academic projects and personal development initiatives')}

If no achievements, write:
"Strong academic performance and continuous learning through online courses and personal projects"

STRICT FORMATTING:
- Section headers: ALL CAPS
- ALL 8 sections MUST appear in resume
- Use "Not provided" or placeholder text if data is missing
- Bullets: single line, action verb + impact
- NO paragraphs except summary
- NEVER skip any section
- Prioritize space efficiency

MANDATORY: Generate ALL 8 sections. Return formatted text ONLY."""


def portfolio_content_prompt(data: dict, role: str) -> str:
    """Generate DETAILED portfolio with ALL SECTIONS MANDATORY."""
    
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
- ALL SECTIONS ARE MANDATORY - include every section below
- If no data provided, create placeholder content
- Complete ALL sections before stopping
- PURE TEXT ONLY - NO image references or placeholders

CANDIDATE DATA:
Name: {data['name']}
Email: {data['email']}
Phone: {data.get('phone', 'Available upon request')}
Location: {data.get('city', 'Location flexible')}
LinkedIn: {data.get('linkedin', 'Available upon request')}
GitHub: {data.get('github', 'Available upon request')}

Education: {data['education']}
Skills: {data['skills']}
Projects: {data['projects']}
Experience: {data.get('experience', 'None provided')}
Certifications: {data.get('certifications', 'None provided')}
Achievements: {data.get('achievements', 'None provided')}

REQUIRED SECTIONS (ALL MANDATORY - NEVER SKIP ANY):

1. ABOUT ME (MANDATORY)
Write a professional introduction (4-5 complete paragraphs):
- Background and education (full paragraph)
- Technical interests and expertise areas (full paragraph)
- Career goals and aspirations for {role} (full paragraph)
- What makes them unique (full paragraph)
- Specific skills and technologies mastered (full paragraph)

IMPORTANT: Write COMPLETE paragraphs. Do NOT use abbreviations.

2. TECHNICAL EXPERTISE (MANDATORY)
Organize skills into detailed categories with explanations:
- Programming Languages (explain proficiency and use cases)
- Frameworks & Libraries (describe experience with each)
- Tools & Platforms (detail what you've built with them)
- Databases (mention projects using each)
- Core Concepts & Methodologies (explain understanding)

3. PROJECT SHOWCASE (MANDATORY)
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

4. PROFESSIONAL EXPERIENCE (MANDATORY - ALWAYS INCLUDE)
If experience provided:
For each role:
- Position Title | Organization | Duration
- Overview (1-2 COMPLETE sentences about role)
- Key Achievements:
  • [Achievement 1 with metrics - COMPLETE sentence]
  • [Achievement 2 - technical contribution - COMPLETE]
  • [Achievement 3 - impact - COMPLETE sentence]
- Technologies & Tools Used: [comprehensive list]

If NO experience provided, write:
"Currently seeking professional opportunities to apply technical expertise in {role}. 
Prepared to contribute strong foundation in [list key skills] to a dynamic team environment.
Eager to leverage academic projects and self-directed learning in a professional setting."

5. EDUCATION & ACADEMIC BACKGROUND (MANDATORY)
- Degree details with CGPA (full information)
- Relevant coursework (if applicable)
- Academic projects or research (if any)
- Honors or distinctions (if any)

6. CERTIFICATIONS & CONTINUOUS LEARNING (MANDATORY - ALWAYS INCLUDE)
If certifications provided:
For each certification:
- Certification Name | Issuing Organization | Year
- Brief description (1-2 sentences)

If NO certifications provided, write:
"Actively pursuing industry-recognized certifications in {role} domain.
Committed to continuous professional development through online learning platforms
including Coursera, Udemy, and specialized technical training programs."

7. ACHIEVEMENTS & RECOGNITION (MANDATORY - ALWAYS INCLUDE)
If achievements provided:
List with context:
- Awards (what, when, why significant - COMPLETE sentences)
- Hackathons (problem solved, rank, team size - FULL details)
- Leadership roles (organization, responsibilities, impact - COMPLETE)
- Publications or talks (title, venue, topic - FULL information)

If NO achievements provided, write:
"Strong academic performance with consistent dedication to technical skill development.
Active participant in online coding communities and open-source contribution initiatives.
Demonstrated problem-solving abilities through personal projects and academic coursework."

8. CONTACT & LINKS (MANDATORY)
Professional contact information with all available links

FORMATTING RULES:
- Use clear section headers (ALL CAPS)
- Use subsection headers (Title Case with colon)
- Write in professional but engaging tone
- Be descriptive and detailed
- Use bullet points for lists
- Use COMPLETE paragraphs for explanations
- NO abbreviations or incomplete words
- PURE TEXT - NO image placeholders or references
- ALL 8 SECTIONS MUST BE PRESENT

FINAL VALIDATION:
Before finishing, check that:
- ALL 8 sections are present
- All sentences are COMPLETE
- No truncated words or phrases
- No "..." ellipsis
- All sections are FULLY written
- Everything is explained in FULL
- NO image references
- Placeholder content used if data is missing

MANDATORY: Include ALL sections. Return complete portfolio content."""