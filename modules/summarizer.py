from typing import Dict
from modules.base_ai_processor import BaseAIProcessor
from modules.ai_prompts import AIPrompts


class EmailSummarizer(BaseAIProcessor):
    def __init__(self):
        super().__init__()

    def process(self, email_content: str, subject: str = "") -> Dict:
        """Process email for summarization"""
        return self.summarize_email(email_content, subject)
        
    def summarize_email(self, email_content: str, subject: str = "") -> Dict:
        """
        Summarizes an email to extract only necessary information
        """
        prompt = AIPrompts.summarizer_prompt(email_content, subject)
        system_message = AIPrompts.get_system_message("summarizer")
        summary = self._make_api_request(prompt, system_message)
        
        if summary.startswith(("API Error", "Request Failed", "No response")):
            summary = f"Unable to generate summary: {summary}"

        return {
            "subject": subject,
            "original_content": email_content,
            "summary": summary
        }