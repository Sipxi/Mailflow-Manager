"""
AI Prompts for Mail Flow Manager
===============================

This module contains all AI prompts used by the email processing system.
Centralizing prompts makes them easier to maintain, modify, and optimize.

Author: Sipxi
"""


class AIPrompts:
    """
    Container class for all AI prompts used in the email processing pipeline.
    
    This class provides a centralized location for managing all AI prompts,
    system messages, and prompt generation logic used throughout the application.
    """
    
    # ============================================================================
    # SYSTEM MESSAGES - Core AI behavior definitions
    # ============================================================================
    
    CATEGORIZER_SYSTEM = "You are an email classifier. Respond only with the category name."
    
    SUMMARIZER_SYSTEM = "You are an email content summarizer focused on extracting actionable information."
    
    IMPORTANCE_SYSTEM = (
        "You are an email importance classifier. You must respond with only one word from: "
        "low, medium, high, urgent, critical."
    )
    
    # ============================================================================
    # EMAIL CATEGORIZATION PROMPTS
    # ============================================================================
    
    @staticmethod
    def categorizer_prompt(email_content: str, categories: list) -> str:
        """
        Generate categorization prompt for email classification.
        
        Args:
            email_content (str): The content of the email to classify
            categories (list): List of available categories for classification
            
        Returns:
            str: Formatted prompt for email categorization
        """
        return f"""You are an email classification system.

AVAILABLE CATEGORIES:
{', '.join(categories)}

EMAIL CONTENT:
{'-' * 60}
{email_content}
{'-' * 60}

CLASSIFICATION GUIDELINES:
• Promotional content → Promotion  
• Suspicious/unwanted content → Spam
• Business/professional content → Work
• Personal communications → Personal
• Banking/financial content → Finance
• Everything else → Other

TASK: Analyze the email content and classify it into ONE of the categories above.

RESPONSE: Respond with ONLY the category name."""

    # ============================================================================
    # EMAIL SUMMARIZATION PROMPTS
    # ============================================================================
    
    @staticmethod
    def summarizer_prompt(email_content: str, subject: str = "") -> str:
        """
        Generate summarization prompt for extracting key information.
        
        Args:
            email_content (str): The content of the email to summarize
            subject (str): The subject line of the email
            
        Returns:
            str: Formatted prompt for email summarization
        """
        return f"""You are an email summarizer. Extract only the essential information from this email.

EMAIL DETAILS:
Subject: {subject if subject else 'N/A'}

EMAIL CONTENT:
{'-' * 60}
{email_content}
{'-' * 60}

SUMMARY REQUIREMENTS:
Create a brief, natural summary in 2-3 sentences that covers:
• What the sender wants or needs
• Key details like dates, names, deadlines, or important information  
• Any urgency or next steps required

FORMATTING GUIDELINES:
• Write in plain language without bullet points, numbered lists, or asterisks
• Keep it conversational and easy to read
• Focus on actionable information only

TASK: Provide a clear, concise summary following the above guidelines."""

    # ============================================================================
    # IMPORTANCE RATING PROMPTS
    # ============================================================================
    
    @staticmethod
    def importance_prompt(email_summary: str, category: str, subject: str = "") -> str:
        """
        Generate importance rating prompt for priority assessment.
        
        Args:
            email_summary (str): Summary of the email content
            category (str): Category classification of the email
            subject (str): Subject line of the email
            
        Returns:
            str: Formatted prompt for importance rating
        """
        return f"""You are an email importance analyzer. Rate the importance of this email.

EMAIL DETAILS:
Subject: {subject if subject else 'N/A'}
Category: {category}

EMAIL SUMMARY:
{'-' * 60}
{email_summary}
{'-' * 60}

IMPORTANCE SCALE:
• LOW: Routine emails, newsletters, non-urgent notifications, general information, social updates
• MEDIUM: Regular work communications, meeting requests, follow-ups, planned tasks, non-urgent updates  
• HIGH: Important business matters, time-sensitive requests, deadline reminders, significant decisions needed
• URGENT: Critical deadlines (within 24-48 hours), important client issues, system problems, immediate action required
• CRITICAL: Emergency situations, security alerts, system failures, legal issues, CEO-level communications, immediate crisis response needed

EVALUATION CRITERIA:
1. Time sensitivity and deadlines (immediate, hours, days, weeks)
2. Business impact (revenue, operations, reputation)
3. Action urgency required from recipient
4. Sender's authority/position in organization
5. Consequences of delay (minor inconvenience vs major business impact)
6. Security or legal implications

TASK: Rate this email's importance using the scale above.

RESPONSE: Respond with ONLY one word: low, medium, high, urgent, or critical"""

    # ============================================================================
    # SYSTEM CONFIGURATION
    # ============================================================================
    
    SYSTEM_MESSAGES = {
        "categorizer": CATEGORIZER_SYSTEM,
        "summarizer": SUMMARIZER_SYSTEM,
        "importance": IMPORTANCE_SYSTEM
    }
    
    @classmethod
    def get_system_message(cls, processor_type: str) -> str:
        """
        Get system message for a specific processor type.
        
        Args:
            processor_type (str): Type of processor ('categorizer', 'summarizer', 'importance')
            
        Returns:
            str: System message for the specified processor type
        """
        return cls.SYSTEM_MESSAGES.get(processor_type, "You are a helpful AI assistant.")
    
    @classmethod
    def list_available_prompts(cls) -> dict:
        """
        List all available prompt types for reference.
        
        Returns:
            dict: Dictionary mapping prompt types to their descriptions
        """
        return {
            "categorizer": "Email classification into predefined categories",
            "summarizer": "Extract essential information in readable format", 
            "importance": "Rate email importance on 5-level scale"
        }
        
    @classmethod
    def get_prompt_info(cls) -> dict:
        """
        Get comprehensive information about all available prompts.
        
        Returns:
            dict: Detailed information about each prompt type
        """
        return {
            "categorizer": {
                "description": "Classifies emails into predefined categories",
                "input": ["email_content", "categories"],
                "output": "Category name (string)",
                "categories": ["Promotion", "Spam", "Work", "Personal", "Finance", "Other"]
            },
            "summarizer": {
                "description": "Extracts essential information in readable format",
                "input": ["email_content", "subject"],
                "output": "Natural language summary (2-3 sentences)",
                "format": "Conversational, no formatting marks"
            },
            "importance": {
                "description": "Rates email importance on 5-level scale",
                "input": ["email_summary", "category", "subject"],
                "output": "Importance level (string)",
                "scale": ["low", "medium", "high", "urgent", "critical"]
            }
        }