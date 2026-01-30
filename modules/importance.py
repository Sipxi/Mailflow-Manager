from typing import Dict
from modules.base_ai_processor import BaseAIProcessor
from modules.ai_prompts import AIPrompts


class ImportanceRater(BaseAIProcessor):
    def __init__(self):
        super().__init__()
        self.importance_scale = ["low", "medium", "high", "urgent", "critical"]

    def process(self, email_summary: str, category: str = "", subject: str = "") -> Dict:
        """Process email for importance rating"""
        return self.rate_importance(email_summary, category, subject)
        
    def rate_importance(self, email_summary: str, category: str, subject: str = "") -> Dict:
        """
        Rates email importance on a 5-level scale: low -> medium -> high -> urgent -> critical
        """
        prompt = AIPrompts.importance_prompt(email_summary, category, subject)
        system_message = AIPrompts.get_system_message("importance")
        raw_importance = self._make_api_request(prompt, system_message).lower()
        
        # Validate the response is one of our expected values
        if raw_importance in self.importance_scale:
            importance = raw_importance
        elif not raw_importance.startswith(("api error", "request failed", "no response")):
            # Try to extract the importance from the response
            for scale in self.importance_scale:
                if scale in raw_importance:
                    importance = scale
                    break
            else:
                importance = "medium"  # default to medium importance
        else:
            importance = raw_importance  # Keep error message

        return {
            "subject": subject,
            "category": category,
            "summary": email_summary,
            "importance": importance,
            "scale": "low -> medium -> high -> urgent -> critical"
        }