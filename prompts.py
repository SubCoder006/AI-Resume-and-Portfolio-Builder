"""
Optimized prompt templates - FIXED for clean PDF output
Prevents formatting issues that cause text to split awkwardly
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
    """Generate DETAILED portfolio - FIXED formatting to prevent text splits."""
    
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
- Complete ALL sections before stopping
- PURE TEXT ONLY - NO image references

FORMATTING RULES (CRITICAL FOR PDF):
- ALWAYS write "Technologies Used:" on SAME LINE as the technologies list
- NEVER put subsection headers on separate line from their content
- Keep section titles together with their descriptions
- No orphaned headers

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

REQUIRED SECTIONS (ALL MANDATORY):

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

CRITICAL FORMAT for each project (MUST FOLLOW EXACTLY):

Project Title: [Full project name]
Technologies Used: [Python, OpenCV, Flask, MongoDB - list ALL on SAME line]

Problem Statement:
[Write 3-4 COMPLETE sentences describing the problem. Start immediately after colon.]

Solution Approach:
[Write 4-5 COMPLETE sentences explaining the technical approach. Start immediately.]

Key Features:
- [Feature 1 - COMPLETE description with technical details]
- [Feature 2 - COMPLETE description with technical details]
- [Feature 3 - COMPLETE description with technical details]

Implementation Highlights:
- [Technical challenge solved - FULL sentence]
- [Algorithm or design pattern - FULL explanation]
- [Performance optimization - COMPLETE description]

Outcomes & Learnings:
[Write 3-4 COMPLETE sentences about results, impact, and learning. NO truncation.]

---

REPEAT above format for EACH project.

4. PROFESSIONAL EXPERIENCE (MANDATORY)

CRITICAL FORMAT for each role (MUST FOLLOW EXACTLY):

Position Title | Organization | Duration

[Write complete overview paragraph immediately. Do NOT put "Overview:" label. Write 2-3 COMPLETE sentences describing the role, responsibilities, and context. Start the paragraph directly without any header.]

Key Achievements:
• [Achievement 1 with metrics - COMPLETE sentence]
• [Achievement 2 - technical contribution - COMPLETE sentence]
• [Achievement 3 - impact - COMPLETE sentence]

Technologies & Tools Used: [Python, TensorFlow, Docker, AWS - list ALL on same line]

---

REPEAT for each role.

If NO experience provided, write:
"Currently seeking professional opportunities to apply technical expertise in {role}. Prepared to contribute strong foundation in [list key skills] to a dynamic team environment. Eager to leverage academic projects and self-directed learning in a professional setting."

5. EDUCATION & ACADEMIC BACKGROUND (MANDATORY)

Degree Name
Institution Name | Years | CGPA

[If relevant coursework exists, list it. Otherwise skip.]

[If academic projects exist, describe them. Otherwise skip.]

[If honors exist, list them. Otherwise skip.]

6. CERTIFICATIONS & CONTINUOUS LEARNING (MANDATORY)

For each certification (CRITICAL FORMAT):
Certification Name | Issuing Organization | Year
[Write 1-2 COMPLETE sentences describing what it covers and relevance. Start immediately.]

If NO certifications provided, write:
"Actively pursuing industry-recognized certifications in {role} domain. Committed to continuous professional development through online learning platforms including Coursera, Udemy, and specialized technical training programs."

7. ACHIEVEMENTS & RECOGNITION (MANDATORY)

For each achievement (CRITICAL FORMAT):
Achievement Title:
[Write 2-3 COMPLETE sentences describing what, when, why significant, team size, impact. Start immediately after colon.]

If NO achievements provided, write:
"Strong academic performance with consistent dedication to technical skill development. Active participant in online coding communities and open-source contribution initiatives. Demonstrated problem-solving abilities through personal projects and academic coursework."

8. CONTACT & LINKS (MANDATORY)

CRITICAL FORMAT (everything on separate lines):
Name: {data['name']}
Email: {data['email']}
Phone: {data.get('phone', 'Available upon request')}
Location: {data.get('city', 'Location flexible')}
LinkedIn: {data.get('linkedin', 'Available upon request')}
GitHub: {data.get('github', 'Available upon request')}

FINAL VALIDATION CHECKLIST:
Before finishing, verify:
- ALL 8 sections are present
- "Technologies Used:" is on SAME LINE as technology list
- Overview paragraphs start immediately after role title
- No orphaned headers or labels
- All sentences are COMPLETE
- No truncated words or phrases
- No "..." ellipsis
- Everything is explained in FULL
- Contact information is COMPLETE on separate lines

MANDATORY: Include ALL sections with proper formatting. Return complete portfolio content."""