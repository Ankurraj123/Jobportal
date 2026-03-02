import io
import re
from pdfminer.high_level import extract_text

def parse_resume(file_path):
    """
    Extracts text from a PDF resume and attempts to identify key sections.
    """
    try:
        text = extract_text(file_path)
        
        # Basic parsing logic (very simplified)
        # In a real app, you'd use more sophisticated NLP
        
        skills_keywords = ['python', 'django', 'react', 'javascript', 'sql', 'java', 'c++', 'aws', 'docker', 'machine learning']
        found_skills = [skill for skill in skills_keywords if skill.lower() in text.lower()]
        
        education_match = re.search(r'(Education|Degree|University|College|B\.?Tech|BS|MS)([\s\S]*?)(Experience|Skills|Projects|Objective)', text, re.IGNORECASE)
        education = education_match.group(2).strip() if education_match else "Not identified"
        
        experience_match = re.search(r'(Experience|Employment|Work History|Career)([\s\S]*?)(Education|Skills|Projects|Reference)', text, re.IGNORECASE)
        experience = experience_match.group(2).strip() if experience_match else "Not identified"
        
        return {
            'bio': text[:200] + "...", # First 200 chars as bio
            'skills': ", ".join(found_skills),
            'education': education[:500],
            'experience': experience[:1000]
        }
    except Exception as e:
        print(f"Error parsing resume: {e}")
        return None
