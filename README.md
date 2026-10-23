# Smart Gatekeeper AI 🛡️

An AI-powered campus visitor management system that converts messy, unstructured guard inputs into clean database records using Google Gemini.

## Setup Instructions
1. Clone this repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install fastapi uvicorn streamlit pydantic google-generativeai python-dotenv sqlalchemy`
5. Create a `.env` file in the root directory and add your free Gemini API key:
   `GEMINI_API_KEY=your_actual_key_here`

## How to Run
You must run the backend and frontend simultaneously in two separate terminals.

**Terminal 1 (Backend):**
```bash
python -m uvicorn main:app --reload