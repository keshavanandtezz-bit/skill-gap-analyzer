# =============================================================================
# SKILL GAP ANALYZER - Skills Database
# =============================================================================
# This module defines the master skills database organized by category.
# Each category maps to a list of recognized skill keywords.
# Adding new skills here will automatically reflect in the analyzer.

SKILLS_DATABASE = {
    "💻 Programming Languages": [
        "python", "java", "javascript", "typescript", "c++", "c#", "c",
        "kotlin", "swift", "go", "rust", "ruby", "php", "scala", "r",
        "matlab", "perl", "bash", "shell scripting", "powershell"
    ],
    "🌐 Web Development": [
        "html", "css", "react", "angular", "vue", "next.js", "nuxt",
        "node.js", "express", "django", "flask", "fastapi", "spring boot",
        "asp.net", "laravel", "bootstrap", "tailwind", "sass", "graphql",
        "rest api", "restful", "jquery", "webpack", "vite"
    ],
    "🤖 AI & Machine Learning": [
        "machine learning", "deep learning", "neural networks", "nlp",
        "computer vision", "tensorflow", "pytorch", "keras", "scikit-learn",
        "opencv", "hugging face", "transformers", "llm", "generative ai",
        "reinforcement learning", "regression", "classification",
        "clustering", "random forest", "xgboost", "lightgbm"
    ],
    "📊 Data Science & Analytics": [
        "data analysis", "data science", "pandas", "numpy", "matplotlib",
        "seaborn", "plotly", "tableau", "power bi", "excel", "statistics",
        "data visualization", "etl", "data wrangling", "spark", "hadoop",
        "kafka", "airflow", "dbt", "looker"
    ],
    "🗄️ Databases": [
        "sql", "mysql", "postgresql", "mongodb", "redis", "sqlite",
        "oracle", "cassandra", "elasticsearch", "neo4j", "dynamodb",
        "firebase", "supabase", "nosql", "database design", "orm"
    ],
    "☁️ Cloud & DevOps": [
        "aws", "azure", "gcp", "google cloud", "docker", "kubernetes",
        "terraform", "ansible", "jenkins", "ci/cd", "git", "github",
        "gitlab", "linux", "nginx", "apache", "microservices",
        "serverless", "lambda", "devops", "sre", "monitoring"
    ],
    "📱 Mobile Development": [
        "android", "ios", "react native", "flutter", "swift", "kotlin",
        "xamarin", "ionic", "mobile development", "ui/ux"
    ],
    "🔐 Cybersecurity": [
        "cybersecurity", "network security", "penetration testing",
        "ethical hacking", "cryptography", "firewalls", "ssl",
        "oauth", "jwt", "vulnerability assessment", "siem"
    ],
    "🧪 Testing & QA": [
        "unit testing", "selenium", "pytest", "jest", "cypress",
        "test automation", "qa", "quality assurance", "postman",
        "load testing", "jmeter", "tdd", "bdd"
    ],
    "🤝 Soft Skills & Tools": [
        "communication", "teamwork", "leadership", "problem solving",
        "agile", "scrum", "jira", "confluence", "figma", "project management",
        "time management", "critical thinking", "adaptability"
    ]
}


def get_all_skills():
    """Return a flat set of all skills from the database."""
    all_skills = set()
    for category_skills in SKILLS_DATABASE.values():
        for skill in category_skills:
            all_skills.add(skill)
    return all_skills


def get_skill_category(skill):
    """Given a skill name, return its category."""
    for category, skills in SKILLS_DATABASE.items():
        if skill in skills:
            return category
    return "🔧 Other"


def extract_skills_from_text(text):
    """
    Extract skills from a block of text.
    
    Args:
        text (str): The input text (resume or job description).
    
    Returns:
        dict: A dictionary mapping category -> set of found skills.
    """
    text_lower = text.lower()
    found_by_category = {}

    for category, skills in SKILLS_DATABASE.items():
        matched = set()
        for skill in skills:
            # Use word-boundary-aware matching to avoid partial matches
            import re
            # Escape special chars in skill name for regex
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                matched.add(skill)
        if matched:
            found_by_category[category] = matched

    return found_by_category


def flatten_skills(skills_by_category):
    """Flatten a category->set dict into a single set of all skills."""
    all_found = set()
    for skill_set in skills_by_category.values():
        all_found.update(skill_set)
    return all_found
