from google import genai
from app.core.config import settings
import json
from datetime import datetime

class AIWorkOrderAgent:
    def __init__(self):
        if settings.GOOGLE_API_KEY and settings.GOOGLE_API_KEY != "YOUR_GOOGLE_API_KEY_HERE":
            self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
            self.model_id = 'gemini-2.0-flash'
        else:
            self.client = None

    def analyze_intent(self, text: str):
        """
        Analyze user text and return an Intent JSON.
        """
        if not self.client:
            return {"error": "AI not configured"}
        
        prompt = f"""
        You are an assistant for a Field Service Management System.
        Analyze the input text and extract the INTENT and PARAMETERS.
        Return ONLY valid JSON with this exact structure:
        {{
            "intent": "INTENT_NAME",
            "params": {{ ... }}
        }}
        
        Current Date: {datetime.now().strftime('%Y-%m-%d')}
        
        Intents:
        1. QUERY_JOBS: User asks about tasks/jobs/schedule.
           - date: 'today', 'tomorrow', 'yesterday' or YYYY-MM-DD
           - status: 'active' (pending/doing), 'completed'
           - status: 'active' (pending/doing), 'completed'
           - period: 'week' (this week), 'next_week'
           - technician_name: Extract name if mentioned (e.g. 'ช่างโต', 'Seal') or 'all'
           - customer_name: Extract customer name if mentioned (e.g. 'ช้าง', 'ลูกค้า A')
           - keyword: Any other specific search term (e.g. 'air con', 'repair TV')
        
        2. GET_JOB_DETAILS: User asks for details of a specific job ID.
           - job_id: integer
           
        3. UPDATE_JOB: User wants to update status or add note.
           - job_id: integer
           - status: 'completed', 'in_progress', 'cancelled' (map closely to these)
           - note: any details mentioned
           
        4. PROFILE_PASSWORD: User wants to change password.
        
        5. QUERY_PROJECTS: User asks about projects (not specific jobs).
           - keyword: Filter by project name (optional)
           - status: 'active', 'completed' (optional)

        6. OTHER_CHAT: General conversation or unknown intent.
           - reply: A helpful response string.

        Input: "{text}"
        JSON:
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            content = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(content)
        except Exception as e:
            error_str = str(e)
            print(f"AI Error: {error_str}")
            
            if "429" in error_str or "Quota exceeded" in error_str:
                return {
                    "intent": "OTHER_CHAT", 
                    "params": {
                        "reply": "⚠️ **System Busy (Rate Limit):**\nI'm receiving too many requests right now. Please wait ~30 seconds and try again."
                    }
                }
                
            return {
                "intent": "OTHER_CHAT", 
                "params": {"reply": "Sorry, I encountered an error responding to that. Please try again."}
            }

    def parse_job_request(self, text: str):
        # Legacy support or specific creation logic
        pass

ai_agent = AIWorkOrderAgent()
