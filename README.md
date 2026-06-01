# 🎯 Skill Gap Analyzer

A Python mini-project that analyzes the gap between a candidate's skills (from their Resume) and the skills required for a job (from a Job Description).

---

## 📁 Project Structure

```
skill-gap-analyzer/
│
├── app.py           → Main Streamlit application (UI)
├── skills_db.py     → Skills database (130+ skills in 10 categories)
├── pdf_reader.py    → PDF text extraction using PyMuPDF
├── analyzer.py      → Core skill comparison and scoring logic
├── charts.py        → Interactive charts using Plotly
├── requirements.txt → Python dependencies
└── README.md        → This file
```

---

## ✨ Features

- 📎 **PDF Upload** — Upload resume and job description as PDF files
- ✏️ **Text Input** — Or paste text directly
- 📊 **Match Score** — Get a percentage score and grade (A/B/C/D/F)
- ✅ **Matched Skills** — Skills present in both resume and job description
- ❌ **Missing Skills** — Skills the job needs but resume lacks
- ⭐ **Bonus Skills** — Extra skills in resume beyond what's required
- 📂 **Category Breakdown** — Skills grouped into 10 categories
- 📚 **Learning Roadmap** — Clickable links to learn missing skills
- 📈 **4 Interactive Charts** — Gauge, Donut, Bar, Radar charts

---

## 🛠️ Tech Stack

| Library      | Purpose                          |
|--------------|----------------------------------|
| `streamlit`  | Web UI framework                 |
| `PyMuPDF`    | PDF text extraction              |
| `plotly`     | Interactive charts               |
| `re`         | Regex-based skill matching       |

---

## ▶️ How to Run

### Step 1 — Install dependencies
Open terminal in this folder and run:
```bash
pip install streamlit PyMuPDF plotly
```

### Step 2 — Run the app
```bash
streamlit run app.py
```

### Step 3 — Open in browser
```
http://localhost:8501
```

---

## 📖 How It Works

### 1. `pdf_reader.py`
- Uses **PyMuPDF (fitz)** to extract text from uploaded PDF files
- Uses `file.getvalue()` to read Streamlit's UploadedFile safely
- Wraps bytes in `io.BytesIO` for PyMuPDF compatibility

### 2. `skills_db.py`
- Contains **130+ skills** organized into 10 categories:
  - 💻 Programming Languages
  - 🌐 Web Development
  - 🤖 AI & Machine Learning
  - 📊 Data Science & Analytics
  - 🗄️ Databases
  - ☁️ Cloud & DevOps
  - 📱 Mobile Development
  - 🔐 Cybersecurity
  - 🧪 Testing & QA
  - 🤝 Soft Skills & Tools
- Uses **regex word boundaries** (`\bskill\b`) to avoid false matches

### 3. `analyzer.py`
- Extracts skills from both resume and job description texts
- Computes:
  - **Matched skills** = resume ∩ job description
  - **Missing skills** = job description − resume
  - **Bonus skills** = resume − job description
  - **Match score** = matched / total_job_skills × 100
- Assigns a **letter grade** based on score
- Generates **prioritized learning recommendations**

### 4. `charts.py`
- **Gauge chart** — Speedometer showing match percentage
- **Donut chart** — Matched vs Missing vs Bonus skill distribution
- **Bar chart** — Per-category match percentage
- **Radar chart** — Multi-dimensional skill coverage map

### 5. `app.py`
- Main Streamlit application
- Dark premium UI with glassmorphism design
- Two-column layout: Resume | Job Description
- Both PDF upload and text paste supported simultaneously

---

## 👩‍🎓 Academic Information

- **Project:** Skill Gap Analyzer
- **Tech:** Python, Streamlit, PyMuPDF, Plotly
- **Concepts Used:**
  - File handling (PDF reading)
  - Data structures (sets for skill matching, dicts for categories)
  - Functions and modular programming
  - String processing & regex
  - Web application development
  - Data visualization
