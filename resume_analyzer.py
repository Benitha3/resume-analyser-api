import re
import requests
import fitz  # PyMuPDF for PDF text extraction

# Predefined skills (example – you can edit this list)
SKILLS = [
    "Python", "Java", "C++", "SQL", "Machine Learning",
    "Deep Learning", "NLP", "Data Analysis", "Excel",
    "Communication", "Leadership", "Teamwork", "Problem Solving"
]

def download_resume(resume_url):
    try:
        # Handle Google Drive link
        if "drive.google.com" in resume_url:
            if "id=" in resume_url:
                file_id = resume_url.split("id=")[1]
            elif "/d/" in resume_url:
                file_id = resume_url.split("/d/")[1].split("/")[0]
            else:
                return None

            resume_url = f"https://drive.google.com/uc?export=download&id={file_id}"

        response = requests.get(resume_url, stream=True)
        if response.status_code == 200:
            with open("resume.pdf", "wb") as f:
                f.write(response.content)
            return "resume.pdf"
        return None
    except Exception as e:
        print(f"❌ Error downloading resume: {e}")
        return None

def extract_text_from_pdf(file_path):
    """Extract all text from a PDF."""
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print("❌ Error extracting text:", e)
        return ""

def analyze_resume(resume_url):
    """Analyze resume for matching skills."""
    # Step 1: Download resume
    pdf_file = download_resume(resume_url)
    if not pdf_file:
        return "Rejected"

    # Step 2: Extract text
    text = extract_text_from_pdf(pdf_file).lower()

    # Step 3: Match skills
    found_skills = [skill for skill in SKILLS if skill.lower() in text]
    score = len(found_skills)

    # Step 4: Decide selection
    if score >= 5:   # adjust threshold
        return "Selected"
    elif score >= 3:
        return "Waiting"
    else:
        return "Rejected"
