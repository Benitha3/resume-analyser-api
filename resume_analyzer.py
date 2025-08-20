import fitz  # PyMuPDF
import os

# Predefined skills
SKILLS = [
    "Python", "Java", "C++", "SQL", "Machine Learning",
    "Deep Learning", "NLP", "Data Analysis", "Excel",
    "Communication", "Leadership", "Teamwork", "Problem Solving"
]

# Folder where Google Form uploads are stored
UPLOAD_FOLDER = "path_to_google_form_upload_folder"  # Replace with your folder path

def extract_text_from_pdf(file_path):
    """Extract all text from a PDF file using PyMuPDF."""
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text("text")
        return text
    except Exception as e:
        print(f"❌ Error extracting text from {file_path}: {e}")
        return ""

def analyze_resume(file_path, candidate_name="candidate"):
    """Analyze PDF for skills."""
    text = extract_text_from_pdf(file_path).lower()
    if not text.strip():
        return "❌ Could not extract text from resume"

    found_skills = [skill for skill in SKILLS if skill.lower() in text]
    score = len(found_skills)

    if score >= 5:
        return f"✅ Selected (skills matched: {', '.join(found_skills)})"
    elif score >= 3:
        return f"⏳ Waiting (skills matched: {', '.join(found_skills)})"
    else:
        return f"❌ Rejected (skills matched: {', '.join(found_skills)})"

def analyze_all_uploads():
    """Analyze all PDFs in the upload folder."""
    results = []
    for file_name in os.listdir(UPLOAD_FOLDER):
        if file_name.lower().endswith(".pdf"):
            file_path = os.path.join(UPLOAD_FOLDER, file_name)
            candidate_name = os.path.splitext(file_name)[0]
            status = analyze_resume(file_path, candidate_name)
            results.append({"Name": candidate_name, "Status": status})
    return results

# Example usage
if __name__ == "__main__":
    results = analyze_all_uploads()
    for r in results:
        print(f"{r['Name']}: {r['Status']}")
