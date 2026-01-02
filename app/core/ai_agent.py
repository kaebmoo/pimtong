import google.generativeai as genai
from app.core.config import settings
import json

class AIWorkOrderAgent:
    def __init__(self):
        if settings.GOOGLE_API_KEY and settings.GOOGLE_API_KEY != "YOUR_GOOGLE_API_KEY_HERE":
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None

    def parse_job_request(self, text: str):
        """
        Parse a natural language job request into a structured JSON for a WorkOrder.
        """
        if not self.model:
            return {"error": "AI not configured"}
        
        prompt = f"""
        Extract the following details from the text below and return as JSON:
        - title (short summary)
        - job_type (sales, project, or service)
        - customer_name
        - customer_phone
        - customer_address
        - scheduled_date (YYYY-MM-DD, assume today is 2024-01-01 if relative)
        - scheduled_time
        
        Text: "{text}"
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Simple cleanup to get JSON if the model returns markdown code blocks
            content = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(content)
        except Exception as e:
            print(f"AI Error: {e}")
            return {"error": "Failed to parse"}

ai_agent = AIWorkOrderAgent()
