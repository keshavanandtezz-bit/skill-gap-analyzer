import streamlit as st
from pdf_reader import read_pdf
from analyzer import analyze_skills

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Skill Gap Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background: #0E1117 !important;
    color: #E8EAF6 !important;
}
#MainMenu, footer, header { visibility: hidden; }
.main .block-container { padding: 2rem 2.5rem !important; max-width: 1300px !important; }

/* Hero */
.hero {
    text-align: center; padding: 2.5rem 1rem 2rem;
    background: linear-gradient(135deg, rgba(108,99,255,.14), rgba(0,212,170,.08));
    border-radius: 20px; border: 1px solid rgba(255,255,255,.07); margin-bottom: 2rem;
}
.hero h1 {
    font-size: 2.6rem; font-weight: 800; margin: 0 0 .4rem;
    background: linear-gradient(135deg,#6C63FF,#00D4AA);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero p { color: #9CA3AF; font-size: 1rem; margin: 0; }

/* Cards */
.card { background: rgba(255,255,255,.03); border: 1px solid rgba(255,255,255,.08); border-radius: 16px; padding: 1.4rem; }

/* Success box */
.success-box {
    background: rgba(0,212,170,.1); border: 1px solid rgba(0,212,170,.4);
    border-radius: 10px; padding: .8rem 1rem; font-size: .87rem; margin-top: .5rem;
}
/* Error box */
.error-box {
    background: rgba(255,92,122,.1); border: 1px solid rgba(255,92,122,.4);
    border-radius: 10px; padding: .8rem 1rem; font-size: .87rem; margin-top: .5rem; color: #FF5C7A;
}

/* OR divider */
.or-row {
    display:flex; align-items:center; gap:.8rem;
    color:#4B5563; font-size:.78rem; font-weight:600; letter-spacing:.08em; margin:1rem 0;
}
.or-row::before,.or-row::after { content:''; flex:1; height:1px; background:rgba(255,255,255,.07); }

/* Analyze button */
div.stButton > button {
    background: linear-gradient(135deg,#6C63FF,#00D4AA) !important;
    color: white !important; font-weight: 700 !important; font-size: 1.05rem !important;
    border: none !important; border-radius: 50px !important;
    padding: .8rem 2rem !important;
    box-shadow: 0 4px 20px rgba(108,99,255,.4) !important;
    transition: all .2s ease !important;
}
div.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 28px rgba(108,99,255,.55) !important; }

/* Metric boxes */
.mbox { background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.09); border-radius:14px; padding:1.1rem; text-align:center; }
.mval { font-size:2rem; font-weight:800; }
.mlbl { font-size:.76rem; color:#9CA3AF; text-transform:uppercase; letter-spacing:.05em; margin-top:.2rem; }

/* Skill tags */
.stag { display:inline-block; padding:.25rem .7rem; border-radius:50px; font-size:.8rem; font-weight:500; margin:.2rem; }
.sm { background:rgba(0,212,170,.15); color:#00D4AA; border:1px solid rgba(0,212,170,.3); }
.sx { background:rgba(255,92,122,.15); color:#FF5C7A; border:1px solid rgba(255,92,122,.3); }
.sb { background:rgba(108,99,255,.15); color:#9D97FF; border:1px solid rgba(108,99,255,.3); }

/* Rec card */
.rcard {
    background:rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.08);
    border-radius:12px; padding:.85rem 1rem; margin-bottom:.45rem;
    display:flex; align-items:center; gap:.9rem;
    transition: border-color .2s, transform .2s;
}
.rcard:hover { border-color:rgba(108,99,255,.4); transform:translateX(4px); }

/* divider */
.hdiv { border:none; height:1px; background:linear-gradient(90deg,transparent,rgba(108,99,255,.3),transparent); margin:2rem 0; }

/* File uploader */
[data-testid="stFileUploader"] section {
    background: rgba(108,99,255,.06) !important;
    border: 2px dashed rgba(108,99,255,.45) !important;
    border-radius: 10px !important;
}
/* Text area */
.stTextArea textarea {
    background: #141826 !important; border: 1px solid rgba(108,99,255,.25) !important;
    border-radius: 10px !important; color: #E8EAF6 !important; font-size:.88rem !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🎯 Skill Gap Analyzer</h1>
    <p>Upload or paste your Resume &amp; Job Description → Get your match score, missing skills &amp; learning roadmap instantly</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# INPUTS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("### 📥 Step 1 — Add Your Documents")
st.caption("Upload a PDF **or** paste text for each section. If both are given, PDF is used.")

col_left, col_right = st.columns(2, gap="large")

# helper to process one side
def process_side(pdf_file, text_input, label):
    """Returns (final_text, word_count, source_label)"""
    if pdf_file is not None:
        try:
            text, pages = read_pdf(pdf_file)
            wc = len(text.split())
            st.markdown(f"""
            <div class="success-box">
                ✅ <b>{label} PDF read!</b> &nbsp;·&nbsp; {pages} page(s) &nbsp;·&nbsp; {wc:,} words extracted
            </div>""", unsafe_allow_html=True)
            with st.expander("👁️ Preview text"):
                st.text(text[:1000] + "\n...[truncated]" if len(text) > 1000 else text)
            return text, wc
        except Exception as e:
            st.markdown(f'<div class="error-box">❌ PDF error: {e}</div>', unsafe_allow_html=True)
            return "", 0

    if text_input.strip():
        wc = len(text_input.split())
        st.caption(f"📝 {wc:,} words")
        return text_input.strip(), wc

    return "", 0

# ── LEFT: Resume ──────────────────────────────────────────────────────────────
with col_left:
    st.markdown("#### 📄 Your Resume / CV")
    st.markdown("**📎 Upload PDF**")
    resume_pdf = st.file_uploader(
        "Upload Resume PDF", type=["pdf"], key="resume_pdf",
        label_visibility="collapsed"
    )
    st.markdown('<div class="or-row">OR PASTE TEXT BELOW</div>', unsafe_allow_html=True)
    st.markdown("**✏️ Paste Resume Text**")
    resume_text = st.text_area(
        "Resume text", height=180, key="resume_text",
        placeholder="Paste your resume content here if you don't have a PDF...",
        label_visibility="collapsed"
    )
    resume_final, resume_wc = process_side(resume_pdf, resume_text, "Resume")

# ── RIGHT: Job Description ────────────────────────────────────────────────────
with col_right:
    st.markdown("#### 💼 Job Description")
    st.markdown("**📎 Upload PDF**")
    job_pdf = st.file_uploader(
        "Upload Job Description PDF", type=["pdf"], key="job_pdf",
        label_visibility="collapsed"
    )
    st.markdown('<div class="or-row">OR PASTE TEXT BELOW</div>', unsafe_allow_html=True)
    st.markdown("**✏️ Paste Job Description Text**")
    job_text = st.text_area(
        "Job description text", height=180, key="job_text",
        placeholder="Paste the job description here if you don't have a PDF...",
        label_visibility="collapsed"
    )
    job_final, job_wc = process_side(job_pdf, job_text, "Job Description")

# ─────────────────────────────────────────────────────────────────────────────
# ANALYZE BUTTON
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
_, bcol, _ = st.columns([1, 2, 1])
with bcol:
    go = st.button("🚀 Analyze My Skills", use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────────────────────────────────────
if go:
    if not resume_final:
        st.warning("⚠️ Please upload a Resume PDF or paste your resume text.")
        st.stop()
    if not job_final:
        st.warning("⚠️ Please upload a Job Description PDF or paste the job description text.")
        st.stop()

    with st.spinner("🔍 Analyzing skills..."):
        results = analyze_skills(resume_final, job_final)

    import charts as ch

    score  = results["score"]
    grade  = results["grade"]
    clr    = "#00D4AA" if score >= 70 else ("#FFB347" if score >= 40 else "#FF5C7A")

    st.markdown('<div class="hdiv"></div>', unsafe_allow_html=True)
    st.markdown("### 📊 Step 2 — Your Results")

    # ── Metrics ───────────────────────────────────────────────────────────────
    c1,c2,c3,c4,c5 = st.columns(5)
    for col, val, lbl, color in [
        (c1, f"{score:.1f}%",               "Match Score",    clr),
        (c2, grade,                          "Grade",          "#9D97FF"),
        (c3, str(len(results["matched_skills"])), "✅ Matched",  "#00D4AA"),
        (c4, str(len(results["missing_skills"])), "❌ Missing",  "#FF5C7A"),
        (c5, str(len(results["extra_skills"])),   "⭐ Bonus",    "#9D97FF"),
    ]:
        with col:
            st.markdown(f"""
            <div class="mbox">
                <div class="mval" style="color:{color}">{val}</div>
                <div class="mlbl">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts ────────────────────────────────────────────────────────────────
    g1, g2 = st.columns(2)
    with g1:
        st.markdown("**🎯 Match Score**")
        st.plotly_chart(ch.create_gauge_chart(score, grade), use_container_width=True)
    with g2:
        st.markdown("**🍩 Skill Distribution**")
        st.plotly_chart(ch.create_donut_chart(
            len(results["matched_skills"]),
            len(results["missing_skills"]),
            len(results["extra_skills"])
        ), use_container_width=True)

    st.markdown('<div class="hdiv"></div>', unsafe_allow_html=True)

    # ── Skill Tags ────────────────────────────────────────────────────────────
    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown("**✅ Matched Skills**")
        if results["matched_skills"]:
            st.markdown("".join(f'<span class="stag sm">{s.title()}</span>' for s in sorted(results["matched_skills"])), unsafe_allow_html=True)
        else:
            st.caption("None matched.")

    with t2:
        st.markdown("**❌ Missing Skills**")
        if results["missing_skills"]:
            st.markdown("".join(f'<span class="stag sx">{s.title()}</span>' for s in sorted(results["missing_skills"])), unsafe_allow_html=True)
        else:
            st.success("🎉 No skills missing!")

    with t3:
        st.markdown("**⭐ Bonus Skills**")
        if results["extra_skills"]:
            st.markdown("".join(f'<span class="stag sb">{s.title()}</span>' for s in sorted(results["extra_skills"])), unsafe_allow_html=True)
        else:
            st.caption("None.")

    # ── Category Charts ───────────────────────────────────────────────────────
    if results["category_breakdown"]:
        st.markdown('<div class="hdiv"></div>', unsafe_allow_html=True)
        st.markdown("**📂 Category Breakdown**")
        b1, b2 = st.columns([1.5, 1])
        with b1:
            st.plotly_chart(ch.create_category_bar_chart(results["category_breakdown"]), use_container_width=True)
        with b2:
            radar = ch.create_radar_chart(results["category_breakdown"])
            if radar:
                st.plotly_chart(radar, use_container_width=True)

    # ── Learning Roadmap ──────────────────────────────────────────────────────
    if results["recommendations"]:
        st.markdown('<div class="hdiv"></div>', unsafe_allow_html=True)
        st.markdown("**📚 Your Learning Roadmap**")
        st.caption("Click any card to open a learning resource.")
        for rec in results["recommendations"]:
            pc = "#FF5C7A" if "High" in rec["priority"] else ("#FFB347" if "Medium" in rec["priority"] else "#00D4AA")
            st.markdown(f"""
            <a href="{rec['resource']}" target="_blank" style="text-decoration:none;color:inherit">
            <div class="rcard">
                <div style="font-size:1.5rem">📘</div>
                <div style="flex:1">
                    <div style="font-weight:600;font-size:.95rem;text-transform:capitalize">{rec['skill'].title()}</div>
                    <div style="font-size:.76rem;color:#9CA3AF">{rec['category']}</div>
                </div>
                <div style="font-size:.76rem;font-weight:600;color:{pc};border:1px solid {pc}55;border-radius:50px;padding:.18rem .6rem">{rec['priority']}</div>
                <div style="color:#9CA3AF">→</div>
            </div></a>""", unsafe_allow_html=True)
    else:
        st.balloons()
        st.success("🎉 Perfect match! Your resume covers all required skills.")
