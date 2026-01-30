from config import Config
import imaplib
import email
import time
import os
import re
from datetime import datetime
from email.header import decode_header

from modules.categorizer import EmailCategorizer
from modules.summarizer import EmailSummarizer
from modules.importance import ImportanceRater

class GmailMonitor:
    def __init__(self):
        # Validate config before starting
        Config.validate()
        
        self.username = Config.MAIL_USERNAME
        self.password = Config.MAIL_APP_PASSWORD
        self.imap_url = "imap.gmail.com"
        self.mail = None
        self.raw_folder = "mails"        # Raw emails folder
        self.evaluated_folder = "evaluated"  # Processed emails folder
        
        # Initialize processing modules
        self.categorizer = EmailCategorizer()
        self.summarizer = EmailSummarizer()
        self.importance_rater = ImportanceRater()

    def _connect(self):
        """Handles connection to Gmail IMAP"""
        try:
            print("🔌 Connecting to Gmail...")
            self.mail = imaplib.IMAP4_SSL(self.imap_url)
            self.mail.login(self.username, self.password)
            self.mail.select("inbox")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False

    def _get_email_body(self, msg):
        """Extracts the plain text body from the email object."""
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass
                    break
        else:
            try:
                body = msg.get_payload(decode=True).decode()
            except:
                pass
        return body

    def _sanitize_filename(self, subject):
        """Removes illegal characters from subject to create a valid filename."""
        # Replace non-alphanumeric chars (except spaces/dashes) with nothing
        safe_subject = re.sub(r'[\\/*?:"<>|]', "", subject)
        # Limit length to 50 chars to prevent OS errors
        return safe_subject[:50].strip()

    def _create_filename(self, subject):
        """Creates filename in format: YYYY-MM-DD_Subject.txt"""
        current_date = datetime.now().strftime("%Y-%m-%d")
        safe_subject = self._sanitize_filename(subject)
        return f"{current_date}_{safe_subject}.txt"

    def _save_raw_email(self, subject, sender, body):
        """Saves raw email content to the 'mails' folder"""
        # Create folder if it doesn't exist
        if not os.path.exists(self.raw_folder):
            os.makedirs(self.raw_folder)

        # Create filename with date-subject format
        filename = self._create_filename(subject)
        filepath = os.path.join(self.raw_folder, filename)

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"Subject: {subject}\n")
                f.write(f"From: {sender}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"\n{'='*60}\n")
                f.write(f"Content:\n{body}")
            print(f"   💾 Raw email saved to: {filepath}")
            return filepath
        except Exception as e:
            print(f"   ⚠️ Failed to save raw email: {e}")
            return None

    def _save_evaluated_email(self, subject, sender, body, category="", summary="", importance=""):
        """Saves evaluated email with processing results to the 'evaluated' folder"""
        # Create folder if it doesn't exist
        if not os.path.exists(self.evaluated_folder):
            os.makedirs(self.evaluated_folder)

        # Create filename with date-subject format
        filename = self._create_filename(subject)
        filepath = os.path.join(self.evaluated_folder, filename)

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"Subject: {subject}\n")
                f.write(f"From: {sender}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Category: {category}\n")
                f.write(f"Importance: {importance}\n")
                f.write(f"Summary: {summary}\n")
                f.write(f"\n{'='*60}\n")
                f.write(f"Original Message:\n{body}")
            print(f"   📊 Evaluated email saved to: {filepath}")
            return filepath
        except Exception as e:
            print(f"   ⚠️ Failed to save evaluated email: {e}")
            return None

    def _process_email(self, subject, sender, body):
        """Complete email processing pipeline: Categorize -> Summarize -> Rate Importance"""
        print(f"\n🔄 Processing email: {subject[:50]}...")
        
        # Step 1: Categorize
        print("   📂 Categorizing...")
        category_result = self.categorizer.categorize_single_email(body, email_id=subject)
        category = category_result.get('category', 'Unknown')
        
        # Step 2: Summarize
        print("   📝 Summarizing...")
        summary_result = self.summarizer.summarize_email(body, subject)
        summary = summary_result.get('summary', 'Unable to summarize')
        
        # Step 3: Rate importance
        print("   ⭐ Rating importance...")
        importance_result = self.importance_rater.rate_importance(summary, category, subject)
        importance = importance_result.get('importance', 'unknown')
        
        # Display results
        print("   ✅ Processing complete!")
        print(f"   📂 Category: {category}")
        print(f"   ⭐ Importance: {importance.upper()}")
        
        return category, summary, importance

    def run(self):
        """Main loop to monitor emails."""
        if not self._connect():
            return

        print("📸 Taking snapshot of current inbox...")
        
        # Initial snapshot to ignore existing emails
        status, messages = self.mail.search(None, 'UNSEEN')
        if messages[0]:
            seen_ids = set(messages[0].split())
        else:
            seen_ids = set()

        print(f"Monitor active. Ignoring {len(seen_ids)} existing unread emails.")
        print("   Waiting for new mail...")

        while True:
            try:
                # Refresh inbox connection
                self.mail.select("inbox")
                status, messages = self.mail.search(None, 'UNSEEN')
                
                if messages[0]:
                    current_ids = set(messages[0].split())
                else:
                    current_ids = set()

                # Calculate new emails
                new_ids = current_ids - seen_ids

                if new_ids:
                    print(f"\n🔔 New Mail Arrived! ({len(new_ids)} new)")
                    
                    for msg_id in new_ids:
                        status, msg_data = self.mail.fetch(msg_id, '(RFC822)')
                        
                        for response_part in msg_data:
                            if isinstance(response_part, tuple):
                                msg = email.message_from_bytes(response_part[1])
                                
                                # Decode Subject
                                subject, encoding = decode_header(msg["subject"])[0]
                                if isinstance(subject, bytes):
                                    subject = subject.decode(encoding if encoding else "utf-8")
                                
                                sender = msg.get("from")
                                body = self._get_email_body(msg)

                                print("="*60)
                                print(f"📧 FROM:    {sender}")
                                print(f"📄 SUBJECT: {subject}")
                                print("="*60)

                                # First, save raw email
                                self._save_raw_email(subject, sender, body)
                                
                                # Process through complete pipeline
                                category, summary, importance = self._process_email(subject, sender, body)
                                
                                # Save evaluated email with processing results
                                self._save_evaluated_email(subject, sender, body, category, summary, importance)

                    # Update seen list
                    seen_ids = current_ids
                
                else:
                    print(".", end="", flush=True)

                time.sleep(10)

            except Exception as e:
                print(f"\n⚠️ Error: {e}")
                print("🔄 Attempting to reconnect...")
                time.sleep(5)
                self._connect()