"""
Test script for Mail Flow Manager components

This script allows you to test individual components of the mail processing pipeline:
- Categorizer
- Summarizer  
- Importance Rater
"""

import sys
import os
from modules.categorizer import EmailCategorizer
from modules.summarizer import EmailSummarizer
from modules.importance import ImportanceRater

def test_categorizer():
    """Test the email categorizer"""
    print("🧪 Testing Email Categorizer...")
    categorizer = EmailCategorizer()
    
    test_email = """
    Subject: Meeting Request - Quarterly Review
    From: manager@company.com
    
    Hi team,
    
    I'd like to schedule a meeting for our quarterly review next week.
    Please let me know your availability for Tuesday or Wednesday afternoon.
    
    Best regards,
    Sarah
    """
    
    result = categorizer.categorize_single_email(test_email, "test_email")
    print(f"   Category: {result['category']}")
    return result

def test_summarizer():
    """Test the email summarizer"""
    print("\n🧪 Testing Email Summarizer...")
    summarizer = EmailSummarizer()
    
    test_email = """
    Subject: Urgent: Server Maintenance Tonight
    
    Dear Team,
    
    We will be performing critical server maintenance tonight from 11 PM to 3 AM EST.
    During this time, all services will be unavailable. Please save your work and
    log out before 11 PM. Emergency contact: John Doe (555-1234).
    
    Thank you for your cooperation.
    """
    
    result = summarizer.summarize_email(test_email, "Server Maintenance Tonight")
    print(f"   Summary: {result['summary'][:100]}...")
    return result

def test_importance_rater():
    """Test the importance rater with new levels"""
    print("\n🧪 Testing Importance Rater...")
    rater = ImportanceRater()
    
    # Test different importance levels
    test_cases = [
        ("Newsletter subscription confirmation", "Promotion", "LOW"),
        ("Meeting request for next week", "Work", "MEDIUM"),  
        ("Urgent: Client issue needs resolution today", "Work", "HIGH/URGENT"),
        ("CRITICAL: Security breach detected", "Work", "CRITICAL")
    ]
    
    for summary, category, expected in test_cases:
        result = rater.rate_importance(summary, category, f"Test: {expected}")
        print(f"   {expected}: {result['importance'].upper()}")
    
    return result

def test_full_pipeline():
    """Test the complete pipeline"""
    print("\n🧪 Testing Complete Pipeline...")
    
    test_email = """
    Subject: Account Security Alert
    From: security@bank.com
    
    We detected unusual activity on your account ending in 1234.
    Please verify your recent transactions and contact us immediately
    if you see anything suspicious. Call 1-800-BANK-SEC.
    """
    
    # Step 1: Categorize
    categorizer = EmailCategorizer()
    category_result = categorizer.categorize_single_email(test_email, "security_alert")
    
    # Step 2: Summarize
    summarizer = EmailSummarizer()
    summary_result = summarizer.summarize_email(test_email, "Account Security Alert")
    
    # Step 3: Rate Importance
    rater = ImportanceRater()
    importance_result = rater.rate_importance(
        summary_result['summary'], 
        category_result['category'], 
        "Account Security Alert"
    )
    
    print(f"   📂 Category: {category_result['category']}")
    print(f"   📝 Summary: {summary_result['summary'][:80]}...")
    print(f"   ⭐ Importance: {importance_result['importance'].upper()}")
    print(f"   📊 Scale: {importance_result['scale']}")

def main():
    """Run all tests"""
    print("🧪 Mail Flow Manager - Component Tests")
    print("=" * 50)
    
    try:
        test_categorizer()
        test_summarizer()  
        test_importance_rater()
        test_full_pipeline()
        
        print("\n✅ All tests completed!")
        print("\nTo run the full mail monitor: python main.py")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("Please check your API configuration in config.py")

if __name__ == "__main__":
    main()
