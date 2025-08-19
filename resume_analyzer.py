import re
import requests
import fitz  # PyMuPDF for PDF text extraction

# Predefined skills (customize as needed)
SKILLS = [
    "Python", "Java", "C++", "SQL", "Machine Learning",
    "Deep Learning", "NLP", "Data Analysis", "Excel",
    "Communication", "Leadership", "Teamwork", "Problem Solving"
]

def fix_google_drive_url(url: str) -> str:
    """Convert different Google Drive links into a direct download link."""
    if "drive.google.com" in url:
        if "id=" in url:  # handles ...open?id=FILE_ID
            file_id = url.split("id=")[-1]
            return f"https://drive.google.com/uc?export=download&id={file_id}"
        elif "/d/" in url:  # handles .../d/FILE_ID/view
            file_id = url.split("/d/")[1].split("/")[0]
            return f"https://drive.google.com/uc?export=download&id={file_id}"
    return url  # return as-is if not a GDrive link


def download_resume(resume_url):
    """Download resume from URL and save locally as resume.pdf"""
    try:
        resume_url = fix_google_drive_url(resume_url)
        response = requests.get(resume_url, stream=True, timeout=15)

        if response.status_code == 200 and "pdf" in response.headers.get("Content-Type", "").lower():
            with open("resume.pdf", "wb") as f:
                f.write(response.content)
            return "resume.pdf"
        else:
            print(f"❌ Invalid response (status {response.status_code}, content-type {response.headers.get('Content-Type')})")
            return None
    except Exception as e:
        print(f"❌ Error downloading resume: {e}")
        return None


def extract_text_from_pdf(file_path):
    """Extract all text from a PDF file using PyMuPDF."""
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text("text")
        return text
    except Exception as e:
        print(f"❌ Error extracting text: {e}")
        return ""


def analyze_resume(resume_url):
    """Download, extract, and analyze resume for matching skills."""
    # Step 1: Download
    pdf_file = download_resume(resume_url)
    if not pdf_file:
        return "❌ Resume could not be downloaded or is not a valid PDF"

    # Step 2: Extract text
    text = extract_text_from_pdf(pdf_file).lower()
    if not text.strip():
        return "❌ Could not extract text from resume"

    # Step 3: Match skills
    found_skills = [skill for skill in SKILLS if skill.lower() in text]
    score = len(found_skills)

    # Step 4: Selection logic
    if score >= 5:
        return f"✅ Selected (skills matched: {', '.join(found_skills)})"
    elif score >= 3:
        return f"⏳ Waiting (skills matched: {', '.join(found_skills)})"
    else:
        return f"❌ Rejected (skills matched: {', '.join(found_skills)})"
