"""
Part C – Question 6: Integration and Documentation
Main entry point combining all FASTA tools into a single interface.
"""

import os
import sys
import logging
from fasta_handler import parse_fasta, search_sequence, SequenceRecord
from performance_tools import performance_test

# --- Logging setup ---
logging.basicConfig(
    filename="genomic_tools.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def display_menu():
    print("\n=== Genomic Assignment 3 – Main Menu ===")
    print("1. View all sequences from FASTA")
    print("2. Search for a keyword in FASTA")
    print("3. Run performance & scalability test")
    print("4. Exit")
    print("========================================")

def run_program():
    try:
        fasta_file = "sample.fasta"
        if not os.path.exists(fasta_file):
            print("❌ FASTA file not found! Please make sure 'sample.fasta' exists.")
            return

        while True:
            display_menu()
            choice = input("Enter your choice (1–4): ").strip()

            if choice == "1":
                print("\n🧬 All sequences in", fasta_file)
                for record in parse_fasta(fasta_file):
                    print(f">{record.header}\n{record.sequence}")

            elif choice == "2":
                keyword = input("Enter keyword to search: ").strip()
                print(f"\n🔍 Searching for '{keyword}' ...")
                matches = search_sequence(fasta_file, keyword)
                if matches:
                    print("✅ Matches found:")
                    for m in matches:
                        print(f">{m.header}\n{m.sequence}")
                else:
                    print("⚠️ No matches found.")
                logging.info(f"Search completed for keyword: {keyword}")

            elif choice == "3":
                print("\n⚙️ Running performance test...")
                performance_test(fasta_file)
                logging.info("Performance test completed.")

            elif choice == "4":
                print("👋 Exiting program. Thank you!")
                break

            else:
                print("❌ Invalid choice, please try again.")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
        logging.warning("Program interrupted manually.")
    except Exception as e:
        print("⚠️ An error occurred:", str(e))
        logging.error("Error: " + str(e))


if __name__ == "__main__":
    run_program()
