import os
import json
from typing import List, Dict
from modules.base_ai_processor import BaseAIProcessor
from utils.ai_prompts import AIPrompts


class EmailCategorizer(BaseAIProcessor):
    def __init__(self, source_folder: str = None):
        super().__init__()
        self.source_folder = source_folder
        self.CATEGORIES = ["Promotion", "Spam", "Work", "Personal", "Finance", "Other"]

    def fetch_all_emails(self) -> List[Dict]:
        """Fetch all emails from folder (for batch processing)"""
        if not self.source_folder:
            raise ValueError("Source folder not set.")
        
        emails = []
        for filename in os.listdir(self.source_folder):
            if not filename.endswith(".txt"):
                continue
            path = os.path.join(self.source_folder, filename)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            emails.append({"id": filename, "content": content})
        return emails

    def categorize_emails(self, emails: List[Dict]) -> List[Dict]:
        """Categorize multiple emails"""
        categorized = []
        for email_item in emails:
            result = self.categorize_single_email(email_item['content'], email_item['id'])
            categorized.append(result)
        return categorized

    def process(self, email_content: str, email_id: str = "single_email") -> Dict:
        """Process email for categorization"""
        return self.categorize_single_email(email_content, email_id)
        
    def categorize_single_email(self, email_content: str, email_id: str = "single_email") -> Dict:
        """Categorize a single email (main method used by Gmail Monitor)"""
        prompt = AIPrompts.categorizer_prompt(email_content, self.CATEGORIES)
        system_message = AIPrompts.get_system_message("categorizer")
        raw_category = self._make_api_request(prompt, system_message)
        
        # Validate category is one of our expected ones
        if raw_category in self.CATEGORIES:
            category = raw_category
        elif not raw_category.startswith(("API Error", "Request Failed", "No response")):
            # Try to match partial response to categories
            for cat in self.CATEGORIES:
                if cat.lower() in raw_category.lower():
                    category = cat
                    break
            else:
                category = "Other"  # default fallback
        else:
            category = raw_category  # Keep error message

        return {
            "id": email_id,
            "content": email_content,
            "category": category
        }

    def output_results(self, categorized_emails: List[Dict]):
        """Display categorization results"""
        for email_item in categorized_emails:
            print(f"[{email_item['category']}] {email_item['id']}")

    def save_results(self, categorized_emails: List[Dict], output_file="results.json"):
        """Save categorization results to JSON file"""
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(categorized_emails, f, indent=2, ensure_ascii=False)
