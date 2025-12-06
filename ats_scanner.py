from typing import Union

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_match(resume_text: str, job_description: str) -> float:
    """
    Safely calculate the match percentage between resume text and job description
    using TF-IDF and cosine similarity.

    Returns:
        Match percentage as a float between 0.0 and 100.0
    """

    # Basic input validation
    if not isinstance(resume_text, str) or not isinstance(job_description, str):
        return 0.0

    resume_text = resume_text.strip()
    job_description = job_description.strip()

    if not resume_text or not job_description:
        return 0.0

    text_list = [resume_text, job_description]

    try:
        # You can tweak vectorizer for better results if needed
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(text_list)

        # Cosine similarity between resume (0) and JD (1)
        similarity = cosine_similarity(tfidf_matrix)[0][1]

        # Clamp to [0, 100] and round
        match_percentage = max(0.0, min(100.0, similarity * 100))
        return float(round(match_percentage, 2))

    except Exception:
        # In case of any unexpected failure, return safe default
        return 0.0


# --- Local Test (runs only when this file is executed directly) ---
if __name__ == "__main__":
    print("--- AI SMART RESUME SCREENER ---")

    job_desc = """
    We are looking for a Python Developer with experience in AI and Machine Learning.
    Must know Scikit-Learn, Pandas, and how to build models.
    Good communication skills and problem-solving ability required.
    """

    my_resume = """
    I am a final year BCA student specializing in AI and ML.
    I have skills in Python, Scikit-Learn, and Data Science.
    I have built projects using Pandas and Machine Learning models.
    I am a good problem solver.
    """

    print("\nAnalyzing match...")
    match_score = calculate_match(my_resume, job_desc)

    print(f"-----------------------------")
    print(f"Match Score: {match_score}%")
    print(f"-----------------------------")

    if match_score >= 60:
        print("Result: Resume Selected! ✅")
    else:
        print("Result: Resume Rejected. ❌ (Add more JD keywords)")
