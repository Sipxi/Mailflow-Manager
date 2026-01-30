# Mail Flow Manager

An automated email processing system that monitors Gmail and processes incoming emails through a complete AI-powered OOP pipeline.

## 🚀 Features

- **Gmail Monitoring**: Real-time monitoring for new emails
- **Smart Categorization**: AI-powered email classification (Promotion, Spam, Work, Personal, Finance, Other)
- **Intelligent Summarization**: Extracts only essential information from emails  
- **5-Level Importance Rating**: Rates emails on scale: `low` → `medium` → `high` → `urgent` → `critical`
- **Dual Storage System**: Raw emails in `mails/` and evaluated emails in `evaluated/`
- **OOP Architecture**: Clean, maintainable code following DRY principles

## 📁 Project Structure

```
Mailflow-Manager/
├── config.py              # Configuration settings
├── main.py                # Main application entry point
├── test.py                # Component testing script
├── requirements.txt       # Dependencies
├── mails/                 # Raw email storage (original content only)
├── evaluated/             # Processed emails (with Category, Importance, Summary)
└── modules/
    ├── base_ai_processor.py   # Base class for AI processors (DRY principle)
    ├── ai_prompts.py          # Centralized AI prompts for all processors
    ├── gmailmonitor.py       # Gmail monitoring & main pipeline
    ├── categorizer.py        # Email categorization
    ├── summarizer.py         # Email summarization  
    └── importance.py         # 5-level importance rating
```

## 🏗️ OOP Architecture

- **BaseAIProcessor**: Abstract base class eliminating code duplication across AI modules
- **AIPrompts**: Centralized prompt management for all AI processors
- **Inheritance**: All AI processors inherit common API handling and error management
- **Polymorphism**: Consistent `process()` method interface across all modules
- **Encapsulation**: Clean separation of concerns between monitoring and processing

## 🔧 Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   Create a `.env` file in the root directory:
   ```env
   API_KEY_OPENAI=your_g4f_api_key_here
   MAIL_USERNAME=your_gmail@gmail.com
   MAIL_APP_PASSWORD=your_gmail_app_password
   ```

3. **Gmail App Password Setup**
   - Enable 2-factor authentication on your Google account
   - Generate an app password for this application
   - Use the app password (not your regular password) in the `.env` file

## 🎯 Usage

### Run the Mail Monitor
```bash
python main.py
```

### Test Individual Components
```bash
python test.py
```

## 🔄 Email Processing Pipeline

When a new email arrives, it goes through this OOP-based pipeline:

1. **📧 Gmail Monitor** - Detects new email and extracts content
2. **💾 Raw Storage** - Saves original email to `mails/` folder
3. **📂 Categorizer** - Classifies the email into categories
4. **📝 Summarizer** - Creates a concise summary of essential information
5. **⭐ Importance Rater** - Rates importance on 5-level scale
6. **📊 Evaluated Storage** - Saves processed email to `evaluated/` folder

## 📄 File Organization

### Raw Emails (`mails/` folder)
Format: `YYYY-MM-DD_Subject.txt`
```
Subject: Meeting Request - Project Review
From: manager@company.com
Date: 2026-01-30 14:30:15

============================================================
Content:
[Original email content only...]
```

### Evaluated Emails (`evaluated/` folder)  
Format: `YYYY-MM-DD_Subject.txt`
```
Subject: Meeting Request - Project Review
From: manager@company.com
Date: 2026-01-30 14:30:15
Category: Work
Importance: medium
Summary: Meeting request for project review. Action required: respond with availability.

============================================================
Original Message:
[Original email content...]
```

## ⚙️ Configuration

The `config.py` file handles all configuration:
- API keys for AI processing
- Gmail credentials
- Validation of required settings

## 🧪 Testing

Use `test.py` to verify individual components:
- Categorizer functionality
- Summarizer performance  
- 5-level importance rating accuracy
- Complete pipeline testing

## 🔐 Security Notes

- Uses Gmail App Passwords (secure authentication)
- API keys stored in environment variables
- No credentials stored in code

## 📊 5-Level Importance Scale

- **LOW**: Routine emails, newsletters, non-urgent notifications, social updates
- **MEDIUM**: Regular work communications, meeting requests, follow-ups, planned tasks  
- **HIGH**: Important business matters, time-sensitive requests, deadline reminders
- **URGENT**: Critical deadlines (24-48 hours), client issues, system problems
- **CRITICAL**: Emergency situations, security alerts, system failures, legal issues

## 🛠️ Customization

The OOP structure makes customization easy:
- **AI Prompts**: All prompts centralized in `ai_prompts.py` for easy modification
- **Email categories**: Update categories in `categorizer.py`
- **Summary style**: Modify prompt in `ai_prompts.py`  
- **Importance levels**: Adjust scale in `importance.py`
- **File naming**: Change format in `gmailmonitor.py`
- **Add new processors**: Extend `BaseAIProcessor` and add prompts to `AIPrompts`

## 📝 License

See LICENSE file for details.