# Smart Gatekeeper AI 🛡️

An AI-powered campus visitor management system that converts unstructured, messy inputs from security guards into clean, structured database records using Google Gemini.

## Overview
This application solves the bottleneck at campus security gates by allowing guards to type natural language sentences (e.g., "Rahul visiting Amit in Room 302 bike DL4S9876") instead of filling out slow, multi-step forms. The AI extracts the entities and logs them into a local database instantly.

## Dependencies
* Python 3.9+
* `fastapi` & `uvicorn` (Backend API)
* `streamlit` (Frontend UI)
* `google-generativeai` (LLM Integration)
* `sqlalchemy` (Database ORM)
* `python-dotenv` (Environment management)

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd smart-gatekeeper
   ```

2. **Create and activate a virtual environment:**
   * **Windows:**
     ```cmd
     python -m venv venv
     venv\Scripts\activate
     ```
   * **Mac/Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install the required packages:**
   ```bash
   pip install fastapi uvicorn streamlit pydantic google-generativeai python-dotenv sqlalchemy pandas
   ```

4. **Required Environment Variables:**
   Create a file named `.env` in the root directory of the project and add your Google Gemini API key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

## How to Run the Application
You must run the backend and frontend simultaneously in two separate terminals.

**Terminal 1 (Start the Backend):**
```bash
python -m uvicorn main:app --reload
```

**Terminal 2 (Start the Frontend):**
```bash
python -m streamlit run app.py
```
The web interface will automatically open at `http://localhost:8501`.

## Known Issues & Limitations
* **Spelling Reliance:** The system relies on the guard's phonetic spelling of names.
* **No Directory Cross-Referencing:** The app does not currently cross-reference a student database to verify if the "visiting student" actually exists in the specified room.
* **Fallback Behavior:** If the Gemini API rate limits or times out, the backend uses a fast regex-based fallback to ensure the gate queue is never delayed, but this fallback is less accurate at parsing names than the AI.