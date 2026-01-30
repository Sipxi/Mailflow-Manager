from modules.categorizer import EmailCategorizer

if __name__ == "__main__":
  print("Starting Email Categorization Process...")
  categorizer = EmailCategorizer(source_folder="dataset")
  print("Fetching emails from dataset...")
  emails = categorizer.fetch_all_emails()
  print(f"Fetched {len(emails)} emails.")
  categorized = categorizer.categorize_emails(emails)
  print("Categorization complete. Outputting results...")

  categorizer.output_results(categorized)
  categorizer.save_results(categorized)
