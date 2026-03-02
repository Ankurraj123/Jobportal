"""
cv_parser.py — Extracts structured sections from a PDF CV using pdfplumber.
Returns a dict with: skills, education, experience, projects, certificates, training, achievements, links
"""
import re
import pdfplumber

# Section heading keywords to detect
SECTION_HEADERS = {
    'skills':        ['skill', 'technical skill', 'core competenc'],
    'education':     ['education', 'academic'],
    'experience':    ['experience', 'work experience', 'employment', 'internship'],
    'projects':      ['project'],
    'certificates':  ['certificate', 'certification'],
    'training':      ['training', 'course'],
    'achievements':  ['achievement', 'award', 'accomplishment'],
    'links':         ['link', 'contact', 'social'],
}


def _detect_section(line: str):
    """Return section key if line looks like a section heading, else None."""
    clean = line.strip().lower().rstrip(':')
    if len(clean) > 40:        # headings are short
        return None
    for key, keywords in SECTION_HEADERS.items():
        for kw in keywords:
            if kw in clean:
                return key
    return None


def _extract_links(text: str) -> dict:
    links = {}
    linkedin = re.search(r'linkedin\.com/in/[\w\-]+', text, re.I)
    github   = re.search(r'github\.com/[\w\-]+', text, re.I)
    email    = re.search(r'[\w.\-]+@[\w.\-]+\.[a-z]{2,}', text, re.I)
    phone    = re.search(r'[+\d][\d\s\-]{8,14}', text)
    if linkedin:  links['linkedin'] = 'https://' + linkedin.group()
    if github:    links['github']   = 'https://' + github.group()
    if email:     links['email']    = email.group()
    if phone:     links['phone']    = phone.group().strip()
    return links


def _clean_lines(lines):
    """Remove empty lines and strip whitespace."""
    return [l.strip() for l in lines if l.strip()]


def _parse_skill_categories(lines):
    """Try to detect sub-categories like Languages:, Frontend:, etc."""
    categories = {}
    current_cat = 'General'
    for line in lines:
        # e.g. "Languages : C++, Java, Python"
        m = re.match(r'^([\w\s/]+?)\s*[:\-]\s*(.+)$', line)
        if m and len(m.group(1)) < 30:
            cat = m.group(1).strip()
            vals = [v.strip() for v in re.split(r'[,;]', m.group(2)) if v.strip()]
            categories[cat] = vals
        else:
            items = [v.strip() for v in re.split(r'[,;]', line) if v.strip()]
            categories.setdefault(current_cat, []).extend(items)
    return categories


def _parse_projects(lines):
    """Parse project blocks. A project starts with a bold / title-like line."""
    projects = []
    current = None
    for line in lines:
        # New project: short line, not a bullet, possibly has a date
        if not line.startswith(('•', '-', '*', '–')) and len(line) < 100 and re.search(r'[A-Z]', line):
            if current:
                projects.append(current)
            current = {'title': line, 'description': [], 'tech': ''}
        elif current:
            if re.search(r'\btech\b|\bstack\b|\bbuilt with\b', line, re.I):
                current['tech'] = line
            else:
                current['description'].append(line.lstrip('•-– '))
    if current:
        projects.append(current)
    # Clean description lists
    for p in projects:
        p['description'] = ' '.join(p['description'])
    return projects


def _parse_education(lines):
    """Parse education entries."""
    entries = []
    current = {}
    for line in lines:
        # degree lines tend to be longer
        if re.search(r'\b(bachelor|master|b\.?tech|m\.?tech|b\.?sc|m\.?sc|phd|diploma|12th|10th|matric|inter)\b', line, re.I):
            if current:
                entries.append(current)
            current = {'degree': line, 'institution': '', 'detail': ''}
        elif current and not current['institution']:
            current['institution'] = line
        elif current:
            current['detail'] += ' ' + line
    if current:
        entries.append(current)
    for e in entries:
        e['detail'] = e['detail'].strip()
    return entries


def _parse_simple_list(lines):
    """Parse a section as a simple list of text items."""
    return [l.lstrip('•-– ').strip() for l in lines if l.lstrip('•-– ').strip()]


def parse_cv(file_path: str) -> dict:
    """
    Main function. Accepts a path to a PDF file.
    Returns a dict with structured CV data.
    """
    full_text = ''
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    full_text += t + '\n'
    except Exception as e:
        return {'error': str(e)}

    if not full_text.strip():
        return {'error': 'Could not extract text from PDF'}

    # --- Split into sections ---
    section_data = {k: [] for k in SECTION_HEADERS}
    current_section = None

    for line in full_text.splitlines():
        detected = _detect_section(line)
        if detected:
            current_section = detected
            continue
        if current_section:
            section_data[current_section].append(line)

    # --- Parse each section ---
    result = {}

    # Skills → comma-separated string for the existing `skills` field
    skill_lines = _clean_lines(section_data['skills'])
    if skill_lines:
        cats = _parse_skill_categories(skill_lines)
        # Flatten all skill values to a comma-sep string for the text field
        all_skills = []
        for vals in cats.values():
            all_skills.extend(vals)
        result['skills'] = ', '.join(all_skills)
        result['skills_categories'] = cats  # bonus structured data
    else:
        result['skills'] = ''
        result['skills_categories'] = {}

    # Education
    edu_lines = _clean_lines(section_data['education'])
    result['education'] = '\n'.join(edu_lines)
    result['cv_education'] = _parse_education(edu_lines)

    # Experience
    exp_lines = _clean_lines(section_data['experience'])
    result['experience'] = '\n'.join(exp_lines)

    # Projects
    result['cv_projects'] = _parse_projects(_clean_lines(section_data['projects']))

    # Certificates
    result['cv_certificates'] = _parse_simple_list(_clean_lines(section_data['certificates']))

    # Training
    result['cv_training'] = _parse_simple_list(_clean_lines(section_data['training']))

    # Achievements
    result['cv_achievements'] = _parse_simple_list(_clean_lines(section_data['achievements']))

    # Links — scan full text
    result['cv_links'] = _extract_links(full_text)

    return result
