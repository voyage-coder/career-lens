import re
SKILLS={"python","java","c++","javascript","typescript","react","node.js","fastapi","flask","django","sql","postgresql","mysql","mongodb","machine learning","deep learning","nlp","scikit-learn","pytorch","tensorflow","html","css","tailwind","git","docker","aws","data analysis","pandas","numpy","communication","leadership"}
SECTIONS={"education":["education","academic"],"experience":["experience","employment","internship","work history"],"projects":["projects","personal projects"],"skills":["skills","technical skills","competencies"],"certifications":["certifications","certificates","licenses"]}
def find_skills(text):
    t=text.lower()
    return sorted(s for s in SKILLS if re.search(r"(?<![a-z0-9])"+re.escape(s)+r"(?![a-z0-9])",t))
def analyze_resume(text):
    words=re.findall(r"\b[\w+#.-]+\b",text); low=text.lower(); skills=find_skills(text)
    sections=[k for k,v in SECTIONS.items() if any(x in low for x in v)]
    missing=[k for k in SECTIONS if k not in sections]
    length=20 if 250<=len(words)<=1000 else (12 if len(words)>=120 else 5)
    section=min(30,len(sections)*6); skill=min(25,len(skills)*2.5)
    contact=15 if re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}",text) else 0
    ats=round(min(100,length+section+skill+contact+(10 if len(sections)>=3 else 4)))
    sentences=max(1,len(re.findall(r"[.!?]+",text))); avg=len(words)/sentences
    readability=round(max(0,min(100,100-abs(avg-18)*2.2)))
    strengths=([f"Detected {len(skills)} skills: {', '.join(skills[:8])}."] if skills else [])
    if "projects" in sections: strengths.append("A projects section is present.")
    if "education" in sections: strengths.append("An education section is present.")
    weaknesses=[]
    if missing: weaknesses.append("Consider adding or clarifying: "+", ".join(missing)+".")
    if not contact: weaknesses.append("No email address was detected.")
    if len(words)<250: weaknesses.append("Resume text appears short; check whether important details are missing.")
    return {"ats_score":ats,"readability_score":readability,"skills":skills,"sections_found":sections,"missing_sections":missing,"word_count":len(words),"strengths":strengths or ["Resume text was extracted successfully."],"weaknesses":weaknesses or ["No major structural gaps detected by basic checks."],"methodology":"Heuristic estimate using section presence, length, detected skills and contact information; not an official ATS score."}
def match_job_description(resume,job):
    a=set(find_skills(resume)); b=set(find_skills(job)); matched=sorted(a&b); missing=sorted(b-a)
    return {"match_percentage":round(100*len(matched)/max(1,len(b))),"matched_skills":matched,"missing_skills":missing,"job_skills_detected":sorted(b),"note":"Skill-based estimate, not a complete semantic assessment."}
