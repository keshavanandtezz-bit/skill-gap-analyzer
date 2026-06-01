# =============================================================================
# SKILL GAP ANALYZER - Core Analysis Engine
# =============================================================================
# This module contains the main analysis logic:
# - Comparing resume vs job description skills
# - Computing match scores
# - Generating learning recommendations

from skills_db import (
    extract_skills_from_text,
    flatten_skills,
    SKILLS_DATABASE
)


def analyze_skills(resume_text: str, job_text: str) -> dict:
    """
    Main analysis function: compares resume and job description.

    Steps:
    1. Extract skills from both texts using skills_db module
    2. Flatten category-based dicts into simple sets
    3. Compute matched, missing, and extra skills
    4. Calculate an overall match score (percentage)
    5. Build category-wise breakdown for detailed view
    6. Generate prioritized learning recommendations

    Args:
        resume_text (str): Full text content of the resume.
        job_text (str): Full text content of the job description.

    Returns:
        dict: Analysis results with keys:
            - matched_skills (set)
            - missing_skills (set)
            - extra_skills (set)
            - score (float): 0-100
            - grade (str): A, B, C, D, F
            - category_breakdown (dict)
            - recommendations (list of dicts)
            - total_job_skills (int)
            - total_resume_skills (int)
    """

    # Step 1: Extract skills by category
    resume_by_cat = extract_skills_from_text(resume_text)
    job_by_cat = extract_skills_from_text(job_text)

    # Step 2: Flatten to simple sets for overall comparison
    resume_skills = flatten_skills(resume_by_cat)
    job_skills = flatten_skills(job_by_cat)

    # Step 3: Compute skill sets
    matched_skills = resume_skills & job_skills          # Skills in both
    missing_skills = job_skills - resume_skills          # Job needs, resume lacks
    extra_skills = resume_skills - job_skills            # Resume has extra (bonus)

    # Step 4: Match score calculation
    if len(job_skills) > 0:
        score = (len(matched_skills) / len(job_skills)) * 100
    else:
        score = 0.0

    # Step 5: Grade assignment
    grade = _calculate_grade(score)

    # Step 6: Category-wise breakdown
    category_breakdown = _build_category_breakdown(
        job_by_cat, resume_by_cat
    )

    # Step 7: Prioritized learning recommendations
    recommendations = _generate_recommendations(missing_skills, job_by_cat)

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills,
        "score": round(score, 2),
        "grade": grade,
        "category_breakdown": category_breakdown,
        "recommendations": recommendations,
        "total_job_skills": len(job_skills),
        "total_resume_skills": len(resume_skills),
        "resume_by_category": resume_by_cat,
        "job_by_category": job_by_cat,
    }


def _calculate_grade(score: float) -> str:
    """Convert a numeric score to a letter grade."""
    if score >= 90:
        return "A+"
    elif score >= 80:
        return "A"
    elif score >= 70:
        return "B+"
    elif score >= 60:
        return "B"
    elif score >= 50:
        return "C"
    elif score >= 35:
        return "D"
    else:
        return "F"


def _build_category_breakdown(job_by_cat: dict, resume_by_cat: dict) -> list:
    """
    Build a category-wise comparison breakdown.
    
    Returns a list of dicts with per-category match info,
    sorted by importance (categories with more required skills first).
    """
    breakdown = []

    for category in job_by_cat:
        job_cat_skills = job_by_cat.get(category, set())
        resume_cat_skills = resume_by_cat.get(category, set())

        cat_matched = job_cat_skills & resume_cat_skills
        cat_missing = job_cat_skills - resume_cat_skills

        cat_score = (
            len(cat_matched) / len(job_cat_skills) * 100
            if job_cat_skills else 0
        )

        breakdown.append({
            "category": category,
            "required": len(job_cat_skills),
            "matched": len(cat_matched),
            "missing": len(cat_missing),
            "score": round(cat_score, 1),
            "matched_skills": cat_matched,
            "missing_skills": cat_missing,
        })

    # Sort by most required skills first
    breakdown.sort(key=lambda x: x["required"], reverse=True)
    return breakdown


def _generate_recommendations(missing_skills: set, job_by_cat: dict) -> list:
    """
    Generate learning path recommendations for missing skills.
    
    Returns a list of dicts with skill, category, priority, and
    suggested learning resource URLs.

    Priority is based on how critical the category is
    (e.g., Programming Languages > Soft Skills).
    """
    PRIORITY_ORDER = [
        "💻 Programming Languages",
        "🤖 AI & Machine Learning",
        "🌐 Web Development",
        "☁️ Cloud & DevOps",
        "📊 Data Science & Analytics",
        "🗄️ Databases",
        "📱 Mobile Development",
        "🔐 Cybersecurity",
        "🧪 Testing & QA",
        "🤝 Soft Skills & Tools",
    ]

    LEARNING_RESOURCES = {
        "python": "https://docs.python.org/3/tutorial/",
        "java": "https://dev.java/learn/",
        "javascript": "https://javascript.info/",
        "typescript": "https://www.typescriptlang.org/docs/",
        "react": "https://react.dev/learn",
        "sql": "https://www.w3schools.com/sql/",
        "machine learning": "https://www.coursera.org/learn/machine-learning",
        "deep learning": "https://www.deeplearning.ai/",
        "docker": "https://docs.docker.com/get-started/",
        "aws": "https://aws.amazon.com/training/",
        "git": "https://git-scm.com/book/en/v2",
        "pandas": "https://pandas.pydata.org/docs/getting_started/",
        "tensorflow": "https://www.tensorflow.org/learn",
        "pytorch": "https://pytorch.org/tutorials/",
        "kubernetes": "https://kubernetes.io/docs/tutorials/",
    }

    DEFAULT_RESOURCE = "https://www.google.com/search?q=learn+"

    # Build a reverse lookup: skill -> category
    skill_to_cat = {}
    for category, skills in job_by_cat.items():
        for skill in skills:
            if skill in missing_skills:
                skill_to_cat[skill] = category

    recommendations = []
    seen = set()

    # Add by priority order first
    for priority_cat in PRIORITY_ORDER:
        for skill in missing_skills:
            if skill not in seen and skill_to_cat.get(skill) == priority_cat:
                resource = LEARNING_RESOURCES.get(
                    skill,
                    DEFAULT_RESOURCE + skill.replace(" ", "+")
                )
                recommendations.append({
                    "skill": skill,
                    "category": priority_cat,
                    "resource": resource,
                    "priority": "🔴 High" if PRIORITY_ORDER.index(priority_cat) < 4 else "🟡 Medium"
                })
                seen.add(skill)

    # Add remaining missing skills not in priority list
    for skill in missing_skills:
        if skill not in seen:
            resource = LEARNING_RESOURCES.get(
                skill,
                DEFAULT_RESOURCE + skill.replace(" ", "+")
            )
            recommendations.append({
                "skill": skill,
                "category": skill_to_cat.get(skill, "Other"),
                "resource": resource,
                "priority": "🟢 Low"
            })
            seen.add(skill)

    return recommendations
