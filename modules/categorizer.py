import os
from typing import List, Dict
from openai import OpenAI
from config import Config


class EmailCategorizer:
    def __init__(self, source_folder: str):
        self.source_folder = source_folder
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=Config.OPENAI_API_KEY,
        )
        self.CATEGORIES = ["Promotion","Spam", "Work","Personal", "Finance", "Other"]

    # Fetch emails
    def fetch_all_emails(self) -> List[Dict]:
        emails = []

        for filename in os.listdir(self.source_folder):
            if not filename.endswith(".txt"):
                continue

            path = os.path.join(self.source_folder, filename)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            emails.append({
                "id": filename,
                "content": content
            })

        return emails

    # Categorize emails
    def categorize_emails(self, emails: List[Dict]) -> List[Dict]:
        categorized = []

        for email in emails:
            prompt = f"""
You are an email classification system.

Categories:
{", ".join(self.CATEGORIES)}

Email:
\"\"\"
{email["content"]}
\"\"\"

Respond with ONLY the category name.
"""

            response = self.client.chat.completions.create(
                model="arcee-ai/trinity-mini:free",
                messages=[{"role": "user", "content": prompt}],
                extra_body={"reasoning": {"enabled": True}}
            )

            category = response.choices[0].message.content.strip()

            categorized.append({
                **email,
                "category": category
            })

        return categorized

    # Print results
    def output_results(self, categorized_emails: List[Dict]):
        for email in categorized_emails:
            print(f"[{email['category']}] {email['id']}")

    # Save results
    def save_results(self, categorized_emails: List[Dict], output_file="results.json"):
        import json

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(categorized_emails, f, indent=2, ensure_ascii=False)
