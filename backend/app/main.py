import json
from fastapi import FastAPI,Depends,HTTPException,UploadFile,File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db import Base,engine,get_db
from app.models import User,Resume,Analysis
from app.schemas import RegisterIn,LoginIn,TokenOut,UserOut,ResumeOut,JobMatchIn
from app.security import hash_password,verify_password,create_token,get_current_user
from app.services.resume_parser import extract_resume_text
from app.ai.analyzer import analyze_resume,match_job_description
from app.ai.gemini_coach import generate_coaching
Base.metadata.create_all(bind=engine)
app=FastAPI(title="AI Resume Analyzer and Career Coach",version="0.1.0")
app.add_middleware(CORSMiddleware,allow_origins=[settings.frontend_origin],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
@app.get("/api/health")
def health(): return {"status":"ok"}
@app.post("/api/auth/register",response_model=UserOut,status_code=201)
def register(p:RegisterIn,db:Session=Depends(get_db)):
    if len(p.password)<8: raise HTTPException(400,"Password must contain at least 8 characters")
    if db.query(User).filter(User.email==p.email.lower()).first(): raise HTTPException(409,"Email already registered")
    u=User(name=p.name.strip(),email=p.email.lower(),password_hash=hash_password(p.password)); db.add(u); db.commit(); db.refresh(u); return u
@app.post("/api/auth/login",response_model=TokenOut)
def login(p:LoginIn,db:Session=Depends(get_db)):
    u=db.query(User).filter(User.email==p.email.lower()).first()
    if not u or not verify_password(p.password,u.password_hash): raise HTTPException(401,"Incorrect email or password")
    return {"access_token":create_token(u.id),"user":u}
@app.get("/api/auth/me",response_model=UserOut)
def me(u:User=Depends(get_current_user)): return u
@app.post("/api/resumes",response_model=ResumeOut,status_code=201)
async def upload(file:UploadFile=File(...),db:Session=Depends(get_db),u:User=Depends(get_current_user)):
    name=file.filename or "resume"
    if not name.lower().endswith((".pdf",".docx")): raise HTTPException(400,"Only PDF and DOCX supported")
    data=await file.read()
    if len(data)>settings.max_upload_mb*1024*1024: raise HTTPException(413,"File exceeds upload limit")
    try: text=extract_resume_text(name,data)
    except Exception as e: raise HTTPException(400,str(e))
    row=Resume(owner_id=u.id,filename=name,content_type=file.content_type or "application/octet-stream",extracted_text=text); db.add(row); db.commit(); db.refresh(row); return row
@app.get("/api/resumes",response_model=list[ResumeOut])
def list_resumes(db:Session=Depends(get_db),u:User=Depends(get_current_user)): return db.query(Resume).filter(Resume.owner_id==u.id).order_by(Resume.created_at.desc()).all()
@app.delete("/api/resumes/{rid}")
def delete_resume(rid:int,db:Session=Depends(get_db),u:User=Depends(get_current_user)):
    row=db.query(Resume).filter(Resume.id==rid,Resume.owner_id==u.id).first()
    if not row: raise HTTPException(404,"Resume not found")
    db.delete(row); db.commit(); return {"message":"Resume deleted"}
@app.post("/api/resumes/{rid}/analyze")
def analyze(rid:int,db:Session=Depends(get_db),u:User=Depends(get_current_user)):
    row=db.query(Resume).filter(Resume.id==rid,Resume.owner_id==u.id).first()
    if not row: raise HTTPException(404,"Resume not found")
    result=analyze_resume(row.extracted_text); saved=Analysis(resume_id=rid,ats_score=result["ats_score"],readability_score=result["readability_score"],result_json=json.dumps(result)); db.add(saved); db.commit(); db.refresh(saved); return {"analysis_id":saved.id,**result}
@app.post("/api/job-match")
def job_match(p:JobMatchIn,db:Session=Depends(get_db),u:User=Depends(get_current_user)):
    row=db.query(Resume).filter(Resume.id==p.resume_id,Resume.owner_id==u.id).first()
    if not row: raise HTTPException(404,"Resume not found")
    if len(p.job_description.strip())<50: raise HTTPException(400,"Provide a job description of at least 50 characters")
    return match_job_description(row.extracted_text,p.job_description)
@app.post("/api/career-coach/{rid}")
def coach(rid:int,db:Session=Depends(get_db),u:User=Depends(get_current_user)):
    row=db.query(Resume).filter(Resume.id==rid,Resume.owner_id==u.id).first()
    if not row: raise HTTPException(404,"Resume not found")
    a=analyze_resume(row.extracted_text)
    try: advice=generate_coaching(a)
    except Exception: raise HTTPException(502,"Gemini service unavailable; check API key and quota")
    if not advice: advice="Gemini is not configured. Add GEMINI_API_KEY to backend/.env. Detected skills: "+", ".join(a["skills"][:10])
    return {"recommendations":advice,"based_on_skills":a["skills"]}
