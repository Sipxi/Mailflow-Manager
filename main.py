"""
Mail Flow Manager - Automated Email Processing System

This application monitors Gmail for new emails and processes them through
a complete OOP-based pipeline:

1. Gmail Monitor - Detects new emails
2. Categorizer - Classifies emails into categories  
3. Summarizer - Extracts essential information
4. Importance Rater - Rates on: low → medium → high → urgent → critical

File Organization:
- Raw emails → 'mails/' folder (original content only)
- Evaluated emails → 'evaluated/category/priority/' folders (with Category, Importance, Summary, Original message)

Both use date-subject filename format: YYYY-MM-DD_Subject.txt
"""

from modules.gmailmonitor import GmailMonitor
from config import Config

def main():
    """Main entry point for the Mail Flow Manager"""
    print("🚀 Mail Flow Manager Starting...")
    print("📧 Pipeline: Monitor → Categorize → Summarize → Rate Importance")
    print(f"Listening on {Config.MAIL_USERNAME} for new emails...")
    print("-" * 70)
    
    try:
        monitor = GmailMonitor()
        monitor.run()
    except KeyboardInterrupt:
        print("\n\n👋 Mail Flow Manager stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check your configuration and try again")

if __name__ == "__main__":
    main()