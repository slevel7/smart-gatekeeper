from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from datetime import datetime
from database import SessionLocal, Visitor

load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable missing.")
genai.configure(api_key=api_key)

app = FastAPI(title="Smart Gatekeeper API")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class RawInputRequest(BaseModel):
    raw_text: str

@app.post("/log-entry")
def log_entry(request: RawInputRequest, db: Session = Depends(get_db)):
    try:
        # The AI Agent Component: Information Extraction
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Extract the following information from the security guard's raw input.
        Return ONLY a valid JSON object with these keys: 
        "visitor_name", "visiting_student", "vehicle_number" (or null if none).
        Raw Input: "{request.raw_text}"
        """
        response = model.generate_content(prompt)
        
        # Clean AI output and parse JSON
        output_text = response.text.strip().replace('```json', '').replace('```', '')
        extracted_data = json.loads(output_text)

        # Save to Database
        new_visitor = Visitor(
            visitor_name=extracted_data.get("visitor_name", "Unknown"),
            visiting_student=extracted_data.get("visiting_student", "Unknown"),
            vehicle_number=extracted_data.get("vehicle_number")
        )
        db.add(new_visitor)
        db.commit()
        db.refresh(new_visitor)
        
        return {"status": "success", "data": new_visitor}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI parsing or DB error: {str(e)}")

@app.get("/active-visitors")
def get_active_visitors(db: Session = Depends(get_db)):
    visitors = db.query(Visitor).filter(Visitor.status == "In Campus").all()
    return visitors

@app.post("/log-exit/{visitor_id}")
def log_exit(visitor_id: int, db: Session = Depends(get_db)):
    visitor = db.query(Visitor).filter(Visitor.id == visitor_id).first()
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    
    visitor.status = "Exited"
    visitor.exit_time = datetime.utcnow()
    db.commit()
    return {"status": "success", "message": f"{visitor.visitor_name} logged out."}